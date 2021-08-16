import socket


def check_connection(ipaddr):
    """
    Checks whether a socket is open for connection.

    Returns
    -------
    int
        The status of connection attempt.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    connection_result = s.connect_ex((ipaddr, 8080))
    s.close()
    return connection_result
