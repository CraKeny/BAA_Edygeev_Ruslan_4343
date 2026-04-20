import pytest
import subprocess
from main import *

def run_program(input_data):
    result = subprocess.run(
        ["python3", str("main.py")],
        input=input_data,
        capture_output=True,
        text=True
    )
    return result.stdout.strip().split('\n')[0]

class TestLevenshtein:
    
    def test_identical_strings(self):
        result = run_program("hello\nhello\n")
        assert result == "0"
    
    def test_single_delete(self):
        result = run_program("cat\nca\n")
        assert result == "1"
    
    def test_single_insert(self):
        result = run_program("ca\ncat\n")
        assert result == "1"
    
    def test_single_replace(self):
        result = run_program("cat\ncut\n")
        assert result == "1"
    
    def test_empty_string(self):
        result = run_program("\nhello\n")
        assert result == "5"
    
    def test_kitten_sitting(self):
        result = run_program("kitten\nsitting\n")
        assert result == "3"
    
    def test_double_insertion(self):
        result = run_program("cat\ncaat\n")
        assert result == "1"
    
    def test_entrance_example(self):
        result = run_program("entrance\nreenterable\n")
        assert result == "5"
    
    def test_completely_different(self):
        result = run_program("abc\nxyz\n")
        assert result == "3"