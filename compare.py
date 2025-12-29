import os
import sys

def get_input(prompt, allow_empty=False):
    """
    Helper function to get user input with validation.
    """
    while True:
        value = input(prompt).strip()
        if not value and not allow_empty:
            print("Error: Input cannot be empty. Please try again.")
        else:
            return value

def load_wordlist(filename):
    """
    Loads all unique words from a file into a set, performing case-insensitive comparison.
    """
    words = set()
    try:
        # 'errors=ignore' helps skip over non-UTF-8 characters in external wordlists
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            # Strip whitespace and convert to lowercase for case-insensitive comparison
            for line in f:
                word = line.strip().lower()
                if word:
                    words.add(word)
        print(f"Loaded {len(words)} unique words from **{filename}**.")
        return words
    except FileNotFoundError:
        print(f"\n[Error] File not found: {filename}")
        return None
    except Exception as e:
        print(f"\n[Error] Failed to read {filename}: {e}")
        return None

def find_unique_words(file1_path, file2_path, output_path):
    """
    Compares two wordlists (file1 and file2) and saves words that are in
    file2 but NOT in file1 to the output file.
    """
    print("\n--- Wordlist Comparison Utility 🔎 ---")
    
    # 1. Load the data
    set1 = load_wordlist(file1_path)
    if set1 is None:
        return
        
    set2 = load_wordlist(file2_path)
    if set2 is None:
        return

    # 2. Perform the Set Difference Operation
    # set2.difference(set1) finds items in set2 that are NOT in set1.
    print(f"\nCalculating the difference (Words in **{file2_path}** but not in **{file1_path}**)...")
    unique_words = set2.difference(set1) 
    
    # 3. Save the results
    try:
        # Sort the words for consistency before saving
        sorted_unique_words = sorted(list(unique_words))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in sorted_unique_words:
                f.write(word + '\n')
                
        print(f"\n[Success] Delta wordlist generated as **{output_path}**")
        print(f"Total unique words found: **{len(sorted_unique_words)}**")
        print(f"Location: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"\n[Error] Could not save output file: {e}")

def main():
    try:
        # --- FILENAMES HARDCODED HERE ---
        file1 = "wordlist.txt"
        file2 = "wordlist2.txt"
        output = "wordlist_difference.txt"
        
        print(f"Comparing **{file2}** against **{file1}**...")
        
        find_unique_words(file1, file2, output)
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()