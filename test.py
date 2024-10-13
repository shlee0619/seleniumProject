import os
file = os.path.abspath('로빈쿡 메스.txt')
print(file)
f = open('로빈쿡 메스.txt'.'r')
s = f.read()
print(s)
f.close