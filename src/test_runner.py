import random, sys, traceback
from test import test
from box import Box
from config import config


def run(todo):
    if todo == "all":
        run_all()
        return

    b4 = Box(config.value.copy())
    random.seed(config.value.seed)
    test_fun = getattr(test, todo, None)

    try:
        oops = test_fun() == False
    except Exception as err:
        print(f"Python Error: {err}")
        traceback.print_exc()
        oops = True

    ExpBudget = config.value.ExpBudget
    if ExpBudget is None:
        ExpBudget = ""
    else:
        ExpBudget = f"_{ExpBudget}"

    if oops:
        print(f"❌ FAIL {todo}{ExpBudget}\n")
    else:
        print(f"✅ PASS {todo}{ExpBudget}\n")

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
