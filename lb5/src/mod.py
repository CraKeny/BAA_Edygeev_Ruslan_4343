from collections import deque

log_file = "log_3.txt"


class AhoCorasick:
    def __init__(self):
        self.trie = [{}]
        self.fail = [0]
        self.output_link = [0]
        self.terminal = [False]
        self.pattern_info = [[]]
    
    def add_pattern(self, pattern, pattern_index, start_pos_in_pattern, length):
        node = 0
        for char in pattern:
            if char not in self.trie[node]:
                self.trie[node][char] = len(self.trie)
                self.trie.append({})
                self.fail.append(0)
                self.output_link.append(0)
                self.terminal.append(False)
                self.pattern_info.append([])
            node = self.trie[node][char]
        
        self.terminal[node] = True
        self.pattern_info[node].append((pattern_index, start_pos_in_pattern, length))
    
    def build_automaton(self):
        q = deque()
        
        for char, next_node in self.trie[0].items():
            self.fail[next_node] = 0
            q.append(next_node)
        
        while q:
            current = q.popleft()
            
            if self.terminal[self.fail[current]]:
                self.output_link[current] = self.fail[current]
            else:
                self.output_link[current] = self.output_link[self.fail[current]]
            
            for char, next_node in self.trie[current].items():
                q.append(next_node)
                
                f = self.fail[current]
                while f != 0 and char not in self.trie[f]:
                    f = self.fail[f]
                
                if char in self.trie[f]:
                    self.fail[next_node] = self.trie[f][char]
                else:
                    self.fail[next_node] = 0
    
    def get_all_patterns(self, node):
        patterns = []
        if self.terminal[node]:
            patterns.extend(self.pattern_info[node])
        current = self.output_link[node]
        while current != 0:
            patterns.extend(self.pattern_info[current])
            current = self.output_link[current]
        return patterns
    
    def show(self):
        f = open(log_file, "w")
        f.write(30 * "=" + "BOHR" + 30 * "=" + "\n")
        node = 0
        level = 0
        def dfs(node, level):
            leaf = self.trie[node]
            f.writelines("\t\t" * level + f"ID({node}) {leaf}" + f" | isTerm - {self.terminal[node]}" + "\n" + level*"\t\t|" + "\n")
            level += 1
            for child in self.trie[node].values():
                dfs(child, level)
        dfs(node, level)
        f.close()


def find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char):
    n = len(text)
    m = len(pattern)
    subpatterns = []
    i = 0
    while i < m:
        if pattern[i] != wildcard_char:
            start = i
            j = i
            while j < m and pattern[j] != wildcard_char:
                j += 1
            subpatterns.append((pattern[start:j], start))
            i = j
        else:
            i += 1
    
    k = len(subpatterns)
    
    if k == 0 or m > n:
        return []

    ac = AhoCorasick()
    for idx, (subpattern, start_pos) in enumerate(subpatterns):
        ac.add_pattern(subpattern, idx, start_pos, len(subpattern))
    ac.show()
    
    ac.build_automaton()
    C = [0] * n
    node = 0
    
    for pos, char in enumerate(text):
        while node != 0 and char not in ac.trie[node]:
            node = ac.fail[node]
        if char in ac.trie[node]:
            node = ac.trie[node][char]
        else:
            node = 0
        patterns_found = ac.get_all_patterns(node)

        for pattern_idx, start_pos_in_pattern, length in patterns_found:
            pattern_start_in_text = pos - length + 1 - start_pos_in_pattern
            if 0 <= pattern_start_in_text < n:
                valid = True
                j = 0
                current_pos_in_pattern = 0
                
                for subpattern, sub_start in subpatterns:
                    while current_pos_in_pattern < sub_start:
                        text_pos = pattern_start_in_text + current_pos_in_pattern
                        if text_pos < n and text[text_pos] == forbidden_char:
                            valid = False
                            break
                        current_pos_in_pattern += 1
                    
                    if not valid:
                        break

                    current_pos_in_pattern += len(subpattern)

                while valid and current_pos_in_pattern < m:
                    text_pos = pattern_start_in_text + current_pos_in_pattern
                    if text_pos < n and text[text_pos] == forbidden_char:
                        valid = False
                        break
                    current_pos_in_pattern += 1
                
                if valid:
                    C[pattern_start_in_text] += 1

    results = []
    for i in range(n - m + 1):
        if C[i] == k:
            results.append(i + 1)
    
    return results


def main():
    text = input().strip()
    pattern = input().strip()
    wildcard_char = input().strip()
    forbidden_char = input().strip()  
    
    positions = find_pattern_with_wildcard_excluding(
        text, pattern, wildcard_char, forbidden_char
    )
    
    for pos in positions:
        print(pos)


if __name__ == "__main__":
    main()