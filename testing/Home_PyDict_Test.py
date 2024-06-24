import streamlit as st
from itertools import product
from PyDictionary import PyDictionary

dictionary = PyDictionary()

def is_valid_word(word):
    try:
        # Check if the word has any meanings
        meaning = dictionary.meaning(word)
        if meaning:
            return True
    except:
        pass
    return False

def generate_words(letters, must_include, min_length, max_length, starts_with):
    valid_words = set()
    letters = letters.lower()
    must_include = must_include.lower()
    starts_with = starts_with.lower()

    # Generate valid words using product to handle repeated letters
    for i in range(min_length, max_length + 1):
        for comb in product(letters, repeat=i):
            if must_include in comb:
                word = ''.join(comb)
                if word.startswith(starts_with) and is_valid_word(word):
                    valid_words.add(word)
    
    return valid_words

def main():
    st.title("Spelling Bee Helper :bee:")

    # Sidebar inputs
    min_length = st.sidebar.slider("Minimum word length", min_value=4, max_value=12, value=4)
    max_length = st.sidebar.slider("Maximum word length", min_value=4, max_value=12, value=8)
    starts_with = st.sidebar.text_input("Starts with (optional):", value="")
    st.sidebar.caption("One or more starting letters")

    letters = st.text_input("Enter the 7 letters (no spaces):").lower()
    must_include = st.text_input("Enter the mandatory letter:").lower()

    if st.button("Find Words"):
        if len(letters) == 7 and must_include in letters:
            words = generate_words(letters, must_include, min_length, max_length, starts_with)

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