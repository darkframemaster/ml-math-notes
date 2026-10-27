#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import subprocess


print('$ nslookup www.python.org')
r=subprocess.call(['nslookup','www.python.org'])
print('Exit code:',r)

print('\n'+'------------------------------')
p=subprocess.Popen(['nslookup'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

#communicate set param
output,err=p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:',p.returncode)
