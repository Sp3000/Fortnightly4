import os
import random
import subprocess
import unittest

COMMAND = "py -3 main.py"
TEST_FOLDER = "correctness_tests"

class TestBlockStructure(unittest.TestCase):        
    def setUp(self):
        self.process = subprocess.Popen(COMMAND.split(),
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        

    def run_test(self, in_filepath, expected_filepath):
        with open(expected_filepath) as expectedfile:
            # Possible answers are separated by |
            expected = [[x.strip() for x in line.strip().split("|")]
                        for line in expectedfile.read().strip().split("\n")]

        with open(in_filepath) as infile:
            input_ = infile.read().encode()

        output = self.process.communicate(input_)
        assert not output[1] # stderr
        
        stdin_output = [line.strip() for line in
                        output[0].decode().strip().split("\n")]

        if len(expected) != len(stdin_output):
            raise AssertionError("Expected {} lines, outputted {}".format(
                                 len(expected), len(stdin_output)))

        for i in range(len(expected)):
            if stdin_output[i] not in expected[i]:
                raise AssertionError("Output '{}' not in {}".format(stdin_output[i], expected[i]))


    def tearDown(self):
        self.process.terminate()


def create_test(testname):
    def run_testname(self):
        self.run_test("{}/{}.input".format(TEST_FOLDER, testname),
                      "{}/{}.expected".format(TEST_FOLDER, testname))

    return run_testname


if __name__ == '__main__':
    input_ = set()
    expected = set()

    for filename in os.listdir(TEST_FOLDER):
        if filename.endswith(".input"):
            input_.add(filename[:-6])

        if filename.endswith(".expected"):
            expected.add(filename[:-9])

    tests = input_ & expected

    for testname in tests:
        setattr(TestBlockStructure, "test_{}".format(testname), create_test(testname))

    ignored = input_ ^ expected

    if ignored:
        print("Ignored:", *ignored)
        
    unittest.main()
