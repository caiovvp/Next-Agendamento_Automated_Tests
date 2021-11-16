#!/usr/bin/env python

#############################################################################
# Copyright 2020 F4E / GTD-SIR Barcelona, Spain
##
# testrunner is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# testrunner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with testrunner.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

import os
import argparse
from argparse import RawTextHelpFormatter
import subprocess as sp
from multiprocessing import Process


def worker_scenario(scenario_names, feature_files, output):
    """Runs a given scenario a single time"""
    cmd = ["behave"]
    if scenario_names is not None:
        for i in range(len(scenario_names)):
            cmd = cmd + ["-n"] + [scenario_names[i]]
    elif feature_files is not None:
        for i in range(len(feature_files)):
            cmd = cmd + [feature_files[i]]
    else:
        print("Running whole testsuite\n")
    if output is not None:
        cmd = cmd + ["-o"] + [output]
    sp.call(cmd)
    print("\n\n\n")


def runner_scenario_x_times(repetitions, scenario_names, feature_files, out):
    """
    Runs 'repetitions' times some given behave scenarios, features, or
    the whole testsuite.

    :param repetitions: (int) number of times that a given test scenario,
                        feature file, or whole test suite, shall be run
    :param scenario_names: (seq) list of scenario names to be run a given
                           'repetitions' times
    :param feature_files: (seq) list of feature-files to be run a given
                          'repetitions' times
    """
    if scenario_names is not None:
        to_test = scenario_names
    elif feature_files is not None:
        to_test = feature_files
    else:
        to_test = "testsuite"
    msg = ("\nRunning " + str(repetitions) + " times test(s):\n "
           + str(to_test) + "\n")
    print(msg)
    if out:
        out_name = os.path.splitext(out)[0]
        ext = os.path.splitext(out)[1]
    for i in range(repetitions):
        print("Iteration number: " + str(i+1))
        if out:
            out = out_name + "-" + str(i) + ext
        p = Process(target=worker_scenario,
                    args=(scenario_names, feature_files, out))
        p.start()
        p.join()


def main():

    parser = argparse.ArgumentParser(
                 description="Test Runner allowing to run n test scenarios",
                 formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "repetitions", type=int, nargs="?", default=1,
        help="Number of repetitions to run some given test/s\n"
        + "(default=1)")
    parser.add_argument(
        "-n", "--scenario-names", type=str, nargs="+", default=None,
        help="Name of the scenario/s to be run 'x' times\n"
             + "(default=None)")
    parser.add_argument(
        "-f", "--feature-files", type=str, nargs="+", default=None,
        help="Name of the behave feature-file/s to be run 'x' times\n"
             + "(default=None)")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Write output on specified file instead of stdout\n"
             + "(default=None)")

    args = parser.parse_args()

    runner_scenario_x_times(args.repetitions,
                            args.scenario_names,
                            args.feature_files,
                            args.output)


if __name__ == "__main__":
    main()

