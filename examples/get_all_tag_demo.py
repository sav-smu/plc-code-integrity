import sys_parent # noqa
from plantio.client import Client

sa_client = Client(cache_time_limit=0)
data = sa_client.get_all_tag_values()
print(f"{data['Timestamp']} => {data['LIT101']}")
