import sys
import time
from datetime import date
import matplotlib.pyplot as plt
sys.path.append('..')
from methods import *
from security import *
from utils import *
DEBUG = True
BUILT_IN = True
# File name and mode
filename = ''
mode = "a+"  # "a+" mode opens the file for both reading and appending

LIST_KEYS = []
PLAIN_TEXT = 'life is a journey and every step we take every decision we make shapes our destiny and defines who we are as individuals'

BUILT_IN_choice = input('Choose to use built in or not (1 for yes) (0 for no) any thing else to exit : ')
if BUILT_IN_choice == '1':
    BUILT_IN = True
    LIST_KEYS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 
            130, 140, 150, 160, 170, 180]
    filename = "TimeCalculatedRSA_Builtin.txt"
elif BUILT_IN_choice == '0':
    BUILT_IN = False
    LIST_KEYS = [30, 40, 50]
    filename = "TimeCalculatedRSA_MyFunction.txt"
else:
    print('EXIT')
    exit()



# Encrypt Word
def encrypt_word(word, e, n):
    return pow(word, e, n)

# Decrypt Word
def decrypt_word(word, d, n):
    return pow(word, d, n)

# Encrypt Text
def encrypt_text(text, e, n):
    encrypted_text = []
    for word in text:
        encrypted_text.append(encrypt_word(word, e, n))
    return (encrypted_text)
# Decrypt Text
def decrypt_text(text, d, n):
    decrypted_text = []
    for word in text:
        decrypted_text.append(decrypt_word(word, d, n))
    return (decrypted_text)

# this code gets the private key for breaking of RSA algo by prime factorization
def attack_RSA(public_key):
    e, n = public_key
    # factorize n
    factors = prime_factors_builtin(n) if BUILT_IN else prime_factors(n)
    # get d
    phi = (factors[0] - 1) * (factors[1] - 1)
    d = pow(e, -1, phi)
    return (d, n)

# this function return the time to break the cipher
def time_to_break_RSA(cipher, public_key):

    # start timer
    start_time = time.time()
    # get private key
    private_key = attack_RSA(public_key)
    # get the decrypted mess
    dec_mess = decrypt_text(cipher, private_key[0], private_key[1])
    # get the message
    mess = decode_text(dec_mess)
    # check the attack status
    if mess != PLAIN_TEXT:
        print(mess) if DEBUG else None
        print(PLAIN_TEXT) if DEBUG else None
        return -1
    # stop timer
    end_time = time.time()
    # calculate time taken
    time_taken = (end_time - start_time)

    return time_taken
    

# this functio loops on the LIST_KEYS
def test_Key(key):
    rsa1 = RSA(key)
    rsa2 = RSA(key)
    rsa1.set_other_public_key(str(rsa2.public_key))
    rsa2.set_other_public_key(str(rsa1.public_key))
    cipher = rsa1.encrypt_text(encode_text(PLAIN_TEXT))
    time_taken = time_to_break_RSA(cipher, rsa2.public_key)
    print("Time taken:", time_taken * 1000, "milliseconds") if DEBUG else None
    print("Time taken:", time_taken, "seconds") if DEBUG else None
    print('SUCCESS CRACK' if time_taken != -1 else 'FAILED CRACK') if DEBUG else None
    return time_taken

TIME_sec = []
TIME_ms = []

# Open the file in append mode, creating it if it doesn't exist
with open(filename, mode) as file:
    
    # Write the current date to the file
    file.write("Date: " + str(date.today()) + '\n')
    # for loop in keys
    for key in LIST_KEYS:
        print("Key: " + str(key) + '\n')  if DEBUG else None
        # Write the current key to the file
        file.write("Key: " + str(key) + '\n')
        # Write the current time to the file
        time_to_break = test_Key(key)
        if time_to_break == -1:
            file.write("Time: " + "NA" + '\n')
            file.write("Status: " + "FAILED CRACK" + '\n')
        else:
            time_sec = time_to_break
            time_ms = time_to_break * 1000
            TIME_sec.append(time_sec)
            TIME_ms.append(time_ms)
            file.write("Time: " + str(time_sec) + " seconds" + '\n')
            file.write("Time: " + str(time_ms) + " milliseconds" + '\n')
            file.write("Status: " + "SUCCESS CRACK" + '\n')
        file.write("-----------------------------------------------------------" + '\n')
        print(f'Key {key} finished')  if DEBUG else None



# plot time in sec
plt.plot(LIST_KEYS, TIME_sec, label='CRACK TIME')
plt.xlabel('Key Size of (n) in Bits')
plt.ylabel('Time in Seconds')
plt.title('Analyze CRACK of Different key sizes in seconds')
plt.legend()
plt.show()

# plot time in ms
plt.plot(LIST_KEYS, TIME_ms, label='CRACK TIME')
plt.xlabel('Key Size of (n) in Bits')
plt.ylabel('Time in milliseconds')
plt.title('Analyze CRACK of Different key sizes in milliseconds')
plt.legend()
plt.show()

