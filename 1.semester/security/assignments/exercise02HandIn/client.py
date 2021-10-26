import socket
from commen_functions import *

HOST = 'localhost'
PORT = 42424

BOB_PRIVATE_KEY = import_key_from_file("keys/bob_private_key.pem")
BOB_PUBLIC_KEY = import_key_from_file("keys/bob_public_key.pem")

ALICE_PUBLIC_KEY = import_key_from_file("keys/alice_public_key.pem")


def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    try:
        play_game(s)
    except Exception as e:
        print(e)
        s.close()


def play_game(socket):
    dies = []
    for _ in range(2):
        # session key exchange
        encrypted_session_key = receive_byte_message(socket)
        session_key = asymmetric_decrypt_message(BOB_PRIVATE_KEY, encrypted_session_key)
        print("session key revived")

        # overall bob dice
        # bob commit
        bob_commit_key = create_session_key()
        bob_dice_bytes = create_dice_bytes()
        send_crypto_message(socket, create_commitment(bob_dice_bytes, bob_commit_key, BOB_PRIVATE_KEY), session_key) # sends commit

        send_crypto_message(socket, create_crypto_message(hash_message(bob_commit_key), BOB_PRIVATE_KEY), session_key)  # sends hash of commit key

        # alice commit
        alice_dice_commit = receive_crypto_message(socket, session_key)
        alice_dice_commit.verify_crypto_message(ALICE_PUBLIC_KEY)

        alice_dice_commit_key_hash = receive_crypto_message(socket, session_key)
        alice_dice_commit_key_hash.verify_crypto_message(ALICE_PUBLIC_KEY)
        alice_dice_commit_key_hash = alice_dice_commit_key_hash.message

        # send bob commit key
        send_crypto_message(socket, create_crypto_message(bob_commit_key, BOB_PRIVATE_KEY), session_key)
        # send_crypto_message(socket, create_crypto_message(create_session_key(), BOB_PRIVATE_KEY), session_key)

        # revive alice commit key
        alice_dice_commit_key_crypto_messsage = receive_crypto_message(socket, session_key)
        alice_dice_commit_key_crypto_messsage.verify_crypto_message(ALICE_PUBLIC_KEY)
        alice_dice_commit_key = alice_dice_commit_key_crypto_messsage.message

        if alice_dice_commit_key_hash != hash_message(alice_dice_commit_key):
            raise Exception("not the correct commit key sent from alice")

        alice_dice_bytes = symmetric_decrypt_message(alice_dice_commit_key, alice_dice_commit.message)

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


if __name__ == '__main__':
    main()
