#!/usr/bin/python

"""
General operations for the code.

"""

from datetime import datetime
import os


def check_path(file_path):
    """
    Check if directory exists. If not, create one.

    PARAMETERS
        file_path : str
            path to directory to save files (i.e. /Desktop/temp_folder/)

    RETURNS
        Nothing
    """

    if not os.path.exists(file_path):
        os.mkdir(file_path)


def write_to_log(msg,
                 log_file_dir="logs/",
                 log_text_file="ancira_car_log.txt"):
    """
    Document operations within a process.

    PARAMETERS
	    msg : str
	        the message you want documented in the log to track an operation

	    alert_time : datetime obj
			time at which the operation is running
			YYYY-MM-DD H : M : s : ss

		log_file_dir : str
			local path to directory to save log file

		log_text_file : str
		    name of the file.extension

	RETURNS
	"""

    check_path(log_file_dir)

    alert_time = datetime.now()

    log_file_path = log_file_dir + log_text_file
    f = open(log_file_path, "a+")
    f.write(f"{alert_time} : {msg} \n")
    f.close()

    print(f"{alert_time} : {msg} \n")