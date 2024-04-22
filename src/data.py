import utils
import random
import math
import sys
from row import Row
from cols import Cols
from node import Node
from config import config
from typing import List
from progressive_scorer import (
    progressive_score,
    exploitation_score,
    exploration_score,
    ProgressiveScorer,
)
from matplotlib import pyplot as plt
from logger import logger, br_logger
from utils import custom_normalize


class Data:
    def __init__(self, src, fun=None, sortD2H=False):
        self.rows = []
        self.cols = None
        if type(src) == str:
            for _, x in utils.csv(src):
                self.add(x, fun)
        else:
            self.add(src, fun)
        if sortD2H:
            self.sortD2H()

    def sortD2H(self):
        self.rows = sorted(self.rows, key=lambda row: row.d2h(self))

    def add(self, t, fun=None):
        row = t if hasattr(t, "cells") else Row(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = Cols(row)

    def mid(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.mid())
        return Row(u)

    def div(self, cols=None):
        u = []
        for col in cols or self.cols.all:
            u.append(col.div())
        return Row(u)

    def stats(self, cols=None, fun=None, ndivs=2):
        u = {".N": len(self.rows)}
        for _, col in self.cols.y.items():
            u[col.txt] = round(col.mid(), ndivs)
        return u

    def split(
        self,
        best,
        rest,
        lite,
        dark,
        score=lambda b, r: abs(b + r) / abs(b - r + 1e-300),
    ):
        selected = Data(self.cols.names)
        max = -1e30
        out = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)

            tmp = score(b, r)
            if tmp > max:
                out, max = i, tmp
        return out, selected

    def split_progressive_scorer(
        self,
        best,
        rest,
        lite,
        dark,
        past_best_d2hs,
        progress: float,
    ):
        selected = Data(self.cols.names)
        max = -1e30
        out = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            # br_logger.info(f"b: {b}, r: {r}")
            if b > r:
                selected.add(row)

            tmp = b if progress >= 0.85 else progressive_score(b, r, past_best_d2hs)

            if tmp > max:
                out, max = i, tmp
        # logger.info(f"Selected row: {out}, Score: {max}")
        return out, selected

    def best_rest(self, rows, want, best=None, rest=None):
        rows.sort(key=lambda x: x.d2h(self))
        best, rest = Data(self.cols.names), Data(self.cols.names)
        for i in range(len(rows)):
            if i <= want:
                best.add(rows[i])
            else:
                rest.add(rows[i])
        return best, rest

    def gate(self, budget0: int, budget, some, info=None):
        stats = []
        bests = []

        if not info:
            info = {
                "top6": [],
                "top50": [],
                "most": [],
                "rand": [],
                "mid": [],
                "top": [],
            }

        y_indices = self.cols.y.keys()

        random.shuffle(self.rows)

        info["top6"].append(
            [[row.cells[y] for y in y_indices] for row in self.rows[:6]]
        )
        info["top50"].append(
            [[row.cells[y] for y in y_indices] for row in self.rows[:50]]
        )

        self.rows.sort(key=lambda x: x.d2h(self))
        info["most"].append([self.rows[0].cells[y] for y in y_indices])

        random.shuffle(self.rows)
        lite = utils.slice(self.rows, 0, budget0)
        dark = utils.slice(self.rows, budget0 + 1)

        for i in range(budget):
            best, rest = self.best_rest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            stats.append(selected.mid())
            bests.append(best.rows[0])

            rand = Data(self.cols.names)
            for row in random.sample(dark, budget0 + 1):
                rand.add(row)

            info["rand"].append([rand.mid().cells[y] for y in y_indices])
            info["mid"].append([selected.mid().cells[y] for y in y_indices])
            info["top"].append([best.rows[0].cells[y] for y in y_indices])

            lite.append(dark.pop(todo))

        return stats, bests, info

    def smo(self, score=None):
        random.shuffle(self.rows)

        lite = utils.slice(self.rows, 0, config.value.budget0)
        dark = utils.slice(self.rows, config.value.budget0 + 1)

        data = self.clone(lite, sortD2H=True)

        best_d2hs = []

        for i in range(config.value.Budget):
            best, rest = self.best_rest(
                data.rows, int(len(data.rows) ** config.value.Top + 0.5)
            )
            todo, _ = self.split(best, rest, self.rows, dark, score=score)

            lite.append(dark.pop(todo))
            data = self.clone(lite, sortD2H=True)

            best_d2hs.append(data.rows[0].d2h(self))

        return data.rows[0], best_d2hs

    def smo_exp_progressive(self, score=None):
        random.shuffle(self.rows)

        lite = utils.slice(self.rows, 0, config.value.budget0)
        dark = utils.slice(self.rows, config.value.budget0 + 1)
        data = self.clone(lite, sortD2H=True)

        exp_values = []
        for i in range(config.value.Budget):
            exp_values.append(math.exp(0.25 * i))
        norm_exp_values = custom_normalize(exp_values)

        best_d2hs = []

        for i in range(config.value.Budget):
            best, rest = self.best_rest(
                data.rows, int(len(data.rows) ** config.value.Top + 0.5)
            )
            want_to_exploit, want_to_explore = (
                norm_exp_values[i],
                1 - norm_exp_values[i],
            )
            logger.info(
                f"EXP Want to exploit: {want_to_exploit}, want to explore: {want_to_explore}\n"
            )
            # Pick the next sample based on the weighted sum of exploitation and exploration scores
            todo, _ = self.split(
                best,
                rest,
                self.rows,
                dark,
                score=lambda b, r: want_to_exploit * exploitation_score(b, r)
                + want_to_explore * exploration_score(b, r),
            )

            lite.append(dark.pop(todo))
            data = self.clone(lite, sortD2H=True)

            best_d2hs.append(data.rows[0].d2h(self))

        return data.rows[0], best_d2hs, norm_exp_values

    def smo_progressive_scorer(self):
        random.shuffle(self.rows)

        lite = utils.slice(self.rows, 0, config.value.budget0)
        dark = utils.slice(self.rows, config.value.budget0 + 1)

        data = self.clone(lite, sortD2H=True)

        progressive_scorer = ProgressiveScorer(budget=config.value.Budget)

        for i in range(config.value.Budget):
            best, rest = self.best_rest(
                data.rows, int(len(data.rows) ** config.value.Top + 0.5)
            )
            progressive_scorer.add_history(best.rows[0].d2h(self))

            logger.info(f"\n\nSMO PROGRESSIVE ITERATION {i}\n\n")

            todo, _ = self.split(
                best, rest, self.rows, dark, score=progressive_scorer.score
            )

            lite.append(dark.pop(todo))
            data = self.clone(lite, sortD2H=True)
        # progressive_scorer.plot_performance()
        # plt.show()
        return data.rows[0], progressive_scorer

    def smo_sim_annealing(self):
        random.shuffle(self.rows)

        lite = utils.slice(self.rows, 0, config.value.budget0)
        dark = utils.slice(self.rows, config.value.budget0 + 1)

        data = self.clone(lite, sortD2H=True)
        exp_values = []

        for i in range(config.value.Budget):
            exp_values.append(math.exp(0.25 * i))
        norm_exp_values = custom_normalize(exp_values, 1, 2)
        # print("Norm exp values: ", norm_exp_values)

        best_d2hs = []

        for i in range(config.value.Budget):
            best, rest = self.best_rest(
                data.rows, int(len(data.rows) ** config.value.Top + 0.5)
            )

            exp_dec_score = lambda b, r: abs(
                ((b + 1) ** norm_exp_values[i]) + (r + 1)
            ) / abs(b - r + 1e-300)

            todo, _ = self.split(best, rest, self.rows, dark, score=exp_dec_score)

            lite.append(dark.pop(todo))
            data = self.clone(lite, sortD2H=True)

            best_d2hs.append(data.rows[0].d2h(self))

        return data.rows[0], best_d2hs, norm_exp_values

    def farapart(self, rows, sortp=None, a=None):
        far = int((len(rows) * config.value.Far))
        evals = 1 if a else 2
        a = a or utils.any(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        return a, b, a.dist(b, self), evals

    def branch(self, stop=None, rest=None, _branch=None, evals=None):
        evals = 1
        rest = []

        stop = stop if stop else (2 * (len(self.rows) ** 0.5))

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals

            if len(data.rows) > stop:
                lefts, rights, left, _, _, _, _ = self.half(data.rows, True, above)
                evals += 1
                for row1 in rights:
                    rest.append(row1)
                return _branch(self.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals

        return _branch(self)

    def tree(self, sortp):
        evals = 0

        def _tree(data, above=None):
            nonlocal evals

            node = Node(data)
            if len(data.rows) > (2 * (len(self.rows) ** 0.5)):
                (
                    lefts,
                    rights,
                    node.left,
                    node.right,
                    node.C,
                    node.cut,
                    evals1,
                ) = self.half(data.rows, sortp, above)
                evals = evals + evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node

        return _tree(self), evals

    def half(self, rows, sortp, before):
        a_list, b_list = [], []
        some = utils.many(rows, min(config.value.Half, len(rows)))
        a, b, C, evals = self.farapart(some, sortp, before)

        def d(row1, row2):
            return row1.dist(row2, self)

        def project(r):
            return (d(r, a) ** 2 + C**2 - d(r, b) ** 2) / (2 * C)

        for n, row in enumerate(sorted(rows, key=project)):
            if n <= math.floor(len(rows) / 2):
                a_list.append(row)
            else:
                b_list.append(row)

        return a_list, b_list, a, b, C, d(a, b_list[0]), evals

    def clone(self, rows, sortD2H=False):
        new = Data(self.cols.names)
        for _, row in enumerate(rows):
            new.add(row)

        if sortD2H:
            new.sortD2H()

        return new
