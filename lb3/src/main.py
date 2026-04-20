import os


def show(str1, str2, last, new, i, choise):
    with open("log.txt", "a") as f:
        f.writelines("  #\t")
        f.writelines(f'{i}\t' for i in str1)
        f.writelines('-----------' + f"Chosen operation: {choise}" + '\n')

        f.writelines("# ")
        f.writelines(f'{i}\t' for i in last)
        f.write('\n')

        f.writelines(str2[i - 1] + ' ')
        f.writelines(f'{i}\t' for i in new)
        f.write('\n')
        f.write('\n')

ops = {
    "del" : 1,
    "ins" : 1,
    "rep" : 1,
    "dins" : 2
}

def reconstruction(size, str1, str2):
    arr = []
    with open("out.txt", "r") as f:
        for _ in range(size):
            row = list(map(float, f.readline().split()))
            arr.append(row)
    
    j = len(arr) - 1
    i = len(arr[0]) - 1
    stack = []

    while j > 0 or i > 0:
        current = arr[j][i]
        
        if j >= 2 and str2[j-1] == str2[j-2]:
            if abs(current - (arr[j-2][i] + ops["dins"])) < 1e-9:
                stack.append(('(', 'DI', ' - ', str2[j - 2], ')'))
                j -= 2
                continue

        if j > 0 and abs(current - (arr[j-1][i] + ops["del"])) < 1e-9:
            stack.append(('(', 'I', ' - ', str2[j - 1], ')'))
            j -= 1
            continue

        if i > 0 and abs(current - (arr[j][i-1] + ops["ins"])) < 1e-9:
            stack.append(('(', 'D', ' - ', str1[i - 1], ')'))
            i -= 1
            continue
        
        if j > 0 and i > 0:
            if str1[i-1] == str2[j-1]:
                if abs(current - arr[j-1][i-1]) < 1e-9:
                    stack.append(('(', 'M', ' - ', str1[i - 1], ' = ', str2[j - 1], ')'))
                    j -= 1
                    i -= 1
                    continue
            else:
                if abs(current - (arr[j-1][i-1] + ops["rep"])) < 1e-9:
                    stack.append(('(', 'R', ' - ', str1[i - 1], ' -> ', str2[j - 1], ')'))
                    j -= 1
                    i -= 1
                    continue
        print(f"Error at ({j},{i}), current={current}")
        break
    stack.reverse()
    return stack

def main():
    if os.path.exists("log.txt"):
        os.remove("log.txt")

    if os.path.exists("out.txt"):
        os.remove("out.txt")

    str1 = list(input())
    str2 = list(input())

    if not str1:
        str1 = ""

    if not str2:
        print(len(str1))
        return

    n = len(str1) + 1
    m = len(str2) + 1

    row = [x for x in range(0, n)]
    col = [x for x in range(0, m)]

    last_last_row = row
    last_row = [0] * (n - 1)
    last_row.insert(0, col[1])
    for j in range(1, n):
        choise = None
        if str1[j - 1] == str2[0]:
            last_row[j] = min(last_last_row[j] + ops["del"], last_row[j - 1] + ops["ins"], last_last_row[j - 1])
        elif str1[j - 1] != str2[0]:
            last_row[j] = min(last_last_row[j] + ops["del"], last_row[j - 1] + ops["ins"], last_last_row[j - 1] + ops["rep"])
        
        if last_row[j] == last_last_row[j] + ops["del"]: choise = "delete"
        elif last_row[j] == last_row[j - 1] + ops["ins"]: choise = "insert"
        elif last_row[j] == last_row[j] == last_last_row[j - 1] + ops["rep"]: choise = "replace"
        elif last_row[j] == 0: choise = "None"
        show(str1, str2, last_last_row, last_row, 1, choise)

    with open("out.txt", "w") as out:
        out.writelines(f'{i}\t' for i in last_last_row)
        out.write('\n')
        out.writelines(f'{i}\t' for i in last_row)
        out.write('\n')

    for i in range(2, m):
        new = [0]*(n - 1)
        new.insert(0, col[i])
        for j in range(1, n):
            choise = None
            cost = 0
            if str1[j - 1] == str2[i - 1]:
                cost = min(last_row[j] + ops["del"], new[j - 1] + ops["ins"], last_row[j - 1])
            elif str1[j - 1] != str2[i - 1]:
                cost = min(last_row[j] + ops["del"], new[j - 1] + ops["ins"], last_row[j - 1] + ops["rep"])
            
            if str2[i - 1] == str2[i - 2]:
                cost = min(cost, last_last_row[j] + ops["dins"])
            
            new[j] = cost
            if new[j] == last_row[j] + ops["del"]: choise = "delete"
            elif new[j] == new[j - 1] + ops["ins"]: choise = "insert"
            elif new[j] == last_row[j - 1] or new[j] == last_row[j - 1] + ops["rep"]: choise = "replace"
            elif new[j] == last_last_row[j] + ops["dins"]: choise = "double insertion"
            elif last_row[j] == 0: choise = "None"
            show(str1, str2, last_row, new, i, choise)

        last_last_row = last_row
        last_row = new
        with open("out.txt", "a") as out:
            out.writelines(f'{i}\t' for i in last_row)
            out.write('\n')

    print(last_row[-1])
    reverse = reconstruction(m, str1, str2)
    with open("out.txt", "a") as f:
        for line in reverse:
            f.writelines(f'{i}' for i in line)
            f.write('\n')
        f.write(f"Answer: {str(last_row[-1])}")

if __name__ == "__main__":
    main()