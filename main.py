"""Runs 5 Bit Computer

Author: Drake Setera

Date: 6/20/2025

Version: 3.1.0
"""


from Computer import Computer
from time import perf_counter_ns

# Change file name to 5 Bit file to execute 
comp = Computer('test2.5b')


start = perf_counter_ns()
comp.run()
end = perf_counter_ns()
print(end - start)
print(comp.RAM)