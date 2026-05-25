import sys
import heapq
import random

file = "out.txt"


def show(matrix, n, f):
    f.write("\n")
    f.write("\t")
    f.writelines([f"{x}\t\t" for x in range(n)])
    f.write("\n")
    for i in range(n):
        f.write(f"{i}\t")
        f.writelines([f"{x}\t\t" for x in matrix[i]])
        f.write("\n")
    f.write("\n")

def show_lb(lower_bound, f):
    f.write(f"\t\tLOWER_BOUND = {lower_bound}\n\n")

def reduce_matrix_fast(matrix, n):
    lower_bound = 0
    for i in range(n):
        min_val = float('inf')
        row = matrix[i]
        for j in range(n):
            if row[j] < min_val:
                min_val = row[j]
        if min_val > 0 and min_val != float('inf'):
            lower_bound += min_val
            for j in range(n):
                if row[j] != float('inf'):
                    row[j] -= min_val
    for j in range(n):
        min_val = float('inf')
        for i in range(n):
            if matrix[i][j] < min_val:
                min_val = matrix[i][j]
        if min_val > 0 and min_val != float('inf'):
            lower_bound += min_val
            for i in range(n):
                if matrix[i][j] != float('inf'):
                    matrix[i][j] -= min_val
    return lower_bound

def find_best_arc(matrix, n):
    max_penalty = -1
    best_arc = None
    for i in range(n):
        row = matrix[i]
        for j in range(n):
            if row[j] == 0:
                min_row = float('inf')
                for k in range(n):
                    if k != j:
                        val = row[k]
                        if val < min_row:
                            min_row = val
                min_col = float('inf')
                for k in range(n):
                    if k != i:
                        val = matrix[k][j]
                        if val < min_col:
                            min_col = val
                penalty = min_row + min_col
                if penalty > max_penalty:
                    max_penalty = penalty
                    best_arc = (i, j, max_penalty)
    return best_arc

def get_forbidden_arc(path, new_arc, n):
    i, j, _ = new_arc
    incoming = [-1] * n
    outgoing = [-1] * n
    for u, v in path:
        outgoing[u] = v
        incoming[v] = u
    outgoing[i] = j
    incoming[j] = i
    curr = j
    start = i
    visited = set()
    while curr != -1 and curr not in visited:
        visited.add(curr)
        curr = outgoing[curr]
    if curr == -1:
        return (j, i)
    cycle_end = curr
    curr = start
    while curr != cycle_end and curr != -1:
        curr = incoming[curr]
    if curr == -1:
        return (j, cycle_end)
    return (j, i)

def solve_tsp(n, matrix_orig):
    ids = [x for x in range(2, 100000)]

    n = len(matrix_orig)
    matrix = [row[:] for row in matrix_orig]

    lower_bound = reduce_matrix_fast(matrix, n)

    pq = []
    ident = 1
    pid = 0
    heapq.heappush(pq, (ident, pid, lower_bound, 0, matrix, []))
    best_cost = float('inf')
    best_path = None
    while pq:
        ident, pid, lb, _, mat, path = heapq.heappop(pq)

        if lb >= best_cost:
            f = open(file, "a")
            f.write("\n\n==============================================================================\n")
            f.write(f"\t\tNODE (ident={ident}, PID={pid}) CUTTED: LB={lb} >= best_cost={best_cost}\n")
            f.write("\n==============================================================================\n\n")
            f.close()
            continue
        if len(path) == n - 1:
            remaining_i = -1
            remaining_j = -1
            for i in range(n):
                for j in range(n):
                    if mat[i][j] != float('inf'):
                        remaining_i = i
                        remaining_j = j
                        break
                if remaining_i != -1:
                    break
            if remaining_i != -1:
                full_path = path + [(remaining_i, remaining_j)]
                incoming = [-1] * n
                outgoing = [-1] * n
                for u, v in full_path:
                    outgoing[u] = v
                    incoming[v] = u
                tour = []
                start = 0
                curr = start
                for _ in range(n):
                    tour.append(curr)
                    curr = outgoing[curr]
                if len(set(tour)) == n:
                    cost = 0
                    for u, v in full_path:
                        cost += matrix_orig[u][v]
                    if cost < best_cost:
                        best_cost = cost
                        best_path = full_path
            continue
        arc = find_best_arc(mat, n)
        if arc is None:
            continue
        i, j, max_pen = arc
        mat_right = [row[:] for row in mat]
        mat_right[i][j] = float('inf')

        lb_right = lb + reduce_matrix_fast(mat_right, n)

        if lb_right < best_cost:
            pid = ident
            ident = random.choice(ids)
            ids.pop(ident - 2)
            heapq.heappush(pq, (ident, pid, lb_right, len(path), mat_right, path))
        mat_left = [row[:] for row in mat]
        for k in range(n):
            mat_left[i][k] = float('inf')
            mat_left[k][j] = float('inf')

        f = open(file, "a")
        f.write("\n--------------------------------------------------------------\n")
        f.write(f"(ident={ident} | PID={pid}) RIGHT BRANCH ---- excluded edge - {i} - {j}, penalty = {max_pen}")
        show(mat_right, len(mat_right), f)
        show_lb(lb_right, f)
        f.write("\n--------------------------------------------------------------\n")

        forbid_arc = (j, i)
        if len(path) >= 1:
            forbid_arc = get_forbidden_arc(path, arc, n)
        mat_left[forbid_arc[0]][forbid_arc[1]] = float('inf')
        lb_left = lb + reduce_matrix_fast(mat_left, n)
        new_path = path + [(i, j)]

        if lb_left < best_cost:
            ident = random.choice(ids)
            ids.pop(ident - 2)
            heapq.heappush(pq, (ident, pid, lb_left, len(path) + 1, mat_left, path + [(i, j)]))

        f.write("\n--------------------------------------------------------------\n")
        f.write(f"(ident={ident} | PID={pid}) LEFT BRANCH ---- forbidden row - {i}, col - {j}\n")
        f.write(f"\t\tFORBIDDEN ROW {i} and col {j}\n")
        f.write(f"\t\tFORBIDDEN EDGE: {forbid_arc}\n")
        f.write(f"\t\tCURRENT PATH = {new_path}\n")
        show(mat_left, len(mat_left), f)
        show_lb(lb_left, f)
        f.write("\n--------------------------------------------------------------\n")
        f.close()

    incoming = [-1] * n
    outgoing = [-1] * n
    if best_path:
        for u, v in best_path:
            outgoing[u] = v
            incoming[v] = u
    else:
        return "no path"
    tour = []
    curr = 0
    for _ in range(n):
        tour.append(curr)
        curr = outgoing[curr]
    return best_cost, tour

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    n = int(data[0])

    f = open(file, "w")
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
                row.append(float('inf'))
            else:
                row.append(val)
            idx += 1
        matrix.append(row)
        f.write(f"{i}\t")
        f.writelines([f"{x}\t\t" for x in row])
        f.write("\n")
    f.write("\n")
    f.close()

    result = solve_tsp(n, matrix)
    if result == "no path":
        print("no path")
        return
    cost, tour = result
    res = ' '.join(map(str, tour))
    print(res)
    print(f"{cost:.1f}")

    f = open(file, "a")
    f.write("\n\n============ ANSWER ============\n")
    f.writelines([f"{x} - " for x in tour])
    f.write(f" {tour[0]}")
    f.write(f"\n{cost:.1f}")
    f.close()

if __name__ == "__main__":
    main()