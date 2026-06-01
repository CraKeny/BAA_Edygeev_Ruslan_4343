import pytest
import sys
from io import StringIO
import os
sys.path.append(os.path.abspath('..'))
from joker import *


class TestWildcardSearch:
    def test_no_wildcards(self):
        text = "abcdefabc"
        pattern = "abc"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [1, 7]  
        assert result == expected
    
    def test_single_wildcard(self):
        text = "abcxabcyabcz"
        pattern = "ab?"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [1, 5, 9]
        assert result == expected
    
    def test_multiple_wildcards(self):
        text = "a1b2c3d4e"
        pattern = "a?b?c"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [1]
        assert result == expected
    
    def test_wildcards_at_ends(self):
        text = "xyzabcxyz"
        pattern = "?abc?"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [3]
        assert result == expected
    
    def test_pattern_longer_than_text(self):
        text = "abc"
        pattern = "abcdef"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = []
        assert result == expected
    
    def test_empty_pattern(self):
        text = "abc"
        pattern = "???"
        wildcard_char = "?"

        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = []
        assert result == expected
    
    def test_all_wildcards(self):
        text = "abcde"
        pattern = "????"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = []  
        assert result == expected
    
    def test_overlapping_matches(self):
        text = "aaaaa"
        pattern = "a?a"
        wildcard_char = "?"
    
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [1, 2, 3]
        assert result == expected
    
    def test_wildcard_between_same_chars(self):
        text = "a1a a2a a3a"
        pattern = "a?a"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [1, 3, 5, 7, 9]  
        assert result == expected
    
    def test_boundary_matches(self):
        text = "abcabc"
        pattern = "ab?"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = [1, 4]
        assert result == expected
    
    def test_no_matches_with_wildcards(self):
        text = "abcdef"
        pattern = "xyz"
        wildcard_char = "?"
        
        result = find_pattern_with_wildcards(text, pattern, wildcard_char)
        expected = []
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])