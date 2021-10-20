import socket
from commen_functions import *
import json


HOST = 'localhost'
PORT = 42424

ALICE_PRIVATE_KEY = import_key_from_file("keys/alice_private_key.pem")
ALICE_PUBLIC_KEY = import_key_from_file("keys/alice_public_key.pem")

BOB_PUBLIC_KEY = import_key_from_file("keys/bob_public_key.pem")


def start_server():
    s = socket.socket()
    s.bind((HOST, PORT))

    s.listen(1)
    c, addr = s.accept()
    try:
        play_game(c)
    except Exception as e:
        print(e)
        s.close()


def play_game(socket):

    dies = []

    for _ in range(2):
    # send session key
        session_key = create_session_key()
        encrypted_session_key = asymmetric_encrypt_message(BOB_PUBLIC_KEY, session_key)
        send_byte_message(socket, encrypted_session_key)
        print("session key sent")

        # overall bob dice
        # bob commit
        bob_dice_commit = receive_crypto_message(socket, session_key)
        bob_dice_commit.verify_crypto_message(BOB_PUBLIC_KEY)

        # alice commit
        alice_commit_key = create_session_key()
        alice_dice_bytes = create_dice_bytes()
        send_crypto_message(socket, create_commitment(alice_dice_bytes, alice_commit_key, ALICE_PRIVATE_KEY), session_key)

        # revive bob commit key
        bob_dice_commit_key_crypto_messsage = receive_crypto_message(socket, session_key)
        bob_dice_commit_key_crypto_messsage.verify_crypto_message(BOB_PUBLIC_KEY)
        bob_dice_commit_key = bob_dice_commit_key_crypto_messsage.message

        # send alice commit key
        send_crypto_message(socket, create_crypto_message(alice_commit_key, ALICE_PRIVATE_KEY), session_key)

        bob_dice_bytes = symmetric_decrypt_message(bob_dice_commit_key, bob_dice_commit.message)
        
        die = byte_xor(bob_dice_bytes, alice_dice_bytes) 
        die = (int.from_bytes(die, "big", signed=False) % 6) + 1
        
        dies.append(die)

    print(f"Alice die {dies[0]} Bob die {dies[1]}")

    if dies[0] > dies[1]:
        print("Alice wins")
    elif dies[1] > dies[0]:
        print("Bob wins")
    else:
        print("Tie")

    return 1


if __name__ == "__main__":
    start_server()
