import fileinput, re, ast, os
import random
import math
from typing import Tuple


# Reference: https://discord.com/channels/1191838787219759154/1192507528882438247/1195863830136377345
# Returns the values in the next row of the CSV as a list along with the row number of the next
def csv(filename: str = "-"):
    i = 0
    with fileinput.FileInput(None if filename == "-" else filename) as src:
        for line in src:
            line = re.sub(r'([\n\t\r"\' ]|#.*)', "", line)
            if line:
                i += 1
                yield i, [coerce(x) for x in line.split(",")]


def output(x):
    items = ", ".join([f"{k}: {v}" for k, v in sorted(x.items()) if k[0] != "_"])
    return f"{{{items}}}"


def coerce(s: str):
    # Converts string rep to python datatype
    try:
        return ast.literal_eval(s)
    except Exception:
        return s.strip()


def slice(t: list, go: int = None, stop: int = None, inc: int = None) -> list:
    go = go or 0
    stop = stop or len(t)
    inc = inc or 1

    if go < 0:
        go += len(t)
    if stop < 0:
        stop += len(t)

    return t[go:stop:inc]


def output_gate20_info(info):
    for i, (k, v) in enumerate(info.items()):
        for t in v:
            print(f"{i + 1}. {k:<5} {pad_numbers(t)}")
        print()


def pad_numbers(t):
    s = ""
    if isinstance(t[0], list):
        s = f"[{', '.join([f'{pad_numbers(v)}' for v in t])}]"
    else:
        s = f"[{', '.join([f'{v:5.2f}' for v in t])}]"
    return s


def align_list(lst, precision=2, pad=15):
    out = "["
    for i, cell in enumerate(lst):
        if isinstance(cell, (int, float)):
            cell = cell if int(cell) == cell else round(cell, precision)
        if isinstance(cell, str):
            cell = f"'{cell}'"
        out += f"{str(cell):{pad if i < (len(lst) - 1) else 0}}"
    out += "]"
    return out


def any(t):
    return random.choice(t)


def many(t, n):
    if n == None:
        n = len(t)

    u = []
    for i in range(n):
        u.append(any(t))

    return u


def oo(x):
    print(o(x))
    return x


def o(t, n=2):
    if isinstance(t, (int, float)):
        return str(round(t, n))
    if not isinstance(t, dict):
        return vars(t)

    u = []
    for k, v in t.items():
        if not str(k).startswith("_"):
            if len(t) > 0:
                u.append(o(v, n))
            else:
                u.append(f"{o(k, n)}: {o(v, n)}")

    return "{" + ", ".join(u) + "}"


def as_list(t):
    return [v for v in t.values()]


def score(t, goal, LIKE, HATE, Support):
    like = 0
    hate = 0
    tiny = 1e-30

    for klass, n in t.items():
        if klass == goal:
            like += n
        else:
            hate += n

    like = like / (LIKE + tiny)
    hate = hate / (HATE + tiny)

    if hate > like:
        return 0
    else:
        return like**Support / (like + hate)


def entropy(t: dict) -> Tuple[float]:
    n = 0
    for v in t.values():
        n += v

    e = 0
    for v in t.values():
        e -= v / n * math.log2(v / n)

    return e, n


def custom_normalize(values, start=0, end=1):
    scale = end - start
    normalized_data = [
        ((x - min(values)) / (max(values) - min(values)) * scale) + start
        for x in values
    ]
    return normalized_data


def get_filename_and_parent(path):
    filename_ext = os.path.basename(path)
    filename = os.path.splitext(filename_ext)[0]
    parent_folder = os.path.basename(os.path.dirname(path))

    return filename, parent_folder


def get_cumulative_density(x, mean, sd):
    cdf = lambda z: 1 - 0.5 * 2.718 ** (-0.717 * z - 0.416 * z * z)
    z = (x - mean) / sd
    return cdf(z) if z >= 0 else 1 - cdf(-z)


def get_probability_density(x, mean, sd):
    z = (x - mean) / sd
    e = 2.718
    return (0.399 / sd) * (e ** (-(z**2) / 2))


# debug this!
def get_interpolated_distance(dist_row_a, dist_row_b, dist_ab, d2h_a, d2h_b):
    inconsistency = False
    # Should we move these 3 lines to the cosine project fn?
    projection_dist_a = abs(cosine_project(dist_ab, dist_row_a, dist_row_b))
    projection_dist_b = abs(dist_ab - projection_dist_a)

    if not (dist_row_a > dist_row_b) ^ (projection_dist_a > projection_dist_b):
        # print(f"\n\nINCONSISTENCY OBSERVED!!!")
        # print(f" dist_row_a: {dist_row_a}, dist_row_b: {dist_row_b}, dist_ab: {dist_ab}, projection_dist_a: {projection_dist_a}, projection_dist_b: {projection_dist_b} \n")
        inconsistency = True

    # Weight of 'a' should be higher if the projection is closer to a and farther away from b
    a_weight = projection_dist_b / (projection_dist_a + projection_dist_b)
    b_weight = projection_dist_a / (projection_dist_a + projection_dist_b)

    d2h_row = (a_weight * d2h_a) + (b_weight * d2h_b)

    return d2h_row, inconsistency


def cosine_project(ab, ra, rb):
    return (ab**2 + ra**2 - rb**2) / (2 * ab)
