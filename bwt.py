import copy
import functools
import random
import string
import time


ALPHABET = ["$"] + list(string.ascii_letters) + [" "]
ALPHABET_IDX = {c: i for i, c in enumerate(ALPHABET)}

def transform(string_bytes: list[int], orderings=None, verbose=0, verbose_letters=None) -> list[int]:
    if (verbose >= 1):
        if (verbose_letters is None):
            verbose_letters = ALPHABET
    
    bytes_matrix = []
    for i in range(len(string_bytes)):
        bytes_matrix.append(string_bytes[i:len(string_bytes)] + string_bytes[:i])
    
    if (verbose >= 2):
        bytes_matrix_unsorted = copy.deepcopy(bytes_matrix)

    sort_bytes_matrix(bytes_matrix, orderings=orderings)
    if (verbose >= 2):
        print("Unsorted                 Sorted")
        for bytes1, bytes2 in zip(bytes_matrix_unsorted, bytes_matrix):
            old_string = bytes_to_str(bytes1, verbose_letters, sep=' ')
            new_string = bytes_to_str(bytes2, verbose_letters, sep=' ')
            print(f"{old_string}        {new_string}")
    
    last_row_bytes = [bytes[-1] for bytes in bytes_matrix]
    original_row_idx = bytes_matrix.index(string_bytes)
    if (verbose >= 1):
        print(f"L = {bytes_to_str(last_row_bytes, ALPHABET)}, I = {original_row_idx}")
    
    return last_row_bytes
    
def sort_bytes_matrix(bytes_matrix: list[list[int]], orderings=None) -> list[list[int]]:
    if (orderings is None):
        # Ordering: epsilon = "", x = None, "aa" = "aa".
        # "aa": [0, 1, 2, ...]
        orderings = {"": list(range(len(ALPHABET)))}

    # Get orderings of each length, 1, 2, ... n - 1
    #print(orderings)

    # Sort according to 0 (epsilon="")
    ordering = orderings[""]
    ordering_idxs = {i: k for i, k in enumerate(ordering)}
    sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, ordering=orderings[""], ordering_idxs=ordering_idxs, start_idx=0)
    bytes_matrix.sort(key=functools.cmp_to_key(sop))

    # Sort according to 1, 2, ... n - 1
    if (len(orderings) > 1):
        for i in range(1, len(bytes_matrix[0])):
            orderings_keys = [key for key in orderings if key is not None and len(key) == i]
            
            for key in orderings_keys:
                ordering = orderings[key]
                ordering_idxs = {i: k for i, k in enumerate(ordering)}
                sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, ordering=orderings[key], ordering_idxs=ordering_idxs, start_idx=i)
                bytes_matrix.sort(key=functools.cmp_to_key(sop))

    # Sort according to n (x=None)
    if (None in orderings):
        ordering = orderings[None]
        ordering_idxs = {i: k for i, k in enumerate(ordering)}
        sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, ordering=orderings[None], ordering_idxs=ordering_idxs, start_idx=i + 1) # i or i + 1
        bytes_matrix.sort(key=functools.cmp_to_key(sop))



def sort_ordering(bytes1, bytes2, ordering: list[int], ordering_idxs: dict[int, int], start_idx=0) -> bool:
    if (bytes1[:start_idx] != bytes2[:start_idx]):
        return 0
    
    for a, b in list(zip(bytes1, bytes2))[start_idx:]:
        if (a != b):
            a_idx = ordering_idxs[a]
            b_idx = ordering_idxs[b]

            return a_idx - b_idx
    return 0


def str_to_bytes(s: str, letters: list[str]=None) -> list[int]:
    if (letters is None):
        letters = ALPHABET
    return [letters.index(c) for c in s]

def bytes_to_str(bytes: list[int], letters: list[str]=None, sep: str="") -> str:
    if (letters is None):
        letters = ALPHABET
    return sep.join(letters[b] for b in bytes)

def compute_runs_count(bytes: list[int]) -> int:
    runs_count = 0
    for i in range(len(bytes) - 1):
        if (bytes[i] != bytes[i + 1]):
            runs_count += 1
    return runs_count

def reverse():
    pass

if __name__ == "__main__":


    s = "mississippi$"
    bytes = str_to_bytes(s)
    bytes_t = transform(bytes, orderings=None, verbose=1)
    #s = "this string should be relatively easy to compress since there is probably a lot of repitions questionmark$"
    s = "this string is highly compressible highly compress string is high ly string which accepts the problem of compressibility$"
    bytes = str_to_bytes(s)
    bytes_t = transform(bytes, orderings=None, verbose=1)
    #print(compute_runs_count(str_to_bytes(s)))
    #s = "aaababababaaabaaaabaaaabbbbaabaaaababbbbbc"

    time_start = time.time()

    random.seed(2)

    i = 0
    idx_list = list(range(len(ALPHABET)))
    strs_possible = list(set(s))
    runs_count_min = 10e6
    while i < 100:
        orderings = {"": idx_list}
        for _ in range(100):
            key = ""
            while (random.choice([False, True, True])):
                key += random.choice(strs_possible)
            orderings[key] = random.sample(idx_list, len(idx_list))
        orderings[None] = random.sample(idx_list, len(idx_list))

        bytes_t = transform(bytes, orderings=orderings)
        runs_count = compute_runs_count(bytes_t)
        
        runs_count_min = min(runs_count_min, runs_count)

        i += 1

    print(f"time diff: {time.time() - time_start}, run_min: {runs_count_min}")

    """
    idx_list = list(range(len(ALPHABET)))
    strs_possible = list(set(s))
    runs_count_min = 10e6
    while random.choice([True for _ in range(100)] + [False]):
        orderings = {"": idx_list}
        for _ in range(50):
            key = ""
            while (random.choice([False, True, True])):
                key += random.choice(strs_possible)
            orderings[key] = random.sample(idx_list, len(idx_list))
        orderings[None] = random.sample(idx_list, len(idx_list))

        bytes_t = transform(bytes, orderings=orderings)
        runs_count = compute_runs_count(bytes_t)

        if (runs_count_min > runs_count):
            runs_count_min = runs_count
            print(orderings)
            print(bytes_to_str(bytes_t))
            print(f"Runs count: {runs_count}.")
            if (bytes_to_str(bytes_t) == "aaaaaabbc"):
                print("DONE")

    
    """