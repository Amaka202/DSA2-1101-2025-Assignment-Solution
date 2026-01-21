def isPalindrome(word: str) -> bool:
    """
    Recursive palindrome check (case-insensitive).
    Returns True if word reads the same forwards and backwards, else False.
    Assumption: input is a single word (no spaces).
    """
    w = word.lower()

    if len(w) <= 1:
        return True

    if w[0] != w[-1]:
        return False

    return isPalindrome(w[1:-1])
