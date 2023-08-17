"""
An iterative implementation of the Ramer-Douglas-Peucker algorithm to select significant points of a sequence of points.
"""

from typing import Sequence

Sample = tuple[float, float]


def calc_slopes(sample1: Sample, sample2: Sample, epsilon: float) -> tuple[float, float]:
    """
    Calculate the slopes between two samples.

    :param sample1: The first sample, must be a tuple of x and y coordinates.
    :param sample2: The second sample, must be a tuple of x and y coordinates.
    :param epsilon: The epsilon value to be added and subtracted from the y value of `sample2`.
    :return: A tuple of the top and bottom slopes.
    """
    if epsilon < 0:
        raise ValueError("Epsilon must be non-negative.")

    x0, y0 = sample1
    x1, y1 = sample2
    dx = x1 - x0
    dy = y1 - y0
    return (
        (dy + epsilon) / dx,
        (dy - epsilon) / dx,
    )


def simplify_iterative_functional(samples: Sequence[Sample], epsilon: float) -> list[int]:
    """
    :param samples: A sequence of `(x,y)` value pairs representing a set of data points. The `x` values must be strictly
                    monotonously increasing.
    :param epsilon: A float value representing the tolerance level for data points considered significant or not.
    :return: An iterable of indices representing the simplified set of data points.

    Example usage:
    >>> simplify_iterative_functional([(1, 1), (2, 1), (3, 1), (4, 100)], 1)
    [0, 2, 3]
    """
    p0 = 0

    r = []
    while p0 < len(samples) - 1:
        # we always have the most recent significant index in p0
        r.append(p0)

        x0, y0 = samples[p0]

        # init the funnel by calculating the funnel edges from the first 2 points
        slope_top, slope_bottom = calc_slopes((x0, y0), samples[p0 + 1], epsilon)

        for next_p in range(p0 + 2, len(samples)):
            current_slope_top, current_slope_bottom = calc_slopes((x0, y0), samples[next_p], epsilon)

            # narrow the funnel down
            slope_top = min(slope_top, current_slope_top)
            slope_bottom = max(slope_bottom, current_slope_bottom)
            if slope_top < slope_bottom:
                # when top and bottom become invalid, we have found a point outside our funnel, so we return the
                # previous significant element
                p0 = next_p - 1
                break
        else:
            # if we reach the end without finding a new significant point, we're done
            break
    r.append(len(samples) - 1)
    return r


def simplify_recursive_reference(samples: Sequence[Sample], epsilon: float, i_start: int, i_end: int) -> list[int]:
    """
    The Ramen-Douglas-Peucker algorithm, which simplifies a curve with regards to an epsilon.
    :param samples: The `(x, y)` coordinates of the sample points.
    :param epsilon: The maximum permitted error between the true curve and its simplification.
    :param i_start: The array index of the first sample point.
    :param i_end: The array index of the last sample point.
    :return: List of indices in `samples` representing the simplified curve.
    """
    # Find the point with the maximum distance
    d_max = 0
    i_max = 0

    # calculate the reference line
    x0, y0 = samples[i_start]
    x1, y1 = samples[i_end]
    dx = x1 - x0
    dy = y1 - y0

    for i in range(i_start, i_end):
        x, y = samples[i]
        x -= x0
        expected = y0 + x * dy / dx
        d = abs(y - expected)
        if d >= d_max:
            i_max = i
            d_max = d

    # If max distance is greater than epsilon, recursively simplify
    if d_max > epsilon:
        # Recursive call
        left = simplify_recursive_reference(samples, epsilon, i_start, i_max)[:-1]
        right = simplify_recursive_reference(samples, epsilon, i_max, i_end)
        return left + right
    else:
        return [i_start, i_end]


def simplify_reference_functional(samples: Sequence[Sample], epsilon: float) -> list[int]:
    """
    The original Ramen-Douglas-Peucker algorithm.
    """
    if len(samples) == 1:
        return [0]

    elems = simplify_recursive_reference(samples, epsilon, 0, len(samples) - 1)
    if len(elems) > 1 and elems[-1] == elems[-2]:
        elems = elems[:-1]
    return elems
