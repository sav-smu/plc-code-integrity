import sys_parent # noqa
from plantio.client.subscribers import (
    ChannelType,
    DetectorSubscriber,
    SubscriberType
)

# Subscribes to the single type data from the 'DAD' detector
# and only for anomalies.
ds = DetectorSubscriber(
    detector_name="DAD",
    channel=ChannelType.SINGLE,  # [SINGLE, GROUP]
    subscriber_type=SubscriberType.ANOMALY  # [ALL, ANOMALY, PREDICTION]
)

# .poll_data() waits for the timeout period before returning the
# value or None if no data is received.
print(ds.poll_data())

# .wait_data() waits for the data to be received. It blocks
# execution.
print(ds.wait_data())
