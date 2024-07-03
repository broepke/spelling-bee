import streamlit as st
from wordfreq import top_n_list
from itertools import product
import time

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
    st.title("Spelling Bee Helper :bee:")

    # Sidebar inputs
    top_n = st.sidebar.number_input("Number of words to check", min_value=10000, value=100000, max_value=50000000)
    min_length = st.sidebar.slider("Minimum word length", min_value=4, max_value=12, value=4)
    max_length = st.sidebar.slider("Maximum word length", min_value=4, max_value=12, value=8)
    starts_with = st.sidebar.text_input("Starts with (optional):", value="")
    st.sidebar.caption("One or more starting letters")

    letters = st.text_input("Enter the 7 letters (no spaces):").lower()
    must_include = st.text_input("Enter the mandatory letter:").lower()

    if st.button("Find Words"):
        if len(letters) == 7 and must_include in letters:
            start_time = time.time()  # Start the timer
            words = generate_words(letters, must_include, top_n, min_length, max_length, starts_with)
            end_time = time.time()  # End the timer

            elapsed_time = end_time - start_time

            # Correct pangram check
            unique_letters = set(letters)
            pangrams = [word for word in words if unique_letters.issubset(set(word))]

            st.caption(f"Execution time: {elapsed_time:.2f} seconds")  # Display execution time
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