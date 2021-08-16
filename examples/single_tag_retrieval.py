import sys_parent # noqa
from plantio.client import LIT

# Instantiates LIT class for LIT101
lit101 = LIT(1, 101)

lit101_val = lit101.value
lit101_time = lit101.time  # Retrieves timestamp for the current value
print(f"{lit101.tag}: {lit101_time} => {lit101_val}")
