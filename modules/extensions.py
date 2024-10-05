from os.path import isfile

def f(path: str, *, root: str="web/", tokenizer: callable=lambda s: f"[[{s}]]", **replace) -> str:
	"""
	Checks if a file exists and if does returns its contents or else an empty string if not.
	"""

	fpath = root + path
	
	if not isfile(fpath): return ""
	
	data = ""
	with open(fpath, "r") as file:
		data = file.read()
		file.close()
	
	if not replace: return data

	for rkey in replace:
		data = data.replace(tokenizer(rkey), str(replace[rkey]))
	
	return data

def encrypt(data: str) -> str:
	"""
	Encrypts data
	"""

	cipher_num = "".join([str(ord(ch) * len(data) * i) for i, ch in enumerate(data)])
	cipher = ""

	if len(cipher_num) % 2 == 1: cipher_num += "0"

	buffer = ""
	for i, c in enumerate(cipher_num):
		if i % 2 == 1: buffer = c; continue
		cipher += chr((int(buffer + c) % 65) + 65)
	
	return cipher[::-2] + cipher[1::2]

