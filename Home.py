import streamlit as st
from wordfreq import top_n_list
import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

def generate_words(trie, letters, must_include, min_length, max_length, starts_with):
    valid_words = set()
    letters = letters.lower()
    must_include = must_include.lower()
    starts_with = starts_with.lower()

    def backtrack(path):
        if len(path) >= min_length and len(path) <= max_length and must_include in path:
            word = ''.join(path)
            if trie.search(word) and word.startswith(starts_with):
                valid_words.add(word)
        if len(path) < max_length:
            for letter in letters:
                path.append(letter)
                if trie.starts_with(''.join(path)):
                    backtrack(path)
                path.pop()

    backtrack([])
    return valid_words

def main():
    st.title("Spelling Bee Helper :bee:")

    # Sidebar inputs
    top_n = st.sidebar.number_input("Number of words to check", min_value=10000, value=100000, max_value=5000000)
    min_length = st.sidebar.slider("Minimum word length", min_value=4, max_value=13, value=4)
    max_length = st.sidebar.slider("Maximum word length", min_value=4, max_value=13, value=8)
    starts_with = st.sidebar.text_input("Starts with (optional):", value="")
    st.sidebar.caption("One or more starting letters")

    letters = st.text_input("Enter the 7 letters (no spaces):").replace(" ", "").lower()
    must_include = st.text_input("Enter the mandatory letter:").lower()

    if st.button("Find Words"):
        if len(letters) == 7 and must_include in letters:
            start_time = time.time()  # Start the timer
            top_words = top_n_list('en', top_n)
            trie = Trie()
            for word in top_words:
                trie.insert(word)
            words = generate_words(trie, letters, must_include, min_length, max_length, starts_with)
            end_time = time.time()  # End the timer

            elapsed_time = end_time - start_time

            # Correct pangram check
            unique_letters = set(letters)
            pangrams = [word for word in words if unique_letters.issubset(set(word))]

            # Display execution time
            st.caption(f"Execution time: {elapsed_time:.2f} seconds")
            
            st.write("## Valid Words")
            st.write(sorted(list(words)))  # Display words as a list
                
            st.write("## Pangrams")
            if pangrams:
                st.write(sorted(list(pangrams)))  # Display pangrams as a list
            else:
                st.warning("No pangrams found.")
        else:
            st.error("Please enter exactly 7 letters, including the mandatory letter.")

if __name__ == "__main__":
    main()