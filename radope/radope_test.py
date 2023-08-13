from radope import simplify_iterative_functional


def test_simplify_single_datapoint():
    points = [(1, 1)]

    assert list(simplify_iterative_functional(points, 1000)) == [0]


def test_simplify_start_end_datapoints():
    assert list(simplify_iterative_functional([(1, 1), (2, 1)], 1000)) == [0, 1]
    assert list(simplify_iterative_functional([(1, 1), (2, 1), (3, 1)], 1000)) == [0, 2]


def test_simplify_significant_points():
    assert list(simplify_iterative_functional([(1, 1), (2, 100), (3, 1)], 1)) == [0, 1, 2]
    assert list(simplify_iterative_functional([(1, 1), (2, 100), (3, 1), (4, 1)], 1)) == [0, 1, 2, 3]
    assert list(simplify_iterative_functional([(1, 1), (2, 1), (3, 1), (4, 100)], 1)) == [0, 2, 3]
    assert list(simplify_iterative_functional([(1, 1), (3, 1), (4, 100)], 1)) == [0, 1, 2]
