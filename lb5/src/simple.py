from collections import deque

log_file = "log_1.txt"

class AhoCorasick:
    def __init__(self):
        self.trie = [{}]
        self.fail = [0]
        self.terminal_link = [0]  
        self.terminal = [False]   
        self.output = [[]]        
    
    def add_pattern(self, pattern, index):
        node = 0
        for char in pattern:
            if char not in self.trie[node]:
                self.trie[node][char] = len(self.trie)
                self.trie.append({})
                self.fail.append(0)
                self.terminal_link.append(0)
                self.terminal.append(False)
                self.output.append([])
            node = self.trie[node][char]
        self.terminal[node] = True
        self.output[node].append(index)
    
    def build_links(self):
        q = deque()

        for char, next_node in self.trie[0].items():
            self.fail[next_node] = 0
            q.append(next_node)
            
            self.terminal_link[next_node] = 0
        while q:
            current = q.popleft()
            if self.terminal[self.fail[current]]:
                self.terminal_link[current] = self.fail[current]
            else:
                self.terminal_link[current] = self.terminal_link[self.fail[current]]
            
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
            patterns.extend(self.output[node])
        current = self.terminal_link[node]
        while current != 0:
            patterns.extend(self.output[current])
            current = self.terminal_link[current]
        return patterns
    
    def search(self, text, pattern_lengths):
        results = []
        node = 0
        
        for i, char in enumerate(text):
            while node != 0 and char not in self.trie[node]:
                node = self.fail[node]
            if char in self.trie[node]:
                node = self.trie[node][char]
            else:
                node = 0
            for pattern_index in self.get_all_patterns(node):
                start_pos = i - pattern_lengths[pattern_index] + 2
                results.append((start_pos, pattern_index))
        return results

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

def main():
    text = input().strip()
    n = int(input().strip())
    patterns = []
    for _ in range(n):
        patterns.append(input().strip())
    
    ac = AhoCorasick()
    for i, pattern in enumerate(patterns, 1):
        ac.add_pattern(pattern, i)
    
    ac.build_links()
    ac.show()

    pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
    results = ac.search(text, pattern_lengths)
    
    results.sort()
    for pos, idx in results:
        print(pos, idx)


if __name__ == "__main__":
    main()