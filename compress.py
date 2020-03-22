import sys
import re

with open(sys.argv[1], 'r') as f:
    lines = [line for line in f]

text = "".join(lines)

text = re.sub(r"\s+"," ",text)
text = text.lower()

word_to_id = {}
id_to_word = {}

words = text.split()

index = 0
for word in words:
    if not word in word_to_id:
        word_to_id[word] = index
        id_to_word[index] = word
        index += 1

word_ids = [word_to_id[word] for word in words]
suffixes = [word_ids[i:] for i in range(len(word_ids))]
suffix_array = sorted(suffixes)

def lcp(s1, s2):
    l = 0
    i = 0
    while i < len(s1) and i < len(s2):
        if s1[i] == s2[i]:
            l += 1
        else: 
            break
        i += 1
    return l

lcp_array = [lcp(suffix_array[i], suffix_array[i+1]) for i in range(len(suffix_array) - 1)] + [0]

def abbreviation_value(substring, occurrences):
    """Characters saved by introducing an abbreviation for the substring."""
    n = len(substring)
    m = sum(len(id_to_word[i]) for i in substring)
    chars_before = (m + n - 1) * occurrences
    chars_after = (m + n - 1) + 2 + n * (occurrences)
    return chars_before - chars_after

for i, lcp in enumerate(lcp_array[:-1]):
    substr_length = lcp
    substr_count = 2
    substr_value = abbreviation_value(suffix_array[i][:substr_length], substr_count)

    best_val = substr_value
    best_len = lcp
    best_count = 2

    for j in range(i+1, len(lcp_array)):
        if lcp_array[j] == 0: break
        substr_length = min(substr_length, lcp_array[j])
        substr_count += 1
        substr_value = abbreviation_value(suffix_array[i][:substr_length], substr_count)

        if substr_value > best_val:
            best_val = substr_value
            best_len = substr_length
            best_count = substr_count


    print(best_len, best_val, best_count)
    if best_val > 0:
        print(" ".join([id_to_word[x] for x in suffix_array[i][:best_len]]))
