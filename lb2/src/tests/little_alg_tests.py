import pytest
import sys
import os
sys.path.append(os.path.abspath('..'))
from io import StringIO
from little_alg import *


def parse_input(input_str):
    lines = input_str.strip().split('\n')
    n = int(lines[0].strip())
    graph = []
    for i in range(1, n + 1):
        row = list(map(float, lines[i].strip().split()))
        graph.append([float(x) for x in row])
    
    for i in range(n):
        for j in range(n):
            if i == j:
                graph[i][j] = float('inf')
            elif graph[i][j] == -1:
                graph[i][j] = float('inf')
            elif graph[i][j] == 0:
                graph[i][j] = float('inf')
    
    return n, graph


class TestTSP:
    
    def test_simple_4_vertices(self):
        input_data = """
4
-1 10 15 20
10 -1 35 25
15 35 -1 30
20 25 30 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 80
        else:
            assert False
    
    def test_missing_edges(self):
        input_data = """
4
-1 10 -1 20
10 -1 35 -1
-1 35 -1 30
20 -1 30 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        assert result[0] == 95.0
    
    def test_complete_5_vertices(self):
        input_data = """
5
-1 10 8 9 7
10 -1 10 5 6
8 10 -1 8 9
9 5 8 -1 6
7 6 9 6 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 34
        else:
            assert False
    
    def test_float_weights(self):
        input_data = """
4
-1 2.5 3.0 4.0
2.5 -1 5.5 3.5
3.0 5.5 -1 2.0
4.0 3.5 2.0 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert abs(cost - 11.0) < 1e-9
        else:
            assert False
    
    def test_large_graph_with_minus_one(self):
        input_data = """
6
-1 20 30 10 11 15
20 -1 16 21 14 9
30 16 -1 25 18 19
10 21 25 -1 12 17
11 14 18 12 -1 13
15 9 19 17 13 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 80.0
        else:
            assert False
    
    def test_zero_edges(self):
        input_data = """
4
-1 -1 -1 -1
-1 -1 35 25
15 35 -1 -1
20 25 30 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        assert result == "no path"
    
    def test_triangle(self):
        input_data = """
3
-1 10 15
10 -1 20
15 20 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 45
        else:
            assert False
    
    def test_5_vertices_some_minus_one(self):
        input_data = """
5
-1 12 10 -1 15
12 -1 8 14 -1
10 8 -1 11 5
-1 14 11 -1 6
15 -1 5 6 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 47.0
        else:
            assert False
    
    def test_symmetric_large_values(self):
        input_data = """
4
-1 100 200 300
100 -1 400 500
200 400 -1 600
300 500 600 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 1400.0
        else:
            assert False
    
    def test_disconnected_graph(self):
        input_data = """
5
-1 10 -1 -1 -1
10 -1 -1 -1 -1
-1 -1 -1 20 30
-1 -1 20 -1 40
-1 -1 30 40 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        assert result == "no path"
    
    def test_alternative_optimal_path(self):
        input_data = """
4
-1 10 20 10
10 -1 10 20
20 10 -1 10
10 20 10 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost == 40
            assert path[0] == 0 and len(path) == 4
        else:
            assert False
    
    def test_asymmetric_graph(self):
        input_data = """
4
-1 10 15 20
20 -1 35 25
15 30 -1 30
25 25 35 -1
"""
        n, graph = parse_input(input_data)
        result = solve_tsp(n, graph)
        if isinstance(result, tuple):
            cost, path = result
            assert cost != float('inf')
            assert path[0] == 0 and len(path) == 4
        else:
            assert False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])