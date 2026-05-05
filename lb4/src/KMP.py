import sys


file = "out.txt"

def kmp_prefix_function(s: str):
    n = len(s)
    pi = [0] * n

    f = open(file, "w")
    f.writelines(f'{i} ' for i in range(n))
    f.write('\n')
    f.writelines(f'{i} ' for i in s)
    f.write("\n\n\n")

    for i in range(1, n):
        f.writelines(f'{i} ' for i in pi)
        f.write(" ------------------ prefix-function, \t" + f"i = {i if n > 1 else '-'}" + "\n")

        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            f.write(f"\t\tj = {j}, \t{s[i]} = {s[j]}\tsearching...\n")
            j += 1
        else:
            f.write(f"\t\t{s[i]} != {s[j]}\tEnd of search, length = {j}\n")
        pi[i] = j

    f.writelines(f'{i} ' for i in pi)
    f.write(" ------------------ prefix-function, \t" + f"i = {i if n > 1 else '-'}" + "\n")
    f.close()
    return pi

def cyclic_shift_search(A: str, B: str):
    f = open(file, "a")
    f.write("\n\n\t\tАЛГОРИТМ КМП / ПОИСК ЦИКЛИЧЕСКОГО СДВИГА\n\n")

    n = len(A)
    if n != len(B):
        f.write(f"ERROR: len(A) != len(B) ---> {len(A)} != {len(B)}")
        return -1
    
    if n == 0:
        f.write("Длина строки 0, ответ - 0")
        return 0
    
    pi = kmp_prefix_function(B)
    
    f.write("\t\t\t")
    f.writelines(f'{i} ' for i in range(len(A)))
    f.write('\n')
    f.write("STR A:\t\t")
    f.writelines(f'{i} ' for i in A)
    f.write('\n')
    f.write("STR B:\t\t")
    f.writelines(f'{i} ' for i in B)
    f.write("\n\n\n")

    j = 0
    for i in range(2 * n - 1):
        f.write(f"i = {i})")
        char = A[i % n]
        while j > 0 and char != B[j]:
            f.write(f"\t\t{char} != {B[j]}, j->({j}) = pi[j - 1]->({pi[j - 1]})\n")
            j = pi[j - 1]
        if char == B[j]:
            f.write(f"\t\t{char} = {B[j]}, j->({j}) = (j + 1)->({j + 1})\n")
            j += 1
        if j == n:
            f.write("j = n, завершение работы")
            f.write(f"\n\nANSWER: {i - n + 1}")
            f.close()
            return i - n + 1
        f.write('\n')
        
    f.close()
    return -1

def kmp_search(pattern: str, text: str):
    n = len(pattern)
    pi = kmp_prefix_function(pattern)

    result = []
    j = 0

    f = open(file, "a")
    f.write("\n\n\t\tАЛГОРИТМ КМП / ПОИСК ПОДСТРОКИ В СТРОКЕ\n\n")
    f.write("\t\t\t")
    f.writelines(f'{i} ' for i in range(len(text)))
    f.write('\n')
    f.write("PATTERN:\t")
    f.writelines(f'{i} ' for i in pattern)
    f.write('\n')
    f.write("TEXT:\t\t")
    f.writelines(f'{i} ' for i in text)
    f.write("\n\n\n")

    for i in range(len(text)):
        f.write(f"i = {i})")
        while j > 0 and text[i] != pattern[j]:
            f.write(f"\t\t{text[i]} != {pattern[j]}, j->({j}) = pi[j - 1]->({pi[j - 1]})\n")
            j = pi[j - 1]
        if text[i] == pattern[j]:
            f.write(f"\t\t{text[i]} = {pattern[j]}, j->({j}) = (j + 1)->({j + 1})\n")
            j += 1
        if j == n:
            f.write(f"\t\t\tRESULT += (i - n + 1)->({i - n + 1}), j->({j}) = pi[j - 1]->({pi[j - 1]})\n")
            result.append(i - n + 1)
            j = pi[j - 1]
        f.write('\n')

    f.write("\n\nANSWER = ")
    f.writelines(f'{i} ' for i in result)
    f.close()

    return result

def ref():
    print("Usage:")
    print("  python program.py                    - обычный поиск подстроки")
    print("  python program.py -c                 - поиск циклического сдвига")
    print("  python program.py -h                 - показать эту справку")
    print()

if __name__ == "__main__":
    args = sys.argv[1:]
    if "-h" in args:
        ref()
        exit(0)

    P = input().strip()
    T = input().strip()
    if(not P or not T):
        print("EMPTY STRINGS")
        exit(0)

    if not "-c" in args:
        positions = kmp_search(P, T)
        if not positions:
            print(-1)
        else:
            print(",".join(map(str, positions)))
    else:
        positions = cyclic_shift_search(P, T)
        print(positions)