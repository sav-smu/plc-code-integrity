import signal
import zmq
from pymemcache.client import base
from ..helpers.data_helpers import json_deserializer, json_serializer


class Singleton(type):
    """ Used to create a single instance of a subclass

    Attributes
    ----------
    _instances : dict
        Instances of the subclass

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Called when used by a subclass

        Parameters
        ----------
        cls : type
            The class which is being called

        Returns
        -------
        __call__ function of the instance
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                                                            *args,
                                                            **kwargs)
        return cls._instances[cls]


class GracefulKiller(metaclass=Singleton):
    """ A class used for checking for SIGINT or SIGTERM

    Attributes
    ----------
    _kill_now : bool
        Flag used to indicate whether signal has been received

    """
    _kill_now = False

    def __init__(self):
        """ Registers callbacks to SIGINT and SIGTERM """
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    @property
    def kill_now(self):
        """ Returns the current value of _kill_now """
        return self._kill_now

    @kill_now.setter
    def kill_now(self, value):
        """ Sets the values of _kill_now """
        self._kill_now = value

    def exit_gracefully(self, signum, frame):
        """ Mainly used as a callback function for the signals

        This sets the _kill_now to True using the setter
        """
        self._kill_now = True


class StatusChecker:
    """ Class mainly used for checking the running status of modules
    in memcached using pymemcache

    Attributes
    ----------
    ad_name : str
        The name of the anomaly detector
    module_name : str
        Module name without the '.py' extension
    client : pymemcache.client.base.Client
        The instance of client used to access memcached via pymemcache

    Raises
    ------
    Execption
        If detector name or file name is None

    """
    def __init__(self, ad_name=None, file_name=None):
        if ad_name is None or file_name is None:
            raise Exception((
                "Please ensure that ad_name and file_name has been "
                "provided."))
        self.ad_name = ad_name
        self.module_name = file_name.replace(".py", "")
        self.client = base.Client(
                        ("localhost", 11211),
                        serializer=json_serializer,
                        deserializer=json_deserializer
                        )

    def is_running(self):
        """ Checks the memcached for the running status of a module in a detector

        Returns
        -------
        bool
            Whether the module is currently running or not

        """
        running_status = self.client.get(f"running_status#{self.ad_name}", {})
        if self.module_name not in running_status:
            return False
        return running_status.get(self.module_name, False)


class StatusCheckerInternal:
    """ Class mainly used for checking the running status of modules
    in memcached using pymemcache

    Attributes
    ----------
    ad_name : str
        The name of the anomaly detector
    module_name : str
        Module name without the '.py' extension
    socket : zmq.Context.socket
        Socket for connecting to internal server for status
    poller : zmq.Poller
        Poller to poll socket's file descriptor.

    Raises
    ------
    Execption
        If detector name or file name is None

    """
    def __init__(self, ad_name=None, file_name=None):
        if ad_name is None or file_name is None:
            raise Exception((
                "Please ensure that ad_name and file_name has been "
                "provided."))
        self.ad_name = ad_name
        self.module_name = file_name.replace(".py", "")
        ctx = zmq.Context.instance()
        self.socket = ctx.socket(zmq.REQ)
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def is_running(self):
        """
        Checks the interal server for the running status of a module in a
        detector.

        Returns
        -------
        bool
            Whether the module is currently running or not
        """
        self.socket.send_json(self.module_name)
        evts = dict(self.poller.poll(50))
        if self.socket in evts:
            return self.socket.recv_json()
        return False


graceful_killer = GracefulKiller()
