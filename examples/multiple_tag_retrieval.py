import sys_parent # noqa
from plantio.client import (
    Client,
    FIT,
    LIT
)

# Instantiates tag classes for LIT101, LIT301, FIT101, FIT301
lit101 = LIT(1, 101)
lit301 = LIT(3, 301)
fit101 = FIT(1, 101)
fit301 = FIT(3, 301)

sa_client = Client()
# Use this if you want cached values
# sa_client = Client(cache_time_limit=0.1)
# Shares the socket for the different tags
sa_client.share_client([
    fit101,
    fit301,
    lit101,
    lit301
])

fit101_val = fit101.value
fit101_time = fit101.time

fit301_val = fit301.value
fit301_time = fit301.time

lit101_val = lit101.value
lit101_time = lit101.time

lit301_val = lit301.value
lit301_time = lit301.time

print(f"{fit101.tag}: {fit101_time} => {fit101_val}")
print(f"{fit301.tag}: {fit301_time} => {fit301_val}")
print(f"{lit301.tag}: {lit101_time} => {lit101_val}")
print(f"{lit301.tag}: {lit301_time} => {lit301_val}")
