def isPalindrome(word: str) -> bool:
    """
    Recursive palindrome check.
    Returns True if word reads the same forwards and backwards, else False.

    Assumption: input is a single word (no spaces).
    Case-sensitive by default (so "Pop" is not the same as "pop").
    """
    if len(word) <= 1:
        return True

    if word[0] != word[-1]:
        return False

    return isPalindrome(word[1:-1])
