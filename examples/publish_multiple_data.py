import sys_parent # noqa
from plantio.client import (
    Client,
    FIT,
    GroupOutputAdapter,
    LIT,
)

# Instantiates OutputAdapter with the following details:
# MY_DETECTOR_NAME - name of detector
# remote: True - this means that your code will not be running on
#   PlantIO server, but on your own local machine
oa = GroupOutputAdapter("MY_DETECTOR_NAME", remote=True)
# Instantiates tag classes for LIT101, LIT301, FIT101, FIT301
lit101 = LIT(1, 101)
lit301 = LIT(3, 301)
fit101 = FIT(1, 101)
fit301 = FIT(3, 301)

sa_client = Client(cache_time_limit=0.1)
# Shares the socket for the different tags
sa_client.share_client([
    fit101,
    fit301,
    lit101,
    lit301
])

fit101_val = fit101.value
timestamp = fit101.time
fit301_val = fit301.value
lit101_val = lit101.value
lit301_val = lit301.value

# Data format is as such:
data = {
    fit101.tag: {
        "actual": fit101_val,
        "is_anomaly": True,
        "predicted": fit101_val + 10,
        "process": "PLC1"
    },
    "INVARIANT_1": {
        "actual": {
            "IS_ON": False,
            fit301.tag: fit301_val
        },
        "is_anomaly": True,
        "predicted": {
            "IS_ON": True
        },
        "process": "PLC1"
    },
    "INVARIANT_2": {
        "actual": {
            lit101.tag: lit101_val,
            lit301.tag: lit301_val
        },
        "is_anomaly": False,
        "predicted": {
            lit101.tag: lit101_val,
            lit301.tag: lit301_val
        },
        "process": "MIXED"
    }
}

# publish_prediction parameters:
# 1. timestamp
# 2. tag being predicted
# 3. data_source
# 4. annotation (optional)
# 5. additional fields (optional)
oa.publish_prediction(
    timestamp,
    data,
    data_source=lit301.client.data_source
)
