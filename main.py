"""Runs 5 Bit Computer

Author: Drake Setera

Date: 6/11/2025

Version: 3.0.0
"""


from Computer import Computer
from time import perf_counter_ns

# Change file name to 5 Bit file to execute 
comp = Computer('sub.5b')


start = perf_counter_ns()
comp.run()
end = perf_counter_ns()
print(end - start)
