import os
import sys
import re
from datetime import date

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

def get_list_input(item_name):
    """
    Helper to get a list of items from the user.
    """
    items = []
    while True:
        count_str = get_input(f"How many {item_name} do you want to enter? ")
        if not count_str.isdigit():
            print(f"Please enter a valid *positive* number for {item_name}.")
            continue
        
        count = int(count_str)
        if count < 0:
            print("The number must be zero or positive.")
            continue

        for i in range(count):
            item = get_input(f"Enter {item_name} #{i+1}: ")
            items.append(item)
        return items

def convert_date_to_words(date_part):
    """
    Converts a two-digit month or day (01-12) to its name and common abbreviations.
    Example: '01' -> {'january', 'jan', '1'}
    """
    words = set()
    try:
        num = int(date_part)
    except ValueError:
        return words # Not a valid number

    # Mapping of month numbers (1-12) to their full name and abbreviation
    month_map = {
        1: ('january', 'jan'), 2: ('february', 'feb'), 3: ('march', 'mar'),
        4: ('april', 'apr'), 5: ('may', 'may'), 6: ('june', 'jun'),
        7: ('july', 'jul'), 8: ('august', 'aug'), 9: ('september', 'sep'),
        10: ('october', 'oct'), 11: ('november', 'nov'), 12: ('december', 'dec')
    }

    # If it's a valid month number (1-12)
    if 1 <= num <= 12:
        full, abbr = month_map[num]
        words.add(full)
        words.add(abbr)

    # Common numeric representations
    words.add(str(num)) # e.g., '1', '10'
    
    # Keep the leading zero if it was present and the number is less than 10
    if len(date_part) == 2 and date_part.startswith('0'):
        words.add(date_part) # e.g., '01'

    return words

def extract_date_components(date_string):
    """
    Analyzes a date string (e.g., '01/01/1999') and extracts all relevant
    numerical and word components for password generation, including YYMMDD formats.
    """
    components = set()
    date_string = date_string.strip()

    if not date_string:
        return components

    # Add the raw date string itself
    components.add(date_string) 

    # --- 1. Numerical Components (Pure Digits) ---
    pure_digits = re.sub(r'[^0-9]', '', date_string)
    if pure_digits:
        components.add(pure_digits) 

        # Extract numeric suffixes
        if len(pure_digits) >= 4:
            year_4d = pure_digits[-4:]
            year_2d = pure_digits[-2:]
            month_day = pure_digits[:-4] 

            components.add(year_4d) # Full 4-digit year (e.g., '1999')
            components.add(year_2d) # 2-digit year (e.g., '99')
            
            # --- Generate YYYYMMDD and YYMMDD/DDMMYY formats ---
            if len(month_day) >= 4:
                month_part = month_day[:2]
                day_part = month_day[2:4]
                
                # YYYYMMDD (e.g., 19990101)
                components.add(year_4d + month_part + day_part)
                
                # YYMMDD (e.g., 990101)
                components.add(year_2d + month_part + day_part) 
                
                # MMDDYY (e.g., 010199)
                components.add(month_part + day_part + year_2d)
                
                # DDMMYY (e.g., 010199 - if date input was DDMMYYYY) - Adding common alternative
                components.add(day_part + month_part + year_2d)

        if len(pure_digits) >= 6:
            components.add(pure_digits[:-4]) # MMDD or DDMM (e.g., '0101')
            
    # --- 2. Word Components (Month/Day names) ---
    parts = re.split(r'[./-]', date_string) 
    
    # Process simple parts (Month, Day, Year)
    for part in parts:
        if part:
            components.add(part) 
            
            # Check if it's a month or day (up to 2 digits)
            if len(part) <= 2 and part.isdigit():
                components.update(convert_date_to_words(part))

    # Filter out empty strings and return
    return {c for c in components if c}


def collect_user_data():
    """
    Collects all necessary information from the user.
    """
    print("--- Personal Information Wordlist Generator 🛠️ ---")
    print("Please answer the following questions to build your wordlist.\n")

    data = {}

    # Names
    print("\n[Names]")
    data['names'] = get_list_input("names (First, Middle, or Last)")

    # Dates
    print("\n[Important Dates]")
    print("Formats: MMDDYYYY, YYYY, M/D/YYYY, etc.") 
    data['dates'] = get_list_input("dates (Birthdays, Anniversaries, etc.)")

    # Mobile Numbers (NEW INPUT)
    print("\n[Mobile Numbers]")
    print("Enter numbers as pure digits (e.g., 9171234567).")
    data['mobiles'] = get_list_input("11-digit mobile numbers")

    # Pet Names
    print("\n[Pet Names]")
    data['pets'] = get_list_input("pet names")

    # School Names
    print("\n[School Names]")
    data['schools'] = get_list_input("school names")

    # Favorite Words/Nicknames
    print("\n[Favorite Words/Nicknames]")
    data['nicknames'] = get_list_input("favorite words or nicknames")

    # Custom Keywords
    print("\n[Custom Keywords]")
    data['keywords'] = get_list_input("custom keywords")

    return data

