import pytest
import sys
from io import StringIO
import os
sys.path.append(os.path.abspath('..'))
from mod import *

class TestWildcardExcluding:
    def test_no_wildcards(self):
        text = "abcdefabc"
        pattern = "abc"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = [1, 7]
        assert result == expected
    
    def test_forbidden_blocks_match(self):
        text = "abcxabc"
        pattern = "ab?c"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []  
        assert result == expected
    
    def test_multiple_wildcards_with_forbidden(self):
        text = "a1b2c3d4e"
        pattern = "a?b?c"
        wildcard_char = "?"
        forbidden_char = "2"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected
    
    def test_wildcard_at_start_with_forbidden(self):
        text = " xabc xabc"
        pattern = "?abc"
        wildcard_char = "?"
        forbidden_char = " "
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = [2, 7]
        assert result == expected
    
    def test_wildcard_at_end_with_forbidden(self):
        text = "abc abc abc"
        pattern = "abc?"
        wildcard_char = "?"
        forbidden_char = " "
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected
    
    def test_multiple_subpatterns_with_forbidden(self):
        text = "AB1CD AB2CD AB3CD"
        pattern = "AB?CD"
        wildcard_char = "?"
        forbidden_char = "2"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = [1, 13]
        assert result == expected
    
    def test_pattern_longer_than_text(self):
        text = "abc"
        pattern = "abcdef"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected
    
    def test_empty_pattern(self):
        text = "abc"
        pattern = "???"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected
    
    def test_overlapping_matches_with_forbidden(self):
        text = "aaaaa"
        pattern = "a?a"
        wildcard_char = "?"
        forbidden_char = "b"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = [1, 2, 3]
        assert result == expected
    
    def test_complex_forbidden_scenario(self):
        text = "a1b2c3d4e5f"
        pattern = "a?b?c?d"
        wildcard_char = "?"
        forbidden_char = "2"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected
    
    def test_forbidden_equals_normal_char(self):
        text = "abxcd abxcd"
        pattern = "abxcd"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = [1, 7]
        assert result == expected
    
    def test_empty_text(self):
        text = ""
        pattern = "abc"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected
    
    def test_no_matches(self):
        text = "abcdef"
        pattern = "xyz"
        wildcard_char = "?"
        forbidden_char = "x"
        
        result = find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char)
        expected = []
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])