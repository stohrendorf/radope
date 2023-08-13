"""
An iterative implementation of the Ramer-Douglas-Peucker algorithm to select significant points of a sequence of points.
"""

from typing import Iterable, Sequence

Sample = tuple[float, float]


def calc_slopes(sample1: Sample, sample2: Sample, epsilon: float) -> tuple[float, float]:
    """
    Calculate the slopes between two samples.

    :param sample1: The first sample, must be a tuple of x and y coordinates.
    :param sample2: The second sample, must be a tuple of x and y coordinates.
    :param epsilon: The epsilon value to be added and subtracted from the y value of `sample2`.
    :return: A tuple of the top and bottom slopes.
    """
    x0, y0 = sample1
    x1, y1 = sample2
    dx = x1 - x0
    dy = y1 - y0
    return (
        (dy + epsilon) / dx,
        (dy - epsilon) / dx,
    )


def simplify_iterative_functional(samples: Sequence[Sample], epsilon: float) -> Iterable[int]:
    """
    :param samples: A sequence of `(x,y)` value pairs representing a set of data points. The `x` values must be strictly
                    monotonously increasing.
    :param epsilon: A float value representing the tolerance level for data points considered significant or not.
    :return: An iterable of indices representing the simplified set of data points.

    Example usage:
    >>> list(simplify_iterative_functional([(1, 1), (2, 1), (3, 1), (4, 100)], 1))
    [0, 2, 3]
    """
    p0 = 0

    while p0 < len(samples) - 1:
        # yield it, as we always have the most recent significant index in p0
        yield p0

        x0, y0 = samples[p0]

        # init the funnel by calculating the funnel edges from the first 2 points
        xi_top, xi_bottom = calc_slopes((x0, y0), samples[p0 + 1], epsilon)

        for next_p, sample in enumerate(samples[p0 + 2 :], p0 + 2):
            current_xi_top, current_xi_bottom = calc_slopes((x0, y0), sample, epsilon)

            # narrow the funnel down
            xi_top = min(xi_top, current_xi_top)
            xi_bottom = max(xi_bottom, current_xi_bottom)
            if xi_top < xi_bottom:
                # when top and bottom become invalid, we have found a point outside our funnel, so we return the
                # previous significant element
                p0 = next_p - 1
                break
        else:
            # if we reach the end without finding a new significant point, we're done
            break
    yield len(samples) - 1