def generate_variations(data):
    """
    Generates wordlist variations based on collected data.
    """
    wordlist = set()
    
    # Combine all base words for easy permutation
    base_words = (
        data['names'] + 
        data['pets'] + 
        data['schools'] + 
        data['nicknames'] + 
        data['keywords']
    )
    
    # Generate all date components (numerical and word-based)
    date_components = set()
    for date_str in data['dates']:
        date_components.update(extract_date_components(date_str))
        
    # Add mobile numbers to the numerical components set
    mobile_components = set()
    for num in data['mobiles']:
        # Ensure only pure digits are used for combination
        pure_num = re.sub(r'[^0-9]', '', num)
        if pure_num:
            mobile_components.add(pure_num)
            # Add common partial number patterns
            if len(pure_num) >= 4:
                mobile_components.add(pure_num[-4:]) # Last 4 digits
            if len(pure_num) >= 7:
                mobile_components.add(pure_num[-7:]) # Last 7 digits

    # Combine all numeric sources (dates, mobiles, and their parts)
    numerical_components = date_components.union(mobile_components)
    
    # Combine all words (base words + date words) into a master word list
    master_words = base_words + [c for c in date_components if not c.isdigit() and len(c) > 3]

    # Separators: Used for Word + Component and Word + Word combinations
    separators = ['', '_', '.', '-'] 
    
    # Symbols/Numbers typically appended to the end
    symbols_and_numbers = ['!', '@', '#', '$', '123']

    # --- 1. Single words (Case and Simple Leet variations) ---
    for word in master_words:
        wordlist.add(word)
        wordlist.add(word.lower())
        wordlist.add(word.upper())
        wordlist.add(word.capitalize())
        # Leet speak variations (simple)
        wordlist.add(word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0'))

    # --- 2. Word + Word Combinations (Permutation of all collected words) ---
    for word1 in master_words:
        for word2 in master_words:
            if word1 == word2: 
                continue
            
            for sep in separators:
                base = f"{word1}{sep}{word2}"
                wordlist.add(base)
                wordlist.add(base.lower())
                wordlist.add(base.capitalize())


    # --- 3. Word + Numeric Component combinations (Mobile Numbers & Dates) ---
    
    # Filter the numerical_components set to exclude words and only include digits or date/number separators
    pure_numerical_components = {c for c in numerical_components if c.isdigit() or re.match(r'[/\.-]', c)}
    
    for word in master_words:
        for component in pure_numerical_components:
            # If the component is a 'clean' number (no separators), we can add separators
            if component.isdigit():
                for sep in separators:
                    base = f"{word}{sep}{component}"
                    wordlist.add(base)
                    wordlist.add(base.lower())
            
            # If the component contains separators (e.g., '01/01/1999' or '917-123-4567'), combine without separators
            else:
                 base = f"{word}{component}"
                 wordlist.add(base)
                 wordlist.add(base.lower())
                 
            # Also add the reverse (Component + Word)
            base_rev = f"{component}{word}"
            wordlist.add(base_rev)
            wordlist.add(base_rev.lower())
            
            # Reverse with separator only if it's a clean number
            if component.isdigit():
                 for sep in separators:
                     base_rev_sep = f"{component}{sep}{word}"
                     wordlist.add(base_rev_sep)
                     wordlist.add(base_rev_sep.lower())

    # --- 4. Word + Symbol/Number combinations (at the end) ---
    for word in master_words:
        for suffix in symbols_and_numbers:
            base = f"{word}{suffix}"
            wordlist.add(base)
            wordlist.add(base.lower())
            wordlist.add(base.capitalize())

    # Final cleanup
    return sorted(list(wordlist))

def save_wordlist(wordlist):
    """
    Saves the generated wordlist to a unique file name (e.g., wordlist.txt, wordlist2.txt).
    """
    base_name = "wordlist"
    extension = ".txt"
    counter = 1
    filename = base_name + extension

    # Check for existing files and increment the counter until an unused name is found
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_name}{counter}{extension}"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for word in wordlist:
                f.write(word + '\n')
        print(f"\n[Success] Wordlist successfully generated as **{filename}**")
        print(f"Total words generated: **{len(wordlist)}**")
        print(f"Location: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\n[Error] Could not save file: {e}")

def main():
    try:
        user_data = collect_user_data()
        
        # Check if we have enough data to generate something
        total_inputs = sum(len(v) for v in user_data.values())
        if total_inputs == 0:
            print("\n[Warning] No input provided. Wordlist will be empty.")
        
        print("\nGenerating wordlist variations...")
        final_list = generate_variations(user_data)
        
        save_wordlist(final_list)
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()