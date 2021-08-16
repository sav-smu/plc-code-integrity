import hashlib
import time
import zmq
from ..constants import (
    ATTACK_TOPIC,
    GENERAL_FORWARDER_ENTRY_PORT
)
import sqlite3 as sql
from datetime import datetime as dt


class AttackState(object):
    """
    Object to hold the different states of an attack.

    Attributes
    ----------
    START : str
        Maps to 'AL' which indicates 'Attack Launch'
    STOP : str
        Maps to 'AR' which indicates 'Attack Removed'
    UPDATE : str
        Maps to 'AU' which indicates 'Attack Updated'
    """
    START = "AL"
    STOP = "AR"
    UPDATE = "AU"


class AttackAdapter:
    """
    An adapter used to publish attack information.

    Attributes
    ----------
    end_time : int or None
        The end time of an attack.
    start_time : int or None
        The start time of an attack.
    attacker : str
        The attacker name conducting the attack.
    attack_name : str
        The name of the attack.
    time_offset : int or float
        The time difference between user's machine and historian's.
    intent : str
        The intent of the attack being carried out.
    attack_type : str
        The type of attack being carried out.
    attack_target : str
        The target of the attack being carried out.
    forwarder_host : str
        The host address for the forwarder device.

    Parameters
    ----------
    attacker : str
        The attacker name conducting the attack.
    attack_name : str
        The name of the attack.
    time_offset : int or float, optional
        The time difference between user's machine and historian's.
    intent : str, optional
        The intent of the attack being carried out.
    attack_type : str, optional
        The type of attack being carried out.
    attack_target : str, optional
        The target of the attack being carried out.
    forwarder_host : str, optional
        The host address for the forwarder device.

    Raises
    ------
    Exception
        When `attacker` or `attack_name` is None. Also when `attacker` or
        `attack_name` is of inappropriate lengths.
    """
    end_time = None
    start_time = None

    def __init__(self, attacker=None, attack_name=None,
                 time_offset=0, intent="", attack_type="", attack_target="",
                 forwarder_host="localhost"):
        self.attacker = attacker
        self.attack_name = attack_name
        self.attack_hash = ""
        self.time_offset = time_offset
        self.intent = intent
        self.attack_type = attack_type
        self.attack_target = attack_target
        self.forwarder_host = forwarder_host

        if self.attacker is None or self.attack_name is None:
            raise Exception((
                "Please include attacker and attack names as a "
                "keyword argument e.g. "
                "AttackAdapter(attacker='John', attack_name='NN_ATTACK')"))
        elif ((len(self.attacker) > 20 or len(self.attacker) == 0)
              or (len(self.attack_name) > 20 or len(self.attack_name) == 0)):
            raise Exception("Please ensure that attacker and attack names "
                            "are more than 0 and less than or equal to 20")
        self.__connect_socket()
        self.__create_local_table()

    def __connect_socket(self):
        """
        Connects the ZMQ socket to the forwarder device.
        """
        ctx = zmq.Context.instance()
        self.socket = ctx.socket(zmq.PUB)
        self.socket.connect(
            f"tcp://{self.forwarder_host}:{GENERAL_FORWARDER_ENTRY_PORT}"
        )

    def __create_local_table(self):
        """
        Creates local SQLite file with attack_log table
        """
        con = sql.connect("swat.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS 'attack_log' ("
            "'start_time'	INTEGER NOT NULL DEFAULT 0,"
            "'end_time'	INTEGER NOT NULL DEFAULT 0,"
            "'team'	TEXT NOT NULL,"
            "'attack_name'	TEXT NOT NULL,"
            "'attack_hash'	TEXT NOT NULL,"
            "'time_offset'	REAL NOT NULL DEFAULT 0,"
            "'attack_info'	TEXT NOT NULL DEFAULT '',"
            "'attack_type'	TEXT,"
            "'attack_target'	TEXT,"
            "'timestamp'	INTEGER NOT NULL DEFAULT 0);"
        )
        con.commit()
        con.close()

    def __publish_data(self, timestamp, attack_state):
        """
        Publishes the attack data to the forwarder device.

        Parameters
        ----------
        timestamp : int
            The timestamp to be published.
        attack_state : str
            The attack state which the current data is associated to.
        """
        timestamp_string = time.strftime(
                        "%d/%m/%Y "
                        "%H:%M:%S",
                        time.localtime(timestamp)
                    )
        attributes = {
            "attack_name": self.attack_name,
            "attack_hash": self.attack_hash,
            "attack_type": self.attack_type,
            "attack_target": self.attack_target,
            "intent": self.intent,
            "attacker": self.attacker,
            "time_offset": self.time_offset
        }
        self.socket.send_string(
            ATTACK_TOPIC,
            flags=zmq.SNDMORE
        )
        self.socket.send_json(
            {
                **attributes,
                "Timestamp": timestamp,
                "Timestamp_string": timestamp_string,
                "attack_state": attack_state
            }
        )

    def add_new_info(self, start_time, end_time, timestamp):
        con = sql.connect("swat.db")
        cur = con.cursor()
        cur.execute(
            (
                "INSERT INTO attack_log "
                "(start_time, end_time, team, attack_name, attack_hash, "
                "time_offset, attack_info, attack_type, attack_target, "
                "timestamp) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)"),
            (
                start_time,
                end_time,
                self.attacker,
                self.attack_name,
                self.attack_hash,
                self.time_offset,
                self.intent,
                self.attack_type,
                self.attack_target,
                timestamp
            )
        )
        con.commit()
        con.close()

    def start(self):
        """
        Creates a `start_time` and publishes data with `AL` attack state.

        Raises
        ------
        Exception
            When the attack was not stopped, and a new attack is being created.
        """
        if self.start_time is not None:
            raise Exception((
                "Please stop the current attack before starting "
                "a new one."))
        self.start_time = int(time.time())
        self.attack_hash = hashlib.md5(
                                (
                                    f"{self.start_time}"
                                    f"{self.attacker}"
                                    f"{self.attack_name}"
                                ).encode("utf-8")
                            ).hexdigest()
        self.__publish_data(
            self.start_time,
            AttackState.START
        )
        now = dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
        self.add_new_info(
            now,
            0,
            0
        )

    def set_intent(self, intent):
        self.intent = intent

    def set_type(self, attack_type):
        self.attack_type = attack_type

    def set_target(self, target):
        self.attack_target = target

    def stop(self):
        """
        Resets the `start_time` and also creates a new `end_time`.
        Publishes data with the `AR` attack state.

        Raises
        ------
        Exception
            When no attack is currently being tracked and this function
            is called.
        """
        if self.start_time is None:
            raise Exception((
                "Please start the attack before stopping. Currently there are "
                "no attacks being recorded."
            ))
        self.start_time = None
        self.end_time = int(time.time())
        self.__publish_data(
            self.end_time,
            AttackState.STOP
        )
        now = dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
        self.add_new_info(
            0,
            now,
            0
        )

    def update_intent(self, intent, at_type, target):
        """
        Updates the `intent`, `attack_type` and `attack_target` attributes
        and publishes data with the 'AU' attack state.

        Raises
        ------
        Exception
            When there is no attack currently being tracked and this function
            is called.
        """
        if self.start_time is None:
            raise Exception((
                "Please start the attack before updating. Currently there are "
                "no attacks being recorded."
            ))
        self.set_intent(intent)
        self.set_type(at_type)
        self.set_target(target)
        self.__publish_data(
            int(time.time()),
            AttackState.UPDATE
        )
        now = dt.now().strftime("%d/%m/%Y %I:%M:%S %p")
        self.add_new_info(
            0,
            0,
            now
        )
