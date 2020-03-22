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
    maximal_replacement_val = 0
    maximal_replacement_len = None
    maximal_replacement_loc = None
    maximal_replacemant_count = 0

    def sa_substring(suffix_rank, substr_len):
        global text_ids, suffix_array
        suffix_begin = suffix_array[suffix_rank]
        return text_ids[suffix_begin:suffix_begin + substr_len]

    for i, lcp in enumerate(lcp_array[:-1]):
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

            substr_count += 1
            substr_value = abbreviation_value(sa_substring(i, substr_length), substr_count)

            if substr_value > best_val:
                best_val = substr_value
                best_len = substr_length
                best_count = substr_count

        
        #if best_val > 0:
        print("Len:",best_len, "Val:",best_val, "Count:",best_count)
        print(" ".join([id_to_word[x] for x in sa_substring(i, best_len)]))

        if best_val > maximal_replacement_val:
            maximal_replacement_val = best_val
            maximal_replacement_loc = i
            maximal_replacement_len = best_len
            maximal_replacemant_count = best_count

    if maximal_replacement_val <= 0: break

    print("best")
    print(maximal_replacement_val, maximal_replacement_loc, maximal_replacement_len, maximal_replacemant_count)
    print(" ".join([id_to_word[x] for x in sa_substring(maximal_replacement_loc, maximal_replacement_len)]))

    abbrev_substring = sa_substring(maximal_replacement_loc, maximal_replacement_len)
    abbrev_words = [id_to_word[x] for x in sa_substring(maximal_replacement_loc, maximal_replacement_len)]
    abbreviation = "".join([word[0] for word in abbrev_words]).upper()

    word_to_id[abbreviation] = TOP_IDX
    id_to_word[TOP_IDX] = abbreviation
    TOP_IDX += 1

    print(abbreviation)


    break




