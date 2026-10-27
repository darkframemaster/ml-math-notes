#!/usr/bin/env python
import crypt
import hashlib

def testPass(cryptPass, crypt_in = None):
	'''
	dictionary.txt stores words which has passibility to be the passwd
	'''
	salt = cryptPass[0:2]
	dictFile = open('dictionary.txt', 'r')
	for word in dictField.readlines():
		word = word.strip('\n')
		if not crypt_in:
			cryptWord = crypt.crypt(word, salt)
		if crypt_in == 'sha_512':
			cryptWord = hashlib.sha512(word)
			
		if cryptWord == cryptPass:
			print "[+] Found Password: " + word + "\n"
			return
	print "[-] Password Not Found.\n"
	return


def main():
	'''
	passwords.txt is the file stores passwd's hash code, ex:
		/etc/shadow
	'''
	passFile = open('passwords.txt')
	for line in passFile.readlines():
		if ":" in line:
			user = line.split(':')[0]
			cryptPass = line.split(':')[1].strip(' ')
			print "[*] Cracking Password Fpr: " + user
			testPass(cryptPass)


if __name__ == '__main__':
	main()
