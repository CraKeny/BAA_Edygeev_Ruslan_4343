import pytest
from KMP import *

class TestPrefixFunction:
    def test_empty_string(self):
        assert kmp_prefix_function("") == []

    def test_single_char(self):
        assert kmp_prefix_function("a") == [0]
    
    def test_all_same_chars(self):
        assert kmp_prefix_function("aaaa") == [0, 1, 2, 3]
        
    def test_no_repeats(self):
        assert kmp_prefix_function("abcde") == [0, 0, 0, 0, 0]
    
    def test_complex_pattern(self):
        assert kmp_prefix_function("abacab") == [0, 0, 1, 0, 1, 2]
    
    def test_prefix_suffix_overlap(self):
        assert kmp_prefix_function("abcabc") == [0, 0, 0, 1, 2, 3]


class TestKMPSearch:
    def test_basic_search(self):
        result = kmp_search("ab", "abab")
        assert result == [0, 2], f"Ожидалось [0, 2], получено {result}"
    
    def test_no_match(self):
        result = kmp_search("xyz", "abcdef")
        assert result == [], f"Ожидался пустой список, получено {result}"
    
    def test_pattern_at_end(self):
        result = kmp_search("cd", "abcd")
        assert result == [2], f"Ожидалось [2], получено {result}"
    
    def test_multiple_matches(self):
        result = kmp_search("aa", "aaaa")
        assert result == [0, 1, 2], f"Ожидалось [0, 1, 2], получено {result}"
    
    def test_single_char_pattern(self):
        result = kmp_search("a", "banana")
        assert result == [1, 3, 5], f"Ожидалось [1, 3, 5], получено {result}"
    
    def test_pattern_longer_than_text(self):
        result = kmp_search("abcd", "abc")
        assert result == [], f"Ожидался пустой список, получено {result}"
    
    def test_empty_text(self):
        result = kmp_search("abc", "")
        assert result == [], f"Ожидался пустой список, получено {result}"


class TestCyclicShift:
    def test_basic_cyclic_shift(self):
        result = cyclic_shift_search("defabc", "abcdef")
        assert result == 3, f"Ожидалось 3, получено {result}"
    
    def test_no_shift(self):
        result = cyclic_shift_search("abc", "abc")
        assert result == 0, f"Ожидалось 0, получено {result}"
    
    def test_full_rotation(self):
        result = cyclic_shift_search("eabcd", "abcde")
        assert result == 1, f"Ожидалось 1, получено {result}"
    
    def test_not_cyclic_shift(self):
        result = cyclic_shift_search("abc", "xyz")
        assert result == -1, f"Ожидалось -1, получено {result}"
    
    def test_different_lengths(self):
        result = cyclic_shift_search("abc", "abcd")
        assert result == -1, f"Ожидалось -1, получено {result}"
    
    def test_empty_strings(self):
        result = cyclic_shift_search("", "")
        assert result == 0, f"Ожидалось 0, получено {result}"
    
    def test_single_char(self):
        result = cyclic_shift_search("a", "a")
        assert result == 0, f"Ожидалось 0, получено {result}"
    
    def test_performance_array(self):
        base = "abcdefghij"
        for shift in range(len(base)):
            shifted = base[shift:] + base[:shift]
            result = cyclic_shift_search(shifted, base)
            assert result == (len(base) - shift) % len(base), \
                f"Сдвиг {shift}: ожидалось {(len(base)-shift) % len(base)}, получено {result}"
            
if __name__ == "__main__":
    pytest.main([__file__, "-v"])