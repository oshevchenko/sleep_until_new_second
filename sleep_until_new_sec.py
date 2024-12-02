import os
import time
import sys
import logging
from datetime import datetime, timedelta, timezone

def main():
    while True:
        # Get the current datetime
        current_datetime = datetime.now()
        # Calculate how much time to sleep to start at the beginning of the next second
        # Create a timedelta representing the time until the next second
        remaining_until_next_second = timedelta(seconds=1) - timedelta(microseconds=current_datetime.microsecond)
        # Add 100 milliseconds to the remaining time to ensure we are in the next second
        # remaining_until_next_second += timedelta(milliseconds=100)
        current_datetime += remaining_until_next_second

        # Sleep for the calculated duration (converted to seconds)
        time.sleep(remaining_until_next_second.total_seconds())
        # Get the current time again
        current_datetime = datetime.now()
        # Print the current time
        logging.info(f"Current time: {current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")



if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    # Run the main function
    main()
