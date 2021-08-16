
import re
import zmq
import time
import json
from ..constants import (
    ACTUAL_TOPIC,
    GENERAL_FORWARDER_EXIT_PORT,
    LIMITS
)
from .graceful_killer import graceful_killer


class SA:
    LowLow = 0
    Low = 1
    High = 2
    HighHigh = 3


# Topic map for when data_source is specified by user.
# Subject to change in future
TOPIC_MAP = {
    "CSV": ACTUAL_TOPIC,
    "DIGITALTWIN": ACTUAL_TOPIC,
    "HISTORIAN": ACTUAL_TOPIC
    }


class Client:
    end_of_code = False

    def __init__(self, host="localhost", port=GENERAL_FORWARDER_EXIT_PORT,
                 topic=ACTUAL_TOPIC, cache_time_limit=0, data_source=None,
                 location="SWaT"):
        # private attributes
        self.__re_pattern = re.compile(r"((AIT|DPIT|DPSH|FIT|LIT|MV|P|PIT|"
                                       r"PSH|UV)[0-9]{3}|"
                                       r"P\dSA1|"
                                       r"Plant|"
                                       r"PLC[0-9])")
        self.__ip_patten = re.compile(r"(^\d{1,3}\."
                                      r"\d{1,3}\."
                                      r"\d{1,3}\."
                                      r"\d{1,3}$)")
        self.__topic_pattern = re.compile(r"^\#([^\r\n\t\f\v\# ]+)\#$")
        self.__range_limit = (0, 1)
        self.latest_timestamp = 0
        self.loc_limits = LIMITS[location]

        self.config(
            host=host, port=port,
            topic=topic, cache_time_limit=cache_time_limit,
            data_source=data_source)

        self.local_cache = {}
        self.last_cache_time = time.time()

    def __check_set_cache_time_limit(self, cache_time_limit):
        if not (self.__range_limit[0]
                <= cache_time_limit <=
                self.__range_limit[1]):
            raise Exception("Error: cache_time_limit has to be in the range "
                            "0 <= x <= 1 .")
        self.cache_time_limit = cache_time_limit

    def __check_set_data_source(self, data_source):
        if data_source not in ["CSV", "DIGITALTWIN", "HISTORIAN",
                               "PLAYER", None]:
            raise Exception("Error: data_source parameter is not recognised.")
        self.data_source = data_source

    def __check_set_host(self, host):
        match_host = re.match(self.__ip_patten, host)
        if match_host is None and host != "localhost":
            raise Exception("Error: Invalid IP address defined in host "
                            "keyword parameter.")
        if match_host is not None and host != "localhost":
            octets = host.split(".")
            for i in octets:
                if not 0 <= int(i) <= 255:
                    raise Exception("Error: Invalid IP address defined in "
                                    "host keyword parameter.")
        self.host = host

    def __check_set_port(self, port):
        if not port.isdigit():
            raise Exception("Error: Port specified is not a number.")

        if 0 <= int(port) < 1023:
            raise Exception("Error: Port specified is reserved for "
                            "privileged services.")
        self.port = port

    def __check_set_topic(self, topic):
        match_topic = re.match(self.__topic_pattern, topic)
        if match_topic is None:
            raise Exception("Error: Invalid topic format. Topic should start "
                            "and end with '#', and should not contain "
                            "the '#' in the middle.")
        # self.topic = TOPIC_MAP[self.data_source] if
        # self.data_source is not None else topic
        self.topic = topic

    def __connect_socket(self):
        try:
            self.socket.disconnect("tcp://{}:{}".format(self.host, self.port))
        except Exception:
            pass
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        self.socket.connect("tcp://{}:{}".format(self.host, self.port))

        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

    def __poll_data(self):
        if (len(self.local_cache) == 0 or
           time.time() - self.last_cache_time > self.cache_time_limit or
           self.end_of_code):
            poller = zmq.Poller()
            poller.register(self.socket, zmq.POLLIN)
            # wait for an event to process
            while not graceful_killer.kill_now:
                evts = dict(poller.poll(timeout=100))
                if self.socket in evts:
                    try:
                        raw_data = self.socket.recv(zmq.NOBLOCK)
                        raw_data = self.socket.recv_json()
                        # parsed_data = self.decode_data(raw_data)
                        if self.latest_timestamp >= raw_data["Timestamp"]:
                            continue
                        self.local_cache = raw_data
                        self.data_source = self.local_cache["data_source"]
                        self.latest_timestamp = self.local_cache["Timestamp"]
                        self.last_cache_time = time.time()
                        self.end_of_code = False
                    except Exception as e:
                        print("{}".format(e))
                    break

    def config(self, **kwargs):
        key_function_map = {
            "cache_time_limit": self.__check_set_cache_time_limit,
            "data_source": self.__check_set_data_source,
            "host": self.__check_set_host,
            "port": self.__check_set_port,
            "topic": self.__check_set_topic
        }
        for key in key_function_map.keys():
            if key == "data_source" or kwargs.get(key) is not None:
                key_function_map[key](kwargs.get(key))
        self.__connect_socket()

    def decode_data(self, raw_data):
        parsed_data = raw_data.decode("UTF-8")
        parsed_data = parsed_data.split(self.topic)[1]
        parsed_data = json.loads(parsed_data)
        return parsed_data

    def get_all_tags(self):
        all_tags = []
        if len(self.local_cache) != 0:
            search = self.__re_pattern
            for k in self.local_cache:
                if re.match(search, k):
                    all_tags.append(k)
        return all_tags

    def get_all_tag_values(self):
        all_tag_values = {}
        self.__poll_data()
        if len(self.local_cache) != 0:
            search = self.__re_pattern
            for k, v in self.local_cache.items():
                if re.match(search, k):
                    all_tag_values[k] = v
            all_tag_values["Timestamp"] = self.local_cache["Timestamp"]
        return all_tag_values

    def get_current_value(self, tag):
        # Block retrieves new values if cache_time_limit is exceed,
        # else will use local_cache values
        self.__poll_data()
        if tag not in self.local_cache:
            return -99999.99999

        cached_data_source = self.local_cache.get("data_source", None)
        if cached_data_source != self.data_source:
            self.data_source = cached_data_source
        return self.local_cache[tag]

    def share_client(self, tags):
        if type(tags) is not list:
            tags.client = self
        else:
            for tag in tags:
                tag.client = self


