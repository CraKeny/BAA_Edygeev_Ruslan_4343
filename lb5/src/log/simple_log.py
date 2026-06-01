from collections import deque

log_file = "log_1.txt"

class AhoCorasick:
    def __init__(self):
        self.trie = [{}]
        self.fail = [0]
        self.terminal_link = [0]  
        self.terminal = [False]   
        self.output = [[]]
    
    def log(self, msg):
        with open(log_file, "a") as f:
            f.write(msg + "\n")
    
    def add_pattern(self, pattern, index):
        node = 0
        self.log(f"[ADD] pattern {index}: '{pattern}'")
        for pos, char in enumerate(pattern):
            if char not in self.trie[node]:
                new_node = len(self.trie)
                self.trie[node][char] = new_node
                self.trie.append({})
                self.fail.append(0)
                self.terminal_link.append(0)
                self.terminal.append(False)
                self.output.append([])
                self.log(f"      create node {new_node} via '{char}' from {node}")
            node = self.trie[node][char]
        self.terminal[node] = True
        self.output[node].append(index)
        self.log(f"      node {node} is TERMINAL for pattern {index}")
    
    def build_failure_and_terminal_links(self):
        self.log("\n" + "="*60)
        self.log("BUILDING FAILURE & TERMINAL LINKS")
        self.log("="*60)
        
        q = deque()
        self.log("\n[INIT] root children:")
        for char, next_node in self.trie[0].items():
            self.fail[next_node] = 0
            q.append(next_node)
            self.terminal_link[next_node] = 0
            self.log(f"        node {next_node} (via '{char}'): fail=0, term_link=0")
        
        step = 1
        while q:
            current = q.popleft()
            self.log(f"\n[STEP {step}] process node {current}")
            self.log(f"        fail[{current}] = {self.fail[current]}")
            
            
            if self.terminal[self.fail[current]]:
                self.terminal_link[current] = self.fail[current]
                self.log(f"        term_link[{current}] = {self.fail[current]} (fail is terminal)")
            else:
                self.terminal_link[current] = self.terminal_link[self.fail[current]]
                self.log(f"        term_link[{current}] = {self.terminal_link[self.fail[current]]}")
            
            
            for char, next_node in self.trie[current].items():
                q.append(next_node)
                self.log(f"        edge '{char}' -> {next_node}")
                
                f = self.fail[current]
                self.log(f"            start f = {f}")
                
                while f != 0 and char not in self.trie[f]:
                    f = self.fail[f]
                    self.log(f"            follow fail -> f = {f}")
                
                if char in self.trie[f]:
                    self.fail[next_node] = self.trie[f][char]
                    self.log(f"            found '{char}' in node {f} -> {self.trie[f][char]}")
                else:
                    self.fail[next_node] = 0
                    self.log(f"            '{char}' not found, fail = 0")
                
                self.log(f"            fail[{next_node}] = {self.fail[next_node]}")
            
            step += 1
        
        self.log("\n" + "="*60)
        self.log("BUILD COMPLETE")
        self.log("="*60)
    
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
        self.log("\n" + "="*60)
        self.log("SEARCH IN TEXT")
        self.log("="*60)
        self.log(f"Text: '{text}'")
        
        results = []
        node = 0
        
        for i, char in enumerate(text):
            self.log(f"\n[pos {i+1}] char='{char}' state={node}")
            
            
            steps = 0
            while node != 0 and char not in self.trie[node]:
                node = self.fail[node]
                steps += 1
                if steps == 1:
                    self.log(f"        follow fail -> {node}")
            
            
            if char in self.trie[node]:
                node = self.trie[node][char]
                self.log(f"        edge '{char}' -> {node}")
            else:
                self.log(f"        no edge, stay at {node}")
            
            
            patterns_found = self.get_all_patterns(node)
            if patterns_found:
                self.log(f"        FOUND patterns: {patterns_found}")
                for pattern_index in patterns_found:
                    start_pos = i - pattern_lengths[pattern_index] + 2
                    self.log(f"            pattern {pattern_index} at position {start_pos}")
                    results.append((start_pos, pattern_index))
        
        self.log(f"\nTotal matches: {len(results)}")
        return results
    
    def show(self):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n" + "="*60 + "\n")
            f.write("FINAL AUTOMATON STATE\n")
            f.write("="*60 + "\n\n")

            f.write("NODE DETAILS:\n")
            f.write("─"*70 + "\n")
            f.write("Node  Terminal  Patterns  Transitions              fail  term_link\n")
            f.write("─"*70 + "\n")
            
            for node in range(len(self.trie)):
                term = "✓" if self.terminal[node] else "·"
                pat = str(self.output[node]) if self.output[node] else "[]"
                trans = ", ".join([f"{ch}→{nxt}" for ch, nxt in list(self.trie[node].items())[:4]])
                if len(self.trie[node]) > 4:
                    trans += "..."
                trans = trans.ljust(25)[:25]
                fail_str = str(self.fail[node])
                term_link_str = str(self.terminal_link[node])
                f.write(f"{node:4}  {term:3}     {pat:8}   {trans}      {fail_str:3}    {term_link_str:3}\n")
            
            
            f.write("\n" + "─"*70 + "\n")
            f.write("TREE VIEW:\n")
            f.write("─"*70 + "\n")
            
            def dfs(node, depth):
                indent = "  " * depth
                term_mark = " [*]" if self.terminal[node] else ""
                pat_mark = f" {self.output[node]}" if self.output[node] else ""
                f.write(f"{indent}Node{node}{term_mark}{pat_mark}\n")
                for char, child in self.trie[node].items():
                    f.write(f"{indent}  └─ '{char}' → {child}\n")
                    dfs(child, depth + 2)
            dfs(0, 0)
            
            f.write("\n" + "="*60 + "\n")
            f.write(f"STATISTICS: {len(self.trie)} nodes, {sum(1 for t in self.terminal if t)} terminal\n")
            f.write("="*60 + "\n")
    
    def clear_log(self):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("AHO-CORASICK DEBUG LOG\n")
            f.write("="*60 + "\n\n")


def main():
    text = input().strip()
    n = int(input().strip())
    patterns = []
    for _ in range(n):
        patterns.append(input().strip())
    
    ac = AhoCorasick()
    ac.clear_log()
    
    ac.log("INPUT DATA:")
    ac.log(f"  Text: '{text}'")
    ac.log(f"  Patterns count: {n}")
    for i, p in enumerate(patterns, 1):
        ac.log(f"    {i}: '{p}'")
    
    
    ac.log("\n" + "="*60)
    ac.log("ADDING PATTERNS")
    ac.log("="*60)
    for i, pattern in enumerate(patterns, 1):
        ac.add_pattern(pattern, i)

    ac.build_failure_and_terminal_links()
    ac.show()
    pattern_lengths = {i: len(pattern) for i, pattern in enumerate(patterns, 1)}
    results = ac.search(text, pattern_lengths)

    results.sort()
    for pos, idx in results:
        print(pos, idx)
    
    ac.log("\n" + "="*60)
    ac.log(f"FINAL RESULTS: {len(results)} matches")
    for pos, idx in results:
        ac.log(f"  {pos} {idx}")
    ac.log("="*60)


if __name__ == "__main__":
    main()