import hashlib
import sys

def crack_md5(target_hash, wordlist_path):
    try:
        with open(wordlist_path, "r", errors="ignore") as file:
            for line in file:
                word = line.strip()
                hashed_word = hashlib.md5(word.encode()).hexdigest()

                if hashed_word == target_hash:
                    print(f"[+] Match found: {word}")
                    return

        print("[-] No match found in wordlist.")

    except FileNotFoundError:
        print("[-] Wordlist file not found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python crack_md5.py <md5_hash> <wordlist.txt>")
        sys.exit(1)

    target_hash = sys.argv[1].lower()
    wordlist = sys.argv[2]

    crack_md5(target_hash, wordlist)
