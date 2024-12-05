import os
import time
import sys
import logging
from datetime import datetime, timedelta, timezone
import threading
import copy

class NewSecondSender:
    _thread_tx_time_sender_running = False
    _thread_tx_time_sender = None
    _set_tx_time_callback_list = []
    _set_tx_time_callback_thread_safe_list = []
    _mutex = threading.Lock()

    @classmethod
    def start(cls):
        """
        Run the thread that calls the callback methods from the list
        on the beginning of each second.
        """
        cls._thread_tx_time_sender = threading.Thread(target=cls._tx_time_sender)
        cls._thread_tx_time_sender_running = True
        cls._thread_tx_time_sender.start()


    @classmethod
    def stop(cls):
        """
        Stop the thread that calls the callback methods from the list.
        """
        if cls._thread_tx_time_sender_running:
            cls._thread_tx_time_sender_running = False
            cls._thread_tx_time_sender.join()

    @classmethod
    def _tx_time_sender(cls):
        """
        Sleep exactly until the beginning of the next second and call the callback methods.
        """
        while cls._thread_tx_time_sender_running:
            # Get the current datetime
            current_datetime = datetime.now()
            # Calculate how much time to sleep to start at the beginning of the next second
            # Create a timedelta representing the time until the next second
            remaining_until_next_second = timedelta(seconds=1) - timedelta(microseconds=current_datetime.microsecond)
            remaining_until_next_second += timedelta(milliseconds=1)
            # Current datetime is updated to the next second
            current_datetime += remaining_until_next_second
            # Sleep for the calculated duration (converted to seconds)
            time.sleep(remaining_until_next_second.total_seconds())
            datetime_str = current_datetime.strftime('%d.%m.%y %H:%M:%S')
            for set_tx_time_cb in cls._set_tx_time_callback_list:
                set_tx_time_cb(datetime_str)
            # Update the list of callback methods
            with cls._mutex:
                cls._set_tx_time_callback_list = copy.copy(cls._set_tx_time_callback_thread_safe_list)

    @classmethod
    def register_set_tx_time_callback(cls, set_tx_time_callback):
        """
        Register a callback method that will be called on the beginning of each second.
        """
        with cls._mutex:
            cls._set_tx_time_callback_thread_safe_list.append(set_tx_time_callback)


def set_tx_time(tx_time):
    logging.info(f"TX time: {tx_time}")


def main():
    NewSecondSender.start()
    NewSecondSender.register_set_tx_time_callback(set_tx_time)

    while True:
        # Get the current datetime
        current_datetime = datetime.now()
        # Calculate how much time to sleep to start at the beginning of the next second
        # Create a timedelta representing the time until the next second
        remaining_until_next_second = timedelta(seconds=1) - timedelta(microseconds=current_datetime.microsecond)
        # Add 1 millisecond to the remaining time to ensure we are in the next second
        remaining_until_next_second += timedelta(milliseconds=1)
        current_datetime += remaining_until_next_second

        # Sleep for the calculated duration (converted to seconds)
        total_seconds = remaining_until_next_second.total_seconds()
        logging.info(f"Sleeping for {total_seconds} seconds")
        time.sleep(total_seconds)
        # Get the current time again
        # current_datetime = datetime.now()
        # Print the current time
        logging.info(f"Current time: {current_datetime.strftime('%d.%m.%y %H:%M:%S')}")



if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    # Run the main function
    main()
