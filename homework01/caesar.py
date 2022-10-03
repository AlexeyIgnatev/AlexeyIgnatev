import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    low_range = range(ord('a'), ord('z') + 1)
    high_range = range(ord('A'), ord('Z') + 1)

    for i in plaintext:
        if ord(i) not in low_range and ord(i) not in high_range:
            ciphertext += i
            continue
        if ord(i) in low_range:
            index = (ord(i) - ord('a') + shift) % len(low_range)
            ciphertext += chr(ord('a') + index)
        elif ord(i) in high_range:
            index = (ord(i) - ord('A') + shift) % len(high_range)
            ciphertext += chr(ord('A') + index)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    return encrypt_caesar(ciphertext, ord('z') - ord('a') - shift + 1)


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
