from Crypto.Util.number import getPrime, inverse

def file_read(filename):
    try:
        with open(filename, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

def generate_primes():
    p = getPrime(2048)
    g = getPrime(512)
    return p, g

def generate_keys():
    p, g = generate_primes()
    x = getPrime(256)
    y = pow(g, x, p)
    return (p, g, y), x

def encrypt(message, public_key):
    print(public_key)
    p, g, y = public_key
    k = getPrime(512)
    c1 = pow(g, k, p)
    encrypted_parts = []
    if message is None:
        print("The message is None.")
        return
    for i in range(0, len(message), 128):  # Розбиваємо повідомлення на частини по 128 символів
        part = message[i:i+128]
        bytes_data = part.encode('utf-8')
        c2 = (int.from_bytes(bytes_data, byteorder='big') * pow(y, k, p)) % p
        encrypted_parts.append((c1, c2))
    return encrypted_parts

def decrypt(ciphertexts, private_key, public_key):
    p, g, y = public_key
    x = private_key
    decrypted_parts = []
    for ciphertext in ciphertexts:
        c1, c2 = ciphertext
        s = pow(c1, x, p)
        m = (c2 * inverse(s, p)) % p
        bytes_data = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big')
        try:
            decrypted_parts.append(bytes_data.decode('utf-8'))
        except UnicodeDecodeError:
            print("Cannot decode the message. The encrypted message may have been tampered with.")
            return None
    return ''.join(decrypted_parts)

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    print(private_key)
    # print(private_key)
    # message = "Hello"
    # ciphertexts = encrypt(message, public_key)
    # print("Encrypted:", ciphertexts)
    # decrypted_message = decrypt(ciphertexts, private_key, public_key)
    # print("Decrypted:", decrypted_message)
