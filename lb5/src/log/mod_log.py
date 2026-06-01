from collections import deque

log_file = "log_3.txt"


class AhoCorasick:
    def __init__(self):
        self.trie = [{}]
        self.fail = [0]
        self.output_link = [0]
        self.terminal = [False]
        self.pattern_info = [[]]
    
    def log(self, msg):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    
    def add_pattern(self, pattern, pattern_index, start_pos_in_pattern, length):
        self.log(f"[ADD] subpattern {pattern_index}: '{pattern}' (start={start_pos_in_pattern}, len={length})")
        node = 0
        for pos, char in enumerate(pattern):
            if char not in self.trie[node]:
                new_node = len(self.trie)
                self.trie[node][char] = new_node
                self.trie.append({})
                self.fail.append(0)
                self.output_link.append(0)
                self.terminal.append(False)
                self.pattern_info.append([])
                self.log(f"      create node {new_node} via '{char}' from {node}")
            node = self.trie[node][char]
            self.log(f"      -> node {node}")
        
        self.terminal[node] = True
        self.pattern_info[node].append((pattern_index, start_pos_in_pattern, length))
        self.log(f"      node {node} is TERMINAL for subpattern {pattern_index}")
    
    def build_automaton(self):
        self.log("\n" + "="*60)
        self.log("BUILDING AUTOMATON (FAILURE + OUTPUT LINKS)")
        self.log("="*60)
        
        q = deque()
        
        self.log("\n[INIT] root children:")
        for char, next_node in self.trie[0].items():
            self.fail[next_node] = 0
            q.append(next_node)
            self.log(f"        node {next_node} (via '{char}'): fail=0")
        
        step = 1
        while q:
            current = q.popleft()
            self.log(f"\n[STEP {step}] process node {current}")
            self.log(f"        fail[{current}] = {self.fail[current]}")
            
            if self.terminal[self.fail[current]]:
                self.output_link[current] = self.fail[current]
                self.log(f"        output_link[{current}] = {self.fail[current]} (fail is terminal)")
            else:
                self.output_link[current] = self.output_link[self.fail[current]]
                self.log(f"        output_link[{current}] = {self.output_link[self.fail[current]]}")
            
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
            patterns.extend(self.pattern_info[node])
        current = self.output_link[node]
        while current != 0:
            patterns.extend(self.pattern_info[current])
            current = self.output_link[current]
        return patterns
    
    def show(self):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n" + "="*60 + "\n")
            f.write("FINAL AUTOMATON STATE\n")
            f.write("="*60 + "\n\n")
            
            f.write("NODE DETAILS:\n")
            f.write("─"*80 + "\n")
            f.write("Node  Terminal  Subpatterns              Transitions              fail  out_link\n")
            f.write("─"*80 + "\n")
            
            for node in range(len(self.trie)):
                term = "✓" if self.terminal[node] else "·"
                pat = str(self.pattern_info[node]) if self.pattern_info[node] else "[]"
                pat = pat.ljust(25)[:25]
                trans = ", ".join([f"{ch}→{nxt}" for ch, nxt in list(self.trie[node].items())[:4]])
                if len(self.trie[node]) > 4:
                    trans += "..."
                trans = trans.ljust(23)[:23]
                fail_str = str(self.fail[node])
                out_str = str(self.output_link[node])
                f.write(f"{node:4}  {term:3}     {pat}   {trans}      {fail_str:3}    {out_str:3}\n")
            
            f.write("\n" + "─"*80 + "\n")
            f.write("TREE VIEW:\n")
            f.write("─"*80 + "\n")
            
            def dfs(node, depth):
                indent = "  " * depth
                term_mark = " [*]" if self.terminal[node] else ""
                pat_mark = f" {self.pattern_info[node]}" if self.pattern_info[node] else ""
                f.write(f"{indent}Node{node}{term_mark}{pat_mark}\n")
                for char, child in self.trie[node].items():
                    f.write(f"{indent}  └─ '{char}' → {child}\n")
                    dfs(child, depth + 2)
            
            dfs(0, 0)
            
            f.write("\n" + "="*60 + "\n")
            f.write(f"STATISTICS: {len(self.trie)} nodes, {sum(1 for t in self.terminal if t)} terminal\n")
            f.write("="*60 + "\n")


