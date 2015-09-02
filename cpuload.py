import time
import Crypto
print(Crypto.__file__)
print(Crypto.__version__)
from Crypto.PublicKey import RSA
from Crypto import Random


while True:
	i = 0
	while i <= 4:
		random_generator = Random.new().read
		key = RSA.generate(4096, random_generator)
		print key
		i=i+1	
	
	time.sleep(120)


