import os
import glob
import sys
import time
import traceback
from typing import Generator

import requests

from aocdays import AOCDays

modules = filter(lambda x: not x.startswith('_'), glob.glob(os.path.dirname(__file__) + "/*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules]


def day(day_number):
    def day_decorator(cls):
        if not str(cls.__module__).replace("days.", "").startswith("_"):
            AOCDays.get_instance().add_day(day_number, cls)
        return cls
    return day_decorator


class AOCDay:
    creator = "Kevin"
    year = 2020
    day_number = 0
    session_token = ""
    input_filename = ""
    output_filename = ""
    input_data = None

    # Set to True to always print debug, or a combination of "1", "2", and "c" to print debug for part 1, 2, or common.
    # E.g. the value "1c" will print debug for part 1 and common.
    print_debug = False

    _running_common = False
    _running_part1 = False
    _running_part2 = False

    def __init__(self, year, day_number, session_token):
        self.year = year
        self.day_number = day_number
        self.session_token = session_token
        self.input_filename = os.path.join(os.path.dirname(__file__),
                                           "../inputs/day{}_{}".format(self.day_number, "input"))
        if self.creator == "Kevin":
            self.output_filename = os.path.join(os.path.dirname(__file__),
                                                "../outputs/day{}_{}".format(self.day_number, "output"))
        else:
            self.output_filename = os.path.join(os.path.dirname(__file__),
                                                "../outputs/day{}_{}_{}".format(self.day_number, "output", self.creator))

    def log(self, msg):
        print(msg)

    def debug(self, msg):
        if self.print_debug == True or (
                type(self.print_debug) == str and self.print_debug != "" and (
                    (self._running_common and "c" in self.print_debug) or
                    (self._running_part1 and "1" in self.print_debug) or
                    (self._running_part2 and "2" in self.print_debug)
                )
            ):
            print(msg)

    def error(self, msg):
        print(msg, file=sys.stderr)

    def download_input(self):
        if os.path.isfile(self.input_filename):
            return

        print("Could not find input data for day {}, please wait while I download it...".format(self.day_number))

        input_url = "https://adventofcode.com/{}/day/{}/input".format(self.year, self.day_number)
        result = requests.get(input_url, cookies={'session': self.session_token})
        if result.status_code == 200:
            self.input_data = result.text
            with open(self.input_filename, 'w') as f:
                f.write(result.text)
        else:
            raise ConnectionError("Could not connect to AoC website to download input data. "
                                  "Error code {}: {}".format(result.status_code, result.text))

    def load_input(self):
        if self.input_filename:
            with open(self.input_filename, 'r') as f:
                self.input_data = [x.replace("\n", "") for x in f.readlines()]
                if len(self.input_data) == 1:
                    self.input_data = self.input_data[0]

    def run(self):
        self.download_input()
        self.load_input()

        if os.path.isfile(self.output_filename):
            os.remove(self.output_filename)

        with open(self.output_filename, 'w') as output_file:
            def dprint(thing):
                print(thing, file=output_file)
                print(thing)

            input_data = self.input_data

            start_time = time.time()
            exception_or_output = False
            test_exception = False
            try:
                test = self.test(input_data)
                if test:
                    dprint("== Tests Output ==")
                    exception_or_output = True
                    for x in test:
                        dprint(x)
            except Exception as e:
                dprint("== Tests Error ==")
                dprint(''.join(traceback.format_exception(None, e, e.__traceback__)))
                exception_or_output = True
                test_exception = True
            if exception_or_output:
                dprint("== Tests ran in {:.3f} ms ==".format((time.time() - start_time) * 1000))
                dprint("")

            if test_exception:
                dprint("== NOT RUNNING PARTS BECAUSE OF TEST ERRORS ==")
            else:
                self._running_common = True
                start_time = time.time()
                common = self.common(input_data)
                if common:
                    dprint("== Common ==")
                    for x in common:
                        dprint(x)
                    dprint("")
                self._running_common = False

                dprint("== Part 1 ==")
                self._running_part1 = True
                part1 = self.part1(input_data)
                printed = False
                if part1:
                    for x in part1:
                        if not printed:
                            printed = True
                        dprint(x)
                if not printed:
                    dprint("(no output)")
                dprint("== Ran in {:.3f} ms ==".format((time.time() - start_time)*1000))
                self._running_part1 = False
                dprint("")

                self._running_common = True
                start_time = time.time()
                common = self.common(input_data)
                if common:
                    dprint("== Common ==")
                    for x in common:
                        dprint(x)
                    dprint("")
                self._running_common = False

                dprint("== Part 2 ==")
                self._running_part2 = True
                part2 = self.part2(input_data)
                printed = False
                if part2:
                    for x in part2:
                        if not printed:
                            printed = True
                        dprint(x)
                if not printed:
                    dprint("(no output)")
                dprint("== Ran in {:.3f} ms ==".format((time.time() - start_time)*1000))
                self._running_part2 = False
                dprint("")

    def test(self, input_data) -> Generator:
        pass

    def common(self, input_data) -> Generator:
        pass

    def part1(self, input_data) -> Generator:
        pass

    def part2(self, input_data) -> Generator:
        pass
