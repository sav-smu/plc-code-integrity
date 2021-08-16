import json
import zmq
from ..client.graceful_killer import graceful_killer
from ..constants import (
    ANOMALY_TOPIC,
    ATTACK_TOPIC,
    BASE_ANOMALY_TOPIC,
    BASE_GROUP_ANOMALY_TOPIC,
    BASE_GROUP_PREDICTION_TOPIC,
    BASE_PREDICTION_TOPIC,
    GENERAL_FORWARDER_EXIT_PORT,
    GROUP_ANOMALY_TOPIC,
    GROUP_PREDICTION_TOPIC,
    MESSAGE_LEN,
    PREDICTION_TOPIC
)


class BaseSubscriber:
    """
    Base class for creating and connecting sockets

    Parameters
    ----------
    host : str
        Host address for connecting socket.
    port : str
        Host port for connecting socket.
    topics : str or list
        Topics to subscribe to.
    timeout : int
        Timeout in milliseconds to poll for data.
    """
    def __init__(self, host, port, topics, timeout):
        self.socket_params = f"tcp://{host}:{port}"
        self.timeout = timeout
        self.__connect_socket()
        self.__subscribe(topics)
        self.__create_poller()

    def __connect_socket(self):
        ctx = zmq.Context.instance()
        self.socket = ctx.socket(zmq.SUB)
        self.socket.connect(self.socket_params)

    def __create_poller(self):
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def __decode_data(self, message):
        _, data = message
        data = json.loads(data.decode("utf-8"))
        return data

    def __subscribe(self, topics):
        if type(topics) is str:
            self.socket.subscribe(topics)
        elif type(topics) is list:
            for topic in topics:
                self.socket.subscribe(topic)

    def poll_data(self):
        """
        Polls for data and returns regardless of whether data is received
        or not.

        Returns
        -------
        None or dict
            None if no data is available, dict if data is received.
        """
        evts = dict(self.poller.poll(timeout=self.timeout))
        data = None
        if self.socket in evts:
            message = self.socket.recv_multipart()
            if len(message) != MESSAGE_LEN:
                return data
            data = self.__decode_data(message)
        return data

    def wait_data(self):
        """
        A function to block further execution by waiting for data to be
        received by socket.

        Returns
        -------
        None or dict
            None in the case where user cancels the execution, but will
            always return a dict if the user waits and receives data.
        """
        while not graceful_killer.kill_now:
            data = self.poll_data()
            if data is not None:
                return data
        return None


class GeneralSubscriber(BaseSubscriber):
    """
    A subclass to initialize the default kwargs for BaseSubscriber.

    Parameters
    ----------
    host : str, optional
        Host address for connecting socket.
    port : str, optional
        Host port for connecting socket.
    topics : str or list, optional
        Topics to subscribe to.
    timeout : int, optional
        Timeout in milliseconds to poll for data.
    """
    def __init__(self, topics="", host="localhost",
                 port=GENERAL_FORWARDER_EXIT_PORT, timeout=100):
        BaseSubscriber.__init__(self, host, port, topics, timeout)


class ChannelType(object):
    """
    Object to hold channel constants.
    """
    GROUP = "group"
    SINGLE = "single"


class SubscriberType(object):
    """
    Object to hold subscriber constants.
    """
    ALL = "all"
    ANOMALY = "anomaly"
    PREDICTION = "prediction"


class DetectorSubscriber(GeneralSubscriber):
    """
    A subscriber class specifically for subscribing to detector related
    topics.

    Parameters
    ----------
    detector_name : None or str, optional
        Name of detector to subscribe to.
    channel : str, optional
        Channel type to indicate whether group or single type topics are
        to be subcsribed to.
    subscriber_type : str, optional
        Indicated whether to subscribe to anomaly, prediction or all topics
        related to detectors.
    """
    def __init__(self, detector_name=None, channel=ChannelType.SINGLE,
                 subscriber_type=SubscriberType.ALL, *args, **kwargs):
        topics = []
        _anomaly_topic = self.__generate_anomaly_topics(
                            detector_name,
                            channel
                        )
        _prediction_topic = self.__generate_prediction_topics(
                                detector_name,
                                channel
                            )
        if subscriber_type == SubscriberType.ALL:
            topics = [
                _anomaly_topic,
                _prediction_topic
            ]
        elif subscriber_type == SubscriberType.ANOMALY:
            topics = _anomaly_topic
        elif subscriber_type == SubscriberType.PREDICTION:
            topics = _prediction_topic
        GeneralSubscriber.__init__(self, topics=topics, *args, **kwargs)

    def __generate_anomaly_topics(self, detector_name, channel):
        topics = ""
        if detector_name is not None:
            if channel == ChannelType.GROUP:
                topics = GROUP_ANOMALY_TOPIC.format(detector_name)
            elif channel == ChannelType.SINGLE:
                topics = ANOMALY_TOPIC.format(detector_name)
        elif detector_name is None:
            if channel == ChannelType.GROUP:
                topics = BASE_GROUP_ANOMALY_TOPIC
            elif channel == ChannelType.SINGLE:
                topics = BASE_ANOMALY_TOPIC
        return topics

    def __generate_prediction_topics(self, detector_name, channel):
        topics = ""
        if detector_name is not None:
            if channel == ChannelType.GROUP:
                topics = GROUP_PREDICTION_TOPIC.format(detector_name)
            elif channel == ChannelType.SINGLE:
                topics = PREDICTION_TOPIC.format(detector_name)
        elif detector_name is None:
            if channel == ChannelType.GROUP:
                topics = BASE_GROUP_PREDICTION_TOPIC
            elif channel == ChannelType.SINGLE:
                topics = BASE_PREDICTION_TOPIC
        return topics


class AttackSubscriber(GeneralSubscriber):
    """
    A subscriber class to subscribe to attack related topics.
    """
    def __init__(self, *args, **kwargs):
        GeneralSubscriber.__init__(self,
                                   topics=[
                                       ATTACK_TOPIC
                                    ],
                                   *args, **kwargs)
