import sys
import time
from datetime import date
import matplotlib.pyplot as plt
sys.path.append('..')
from security import *
from utils import *

filename = "TimeCalculatedRSA_ENCandDEC.txt"
mode = "a+"  # "a+" mode opens the file for both reading and appending

DEBUG = True
LIST_KEYS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 
            130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 
            230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 
            330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 
            430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 
            530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 
            630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 
            730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 
            830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 
            930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1024]
PLAIN_TEXT = 'life is a journey and every step we take every decision we make shapes our destiny and defines who we are as individuals'

# this function return the time to break the cipher
def time_to_encrypt_decrypt_RSA(text, rsa1, rsa2):
    # encode the text
    encoded_text = encode_text(text)
    # start timer
    start_time = time.time()
    # get cipher
    cipher = rsa1.encrypt_text(encoded_text)
    # stop timer
    end_time = time.time()
    # calculate time taken
    time_enc = (end_time - start_time)
    # start timer
    start_time = time.time()
    # get cipher
    decrypted_mess = rsa2.decrypt_text(cipher)
    # stop timer
    end_time = time.time()
    # calculate time taken
    time_dec = (end_time - start_time)
    # get the decrypted mess
    mess = decode_text(decrypted_mess)
    # check that the encryption and decryption are correct
    if mess != text:
        print(mess) if DEBUG else None
        print(PLAIN_TEXT) if DEBUG else None
        return (-1, -1)

    return (time_enc, time_dec)

# this functio loops on the LIST_KEYS
def test_Key(key):
    rsa1 = RSA(key)
    rsa2 = RSA(key)
    rsa1.set_other_public_key(str(rsa2.public_key))
    rsa2.set_other_public_key(str(rsa1.public_key))
    time_enc, time_dec =time_to_encrypt_decrypt_RSA(PLAIN_TEXT, rsa1, rsa2)
    print("time_enc taken:", time_enc * 1000, "milliseconds") if DEBUG else None
    print("time_enctaken:", time_enc, "seconds") if DEBUG else None
    print("time_dec taken:", time_dec * 1000, "milliseconds") if DEBUG else None
    print("time_dec taken:", time_dec, "seconds") if DEBUG else None
    print('SUCCESS Encryption and Decryption' if (time_enc != -1 and time_dec != -1) else 'FAILED Encryption and Decryption') if DEBUG else None
    return (time_enc, time_dec)


ENC_TIMES_sec = []
DEC_TIMES_sec = []
ENC_TIMES_ms = []
DEC_TIMES_ms = []

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
        time_enc, time_dec = test_Key(key)
        if (time_enc == -1 and time_dec == -1):
            file.write("Time: " + "NA" + '\n')
            file.write("Status: " + "FAILED Encryption and Decryption" + '\n')
        else:
            time_enc_sec = time_enc
            time_enc_ms = time_enc * 1000
            time_dec_sec = time_dec
            time_dec_ms = time_dec * 1000
            ENC_TIMES_sec.append(time_enc_sec)
            DEC_TIMES_sec.append(time_dec_sec)
            ENC_TIMES_ms.append(time_enc_ms)
            DEC_TIMES_ms.append(time_dec_ms)
            file.write("Time Encryption: " + str(time_enc_sec) + " seconds" + '\n')
            file.write("Time Encryption: " + str(time_enc_ms) + " milliseconds" + '\n')
            file.write("Time Decryption: " + str(time_dec_sec) + " seconds" + '\n')
            file.write("Time Decryption: " + str(time_dec_ms) + " milliseconds" + '\n')
            file.write("Status: " + "SUCCESS CRACK" + '\n')
        file.write("-----------------------------------------------------------" + '\n')
        print(f'Key {key} finished')  if DEBUG else None

# plot time in sec
plt.plot(LIST_KEYS, ENC_TIMES_sec, label='Encryption')
plt.plot(LIST_KEYS, DEC_TIMES_sec, label='Decryption')
plt.xlabel('Key Size of (n) in Bits')
plt.ylabel('Time in Seconds')
plt.title('Analyze Different key sizes in seconds')
plt.legend()
plt.show()

# plot time in ms
plt.plot(LIST_KEYS, ENC_TIMES_ms, label='Encryption')
plt.plot(LIST_KEYS, DEC_TIMES_ms, label='Decryption')
plt.xlabel('Key Size of (n) in Bits')
plt.ylabel('Time in milliseconds')
plt.title('Analyze Different key sizes in millies')
plt.legend()
plt.show()