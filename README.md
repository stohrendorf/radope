## Iterative implementation of the Ramer-Douglas-Peucker algorithm

This package provides an iterative implementation of the Ramer-Douglas-Peucker algorithm.

### Performance

Using uniformly random data with values between 0 and 1 on the y axis, evenly spaced on the x axis.
Times are averaged from 5 runs.
Note that the speedup is dependent on the number of samples and epsilon.

| Samples | Epsilon | Reduction | Reference time (s) | Iterative time (s) | Speedup |
|---------|---------|-----------|--------------------|--------------------|---------|
| 1000    | 0.1     | 0.806     | 0.028              | 0.004              | 6.2     |
| 1000    | 0.25    | 0.591     | 0.026              | 0.004              | 7.0     |
| 1000    | 0.5     | 0.316     | 0.024              | 0.002              | 10.2    |
| 1000    | 1.0     | 0.002     | 0.001              | 0.002              | 0.3     |
| 10000   | 0.1     | 0.8174    | 0.606              | 0.045              | 13.5    |
| 10000   | 0.25    | 0.593     | 0.576              | 0.037              | 15.5    |
| 10000   | 0.5     | 0.316     | 0.008              | 0.022              | 25.9    |
| 10000   | 1.0     | 0.0002    | 0.021              | 0.022              | 0.4     |
| 100000  | 0.1     | 0.8194    | 17.8               | 0.443              | 40.3    |
| 100000  | 0.25    | 0.5955    | 17.5               | 0.367              | 47.9    |
| 100000  | 0.5     | 0.318     | 17.2               | 0.211              | 81.5    |
| 100000  | 1.0     | 0.00002   | 0.075              | 0.213              | 0.4     |
