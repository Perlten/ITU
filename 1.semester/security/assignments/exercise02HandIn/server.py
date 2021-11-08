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

    for i in range(2):
        print (f"Round {i + 1}")
        print ("----------------------------------------")
        # send session key
        session_key = create_session_key()
        encrypted_session_key = asymmetric_encrypt_message(BOB_PUBLIC_KEY, session_key)
        send_byte_message(socket, encrypted_session_key)
        print("session key sent \n")

        # overall bob dice
        # bob commit
        bob_dice_commit = receive_crypto_message(socket, session_key)
        print("Revived the commit from bob \n")
        bob_dice_commit.verify_crypto_message(BOB_PUBLIC_KEY)
        print("bob commit verified \n")

        bob_dice_commit_key_hash = receive_crypto_message(socket, session_key)
        print("bob commit key hash received \n")
        bob_dice_commit_key_hash.verify_crypto_message(BOB_PUBLIC_KEY)
        print("bob commit key hash verified \n")
        bob_dice_commit_key_hash = bob_dice_commit_key_hash.message

        # alice commit
        alice_commit_key = create_session_key()
        alice_dice_bytes = create_dice_bytes()
        send_crypto_message(socket, create_commitment(alice_dice_bytes, alice_commit_key, ALICE_PRIVATE_KEY), session_key)  # sends commitment
        print("Send commit \n")

        send_crypto_message(socket, create_crypto_message(hash_message(alice_commit_key), ALICE_PRIVATE_KEY), session_key)  # sends hash of commit key
        print("Send hash of commit key\n")

        # revive bob commit key
        bob_dice_commit_key_crypto_messsage = receive_crypto_message(socket, session_key)
        print("received bobs commit key \n")
        bob_dice_commit_key_crypto_messsage.verify_crypto_message(BOB_PUBLIC_KEY)
        print("verified bobs commit key \n")
        bob_dice_commit_key = bob_dice_commit_key_crypto_messsage.message

        if hash_message(bob_dice_commit_key) != bob_dice_commit_key_hash:
            raise Exception("Bob did not send the correct key")

        # send alice commit key
        print("Send commit key to bob \n")
        send_crypto_message(socket, create_crypto_message(alice_commit_key, ALICE_PRIVATE_KEY), session_key)
        # send_crypto_message(socket, create_crypto_message(create_session_key(), ALICE_PRIVATE_KEY), session_key) # sends an incorrect key

        print("open bobs commit \n")
        bob_dice_bytes = symmetric_decrypt_message(bob_dice_commit_key, bob_dice_commit.message)

        print("xor Alice and Bob commits \n")
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
