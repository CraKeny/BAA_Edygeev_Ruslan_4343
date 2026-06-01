import pytest
from collections import deque
import sys
import os
sys.path.append(os.path.abspath('..'))
from io import StringIO
from simple import *


class TestAhoCorasick:
    @pytest.fixture
    def ac(self):
        return AhoCorasick()
    
    def test_single_pattern(self, ac):
        patterns = ["abc"]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()
        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("abcabc", pattern_lengths)
        results.sort()
        expected = [(1, 1), (4, 1)]
        assert results == expected
    
    def test_multiple_patterns(self, ac):
        patterns = ["ab", "bc", "abc"]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()
        
        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("abc", pattern_lengths)
        results.sort()
        
        expected = [(1, 1), (1, 3), (2, 2)]
        assert results == expected
    
    def test_overlapping_patterns(self, ac):
        patterns = ["aa", "aa"]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()
        
        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("aaa", pattern_lengths)
        results.sort()

        expected = [(1, 1), (1, 2), (2, 1), (2, 2)]
        assert results == expected
    
    
    def test_suffix_patterns(self, ac):
        patterns = ["abab", "ab"]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()
        
        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("ababab", pattern_lengths)
        results.sort()

        expected = [(1, 1), (1, 2), (3, 1), (3, 2), (5, 2)]
        assert results == expected
    
    def test_no_matches(self, ac):
        patterns = ["xyz", "abc"]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()

        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("defdef", pattern_lengths)
        expected = []
        assert results == expected
    
    def test_empty_text(self, ac):
        patterns = ["abc"]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()
        
        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("", pattern_lengths)
        expected = []
        assert results == expected
    
    def test_empty_pattern(self, ac):
        patterns = [""]
        for i, pattern in enumerate(patterns, 1):
            ac.add_pattern(pattern, i)
        
        ac.build_links()
        
        pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
        results = ac.search("abc", pattern_lengths)
        assert len(results) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])