class DataSource(object):
    _time = 0

    def __init__(self, plc, tag):
        self.client = Client()
        self.plc = plc
        self.tag = tag

    def get(self):
        value = self.client.get_current_value(self.tag)
        return value

    @property
    def time(self):
        if self._time <= self.client.latest_timestamp:
            self.get()
        self.time = self.client.latest_timestamp
        return self._time

    @time.setter
    def time(self, value):
        self._time = value


class Numeric(DataSource):

    def __init__(self, plc, subtype, tag):
        super(Numeric, self).__init__(plc, "%s%s" % (subtype, tag))

    @property
    def value(self):
        val = self.get()
        try:
            val = float(val)
        except Exception:
            pass
        return val

    @property
    def isLow(self):
        return self.value <= self.limits[SA.Low]

    @property
    def isLowLow(self):
        return self.value <= self.limits[SA.LowLow]

    @property
    def isHigh(self):
        return self.value >= self.limits[SA.High]

    @property
    def isHighHigh(self):
        return self.value >= self.limits[SA.HighHigh]


class Boolean(DataSource):

    def __init__(self, plc, subtype, tag):
        super(Boolean, self).__init__(plc, "%s%s" % (subtype, tag))

    @property
    def value(self):
        return self.get()

    @property
    def isOn(self):
        return self.get() == 2

    @property
    def isNotOn(self):
        return not self.isOn

    @property
    def isOff(self):
        return self.get() == 1

    @property
    def isTrans(self):
        return self.get() == 0


class NumberTag(DataSource):

    def __init__(self, tag):
        super(NumberTag, self).__init__(None, tag)

    @property
    def value(self):
        return self.get()

    @property
    def isOn(self):
        return self.get()

    @property
    def isOff(self):
        return self.get()
# Correct this


class PLC():

    def __init__(self, plc):
        self.plc = plc
        self.client = Client()

    @property
    def state(self):
        return self.client.get_current_value("PLC%d" % self.plc)

    @property
    def isNotOne(self):
        return self.state != 1

    @property
    def isOne(self):
        return not self.isNotOne


class Plant():

    def __init__(self):
        self.client = Client()

    @property
    def start(self):
        return bool(self.client.get_current_value("Plant"))

    @property
    def stop(self):
        return not self.start


class LIT(Numeric):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(LIT, self).__init__(plc, "LIT", tag)
        self.limits = self.client.loc_limits["LIT"].get(tag)


class AIT(Numeric):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(AIT, self).__init__(plc, "AIT", tag)
        self.limits = self.client.loc_limits["AIT"].get(tag)


class PIT(Numeric):

    def __init__(self, plc, tag):
        super(PIT, self).__init__(plc, "PIT", tag)


class FIT(Numeric):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(FIT, self).__init__(plc, "FIT", tag)
        self.limits = self.client.loc_limits["FIT"].get(tag)


class Pump(Boolean):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(Pump, self).__init__(plc, "P", tag)


class MV(Boolean):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(MV, self).__init__(plc, "MV", tag)


class PSH(Numeric):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(PSH, self).__init__(plc, "PSH", tag)


class DPIT(Numeric):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(DPIT, self).__init__(plc, "DPIT", tag)
        self.limits = self.client.loc_limits["DPIT"].get(tag)


class DPSH(Numeric):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(DPSH, self).__init__(plc, "DPSH", tag)


class UV(Boolean):

    def __init__(self, plc, tag):
        tag = str(tag)
        super(UV, self).__init__(plc, "UV", tag)


class SA1:

    def __init__(self, plc):
        self.plc = plc
        self.client = Client()

    @property
    def state(self):
        return self.client.get_current_value("P%dSA1" % self.plc)


if __name__ == "__main__":
    client = Client()
    test = LIT(1, 101)
    for i in range(5):
        print(test.value)
        print(test.time)
        time.sleep(1)

    test = MV(1, 101)

    for i in range(5):
        print(test.value)
        print(test.time)
        time.sleep(1)

    print(client.get_all_tags())
    print(client.get_all_tag_values())
