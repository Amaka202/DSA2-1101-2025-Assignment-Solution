#TASK 3: Most Frequent Word

import re
from typing import Dict, List, Tuple


def findMostFrequentWord(inputList1: List[str], inputList2: List[str]) -> str:
    """
    Task 3a:
    Return the SECOND most frequent word in inputList1 that is NOT present in inputList2.
    Tie-break: if frequencies are equal, return the word that occurs last in inputList1.

    If there are fewer than 2 eligible unique words, returns an empty string.
    """
    excluded = set(inputList2)

    counts: Dict[str, int] = {}
    last_index: Dict[str, int] = {}

    for i, word in enumerate(inputList1):
        if word in excluded:
            continue
        counts[word] = counts.get(word, 0) + 1
        last_index[word] = i

    if len(counts) < 2:
        return ""

    # Sort by:
    # 1) frequency descending
    # 2) last occurrence index descending (appears last wins tie)
    ranked: List[Tuple[str, int, int]] = []
    for w, c in counts.items():
        ranked.append((w, c, last_index[w]))

    ranked.sort(key=lambda x: (x[1], x[2]), reverse=True)

    # Second most frequent after applying tie-break
    return ranked[1][0]


def findMostFrequentWordInText(text: str) -> str:
    """
    Task 3b:
    Convert text into words only (punctuation removed).
    Return the MOST frequent word not in excluded list:
      Excluded words: “a”, “the”, “in”, “of”, “and”, “to”, “be”, “is”
    Tie-break (not explicitly stated in the task): if same frequency, return the word
    that appears last in the text. This matches Task 3a tie rule.
    """
    excluded_words = {"a", "the", "in", "of", "and", "to", "be", "is"}

    # Extract words only: letters (and apostrophes), ignore punctuation.
    # Example: "don't" is treated as one word.
    words = re.findall(r"[A-Za-z']+", text.lower())

    counts: Dict[str, int] = {}
    last_index: Dict[str, int] = {}

    for i, w in enumerate(words):
        if w in excluded_words:
            continue
        counts[w] = counts.get(w, 0) + 1
        last_index[w] = i

    if not counts:
        return ""

    best_word = ""
    best_count = -1
    best_last = -1

    for w, c in counts.items():
        li = last_index[w]
        if c > best_count or (c == best_count and li > best_last):
            best_word = w
            best_count = c
            best_last = li

    return best_word
