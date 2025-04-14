from Computer import Computer
from time import perf_counter_ns

comp = Computer('ScreenOn.5b',hertz = 0)

start = perf_counter_ns()
comp.run()
end = perf_counter_ns()
print(end - start)

