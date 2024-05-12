import random
import math

def primefiller():
    """
    Fills a set with prime numbers up to 250 using 
    the Sieve of Eratosthenes method.
    
    Returns:
        set: A set containing prime numbers from 2 to 249.
    """
    prime = set()
    sieve = [True] * 250
    sieve[0] = False
    sieve[1] = False
    for i in range(2, 250):
        for j in range(i * 2, 250, i):
            sieve[j] = False

    for i, is_prime in enumerate(sieve):
        if is_prime:
            prime.add(i)
    return prime


def pickrandomprime(prime):
    """
    Picks a random prime number from a set of primes 
    and removes it from the set.
    
    Args:
        prime (set): A set of prime numbers.
        
    Returns:
        int: A randomly selected prime number from the set.
    """
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)
    ret = next(it)
    prime.remove(ret)
    return ret


def setkeys(prime_list):
    """
    Generates public and private keys for the RSA algorithm 
    using a list of prime numbers.
    
    Args:
        prime_list (set): A set of prime numbers.
        
    Returns:
        tuple: A tuple containing the public key, private key, and modulus `n`.
    """
    prime1 = pickrandomprime(prime_list)
    prime2 = pickrandomprime(prime_list)

    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)

    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1

    public_key = e

    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1

    private_key = d

    return public_key, private_key, n


def encrypt(message, pub_k, num):
    """
    Encrypts a given message using the public key and modulus `n` (num).
    
    Args:
        message (int): The message to be encrypted, represented as an integer.
        pub_k (int): The public key (exponent `e`).
        num (int): The modulus (`n`).
        
    Returns:
        int: The encrypted message as an integer.
    """
    e = pub_k
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= num
        e -= 1
    return encrypted_text


def decrypt(encrypted_text, pri_k, num):
    """
    Decrypts a given encrypted message using the private key 
    and modulus `n`.
    
    Args:
        encrypted_text (int): The encrypted message as an integer.
        pri_k (int): The private key (exponent `d`).
        num (int): The modulus (`n`).
        
    Returns:
        int: The decrypted message as an integer.
    """
    d = pri_k
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= num
        d -= 1
    return decrypted


def encoder(message, pub_key, n):
    """
    Encodes a message by converting each character to its 
    ASCII value and encrypting it using the public key.
    
    Args:
        message (str): The message to be encoded.
        pub_key (int): The public key.
        n (int): The modulus (`n`).
        
    Returns:
        list: A list of encrypted ASCII values representing the encoded message.
    """
    return [encrypt(ord(letter), pub_key, n) for letter in message]


def decoder(encoded, pri_key, n):
    """
    Decodes a list of encrypted ASCII values by decrypting them using 
    the private key and converting them back to characters.
    
    Args:
        encoded (list): A list of encrypted ASCII values.
        pri_key (int): The private key.
        n (int): The modulus (`n`).
        
    Returns:
        str: The decoded message as a string.
    """
    s = ''
    for num in encoded:
        s += chr(decrypt(num, pri_key, n))
    return s

def read_message(filename):
    with open(filename, 'r', encoding = 'utf-8') as message_file:
        return message_file.read()

def write_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

if __name__ == '__main__':
    primes = primefiller()
    public_key, private_key, n = setkeys(primes)
    MESSAGE = read_message("kateryna.txt")
    coded = encoder(MESSAGE, public_key, n)
    encoded_message = ''.join(str(p) for p in coded)

    write_to_file(encoded_message, "encoded_message.txt")

    decoded_message = decoder(coded, private_key, n)
    write_to_file(decoded_message, "decoded_message.txt")

    # print("Initial message:")
    # print(MESSAGE)
    # print("\n\nThe encoded message (encrypted by public key)\n")
    # print(encoded_message)
    # print("\n\nThe decoded message (decrypted by private key)\n")
    # print(decoded_message)

