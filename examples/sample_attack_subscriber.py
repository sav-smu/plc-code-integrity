import sys_parent # noqa
from plantio.client.subscribers import (
    AttackSubscriber
)
# Subscribes to the single type data from the 'DAD' detector
# and only for anomalies.
a_s = AttackSubscriber()

# .poll_data() waits for the timeout period before returning the
# value or None if no data is received.
print(a_s.poll_data())

# .wait_data() waits for the data to be received. It blocks
# execution.
print(a_s.wait_data())
