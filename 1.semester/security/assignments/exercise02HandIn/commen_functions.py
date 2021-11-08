from Crypto import Signature
from Crypto import PublicKey
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Random import get_random_bytes


import socket


# NETWORK

def send_message(socket: socket, message: str):
    socket.send(bytes(message, "utf-8"))


def send_byte_message(socket: socket, message: bytes):
    socket.send(message)


def send_crypto_message(socket: socket, crypto_message: "CryptoMessage", session_key):
    ciphertext = symmetric_encrypt_message(session_key, crypto_message.message)
    signature = symmetric_encrypt_message(
        session_key, crypto_message.signature)

    socket.send(ciphertext)
    socket.send(signature)


def receive_crypto_message(socket, session_key):
    ciphertext = receive_byte_message(socket)
    signature = receive_byte_message(socket)

    message = symmetric_decrypt_message(session_key, ciphertext)
    signature = symmetric_decrypt_message(session_key, signature)

    return CryptoMessage(message, signature)


def receive_message(socket: socket) -> str:
    data: bytes = socket.recv(1024)
    message = data.decode("utf-8")
    print(f"message {message}")
    if message.lower() == "quit":
        raise Exception()
    else:
        return message


def receive_byte_message(socket: socket):
    data: bytes = socket.recv(1024)
    return data


# CRYPTO


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

class CryptoMessage:
    def __init__(self, ciphertext: bytes, signature: bytes) -> None:
        self.message = ciphertext
        self.signature = signature

    def verify_crypto_message(self, public_key):
        try:
            verify_message(public_key, self.signature, self.message)
        except:
            raise Exception("Could not verify message")




def create_crypto_message(message, private_key):
    signature = sign_message(private_key, message)
    return CryptoMessage(message, signature)


def create_commitment(message, commitment_key, private_key):
    message = symmetric_encrypt_message(commitment_key, message)
    return create_crypto_message(message, private_key)


def hash_message(message: bytes):
    hash_obj = SHA256.new()
    hash_obj.update(message)
    return hash_obj.digest()


def symmetric_encrypt_message(key, message):
    key = SHA256.new(key)

    # TODO: dont use static vector !!
    static_vector = b'x' * AES.block_size

    obj = AES.new(key.digest(), AES.MODE_CBC, static_vector)
    ciphertext = obj.encrypt(message)
    return ciphertext


def symmetric_decrypt_message(key, ciphertext):
    key = SHA256.new(key)

    # TODO: dont use static vector !!
    static_vector = b'x' * AES.block_size
    obj = AES.new(key.digest(), AES.MODE_CBC, static_vector)
    plaintext = obj.decrypt(ciphertext)

    return plaintext


def asymmetric_encrypt_message(public_key, message):
    rsa = PKCS1_OAEP.new(public_key)
    cipher = rsa.encrypt(message)
    return cipher


def asymmetric_decrypt_message(private_key, message):
    rsa = PKCS1_OAEP.new(private_key)
    plaintext = rsa.decrypt(message)
    return plaintext


def sign_message(private_key, message):
    h = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature


def verify_message(public_key, signature, message):
    h = SHA256.new(message)
    pkcs1_15.new(public_key).verify(h, signature)


def import_key_from_file(path):
    f = open(path, 'r')
    key = RSA.import_key(f.read())
    f.close()
    return key


def create_session_key():
    session_key = get_random_bytes(16)
    return session_key


def create_dice_bytes():
    dice_bytes = get_random_bytes(32)
    return dice_bytes


if __name__ == "__main__":
    # ciphertext = symmetric_encrypt_message("perlt", "hje med dig jeg hedder Nikolai")
    # plaintext = symmetric_decrypt_message("perlt", ciphertext)
    # print(plaintext)

    privatekey = RSA.generate(2048)
    publickey = privatekey.publickey()


    # f = open('alice_private_key.pem','wb')
    # f.write(privatekey.export_key('PEM'))
    # f.close()

    # f = open('alice_public_key.pem','wb')
    # f.write(publickey.export_key('PEM'))
    # f.close()


    # t = asymmetric_encrypt_message(publickey, "perlt")
    # print(asymmetric_decrypt_message(privatekey, t))

    # signature = sign_message(privatekey, "hej med dig")
    # print(verify_message(publickey, signature, "hej med dig"))

    session_key = create_session_key()

    commitment_key = create_session_key()
    commitment: CryptoMessage = create_commitment(b"hjem ed ig hvad lvaer du idag", commitment_key, privatekey)



    commitment.verify_crypto_message(publickey)