from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256, SHA3_256, SHA3_512, MD5, RIPEMD160
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import binascii
import json
import time

def encode_in_hex_with_padding(plaintext: str):
    # Zamieniamy tekst na bajty
    byte_data = plaintext.encode('utf-8')

    # Dodajemy padding PKCS7
    padded_data = pad(byte_data, 16)  # 16 bajtów to blok AES
    print("\nPaddingu: ", padded_data)

    # Kodujemy na hex
    hex_data = binascii.hexlify(padded_data).decode('utf-8')
    print("\nHex: ", hex_data)

    # Formatowanie: każda linia 16 bajtów
    formatted_hex = [hex_data[i:i + 32] for i in range(0,len(hex_data), 32)]

    # Wyświetlamy wynik
    for line in formatted_hex:
        print(line)


def compute_hashes(plaintext: str, showLogs: bool = True):
    # Przekształcamy tekst na bajty
    byte_data = plaintext.encode('utf-8')
    # Obliczamy skrót SHA-256
    sha256_hash = SHA256.new(byte_data).hexdigest()

    # Obliczamy skrót SHA3-256
    sha3_256_hash = SHA3_256.new(byte_data).hexdigest()

    # Obliczamy skrót MD5
    md5_hash = MD5.new(byte_data).hexdigest()

    # Zapisujemy skróty do jednego json
    package = {
        "message": plaintext,
        "hash1": sha256_hash,
        "hash2": md5_hash,
        "hash3": sha3_256_hash,
    }
    # Konwersja json do tablicy bajtów
    package_json = json.dumps(package).encode("utf-8")

    ripemd160_hash = RIPEMD160.new(package_json).hexdigest()


    if showLogs:
        # Wyświetlamy wyniki
        print("\nSkróty:")
        print(f"SHA-256: {sha256_hash}")
        print(f"SHA3-256: {sha3_256_hash}")
        print(f"MD5: {md5_hash}")
        print(f"RIPEMD160: {ripemd160_hash}")



# 1. Bezpieczne generowanie klucza
def generate_secure_key():
    return get_random_bytes(32)


# 2. Funkcja szyfrująca
def encrypt_aes(plaintext: str, password: str) -> str:
    key, iv = hashKeyIV(password)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'),
                                    AES.block_size))
    return ciphertext.hex()


