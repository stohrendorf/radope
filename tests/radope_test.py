from random import seed, uniform
from timeit import repeat

from radope import (
    calc_slopes,
    simplify_iterative_functional,
    simplify_reference_functional,
)


def test_calc_slope():
    assert calc_slopes((0, 0), (1, 1), 0) == (1, 1)
    assert calc_slopes((0, 0), (2, 2), 0) == (1, 1)
    assert calc_slopes((0, 0), (2, 1), 0) == (0.5, 0.5)

    assert calc_slopes((0, 0), (1, 1), 1) == (2, 0)
    assert calc_slopes((0, 0), (2, 2), 1) == (1.5, 0.5)
    assert calc_slopes((0, 0), (2, 1), 1) == (1.0, 0.0)


def _test(samples, epsilon, expected):
    assert list(simplify_iterative_functional(samples, epsilon)) == expected
    assert list(simplify_reference_functional(samples, epsilon)) == expected


def test_simplify_single_datapoint():
    _test([(1, 1)], 1000, [0])


def test_simplify_start_end_datapoints():
    _test([(1, 1), (2, 1)], 1000, [0, 1])
    _test([(1, 1), (2, 1), (3, 1)], 1000, [0, 2])


def test_simplify_significant_points():
    _test([(1, 1), (2, 100), (3, 1)], 1, [0, 1, 2])
    _test([(1, 1), (2, -100), (3, 1), (4, 1)], 1, [0, 1, 2, 3])
    _test([(1, 1), (2, 1), (3, 1), (4, 100)], 1, [0, 2, 3])
    _test([(1, 1), (3, 1), (4, 100)], 1, [0, 1, 2])


def _run_performance_test(samples, epsilon):
    repeats = 5

    print(f"===== Performance for {len(samples)} samples, {repeats} repeats, epsilon {epsilon}")
    seconds_reference = (
        sum(repeat(stmt=lambda: simplify_reference_functional(samples, epsilon), number=repeats)) / repeats
    )
    print(f"reference avg {seconds_reference}s")
    seconds_iterative = (
        sum(repeat(stmt=lambda: simplify_iterative_functional(samples, epsilon), number=repeats)) / repeats
    )
    print(f"iterative avg {seconds_iterative}s")
    reduction = len(simplify_reference_functional(samples, epsilon)) / len(samples)
    print(f"reference/iterative ratio {seconds_reference/seconds_iterative}, reduction {reduction}")


def _gen_samples(n):
    seed(12345)
    return [(x, uniform(0.0, 1.0)) for x in range(10000)]


def test_performance():
    for n in (1000, 10000, 100000):
        for epsilon in (0.1, 0.25, 0.5, 1.0):
            _run_performance_test(_gen_samples(n), epsilon)
