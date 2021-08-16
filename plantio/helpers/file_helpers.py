import logging
import os
import pandas
import time


def create_logger(logger_name, log_file_path, debug=False,
                  file_log_level=logging.INFO,
                  ch_log_level=logging.ERROR, file_name=None):
    """
    Creates a logger instance

    Parameters
    ----------
    logger_name : str
        Name of logger instance.
    log_file_path : str
        File path of log to be saved at.
    debug : bool, optional
        Sets the log level for stream handler.
    file_log_level : logging.LEVEL, optional
        Specifies the log level for file handler.
    ch_log_level : logging.LEVEL, optional
        Specifies the log level for stream handler.
    file_name : str or None, optional
        The log file name. If None, then the time created will be used.

    Returns
    -------
    logger instance
    """
    if file_name is None:
        file_name = time.strftime("%Y%m%dT%H%M%S", time.localtime())
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s()"
        "\n\t%(message)s")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(f"{log_file_path}/{file_name}.log")
    handler.setFormatter(formatter)
    handler.setLevel(file_log_level)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(ch_log_level)
    if debug:
        ch.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(ch)
    return logger


def export_csv(csv_data, csv_path, labels):
    """
    Export data to CSV format.

    Converts list data into dataframe before exporting into a CSV file.

    Parameters
    ----------
    csv_data : list of list
        List containing flexible sub-lists of equal lengths.
    labels : list of str
        List containing the headers for the CSV file. This will determine
        the length of each sub-list in `csv_data`.

    Returns
    -------
    pandas.DataFrame or None
        This dataframe contains the data from `csv_data` and `labels`.
        None is return in the event of exceptions.
    """
    try:
        df = pandas.DataFrame.from_records(csv_data, columns=labels)
        df["Timestamp"] = df["Timestamp"].apply(
                                            lambda x:
                                            time.strftime("%d/%m/%Y "
                                                          "%I:%M:%S %p",
                                                          time.localtime(x)))
        df.to_csv(csv_path, index=False)
        return df
    except Exception:
        return None


def mk_folder(dir_path, folder):
    """
    Creates a folder

    Parameters
    ----------
    dir_path : str
        Location of where to create folder.
    folder : str
        The name of the folder to be created.
    """
    try:
        os.makedirs(dir_path + folder, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(dir_path + folder)
        except OSError as exc:
            if (exc.errno == exc.errno.EEXIST and
               os.path.isdir(dir_path + folder)):
                pass
            else:
                raise


def set_log_level(item, level):
    """
    Sets the log level for any logging instance.

    Parameters
    ----------
    item : str or list
        The name of the logging instance to change the log level.
    level : logging.LEVEL
        The logging level.

    Raises
    ------
    TypeError
        If item is not str or list.
    """
    if type(item) is str:
        logging.getLogger(item).setLevel(level)
    elif type(item) is list:
        for module in item:
            logging.getLogger(module).setLevel(level)
    else:
        raise TypeError("Type of item should be either str or list.")
