import sys
import heapq

file = "out.txt"

def prims(graph, n, start):
    mst = [[] for _ in range(n)]
    visited = [False] * n
    min_edge = [float('inf')] * n
    min_edge[start] = 0
    parent = [-1] * n
    
    pq = [(0, start)]
    
    while pq:
        weight, u = heapq.heappop(pq)
        
        if visited[u]:
            continue
        
        visited[u] = True
        
        if parent[u] != -1:
            v = parent[u]
            mst[u].append((v, weight))
            mst[v].append((u, weight))
        
        for v in range(n):
            if graph[u][v] != -1 and not visited[v] and graph[u][v] < min_edge[v]:
                min_edge[v] = graph[u][v]
                parent[v] = u
                heapq.heappush(pq, (graph[u][v], v))
    
    if not all(visited):
        return None
    
    for i in range(n):
        mst[i].sort(key=lambda x: (x[1], x[0]))
    return mst

def dfs(mst, n, u):
    visited = [False] * n
    euler_path = []
    
    def dfs_recursive(v):
        visited[v] = True
        euler_path.append(v)
        for next_v, w in mst[v]:
            if not visited[next_v]:
                dfs_recursive(next_v)
                euler_path.append(v)
    
    dfs_recursive(u)
    return euler_path

def solve_tsp(graph, n, start):
    mst = prims(graph, n, start)
    
    if mst is None:
        f = open(file, "a")
        f.write("\nМОД не построен - граф несвязный\n")
        f.close()
        return None
    
    
    f = open(file, "a")
    f.write("\n--- Построение МОД (алгоритм Прима) ---\n")
    mst_weight = 0
    for u in range(n):
        for v, w in mst[u]:
            if u < v:  
                f.write(f"  Ребро ({u}, {v}) вес: {w:.2f}\n")
                mst_weight += w
    f.write(f"  Вес МОД: {mst_weight:.2f}\n")
    f.close()
    
    
    euler_path = dfs(mst, n, start)
    
    f = open(file, "a")
    f.write(f"\n--- Эйлеров обход ---\n")
    f.write(f"  {' -> '.join(map(str, euler_path))}\n")
    f.close()
    
    
    path = []
    seen = set()
    for v in euler_path:
        if v not in seen:
            path.append(v)
            seen.add(v)
    
    f = open(file, "a")
    f.write(f"\n--- Shortcutting (удаление повторов) ---\n")
    f.write(f"  {' -> '.join(map(str, path))}\n")
    f.close()
    
    
    path.append(start)
    
    f = open(file, "a")
    f.write(f"\n--- Замыкание цикла ---\n")
    f.write(f"  {' -> '.join(map(str, path))}\n")
    f.close()
    
    
    total_length = 0.0
    f = open(file, "a")
    f.write(f"\n--- Расчёт стоимости ---\n")
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if graph[u][v] == -1 or graph[u][v] == float('inf'):
            f.write(f"  ОШИБКА: нет прямого ребра ({u}, {v})\n")
            f.close()
            return None
        edge_weight = graph[u][v]
        total_length += edge_weight
        f.write(f"  ({u}, {v}) = {edge_weight:.2f}\n")
    
    f.write(f"  Общая стоимость: {total_length:.2f}\n")
    f.close()
    
    print(f"{total_length:.2f}")
    print(' '.join(map(str, path)))
    
    return total_length, path


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    start_vertex = int(data[0])
    
    n = int((len(data) - 1) ** 0.5)
    if start_vertex >= n:
        print("no path, vertex out of range")
        return
    
    f = open(file, "w")
    f.write(f"START: {start_vertex}\n")
    f.write("\t")
    f.writelines([f"{x}\t\t" for x in range(n)])
    f.write("\n")

    matrix = []
    idx = 1  
    for i in range(n):
        row = []
        for j in range(n):
            val = float(data[idx])
            if val <= 0:
                row.append(-1)
            else:
                row.append(val)
            idx += 1
        matrix.append(row)
        f.write(f"{i}\t")
        f.writelines([f"{x:.2f}\t\t" if x != -1 else "-\t\t" for x in row])
        f.write("\n")
    f.write("\n")
    f.close()

    result = solve_tsp(matrix, n, start_vertex)
    if result is None:
        f = open(file, "a")
        f.write("\nno path\n")
        f.close()
        print("no path")
        return
    
    cost, tour = result
    
    f = open(file, "a")
    f.write("\n\n============ ANSWER ============\n")
    f.write(" -> ".join(map(str, tour)))
    f.write(f"\nОбщая стоимость: {cost:.2f}\n")
    f.close()

if __name__ == "__main__":
    main()