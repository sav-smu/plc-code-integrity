import asyncio
import time
import zmq
from tornado.ioloop import IOLoop
from ..constants import (
    ACTUAL_TOPIC,
    EVENT_TOPIC
)


def graceful_shutdown(server, logger, sig, frame):
    """
    Starts the process of shutting down any server in the current
    IOLoop instance and stops the IOLoop once that is done.

    Parameters
    ----------
    server : tornado.httpserver.HTTPServer
        Server to shutdown
    logger : logging.logger
        Logger to be used to logging shutdown sequence.
    sig : signal number
        The signal received by the program that starts the shutdown
        sequence.
    frame : stack frame
        The current stack frame upon shutdown request.
    """
    deadline = 3
    now = time.time()
    io_loop = IOLoop.current()

    tasks = []
    for i in asyncio.all_tasks():
        if i is not asyncio.current_task() and not i.done():
            tasks.append(i)
    if now < deadline and len(tasks) > 0:
        logger.info(f"Awaiting {len(tasks)} pending tasks: {tasks}")
        io_loop.add_timeout(
            now + 1,
            graceful_shutdown,
            server,
            deadline)
        return

    pending_cnx = len(server._connections)
    if now < deadline and pending_cnx > 0:
        logger.info(f"Waiting on {pending_cnx} connections to complete.")
        io_loop.add_timeout(
            now + 1,
            graceful_shutdown,
            server,
            deadline)
    else:
        logger.info(f"Continuing with {pending_cnx} connections open.")
        logger.info("Stopping IOLoop")
        io_loop.stop()
        logger.info("Shutdown complete.")


def publish_actual(socket, data, topic=ACTUAL_TOPIC):
    """
    Publishes data on an actual topic.

    This will send a multipart message. The first part is a string, the
    second part is a JSON object.

    Parameters
    ----------
    socket : zmq.Context.socket
        The socket to be used for publishing.
    data : dict
        Dictionary containing necessary data to be published.
    topic : str, optional
        The topic to publish on.
    """
    socket.send_string(topic,
                       flags=zmq.SNDMORE,
                       encoding="utf-8")
    socket.send_json(data)


def publish_event(detector_name=None, module_name=None, event_type="thread",
                  alive=False, error_msg=None, socket=None):
    """
    Publishes data on the event topic.

    This will send a multipart message. The first part is a string, the
    second part is a JSON object. Set of keys in data are:
    {
        "eventType",
        "detectorName",
        "thread",
        "alive",
        "errorMessage"
    }

    Parameters
    ----------
    detector_name : str or None
        Detector name.
    module_name : str or None
        Module name.
    event_type : str
        Either `thread` or `process`
    alive : bool
        Specifies whether thread/process is alive. Default: False.
    error_msg : str or None,
        The error message that is accompanying the event.
    socket : zmq.Context.socket
        The socket to be used for publishing.

    Raises
    ------
    Exception
        Different exceptions based on whether any of the params is
        None.
    """
    if socket is None:
        raise Exception((
            "Socket object is not provided."
        ))
    if event_type == "process" and module_name is not None:
        raise Exception((
            "The event_type parameter should be 'thread' if "
            "module_name parameter is being used."
        ))
    if event_type == "process" and detector_name is None:
        raise Exception((
            "The event_type parameter is 'thread' but detector_name "
            "is set to 'None'."
        ))
    if event_type not in ["process", "thread"]:
        raise Exception((
            "The event_type parameter should be either 'thread' "
            f"or 'process'. Currently it is '{event_type}'."
        ))
    socket.send_string(EVENT_TOPIC.format(detector_name),
                       flags=zmq.SNDMORE,
                       encoding="utf-8")
    socket.send_json({
        "eventType": event_type,
        "detectorName": detector_name,
        "thread": module_name,
        "alive": alive,
        "errorMessage": error_msg
    })
