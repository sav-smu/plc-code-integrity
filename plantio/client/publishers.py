import time
import zmq
import random
from operator import itemgetter
from itertools import chain
from ..helpers import round_floats
from ..constants import (
    ANOMALY_TOPIC,
    PREDICTION_TOPIC,
    GENERAL_FORWARDER_ENTRY_PORT,
    GROUP_ANOMALY_TOPIC,
    GROUP_PREDICTION_TOPIC
)


class BasePublisher:
    """ Base class to be used for publishing data

    Attributes
    ----------
    host : str
        Host address to connect to for publishing data
    port : str
        Host port to connect to for publishing data

    """
    def __init__(self, host="0.0.0.0", port=GENERAL_FORWARDER_ENTRY_PORT,
                 **kwargs):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.connect("tcp://{}:{}".format(host, port))

    def raise_if_none(self, var):
        """ Raises an exception if var is None

        Parameters
        ----------
        var : str or None
            The variable to be checked

        """
        if var is None or var == "":
            raise Exception(
                "NoneValueError: ad_name is set to None or ''. "
                "Please ensure that ad_name is set to the detector name."
            )


class DetectorGroupPublisher(BasePublisher):
    """
    Class used mainly by detectors for publishing prediction
    and/or anomaly data in groups.

    Attributes
    ----------
    ad_name : str
        Name of anomaly detector
    host : str
        Host address to connect to for publishing data
    port : str
        Host port to connect to for publishing data
    hashes_map : dict
        A mapping of unique hashes to the set of processes/script names/tags.
    consolidated_set : set
        The set containing all processes/script names/tags.
    only_anomaly : bool
        Whether to publish only anomalies
    required_keys : set
        Set of keys required for each prediction dictionary

    Parameters
    ----------
    ad_name : str or None
        Name of anomaly detector
    host : str, optional
        Host address to connect to for publishing data
    port : str, optional
        Host port to connect to for publishing data
    only_anomaly : bool, optional
        Whether to publish only anomalies

    Check for None value in ad_name
    """
    hashes_map = {}
    consolidated_set = set()
    required_keys = {"process",
                     "actual",
                     "predicted",
                     "is_anomaly"}

    def __init__(self, ad_name=None, host="0.0.0.0",
                 port=GENERAL_FORWARDER_ENTRY_PORT, only_anomaly=False):
        BasePublisher.__init__(self, host=host, port=port)
        self.raise_if_none(ad_name)
        self.ad_name = ad_name
        self.only_anomaly = only_anomaly

    def __check_shape(self, predictions):
        """
        Check each element of predictions against the `required_keys`

        Parameters
        ----------
        predictions : dict
            Dictionary of predictions, [tag: {values}]

        Raises
        ------
        TypeError
            If a different data type is provided
        Exception
            When missing keys are detected.
        """
        if not isinstance(predictions, dict):
            raise TypeError(f"Type `dict` expect. Got {type(predictions)}")
        for k, v in predictions.items():
            # Checks if v has all the required keys
            set_diff = self.required_keys.difference(v)
            if len(set_diff) != 0:
                raise Exception(f"Missing keys in `prediction`: {set_diff}")

    def __collate_anomalies(self, hashes_set, predictions):
        """
        Collates all predictions which are present in `hashes_set`

        Parameters
        ----------
        hashes_set : set
            Hashes for which the prediction is associated to.
        predictions : dictionary
            Contains predictions for various tags/invariants/processes.

        Returns
        -------
        dict
            Dictionary containing predictions which are present in `hashes_set`
        """
        collated = {}
        for i in hashes_set:
            collated[i] = predictions[i]
        return collated

    def __compare_sets(self, predictions):
        """
        Compares the `predictions` against the hashes present in
        `consolidated_set`.

        Parameters
        ----------
        predictions : dict
            All current predictions.

        Returns
        -------
        new_to_set : set
            Set containing tags/invariants/processes not previously found in
            `consolidated_set`.
        removed_from_set : set
            Set containing tags/invariants/processes no found in predictions
            but are in `consolidated_set`.
        """
        # Gets all tags/invariants/processes with is_anomaly == True
        current_set = set(
            [k for k, v in predictions.items() if v["is_anomaly"]]
        )
        new_to_set = current_set.difference(self.consolidated_set)
        removed_from_set = self.consolidated_set.difference(current_set)
        return new_to_set, removed_from_set

    def __discard_missing_element(self, hashes_map, removed_from_set):
        """
        Discards elements from `hashes_map` which are found in
        `removed_from_set`.

        Parameters
        ----------
        hashes_map : dict
            Contains {hash: tags/invariants/processes}
        removed_from_set : set
            Set containing tags/invariants/processes to be removed.

        Returns
        -------
        dict
            New dictionary containing removed elements.
        """
        new_hashes_map = {}
        for k, v in hashes_map.items():
            new_v = v
            new_v -= removed_from_set
            if len(new_v) != 0:
                new_hashes_map[k] = new_v
        return new_hashes_map

    def __generate_time_hash(self):
        """
        Generates a hash based on current time, random number and
        detector name.

        Returns
        -------
        str
            Time hash.
        """
        time_hash = "{}{}{}".format(
            str(time.time() * 1000)[:10],
            str(random.randrange(1, 999)).zfill(3),
            self.ad_name)
        return time_hash

    def __publish_anomaly(self, base_data, annotation):
        """
        Publishes anomaly on the group topic.

        Parameters
        ----------
        base_data : dict
            Dictionary containig data passed from publish_prediction.
        annotation : str or None
            Annotation to be passed to subscribers.
        """
        (timestamp, timestamp_string, predictions,
         data_source) = itemgetter(
                            "Timestamp",
                            "Timestamp_string",
                            "predictions",
                            "data_source"
                        )(base_data)
        new_to_set, removed_from_set = self.__compare_sets(predictions)
        self.hashes_map = self.__discard_missing_element(
                            self.hashes_map,
                            removed_from_set)
        new_anomalies = {}
        if len(new_to_set) != 0:
            new_time_hash = self.__generate_time_hash()
            self.hashes_map[new_time_hash] = new_to_set
            new_anomalies = {
                new_time_hash: self.__collate_anomalies(
                                    new_to_set,
                                    predictions
                                )
            }
        self.consolidated_set = set(
                                    chain.from_iterable(
                                        self.hashes_map.values()
                                    )
                                )
        current_anomalies = {}
        for time_hash, anomaly_set in self.hashes_map.items():
            current_anomalies[time_hash] = self.__collate_anomalies(
                                                anomaly_set,
                                                predictions
                                            )
        last_anomalous = (len(current_anomalies) == 0
                          and len(removed_from_set) != 0)
        if len(current_anomalies) != 0 or last_anomalous:
            self.socket.send_string(
                GROUP_ANOMALY_TOPIC.format(self.ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json({
                "Timestamp": timestamp,
                "Timestamp_string": timestamp_string,
                "new_anomalies": new_anomalies,
                "current_anomalies": current_anomalies,
                "old_anomalies": list(removed_from_set),
                "ad_name": self.ad_name,
                "data_source": data_source,
                "annotation": annotation
            })

    def publish_prediction(self, timestamp, predictions,
                           annotation=None, additional_fields={},
                           data_source=None):
        """
        Publishes predictions in a dictionary format for multiple
        processes/scripts/tags.

        Parameters
        ----------
        timestamp : int
            The timestamp in epoch seconds.
        predictions : dict
            Dictionary containing processes/scripts/tags to their values.
        annotation : str or None
            Annotation passed by the detector.
        additional_fields : dict
            Any additional fields that any user might want to include in
            published data.
        """
        self.__check_shape(predictions)
        base_data = {
            "Timestamp": timestamp,
            "Timestamp_string": time.strftime("%d/%m/%Y "
                                              "%I:%M:%S %p",
                                              time.localtime(timestamp)),
            "predictions": predictions,
            "ad_name": self.ad_name,
            "data_source": data_source
            }
        prediction = {**base_data, "additional_fields": additional_fields}
        if not self.only_anomaly:
            self.socket.send_string(
                GROUP_PREDICTION_TOPIC.format(self.ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json(prediction)
        self.__publish_anomaly(base_data, annotation)


class DetectorPublisher(BasePublisher):
    """ Class used mainly by detectors for publishing prediction
    and/or anomaly data

    Attributes
    ----------
    ad_name : str
        Name of anomaly detector
    process : str
        Process name of detector
    host : str
        Host address to connect to for publishing data
    port : str
        Host port to connect to for publishing data
    hash : str
        A unique hash to be generate to distinguish new vs old anomaly
    only_anomaly : bool
        Whether to publish only anomalies

    Parameters
    ----------
    ad_name : str or None
        Name of anomaly detector
    process : str, optional
        Process name of detector
    host : str, optional
        Host address to connect to for publishing data
    port : str, optional
        Host port to connect to for publishing data
    only_anomaly : bool
        Whether to publish only anomalies
    Check for None value in ad_name
    """
    def __init__(self, ad_name=None, process=None,
                 host="0.0.0.0", port=GENERAL_FORWARDER_ENTRY_PORT,
                 only_anomaly=False):
        BasePublisher.__init__(self, host=host, port=port)
        self.raise_if_none(ad_name)
        self.ad_name = ad_name
        self.hash = ""
        self.process = process
        self.only_anomaly = only_anomaly

    def __generate_time_hash(self, timestamp, is_anomaly):
        if is_anomaly and self.hash == "":
            self.hash = "{}{}{}".format(
                str(timestamp),
                str(random.randrange(1, 999)).zfill(3),
                self.ad_name)
            return True
        elif not is_anomaly:
            self.hash = ""
        return False

    def __publish_anomaly(self, prediction, is_anomaly, annotation):
        """ Publishes anomaly on the predefined topic found in
        ..constants.ANOMALY_TOPIC

        Parameters
        ----------
        prediction : dict
            Contains the prediction values
        is_anomaly : bool
            Whether the current prediction is an anomaly or not
        annotation : str or None
            Annotation passed by the detector

        Does not return anything, publishes data instead

        """
        timestamp = itemgetter("Timestamp")(prediction)
        old_hash = self.hash
        is_new_anomaly = self.__generate_time_hash(timestamp, is_anomaly)
        anomaly_data = {
            **prediction,
            "hash": self.hash,
            "is_new_anomaly": is_new_anomaly,
            "annotation": annotation
        }
        if is_anomaly:
            self.socket.send_string(
                ANOMALY_TOPIC.format(self.ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json(anomaly_data)
        elif not is_anomaly and old_hash != "":
            self.socket.send_string(
                ANOMALY_TOPIC.format(self.ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json(anomaly_data)

    def publish_prediction(self, timestamp, tag, oval,
                           pval, is_anomaly, annotation=None,
                           data_source=None, additional_fields={}):
        """ Publishes anomaly on the predefined topic found in
        ..constants.PREDICTION_TOPIC

        Parameters
        ----------
        timestamp : int
            The timestamp in epoch seconds
        tag : str or list
            Tag(s) for which prediction of values are for
        oval : str or float or int or list
            Actual value(s) for the tag(s). List can be any JSON convertible
            format
        pval : str or float or int or list
            Predicted value(s) for the tag(s). List can be any JSON convertible
            format
        is_anomaly : bool
            Whether the current prediction is an anomaly or not
        annotation : str or None
            Annotation passed by the detector
        additional_fields : dict
            Any additional fields that any user might want to include in
            published data

        Does not return anything, publishes data instead.
        Also calls __publish_anomaly

        """
        stringified_tag = tag
        if type(tag) is not str:
            stringified_tag = round_floats(tag)

        base_data = {
            "Timestamp": timestamp,
            "Timestamp_string": time.strftime("%d/%m/%Y "
                                              "%I:%M:%S %p",
                                              time.localtime(timestamp)),
            "ad_name": self.ad_name,
            "process": self.process,
            "tag": stringified_tag,
            "actual": oval,
            "predicted": pval,
            "data_source": data_source,
            "is_anomaly": is_anomaly
            }
        prediction = {**base_data, "additional_fields": additional_fields}
        if not self.only_anomaly:
            self.socket.send_string(
                PREDICTION_TOPIC.format(self.ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json(prediction)
        self.__publish_anomaly(base_data, is_anomaly, annotation)


class GeneralPublisher(BasePublisher):
    """ This class can be used by any script, regardless of detector or not,
    to publish anomaly or prediction data

    Attributes
    ----------
    host : str
        Host address to connect to for publishing data
    port : str
        Host port to connect to for publishing data
    data_source : str
        The data source which is currently being received as actual data
    hash : str
        A unique hash to be generate to distinguish new vs old anomaly

    """
    def __init__(self, host="0.0.0.0", port=GENERAL_FORWARDER_ENTRY_PORT,
                 data_source="CSV", only_anomaly=False):
        BasePublisher.__init__(self, host=host, port=port)
        self.hash = ""
        self.data_source = data_source
        self.only_anomaly = only_anomaly

    def __generate_time_hash(self, timestamp, is_anomaly, ad_name):
        """ Generates a hash to be set to the hash attribute

        Parameters
        ----------
        timestamp : int
            The timestamp in epoch seconds
        is_anomaly : bool
            Whether the current prediction is an anomaly or not
        ad_name : str
            Name of anomaly detector

        Returns
        -------
        bool
            Always True as we are assuming to generate a new hash each time

        """
        self.hash = "{}{}{}".format(
            str(timestamp),
            str(int(time.time() * 1000))[-3:],
            ad_name)
        return True

    def __publish_anomaly(self, prediction, is_anomaly, annotation, ad_name):
        """ Publishes anomaly on the predefined topic found in
        ..constants.ANOMALY_TOPIC

        Parameters
        ----------
        prediction : dict
            Contains the prediction values
        is_anomaly : bool
            Whether the current prediction is an anomaly or not
        annotation : str or None
            Annotation passed by the detector
        ad_name : str
            Name of anomaly detector

        Does not return anything, publishes data instead

        """
        timestamp = itemgetter("Timestamp")(prediction)
        is_new_anomaly = self.__generate_time_hash(
                            timestamp,
                            is_anomaly,
                            ad_name)
        anomaly_data = {
            **prediction,
            "hash": self.hash,
            "is_new_anomaly": is_new_anomaly,
            "annotation": annotation
        }
        if is_anomaly:
            self.socket.send_string(
                ANOMALY_TOPIC.format(ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json(anomaly_data)

    def publish_prediction(self, timestamp, tag, oval,
                           pval, is_anomaly, ad_name=None,
                           process=None, annotation=None,
                           additional_fields={}):
        """ Publishes anomaly on the predefined topic found in
        ..constants.PREDICTION_TOPIC

        Parameters
        ----------
        timestamp : int
            The timestamp in epoch seconds
        tag : str or list
            Tag(s) for which prediction of values are for
        oval : str or float or int or list
            Actual value(s) for the tag(s). List can be any JSON convertible
            format
        pval : str or float or int or list
            Predicted value(s) for the tag(s). List can be any JSON convertible
            format
        is_anomaly : bool
            Whether the current prediction is an anomaly or not
        annotation : str or None
            Annotation passed by the detector
        additional_fields : dict
            Any additional fields that any user might want to include in
            published data

        Does not return anything, publishes data instead.
        Also calls __publish_anomaly

        """
        self.raise_if_none(ad_name)

        stringified_tag = tag
        if type(tag) is not str:
            stringified_tag = round_floats(tag)

        base_data = {
            "Timestamp": timestamp,
            "ad_name": ad_name,
            "process": process,
            "tag": stringified_tag,
            "actual": oval,
            "predicted": pval,
            "data_source": self.data_source
            }

        prediction = {**base_data, **additional_fields}
        if not self.only_anomaly:
            self.socket.send_string(
                PREDICTION_TOPIC.format(ad_name),
                flags=zmq.SNDMORE,
                encoding="utf-8")
            self.socket.send_json(prediction)
        self.__publish_anomaly(base_data, is_anomaly, annotation, ad_name)