def find_pattern_with_wildcard_excluding(text, pattern, wildcard_char, forbidden_char):
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("AHO-CORASICK WILDCARD SEARCH (WITH EXCLUDING CHAR) DEBUG LOG\n")
        f.write("="*60 + "\n\n")
        f.write("INPUT DATA:\n")
        f.write(f"  Text: '{text}'\n")
        f.write(f"  Pattern: '{pattern}'\n")
        f.write(f"  Wildcard char: '{wildcard_char}'\n")
        f.write(f"  Forbidden char: '{forbidden_char}'\n")
        f.write("="*60 + "\n")
    
    n = len(text)
    m = len(pattern)
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\nSTEP 1: SPLIT PATTERN INTO SUBPATTERNS\n")
        f.write("-"*40 + "\n")
    
    subpatterns = []
    i = 0
    while i < m:
        if pattern[i] != wildcard_char:
            start = i
            j = i
            while j < m and pattern[j] != wildcard_char:
                j += 1
            subpatterns.append((pattern[start:j], start))
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"  subpattern: '{pattern[start:j]}' at position {start}\n")
            i = j
        else:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"  wildcard at position {i}\n")
            i += 1
    
    k = len(subpatterns)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n  Total subpatterns: {k}\n")
    
    if k == 0 or m > n:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n  No subpatterns or pattern longer than text -> no matches\n")
        return []
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write("STEP 2: BUILD AHOCORASICK AUTOMATON\n")
        f.write("="*60 + "\n")
    
    ac = AhoCorasick()
    for idx, (subpattern, start_pos) in enumerate(subpatterns):
        ac.add_pattern(subpattern, idx, start_pos, len(subpattern))
    
    ac.show()
    ac.build_automaton()
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write("STEP 3: SEARCH IN TEXT (WITH FORBIDDEN CHAR CHECK)\n")
        f.write("="*60 + "\n")
        f.write(f"Text: '{text}'\n")
        f.write(f"Forbidden char: '{forbidden_char}'\n\n")
    
    C = [0] * n
    node = 0
    
    for pos, char in enumerate(text):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[pos {pos+1}] char='{char}' state={node}\n")
        
        while node != 0 and char not in ac.trie[node]:
            node = ac.fail[node]
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"        follow fail -> {node}\n")
        
        if char in ac.trie[node]:
            node = ac.trie[node][char]
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"        edge '{char}' -> {node}\n")
        else:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"        no edge, stay at {node}\n")
        
        patterns_found = ac.get_all_patterns(node)
        
        if patterns_found:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"        FOUND subpatterns: {patterns_found}\n")
        
        for pattern_idx, start_pos_in_pattern, length in patterns_found:
            pattern_start_in_text = pos - length + 1 - start_pos_in_pattern
            
            if 0 <= pattern_start_in_text < n:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"\n        checking pattern {pattern_idx} start={pattern_start_in_text}\n")
                
                valid = True
                j = 0
                current_pos_in_pattern = 0
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write("        checking wildcard positions:\n")
                
                for subpattern, sub_start in subpatterns:
                    while current_pos_in_pattern < sub_start:
                        text_pos = pattern_start_in_text + current_pos_in_pattern
                        if text_pos < n:
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(f"            pos {current_pos_in_pattern}: text[{text_pos}]='{text[text_pos]}'")
                            if text[text_pos] == forbidden_char:
                                valid = False
                                with open(log_file, "a", encoding="utf-8") as f:
                                    f.write(f" -> FORBIDDEN! (equals '{forbidden_char}')\n")
                                break
                            else:
                                with open(log_file, "a", encoding="utf-8") as f:
                                    f.write(f" -> OK\n")
                        current_pos_in_pattern += 1
                    
                    if not valid:
                        break
                    
                    current_pos_in_pattern += len(subpattern)
                
                while valid and current_pos_in_pattern < m:
                    text_pos = pattern_start_in_text + current_pos_in_pattern
                    if text_pos < n:
                        with open(log_file, "a", encoding="utf-8") as f:
                            f.write(f"            pos {current_pos_in_pattern}: text[{text_pos}]='{text[text_pos]}'")
                        if text[text_pos] == forbidden_char:
                            valid = False
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(f" -> FORBIDDEN! (equals '{forbidden_char}')\n")
                            break
                        else:
                            with open(log_file, "a", encoding="utf-8") as f:
                                f.write(f" -> OK\n")
                    current_pos_in_pattern += 1
                
                if valid:
                    C[pattern_start_in_text] += 1
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(f"        VALID! C[{pattern_start_in_text}] = {C[pattern_start_in_text]}\n")
                else:
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(f"        INVALID (forbidden char found)\n")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n" + "="*60 + "\n")
        f.write("STEP 4: COLLECT RESULTS\n")
        f.write("="*60 + "\n")
        f.write(f"C array (first {n-m+1} positions): {C[:n-m+1]}\n\n")
    
    results = []
    for i in range(n - m + 1):
        if C[i] == k:
            results.append(i + 1)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"  position {i+1}: C[{i}] = {C[i]} == {k} -> MATCH\n")
        else:
            with open(log_file, "a", encoding="utf-8") as f:
                if C[i] > 0:
                    f.write(f"  position {i+1}: C[{i}] = {C[i]} != {k} -> no match\n")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\nTotal matches: {len(results)}\n")
        f.write("="*60 + "\n")
    
    return results


def main():
    text = input().strip()
    pattern = input().strip()
    wildcard_char = input().strip()
    forbidden_char = input().strip()
    
    positions = find_pattern_with_wildcard_excluding(
        text, pattern, wildcard_char, forbidden_char
    )
    
    print("\nRESULTS:")
    for pos in positions:
        print(pos)


if __name__ == "__main__":
    main()