import pytest
import sys
import os
sys.path.append(os.path.abspath('..'))
from io import StringIO
from mot_alg import *


def parse_input(input_str):
    """Преобразует строку ввода в матрицу."""
    lines = input_str.strip().split('\n')
    start_vertex = int(lines[0].strip())
    n = int(lines[1].strip())
    graph = []
    for i in range(2, 2 + n):
        row = list(map(float, lines[i].strip().split()))
        graph.append(row)
    
    # Заменяем диагональ, 0 и отрицательные на -1
    for i in range(n):
        for j in range(n):
            if i == j or graph[i][j] <= 0:
                graph[i][j] = -1
    
    return n, graph, start_vertex


class TestDoubleTree:
    
    def test_triangle(self):
        input_data = """0
3
-1 10 15
10 -1 20
15 20 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        if result is not None:
            cost, path = result
            assert len(path) == n + 1
            assert path[0] == path[-1] == start
            assert cost <= 50.0
        else:
            assert False, "Ожидался тур, получен no path"
    
    def test_square(self):
        input_data = """0
4
-1 20 30 40
20 -1 50 60
30 50 -1 70
40 60 70 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        if result is not None:
            cost, path = result
            assert len(path) == n + 1
            assert path[0] == path[-1] == start
            assert cost <= 180.0
        else:
            assert False
    
    def test_disconnected(self):
        input_data = """0
4
-1 10 -1 -1
10 -1 -1 -1
-1 -1 -1 20
-1 -1 20 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        assert result is None
    
    def test_isolated_vertex(self):
        input_data = """0
4
-1 10 15 -1
10 -1 20 -1
15 20 -1 -1
-1 -1 -1 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        assert result is None
    
    def test_line_with_closing(self):
        input_data = """0
4
-1 10 -1 30
10 -1 10 -1
-1 10 -1 10
30 -1 10 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        if result is not None:
            cost, path = result
            assert len(path) == n + 1
            assert path[0] == path[-1] == start
        else:
            assert False
    
    def test_zero_edges_become_missing(self):
        input_data = """0
3
-1 0 10
0 -1 0
10 0 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        assert result is None
    
    def test_float_weights(self):
        input_data = """0
4
-1 2.5 3.0 4.0
2.5 -1 5.5 3.5
3.0 5.5 -1 2.0
4.0 3.5 2.0 -1"""
        n, graph, start = parse_input(input_data)
        result = solve_tsp(graph, n, start)
        if result is not None:
            cost, path = result
            assert len(path) == n + 1
            assert path[0] == path[-1] == start
        else:
            assert False
    
    def test_large_complete(self):
        import random
        random.seed(123)
        n = 10
        matrix = [[-1] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                w = random.randint(10, 100)
                matrix[i][j] = w
                matrix[j][i] = w
        
        result = solve_tsp(matrix, n, 0)
        if result is not None:
            cost, path = result
            assert len(path) == n + 1
            assert path[0] == path[-1] == 0
        else:
            assert False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])