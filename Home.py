import streamlit as st
from wordfreq import top_n_list
from itertools import product

def generate_words(letters, must_include, top_n, min_length, max_length, starts_with):
    top_words = set(top_n_list('en', top_n))
    valid_words = set()
    letters = letters.lower()
    must_include = must_include.lower()
    starts_with = starts_with.lower()

    # Generate valid words using product to handle repeated letters
    for i in range(min_length, max_length + 1):
        for comb in product(letters, repeat=i):
            if must_include in comb:
                word = ''.join(comb)
                if word in top_words and word.startswith(starts_with):
                    valid_words.add(word)
    
    return valid_words

def main():
    st.title("NYT Spelling Bee Solver")

    # Sidebar inputs
    top_n = st.sidebar.number_input("Top N words", min_value=1, value=100000)
    min_length = st.sidebar.number_input("Minimum word length", min_value=4, max_value=20, value=4)
    max_length = st.sidebar.number_input("Maximum word length", min_value=4, max_value=20, value=8)
    starts_with = st.sidebar.text_input("Starts with (optional):", value="")

    letters = st.text_input("Enter the 7 letters (no spaces):").lower()
    must_include = st.text_input("Enter the mandatory letter:").lower()

    if st.button("Find Words"):
        if len(letters) == 7 and must_include in letters:
            words = generate_words(letters, must_include, top_n, min_length, max_length, starts_with)

            # Correct pangram check
            unique_letters = set(letters)
            pangrams = [word for word in words if unique_letters.issubset(set(word))]

            st.write("## Valid Words")
            st.write(sorted(list(words)))  # Display words as a list
                
            st.write("## Pangrams")
            if pangrams:
                st.write(sorted(list(pangrams)))  # Display pangrams as a list
            else:
                st.write("No pangrams found.")
        else:
            st.write("Please enter exactly 7 letters, including the mandatory letter.")

if __name__ == "__main__":
    main()