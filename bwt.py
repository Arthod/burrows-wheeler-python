import copy
import functools


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
        # Ordering: epsilon = False, x = True, "aa" = "aa".
        # "aa": [0, 1, 2, ...]
        orderings = {True: [i for i in range(len(ALPHABET))]}

    print(orderings)
    matrix_subordering_idxs = []

    # Sort according to 0 (epsilon=False)
    sop = lambda bytes1, bytes2: sort_ordering(bytes1, bytes2, orderings[True])
    bytes_matrix.sort(key=functools.cmp_to_key(sop))

    # Sort according to 1, 2, ... n - 1
    for i in range(1, len(bytes_matrix[0])):
        pass

    # Sort according to n (x=True)

    return bytes_matrix


def sort_ordering(bytes1, bytes2, ordering: list[int]) -> bool:
    for a, b in zip(bytes1, bytes2):
        if (ordering.index(a) > ordering.index(b)):
            return -1
    return 1


def str_to_bytes(s: str, letters) -> list[int]:
    return [letters.index(c) for c in s]

def bytes_to_str(bytes: list[int], letters, sep="") -> str:
    return sep.join(letters[b] for b in bytes)

def reverse():
    pass

if __name__ == "__main__":
    s = "aabaaabac"
    bytes = str_to_bytes(s, ALPHABET)

    orderings = {True: [1, 0, 2]}
    bytes_t = transform(bytes, orderings=orderings, verbose=1)
    print(bytes_t)