import sys_parent # noqa
from plantio.client import (
    LIT,
    OutputAdapter
)

# Instantiates OutputAdapter with the following details:
# MY_DETECTOR_NAME - name of detector
# PLC1 - the stage/process being predicted.
#   Can also be not provided, defaults to None
# remote: True - this means that your code will not be running on
#   PlantIO server, but on your own local machine
oa = OutputAdapter("MY_DETECTOR_NAME", "PLC1", remote=True)
lit101 = LIT(1, 101)
lit101_val = lit101.value
lit101_time = lit101.time

fake_prediction = lit101_val + 10

# publish_prediction parameters:
# 1. timestamp
# 2. tag being predicted
# 3. actual value
# 4. predicted value
# 5. boolean: whether anomaly or not
# 6. data_source
# 7. annotation (optional)
# 8. additional fields (optional)
oa.publish_prediction(
    lit101_time,
    lit101.tag,
    lit101_val,
    fake_prediction,
    False,
    data_source=lit101.client.data_source
)
