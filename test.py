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
            expected = [line.strip().split("|") for line in
                        expectedfile.read().strip().split("\n")]


        with open(in_filepath) as infile:
            input_ = infile.read().encode()

        stdin_output = [line.strip() for line in
                        self.process.communicate(input_)[0].decode().strip().split("\n")]

        if len(expected) != len(stdin_output):
            raise AssertionError("Expected {} lines, outputted {}".format(
                                 len(expected), len(stdin_output)))

        for i in range(len(expected)):
            if stdin_output[i] not in expected[i]:
                raise AssertionError("Output '{}' not in {}".format(stdin_output[i], expected[i]))


    def run_testname(self, testname):
        self.run_test("{}/{}.input".format(TEST_FOLDER, testname),
                      "{}/{}.expected".format(TEST_FOLDER, testname))


    def test_basic(self):
        self.run_testname("basic")


    def test_connect(self):
        self.run_testname("connect")


    def test_place(self):
        self.run_testname("place")


    def test_remove(self):
        self.run_testname("remove")
        

    def tearDown(self):
        self.process.terminate()

if __name__ == '__main__':
    unittest.main()
