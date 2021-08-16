import os

_BASE_TOPIC = "#PlantIO"
BASE_ANOMALY_TOPIC = "{}/anomaly".format(_BASE_TOPIC)
BASE_DETECTOR_RESPONSE_TOPIC = "{}/controller/response".format(_BASE_TOPIC)
BASE_EVENT_TOPIC = "{}/event".format(_BASE_TOPIC)
BASE_PREDICTION_TOPIC = "{}/prediction".format(_BASE_TOPIC)

BASE_GROUP_ANOMALY_TOPIC = f"{_BASE_TOPIC}/group/anomaly"
BASE_GROUP_PREDICTION_TOPIC = f"{_BASE_TOPIC}/group/prediction"

ACTUAL_TOPIC = "{}#".format(_BASE_TOPIC)
ANOMALY_TOPIC = BASE_ANOMALY_TOPIC + "/{}#"
ATTACK_TOPIC = "{}/attack#".format(_BASE_TOPIC)
CONSOLIDATE_TOPIC = "#PlantIO/collate#"
CONTROLLER_COMMAND_TOPIC = "#PlantIO/controller/command#"
DETECTOR_RESPONSE_TOPIC = BASE_DETECTOR_RESPONSE_TOPIC + "/{}#"
EVENT_TOPIC = BASE_EVENT_TOPIC + "/{}#"
PREDICTION_TOPIC = BASE_PREDICTION_TOPIC + "/{}#"

GROUP_ANOMALY_TOPIC = BASE_GROUP_ANOMALY_TOPIC + "/{}#"
GROUP_PREDICTION_TOPIC = BASE_GROUP_PREDICTION_TOPIC + "/{}#"

TOPIC_STREAM_MAP = {
    ACTUAL_TOPIC: "actual",
    BASE_ANOMALY_TOPIC: "anomaly",
    BASE_DETECTOR_RESPONSE_TOPIC: "detector",
    BASE_EVENT_TOPIC: "event",
    BASE_GROUP_ANOMALY_TOPIC: "groupAnomaly",
    BASE_GROUP_PREDICTION_TOPIC: "groupPrediction",
    BASE_PREDICTION_TOPIC: "prediction"
}

CA_CERT = os.path.abspath(
            os.path.join(
                os.path.realpath(__file__),
                os.pardir,
                "files",
                "certs",
                "ca.pem"
                )
            )

CLIENT_CERT = os.path.abspath(
            os.path.join(
                os.path.realpath(__file__),
                os.pardir,
                "files",
                "certs",
                "client-cert.pem"
                )
            )

CLIENT_KEY = os.path.abspath(
            os.path.join(
                os.path.realpath(__file__),
                os.pardir,
                "files",
                "certs",
                "client-key.pem"
                )
            )

CSV_LABELS = [
    "Timestamp",
    "Tag",
    "Actual Value",
    "Predicted Value",
    "Process",
    "Hash"
]
CONSOLIDATE_PORT = "7002"
DETECTOR_FORWARDER_ENTRY_PORT = "5003"
DETECTOR_FORWARDER_EXIT_PORT = "6003"

KNOWN_PREFIX = [
    "AIT",
    "DPIT",
    "DPSH",
    "FIT",
    "LIT",
    "MV",
    "P",
    "PIT",
    "PLC",
    "Plant",
    "PSH",
    "SA1",
    "UV",
    "SS"
]

LEVELS = {
    "SWaT": ["LowLow", "Low", "High", "HighHigh"]
}

LIMITS = {
    "SWaT": {
        "AIT": {
            "201": [50, 250, 260, 950],
            "202": [3.00, 6.95, 7.05, 12.00],
            "203": [100, 440, 480, 750],
            "401": [0, 0, 80, 100],
            "402": [200, 250, 300, 800],
            "501": [0, 0, 0, 0],
            "502": [0, 0, 250, 300],
            "503": [0, 250, 260, 500],
            "504": [0, 0, 30, 35]
        },
        "LIT": {
            "101": [250, 500, 800, 1000],
            "301": [250, 800, 1000, 1198],
            "401": [250, 800, 1000, 1100]
        },
        "FIT": {
            "101": [0.5, 1.0, 3.0, 4.0],
            "201": [0.0, 0.0, 2.5, 3.0],
            "301": [0, 0, 3, 3.5],
            "401": [0.5, 1.0, 2.0, 3.0],
            "501": [0, 1, 2, 3],
            "502": [0, 0, 0, 0],
            "503": [0, 0, 0, 0],
            "504": [0, 0, 1.0, 3.5]
        },
        "DPIT": {
            "301": [10, 15, 40, 100]
        },
    }
}

MESSAGE_LEN = 2

MYSQL_CONF_PATH = os.path.abspath(
                    os.path.join(
                        os.path.realpath(__file__),
                        os.pardir,
                        "files",
                        "db.conf.json"
                        )
                    )

GENERAL_FORWARDER_ENTRY_PORT = "5002"
GENERAL_FORWARDER_EXIT_PORT = "6002"

GENERIC_PYTHON = "python3"

PROXY_PORT_MAP = {
    "CSV": "7001",
    "DIGITALTWIN": "7002",
    "HISTORIAN": "7003"
}

SERVER_CERT = os.path.abspath(
                os.path.join(
                    os.path.realpath(__file__),
                    os.pardir,
                    "files",
                    "server_certs",
                    "server.crt"
                    )
                )

SERVER_KEY = os.path.abspath(
                os.path.join(
                    os.path.realpath(__file__),
                    os.pardir,
                    "files",
                    "server_certs",
                    "server.key"
                    )
                )

SPECIAL_KEYS = ["associatedTags"]

TAG_TYPES = {
    "SWaT": {
        "AIT": "number",
        "DPIT": "number",
        "DPSH": "number",
        "FIT": "number",
        "LIT": "number",
        "MV": "bool",
        "P": "bool",
        "PIT": "number",
        "PSH": "number",
        "UV": "bool"
    }
}

VENV_COMMAND = "/venv/bin/python"

WEBSOCKET_SERVER_PORT = 6001

ZODB_KEYS = [
    "store_settings",
    "detector_settings",
    "mysql_conf",
    "bridge_conf"
]

ZODB_PATH = os.path.abspath(
                os.path.join(
                    os.path.realpath(__file__),
                    os.pardir,
                    "files",
                    "zodb.config"
                    )
                )
