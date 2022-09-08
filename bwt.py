import copy
import functools
import random


ALPHABET = ["a", "b", "c", "d", "e", "f", "g"]

def transform(string_bytes: list[int], orderings=None, verbose=0, verbose_letters=None) -> list[int]:
    if (verbose >= 1):
        if (verbose_letters is None):
            verbose_letters = ALPHABET
    
    bytes_matrix = []
    for i in range(len(string_bytes)):
        bytes_matrix.append(string_bytes[i:len(string_bytes)] + string_bytes[:i])
    
    if (verbose >= 1):
        bytes_matrix_unsorted = copy.deepcopy(bytes_matrix)

    bytes_matrix = sort_bytes_matrix(bytes_matrix, orderings=orderings)
    if (verbose >= 1):
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
    sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, ordering=orderings[""], start_idx=0)
    bytes_matrix.sort(key=functools.cmp_to_key(sop))

    # Sort according to 1, 2, ... n - 1
    if (len(orderings) > 1):
        for i in range(1, len(bytes_matrix[0])):
            orderings_keys = [key for key in orderings if key is not None and len(key) == i]
            
            for key in orderings_keys:
                sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, ordering=orderings[key], start_idx=i)
                bytes_matrix.sort(key=functools.cmp_to_key(sop))

    # Sort according to n (x=None)
    if (None in orderings):
        sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, ordering=orderings[None], start_idx=i)
        bytes_matrix.sort(key=functools.cmp_to_key(sop))

    return bytes_matrix


def sort_ordering(bytes1, bytes2, ordering: list[int], start_idx=0) -> bool:
    if (bytes1[:start_idx] != bytes2[:start_idx]):
        return 0
    result = 1
    for a, b in list(zip(bytes1, bytes2))[start_idx:]:
        if (ordering.index(a) < ordering.index(b)): # TODO: Skal der være <=?
            result = -1
        else:
            break
    return result


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
        if (bytes[i] > bytes[i + 1]):
            runs_count += 1
    return runs_count

def reverse():
    pass

if __name__ == "__main__":
    s = "aabaaabac"
    s = "aaababababaaabaaaabaaaabbbbaabaaaababbbbbc"
    bytes = str_to_bytes(s, ALPHABET)

    orderings = {"": [1, 0, 2], "a": [2, 0, 1], "aa": [1, 0, 2], "aaba": [0, 2, 1], None: [0, 1, 2]}
    bytes_t = transform(bytes, orderings=orderings)
    print(bytes_t)
    print(f"Runs count: {compute_runs_count(bytes_t)}.")

    runs_count_min = 10e6
    while True:
        orderings = {"": [0, 1, 2]}
        for _ in range(20):
            key = ""
            while (random.choice([False, True, True])):
                key += random.choice(["a", "b", "c"])
            orderings[key] = random.sample(list(range(3)), 3)

        orderings.update({None: [0, 1, 2]})
        bytes_t = transform(bytes, orderings=orderings)
        runs_count = compute_runs_count(bytes_t)

        if (runs_count_min > runs_count):
            runs_count_min = runs_count
            print(orderings)
            print(bytes_to_str(bytes_t))
            print(f"Runs count: {runs_count}.")
