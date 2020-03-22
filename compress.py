import sys
import re

with open(sys.argv[1], 'r') as f:
    lines = [line for line in f]

# sanitize input
text = "".join(lines)
text = re.sub(r"\s+"," ",text)
text = text.lower()

# construct word dictionary lookups
word_to_id = {}
id_to_word = {}

text_words = text.split()
TOP_IDX = 0
END_TOKEN = 0xFFFFFFFF

for word in text_words:
    if not word in word_to_id:
        word_to_id[word] = TOP_IDX
        id_to_word[TOP_IDX] = word
        TOP_IDX += 1

# represent text as a list of word ids
text_ids = [word_to_id[word] for word in text_words] + [END_TOKEN]

while True:

    # Construct suffix array:
    # ordering of suffix starting indices by lexicographical order of suffixes
    suffix_array = sorted(range(len(text_ids)), key=lambda i : text_ids[i:])

    def lcp(s1, s2):
        """Compute the longest common prefix between suffixes s1 and s2."""
        l = 0
        i = 0
        while i < len(s1) and i < len(s2):
            if s1[i] == s2[i]:
                l += 1
            else: 
                break
            i += 1
        return l

    # length of longest common prefix of consecutive entries in the suffix array
    lcp_array = [lcp(text_ids[suffix_array[i]:], text_ids[suffix_array[i+1]:]) for i in range(len(suffix_array) - 1)] + [0]

    def abbreviation_value(substring, occurrences):
        """Characters saved by introducing an abbreviation for the substring."""
        n = len(substring)
        m = sum(len(id_to_word[i]) for i in substring)
        chars_before = (m + n - 1) * occurrences
        chars_after = (m + n - 1) + 2 + n * (occurrences)
        return chars_before - chars_after

    # enumerate substrings and number of occurrences from lcp and suffix arrays
    max_replacement_val = 0
    max_replacement_len = None
    max_replacement_loc = None
    max_replacemant_count = 0

    def sa_substring(suffix_rank, substr_len):
        global text_ids, suffix_array
        suffix_begin = suffix_array[suffix_rank]
        return text_ids[suffix_begin:suffix_begin + substr_len]

    for i, lcp in enumerate(lcp_array[:-1]):
        if lcp == 1: continue

        substr_length = lcp
        substr_count = 2
        substr_value = abbreviation_value(sa_substring(i, substr_length), substr_count)

        best_val = substr_value
        best_len = substr_length
        best_count = substr_count

        for j in range(i+1, len(lcp_array)):
            # no common prefix with i'th suffix?
            if lcp_array[j] == 0: break

            substr_length = min(substr_length, lcp_array[j])

            if substr_length == 1: break

            substr_count += 1
            substr_value = abbreviation_value(sa_substring(i, substr_length), substr_count)

            if substr_value > best_val:
                best_val = substr_value
                best_len = substr_length
                best_count = substr_count

        if best_val > max_replacement_val:
            max_replacement_val = best_val
            max_replacement_loc = i
            max_replacement_len = best_len
            max_replacemant_count = best_count

    if max_replacement_val <= 0: break

    print("Stats: len %d at %d x%d (score: %d)" % 
        (max_replacement_len, max_replacement_loc, max_replacemant_count, max_replacement_val))
    print("<=", " ".join([id_to_word[x] for x in sa_substring(max_replacement_loc, max_replacement_len)]))

    abbrev_substring = sa_substring(max_replacement_loc, max_replacement_len)
    abbrev_words = [id_to_word[x] for x in sa_substring(max_replacement_loc, max_replacement_len)]
    abbreviation = "".join([word[0] for word in abbrev_words]).upper()
    abbrev_intro = "("+abbreviation+")"

    word_to_id[abbreviation] = TOP_IDX
    id_to_word[TOP_IDX] = abbreviation
    TOP_IDX += 1

    word_to_id[abbrev_intro] = TOP_IDX
    id_to_word[TOP_IDX] = abbrev_intro
    TOP_IDX += 1

    print("=>", abbreviation)

    first = True
    i = 0
    while i < len(text_ids) - len(abbrev_substring):
        if text_ids[i:i+len(abbrev_substring)] == abbrev_substring:
            if first:
                first = False
                text_ids.insert(i+len(abbrev_substring), word_to_id[abbrev_intro])
            else:
                text_ids[i:i+len(abbrev_substring)] = [word_to_id[abbreviation]]
        i += 1

print(" ".join(id_to_word[i] for i in text_ids[:-1]))
