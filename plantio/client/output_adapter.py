import ZODB.config
from ..helpers import (
    convert_key_value
    )
from .publishers import (
    DetectorGroupPublisher,
    DetectorPublisher
)
from ..constants import (
    GENERAL_FORWARDER_ENTRY_PORT,
    SPECIAL_KEYS,
    ZODB_KEYS,
    ZODB_PATH
)
from .graceful_killer import StatusCheckerInternal


class ZODBAdapter:
    """ An adapter used for accessing ZODB

    Attributes
    ----------
    _zodb : ZODB.config
        This instance is used to access ZODB/relstorage

    """
    def __init__(self):
        self._zodb = ZODB.config.databaseFromURL(ZODB_PATH)
        self.__validate_db(self._zodb)

    def __validate_db(self, db_obj):
        """ Validates ZODB with required keys

        Raises
        ------
        Exception
            If ZODB keys does not match the required keys. This means that
            the keys have not been instantiated in ZODB using the init script.

        """
        with db_obj.transaction() as cnx:
            current_keys = [i for i in cnx.root()]
            if not all([i in current_keys for i in ZODB_KEYS]):
                raise Exception((
                    "settings.db does not contain all of the required keys. "
                    "The required keys are: \n{}\n"
                    "Keys found are: \n{}"
                ).format(ZODB_KEYS, current_keys))

    def __get_all_detector_settings(self, ad_name):
        """ Retrieves the settings for a particular detector

        Parameters
        ----------
        ad_name : str
            Name for anomaly detector

        Returns
        -------
        dict
            Contains settings in dictionary form

        Raises
        ------
        Exception
            If settings is None

        """
        with self._zodb.transaction() as cnx:
            settings = cnx.root.detector_settings.get(ad_name)

        if settings is None:
            raise Exception((
                "The detector {} has not been initialised in the database. "
                "Consider initialising it using the PlantViz GUI."
            ).format(ad_name))
        return settings

    def get_settings(self, ad_name, process=None):
        """ Retrieves the settings for a particular process

        Parameters
        ----------
        ad_name : str
            Name of anomaly detector
        process : str or None
            Process name of detector

        Returns
        -------
        dict
            Contains settings for the detector and process

        """
        settings = self.__get_all_detector_settings(ad_name)
        key_value_settings = convert_key_value(
                                settings.get("processes", {}).get(process, {}),
                                SPECIAL_KEYS)
        return key_value_settings

    def update_settings(self, ad_name, process, new_settings):
        """ Updates the settings for a detector and process

        Parameters
        ----------
        ad_name : str
            Name of anomaly detector
        process : str
            Process name of detector
        new_settings : dict
            Dictionary containing new settings to be replaced in ZODB

        """
        old_settings = self.__get_all_detector_settings(ad_name)

        for k in old_settings.get(process, {}):
            if k in SPECIAL_KEYS:
                continue
            if new_settings.get(k) != old_settings[process][k]["value"]:
                old_settings[process][k]["value"] = new_settings[k]

        with self._zodb.transaction() as cnx:
            all_detector_settings = cnx.root.detector_settings
            all_detector_settings[ad_name] = old_settings
            cnx.root.detector_settings = all_detector_settings


class OutputAdapter(
        DetectorPublisher,
        ZODBAdapter,
        StatusCheckerInternal
        ):
    """ Class used to publish data onto prediction and/or anomaly topic,
    accessing/updating detector settings and also checking the running status
    of any module.

    Attributes
    ----------
    ad_name : str
        Name of anomaly detector
    process : str
        Process name of detector
    remote : bool
        Indicates if detectors is running local to server, or remotely
    host : str
        Host address to connect to for publishing data
    port : str
        Host port to connect to for publishing data
    file_name : str or None
        The file name of the script using this class

    """
    def __init__(self, ad_name=None, process=None, remote=False,
                 host="0.0.0.0", port=GENERAL_FORWARDER_ENTRY_PORT,
                 only_anomaly=False, file_name=None):
        DetectorPublisher.__init__(
            self,
            ad_name=ad_name,
            process=process,
            host=host,
            port=port,
            only_anomaly=only_anomaly)
        self.remote = remote
        if self.remote is False:
            ZODBAdapter.__init__(self)
        if file_name is not None and not self.remote:
            StatusCheckerInternal.__init__(
                self,
                ad_name=ad_name,
                file_name=file_name
            )


class GroupOutputAdapter(
        DetectorGroupPublisher,
        ZODBAdapter,
        StatusCheckerInternal
        ):
    """ Class used to publish data onto prediction and/or anomaly topic,
    accessing/updating detector settings and also checking the running status
    of any module.

    Attributes
    ----------
    ad_name : str
        Name of anomaly detector
    process : str
        Process name of detector
    remote : bool
        Indicates if detectors is running local to server, or remotely
    host : str
        Host address to connect to for publishing data
    port : str
        Host port to connect to for publishing data
    file_name : str or None
        The file name of the script using this class

    """
    def __init__(self, ad_name=None, process=None, remote=False,
                 host="0.0.0.0", port=GENERAL_FORWARDER_ENTRY_PORT,
                 only_anomaly=False, file_name=None):
        DetectorGroupPublisher.__init__(
            self,
            ad_name=ad_name,
            host=host,
            port=port,
            only_anomaly=only_anomaly)
        self.remote = remote
        if self.remote is False:
            ZODBAdapter.__init__(self)
        if file_name is not None and not self.remote:
            StatusCheckerInternal.__init__(
                self,
                ad_name=ad_name,
                file_name=file_name
            )
