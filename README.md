## Iterative implementation of the Ramer-Douglas-Peucker algorithm

This package provides an iterative implementation of the Ramer-Douglas-Peucker algorithm.

Please note that the implemented algorithm only works, given a metric $d$ for a series of samples $x_i$, if and only if $d(x_i, x_0) \leq d(x_{i+1}, x_0) + \delta$ with $\delta > 0$. For example, a series of points where $x_{i>0}$ forms a circle around $x_0$ (i.e., $d(x_0, x_a) = d(x_0, x_b) \forall a,b \neq 0$), this algorithm will only yield two samples. If $\delta$ is small enough, this algorithm will certainly omit samples which you would consider significant.

I tried to describe (and eventually implement) an algorithm that covers the case where $d(x_0, x_i) \leq d(x_0, x_{i+1})$, however my math skills are inferior to describe it properly using linear algebra. The idea is that if $d(x_0, x_i) > d(x_0, x_{i+1})$, then $x_i$ must be a significant sample, and the funnel must start anew from $x_i$.

### Performance

#### Test scenario: uniformly random samples

Using uniformly random data with values between 0 and 1 on the y axis, evenly spaced on the x axis.
Times are averaged from 5 runs.

Note that the speedup is dependent on the number of samples and epsilon.

| Samples | Epsilon | Reduction | Reference time (s) | Iterative time (s) | Speedup |
|---------|---------|-----------|--------------------|--------------------|---------|
| 1000    | 0.1     | 0.806     | 0.028              | 0.004              | 6.2     |
| 1000    | 0.25    | 0.591     | 0.026              | 0.004              | 7.0     |
| 1000    | 0.5     | 0.316     | 0.024              | 0.002              | 10.2    |
| 1000    | 1.0     | 0.002     | 0.001              | 0.002              | 0.3     |
| 10000   | 0.1     | 0.817     | 0.606              | 0.045              | 13.5    |
| 10000   | 0.25    | 0.593     | 0.576              | 0.037              | 15.5    |
| 10000   | 0.5     | 0.316     | 0.008              | 0.022              | 25.9    |
| 10000   | 1.0     | 0.0002    | 0.021              | 0.022              | 0.4     |
| 100000  | 0.1     | 0.819     | 17.8               | 0.443              | 40.3    |
| 100000  | 0.25    | 0.596     | 17.5               | 0.367              | 47.9    |
| 100000  | 0.5     | 0.318     | 17.2               | 0.211              | 81.5    |
| 100000  | 1.0     | 0.00002   | 0.075              | 0.213              | 0.4     |

#### Test scenario: random values with limited range between consecutive samples

Using uniformly random data with a maximum difference of a given delta between each sample pair on the y axis, evenly
spaced on the x axis.
Times are averaged from 5 runs.

This should be a more realistic test scenario.
Note that the speedup is mostly dependent on the number of samples, and somewhat on the ration between variation and
epsilon.

##### Delta = 0.25

| Samples | Epsilon | Reduction | Reference time (s) | Iterative time (s) | Speedup |
|---------|---------|-----------|--------------------|--------------------|---------|
| 1000    | 0.1     | 0.453     | 0.011              | 0.003              | 3.1     |
| 1000    | 0.25    | 0.171     | 0.008              | 0.003              | 3.0     |
| 1000    | 0.5     | 0.068     | 0.006              | 0.002              | 2.6     |
| 1000    | 1.0     | 0.026     | 0.005              | 0.002              | 2.3     |
| 10000   | 0.1     | 0.450     | 0.141              | 0.035              | 4.1     |
| 10000   | 0.25    | 0.171     | 0.109              | 0.025              | 4.3     |
| 10000   | 0.5     | 0.062     | 0.089              | 0.023              | 3.8     |
| 10000   | 1.0     | 0.020     | 0.072              | 0.024              | 3.0     |
| 100000  | 0.1     | 0.458     | 1.82               | 0.353              | 5.1     |
| 100000  | 0.25    | 0.168     | 1.52               | 0.263              | 5.8     |
| 100000  | 0.5     | 0.061     | 1.33               | 0.239              | 5.6     |
| 100000  | 1.0     | 0.020     | 1.15               | 0.228              | 5.0     |
| 1000000 | 0.1     | 0.459     | 21.9               | 3.605              | 6.1     |
| 1000000 | 0.25    | 0.168     | 18.9               | 2.601              | 7.3     |
| 1000000 | 0.5     | 0.061     | 16.8               | 2.343              | 7.2     |
| 1000000 | 1.0     | 0.019     | 15.0               | 2.258              | 6.7     |

##### Delta = 0.5

| Samples | Epsilon | Reduction | Reference time (s) | Iterative time (s) | Speedup |
|---------|---------|-----------|--------------------|--------------------|---------|
| 1000    | 0.1     | 0.662     | 0.012              | 0.004              | 3.0     |
| 1000    | 0.25    | 0.386     | 0.010              | 0.003              | 3.2     |
| 1000    | 0.5     | 0.171     | 0.008              | 0.002              | 3.2     |
| 1000    | 1.0     | 0.068     | 0.006              | 0.002              | 2.7     |
| 10000   | 0.1     | 0.668     | 0.153              | 0.040              | 3.8     |
| 10000   | 0.25    | 0.171     | 0.128              | 0.030              | 4.2     |
| 10000   | 0.5     | 0.171     | 0.109              | 0.025              | 4.4     |
| 10000   | 1.0     | 0.061     | 0.090              | 0.023              | 4.0     |
| 100000  | 0.1     | 0.676     | 1.90               | 0.416              | 4.6     |
| 100000  | 0.25    | 0.381     | 1.71               | 0.314              | 5.4     |
| 100000  | 0.5     | 0.168     | 1.46               | 0.251              | 5.8     |
| 100000  | 1.0     | 0.061     | 1.28               | 0.227              | 5.6     |
| 1000000 | 0.1     | 0.676     | 22.8               | 4.22               | 5.4     |
| 1000000 | 0.25    | 0.380     | 20.3               | 3.18               | 6.4     |
| 1000000 | 0.5     | 0.166     | 18.1               | 2.50               | 7.3     |
| 1000000 | 1.0     | 0.061     | 16.2               | 2.30               | 7.1     |
