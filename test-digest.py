
'''

This program generates a digest using a key and a challange string. It then prints the digest as hexadecimal.
'''
import hmac
k = "banana"
c = "mac"
d=hmac.new(k.encode(),c.encode("utf-8"))
print(d.hexdigest())

exit()