# 3. Funkcja deszyfrująca
def decrypt_aes(hex_ciphertext: str, password: str) -> str:
    key, iv = hashKeyIV(password)
    ciphertext = bytes.fromhex(hex_ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

def hashKeyIV(password: str):
    hash_object = SHA3_512.new(password.encode('utf-8')).digest()
    key = hash_object[:32]
    iv = hash_object[32:48]

    return key, iv

def zad1():
    encode_in_hex_with_padding("Kryptologia 2026 - Sebastian Marcinowski gr. 2")
    start = time.perf_counter()
    for i in range(1000000):
        compute_hashes("Kryptologia 2026 - Sebastian Marcinowski gr. 2", False)
    end = time.perf_counter()
    print(f"Czas: {end - start:.6f} s")


def zad2():
    # key = generate_secure_key()
    password = "kryptologia2026"
    plaintext = "Kryptologia laboratorium 2026 - Sebastian Marcinowski gr. 2"

    # Szyfrowanie
    ciphertext = encrypt_aes(plaintext, password)
    print(f"Zaszyfrowane: {ciphertext}")

    # Deszyfrowanie
    decrypted = decrypt_aes(ciphertext, password)
    print(f"Odszyfrowane: {decrypted}")

    encode_in_hex_with_padding(plaintext)



# Demo szyforwania asymetrycznego
def zad3_szyfr_asym(message: str):
    # Generowanie klucza RSA
    key = RSA.generate(2048)

    # Eksport klucza publicznego i prywatnego
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    print("Klucz publiczny:")
    print(public_key.decode())

    print("\nKlucz prywatny:")
    print(private_key.decode())

    # Tworzenie obiektu szyfrującego z klucza publicznego
    public_key_obj = RSA.import_key(public_key)
    cipher_rsa_encrypt = PKCS1_OAEP.new(public_key_obj)

    # Wiadomość do zaszyfrowania
    message = message.encode("utf-8")

    # Szyfrowanie
    encrypted_message = cipher_rsa_encrypt.encrypt(message)

    print("\nZaszyfrowana wiadomość (hex):")
    print(encrypted_message.hex())
    # Tworzenie obiektu deszyfrującego z klucza prywatnego
    private_key_obj = RSA.import_key(private_key)
    cipher_rsa_decrypt = PKCS1_OAEP.new(private_key_obj)

    # Deszyfrowanie
    decrypted_message = cipher_rsa_decrypt.decrypt(encrypted_message)

    print("\nOdszyfrowana wiadomość:")
    print(decrypted_message.decode())


def zad3_podpis():
    # 1. Generowanie klucza RSA
    key = RSA.generate(2048)

    # 2. Eksport kluczy (opcjonalnie - można zapisać do pliku)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    print("Klucz publiczny:")
    print(public_key.decode())

    # 3. Wiadomość do podpisania
    message = "Sebastian Marcinowski gr. 2".encode("utf-8")

    # 4. Tworzenie skrótu wiadomości
    h = SHA256.new(message)

    # 5. Podpisywanie wiadomości kluczem prywatnym przy użyciu RSA PSS
    signer = pss.new(key)
    signature = signer.sign(h)

    print("\nPodpis (hex):")
    print(signature.hex())

    # 6. Weryfikacja podpisu kluczem publicznym
    public_key_obj = RSA.import_key(public_key)

    verifier = pss.new(public_key_obj)
    h = SHA256.new(message)

    try:
        verifier.verify(h, signature)
        print("\nPodpis jest poprawny!")
    except (ValueError, TypeError):
        print("\nPodpis nie jest poprawny!")


def zad3():
    klucz_alicji = RSA.generate(2048)
    pub_alicji = klucz_alicji.publickey()

    klucz_boba = RSA.generate(2048)
    pub_boba = klucz_boba.publickey()

    tresc = "Sebastian Marcinowski gr. 2".encode("utf-8")
    skrot = SHA256.new(tresc)

    podpisujacy = pss.new(klucz_alicji)
    sygnatura = podpisujacy.sign(skrot)

    klucz_sesji = get_random_bytes(32)
    wektor_iv = get_random_bytes(16)

    aes_szyfr = AES.new(klucz_sesji, AES.MODE_CBC, wektor_iv)
    paczka_danych = pad(tresc + sygnatura, AES.block_size)
    szyfrogram = aes_szyfr.encrypt(paczka_danych)

    rsa_bob = PKCS1_OAEP.new(pub_boba)
    zaszyfrowany_klucz = rsa_bob.encrypt(klucz_sesji + wektor_iv)

    rsa_deszyfr_bob = PKCS1_OAEP.new(klucz_boba)
    odszyfrowany_sekret = rsa_deszyfr_bob.decrypt(zaszyfrowany_klucz)

    wyodrebniony_klucz = odszyfrowany_sekret[:32]
    wyodrebnione_iv = odszyfrowany_sekret[32:]

    aes_deszyfr = AES.new(wyodrebniony_klucz, AES.MODE_CBC, wyodrebnione_iv)
    surowe_dane = unpad(aes_deszyfr.decrypt(szyfrogram), AES.block_size)

    wiadomosc_koncowa = surowe_dane[:-256]
    podpis_koncowy = surowe_dane[-256:]

    weryfikator = pss.new(pub_alicji)
    skrot_weryfikacja = SHA256.new(wiadomosc_koncowa)

    try:
        weryfikator.verify(skrot_weryfikacja, podpis_koncowy)
        print("\nPodpis jest poprawny!")
    except (ValueError, TypeError):
        print("\nPodpis nie jest poprawny!")

    print(wiadomosc_koncowa.decode())

zad3()