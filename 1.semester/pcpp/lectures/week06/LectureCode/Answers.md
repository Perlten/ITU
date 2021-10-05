# 6.1


# OS:   Windows 10; 10.0; amd64
# JVM:  Oracle Corporation; 15.0.1
# CPU:  Intel64 Family 6 Model 165 Stepping 5, GenuineIntel; 16 "cores"
# Date: 2021-10-05T20:54:45+0200


# 6.1.1
Wait time 50
Measure Transactions          123667715.0 ns  213612.66          4

wait time 100
Measure Transactions          216186395.1 ns  692679.16          2


# 6.1.2

By using max and min we avoid a potential deadlock.


# 6.2.1 
countSequential                 7040323.9 ns    8909.98         64
countParallelN  1               7381125.0 ns   12064.05         64
countParallelN  2               4704995.3 ns   23416.39         64
countParallelN  3               3424155.5 ns   22386.14        128
countParallelN  4               2702229.8 ns   18859.33        128
countParallelN  5               2345836.6 ns   24987.51        128
countParallelN  6               2682404.5 ns   35595.86        128
countParallelN  7               2778758.6 ns   30070.93        128
countParallelN  8               2848930.8 ns   20440.26        128
countParallelN  9               2895400.5 ns   24405.50        128
countParallelN 10               2915756.4 ns   29361.25        128
countParallelN 11               2945942.1 ns   14934.83        128
countParallelN 12               2966539.1 ns    9946.52        128
countParallelN 13               3032466.6 ns   43594.42        128
countParallelN 14               3103840.9 ns    6424.90        128
countParallelN 15               3135465.4 ns   25666.71        128
countParallelN 16               3138849.5 ns    9964.88        128

We get the same results as we have previously. So as expected. 

# 6.2.2

countSequential                 7189387.0 ns  119353.67         64
countParallelN  1               6680934.5 ns  260799.93         64
countParallelN  2               4213718.1 ns   28490.53         64
countParallelN  3               3417478.3 ns   20069.96        128
countParallelN  4               2712345.6 ns   32960.11        128
countParallelN  5               2421619.0 ns   12757.60        128
countParallelN  6               2744812.7 ns   44434.89        128
countParallelN  7               2849705.5 ns   14782.63        128
countParallelN  8               2909588.7 ns    7143.83        128
countParallelN  9               3007854.7 ns   26470.45        128
countParallelN 10               3055326.8 ns   17375.18        128
countParallelN 11               3092732.3 ns   10378.73        128
countParallelN 12               3126876.9 ns   17109.78        128
countParallelN 13               3141592.5 ns   20192.61        128
countParallelN 14               3162710.2 ns   25868.55        128
countParallelN 15               3177212.7 ns   18341.45        128
countParallelN 16               3198783.4 ns    9406.41        128

It seems to be a bit faster, however not by a lot. This is properly because we now reuse threads and therefore remove some of the thread creation overhead.


