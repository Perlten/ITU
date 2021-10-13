from random import randint


def main():
    send_message(2000)


g = 666
p = 6661


def send_message(plainText):
    # 1 alice sending a message to bob
    alice_sk = randint(0, p - 1)
    bob_sk = randint(0, p - 1)

    alice_g = cp(g, alice_sk)
    bob_g = cp(g, bob_sk)

    alice_shared_key = cp(alice_g, bob_sk)

    cipher_text = alice_shared_key * plainText

    bob_shared_key = cp(bob_g, alice_sk)
    decryptedMessage = cipher_text / bob_shared_key

    print(decryptedMessage)

    # 2 eve brute forceing bob secret key and reading the message
    eve_bruteforce_sk = None

    for i in range(p):
        if bob_g == cp(g, i):
            eve_bruteforce_sk = i
    not_so_secret_key_anymore = cp(alice_g, eve_bruteforce_sk)
    hacked_message = cipher_text / not_so_secret_key_anymore
    print(hacked_message)

    # 3 we can now no longer brute force out way to a key however we can still change the cipher_text without it
    new_cipher_text = cipher_text * 3
    corupted_decrypted_message = new_cipher_text / bob_shared_key
    print(corupted_decrypted_message)



def cp(x, tp):
    return pow(x, tp) % p


if __name__ == "__main__":
    main()
