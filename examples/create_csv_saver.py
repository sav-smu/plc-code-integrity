import sys_parent # noqa
from plantio.database.data_handler import command_parser

# Creates a saver to save data from the forwarder_device
command_parser([
    "-ll", "20",
    "CSV",
    # Path to CSV file
    "-f", "results.csv",
    # file path to JSON file containing tags for actual values
    "-fth", "actual_tags.json",
    # file path to JSON file containing prediction tags
    "-fpc", "prediction.json",
    # flag for anomaly indicating that only anomalies are to be saved
    "-anom"
])
