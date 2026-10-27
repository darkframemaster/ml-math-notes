#!/usr/bin/env python2.7
#file write
file =open("data2.txt","w")
file.write("Sample file writing\n")
file.write("This is line 2\n")
file.close()
#if there is no such file in the object direcation.it will create one
text_lines=[
	"Chapter 3\n",
	"Sample text data file\n"
	"This is the third line of text\n"
	"The fourth line looks like this\n"
	"Edit the file with any text editor\n"]

file=open("data2.txt","w")
file.writelines(text_lines)
file.close()
#if file has same name the last file will replace the file before

#file read
#each open can be used once
try:
	file =open("try_except.py","r")
except:
	print("what the fuck")

char=file.read(10)#char is not a type name
print(char)
all_data=file.read()
print(all_data)
one_line=file.readline(20)
print(one_line)
all_data=file.readlines()
print(all_data)
#readlines return a list of string
print("Lines:",len(all_data))
for line in all_data:
	print(line.strip())
file.close()


#struct
import struct
file=open("binary.dat","wb")
for n in range(1000):
	data=struct.pack('i',n)
	file.write(data)
file.close()

file=open("binary.dat","rb")
all_data=file.read()
print(all_data)
file.close()

file=open("binary.dat","rb")
size=struct.calcsize("i")
bytes_read=file.read(size)
while bytes_read:
	value=struct.unpack("i",bytes_read)
	value=value[0]
	print(value)
	bytes_read=file.read(size)
file.close()
