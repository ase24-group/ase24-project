import random, sys, traceback, time, os
from test import test
from box import Box
from config import config
from utils import get_filename_and_parent


def run(todo):
    if todo == "all":
        run_all()
        return

    b4 = Box(config.value.copy())
    random.seed(config.value.seed)
    test_fun = getattr(test, todo, None)

    elapsed_time = 0
    try:
        start_time = time.time()
        oops = test_fun() == False
        end_time = time.time()
        elapsed_time = end_time - start_time
    except Exception as err:
        print(f"Python Error: {err}")
        traceback.print_exc()
        oops = True

    experiments = [
        "baseline_stats",
        "progressive_stats",
        "focus_stats",
        "ExpProgressive_stats",
        "bonr_stats",
        "b2_stats",
        "rand_stats",
        "PI_stats",
        "EI_stats",
        "UCB_plus_stats",
        "UCB_minus_stats",
    ]
    csv_filename, csv_parent_folder = get_filename_and_parent(config.value.file)

    if todo not in experiments:
        if oops:
            print(f"❌ FAIL {todo}\n")
        else:
            print(f"✅ PASS {todo}\n")
    else:
        ExpBudget = config.value.ExpBudget
        if ExpBudget is None:
            ExpBudget = ""
        else:
            ExpBudget = f"_{ExpBudget}"

        treatment = todo.removesuffix("_stats")
        experiment = f"{csv_filename}_{treatment}{ExpBudget}"
        if oops:
            print(f"❌ FAIL {experiment}\n", file=sys.stderr)
        else:
            print(f"✅ PASS {experiment}\n", file=sys.stderr)

            times_dir = f"../results/times/{csv_parent_folder}"
            os.makedirs(times_dir, exist_ok=True)

            with open(f"{times_dir}/{experiment}.time.txt", "w") as file:
                budget = ExpBudget.removeprefix("_")
                info = [csv_filename, treatment, budget, str(round(elapsed_time, 4))]
                file.write(f"{','.join(info)}")

    config.value = b4

    return not oops


def run_all():
    all_attributes = dir(test)
    methods = [
        attr
        for attr in all_attributes
        if callable(getattr(test, attr)) and (not attr.startswith("_"))
    ]

    bad = 0
    for method in methods:
        if not run(method):
            bad += 1

    print(f'{"❌ FAIL" if bad > 0 else "✅ PASS"} {bad} fail(s)')
    sys.exit(bad)
