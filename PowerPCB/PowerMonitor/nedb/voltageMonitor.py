#!/usr/bin/env python

import argparse
import logging
import sys
import time
from ina219 import INA219

SHUNT_OHMS = 0.15
MAX_EXPECTED_AMPS = 1.0

def configure(address):
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=address, log_level=logging.INFO)
    ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)
    return ina

def read(address, output_file, monitor_label):
    try:
        ina = configure(address)

        with open(output_file, 'a') as file:
            sys.stdout = file  # Redirect stdout to the file
            print(f"********* {monitor_label} ***********")
            print("  Bus Voltage    : %.3f V" % ina.voltage())
            print("  Bus Current    : %.3f mA" % ina.current())
            print("  Supply Voltage : %.3f V" % ina.supply_voltage())
            print("  Shunt voltage  : %.3f mV" % ina.shunt_voltage())
            print("  Power          : %.3f mW" % ina.power())
            print()

    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        sys.exit(1)  # Exit with a non-zero error code

def useReadInputPower(address):
    try:
        ina = configure(address)
        return ina
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        sys.exit(1)  # Exit with a non-zero error code


def main():
    parser = argparse.ArgumentParser(description="Monitor INA219 sensors")
    parser.add_argument("-o", "--output-file", default="output.txt", help="Output file argument")
    parser.add_argument("-t", "--timespan-to-record", type=int, default=60000, help="Timespan to record in milliseconds")

    args = parser.parse_args()

    print(f"Output file: {args.output_file}")
    print(f"Timespan to Record: {args.timespan_to_record} milliseconds")

    output_file = args.output_file
    print_lines = []  # To store lines for printing and writing

    start_time = time.time()
    end_time = start_time + (args.timespan_to_record / 1000)  # Convert milliseconds to seconds

    while time.time() < end_time:
        read(0x40, output_file, "MONITOR #1")
        read(0x44, output_file, "MONITOR #2")
        read(0x45, output_file, "MONITOR #3")
        time.sleep(5)  # Sleep for 5 seconds before the next iteration

if __name__ == "__main__":
    main()
