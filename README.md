# Personal Information Wordlist Generator & Comparator

A Python-based wordlist generation and comparison toolkit designed for password auditing, security testing, and educational use.  
This project consists of two scripts:

- `wordlist_generator.py` – Generates a custom wordlist based on personal information  
- `compare.py` – Compares two wordlists and extracts unique entries

> ⚠️ Disclaimer  
> This tool is intended for ethical security testing, academic projects, and personal password analysis only. Do not use it against systems you do not own or have explicit permission to test.

---

## Features

### Wordlist Generator
- Interactive command-line interface
- Collects personal information including:
  - Names (first, middle, last)
  - Important dates (birthdays, anniversaries, etc.)
  - Mobile numbers
  - Pet names
  - School names
  - Nicknames and custom keywords
- Intelligent date parsing:
  - Extracts year, month, and day values
  - Generates formats such as `YYYYMMDD`, `YYMMDD`, `MMDDYY`, and `DDMMYY`
  - Converts numeric months into word equivalents and abbreviations
- Generates multiple variations:
  - Case transformations (lowercase, uppercase, capitalized)
  - Simple leetspeak substitutions
  - Word + word combinations
  - Word + number/date combinations
  - Common suffixes
- Automatically removes duplicates
- Saves output to an auto-incremented file:
  - `wordlist.txt`, `wordlist2.txt`, `wordlist3.txt`, etc.

---

### Wordlist Comparison Tool
- Case-insensitive comparison
- Compares two wordlists and extracts:
  - Words present in the second list but not in the first
- Useful for:
  - Tracking newly generated words
  - Incremental wordlist building
  - Removing duplicates between generations
- Outputs results to a separate file

---

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only standard Python libraries)

---

## File Structure

project/
│
├── wordlist_generator.py
├── compare.py
├── wordlist.txt
├── wordlist2.txt
└── wordlist_difference.txt


---

## Usage

### Generate a Wordlist

Run the generator script:


Follow the prompts and enter the requested information.  
The generated wordlist will be saved automatically in the current directory.

---

### Compare Two Wordlists

By default, the comparison script uses:

- `wordlist.txt`
- `wordlist2.txt`

Run:


The script will generate:

- `wordlist_difference.txt`

This file contains words that exist in `wordlist2.txt` but not in `wordlist.txt`.

You can modify the filenames directly inside `compare.py` if needed.

---

## Use Cases

- Password strength evaluation
- Ethical penetration testing
- Cybersecurity coursework and labs
- Security research
- Understanding real-world password patterns

---

## Notes

- All output is sorted for consistency
- Handles large wordlists efficiently using sets
- Gracefully exits on user interruption
- Designed for educational and ethical use

---

## License

This project is provided for educational purposes only.  
The user is responsible for proper and ethical usage.
