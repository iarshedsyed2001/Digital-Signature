# Embedding a digital signature in images to prove ownership in case of piracy

import cv2
SIGNATURE_LENGTH = 100

# This function takes the number say 104 and by using bitwise operator on that number, it returns list containing three elements of length 3,3,2 (which contains only boolean values).
# 104 ---> [‭011,010,00‬]
def getBits(n):
	return [n >> 5, (n & 28)>>2, n & 3]

# This function takes list containing three elements, containing boolean values only of length 3,3,2 and by using bitwise operator we return a number which is combination of all boolean values.
# [‭011,010,00‬] ---> 104
def getByte(bits):
	return (((bits[0]<<3) | bits[1])<<2) | bits[2]

# This function takes the signature and normalize it to the length of SIGNATURE_LENGTH (100 in this case) by putting '*' at the end places if the length of the sign is less than SIGNATURE_LENGTH
def normalize_signature(x):
	return x[:SIGNATURE_LENGTH].ljust(SIGNATURE_LENGTH,'*')

# This function returns the lit of dimensions of points(x,y) where you want to embed the message
def getEmbeddingPoints():
	return [(4, x*2) for x in range(SIGNATURE_LENGTH)]

# This function takes three arguments -result image, source image and signature- respectively and adds digital signature
def embed(srcImage, sign):
	image = cv2.imread(srcImage, cv2.IMREAD_COLOR)
	if image is None:
		print(srcImage, 'not found')
		return

	normalized = normalize_signature(sign)
	embedAt = getEmbeddingPoints()        # embedAt will store the pair of values of the points where message is being embedded.
	cnt = 0
	for x, y in embedAt:             	  # since embedAt has pair of values so x will take first value from the pair and y will take the second value
		data = ord(normalized[cnt])       # ord gives the ASCII of the character
		bits = getBits(data)
		image[x][y][2] = (image[x][y][2] & ~7) | bits[0] # red band
		image[x][y][1] = (image[x][y][1] & ~7) | bits[1] # green band
		image[x][y][0] = (image[x][y][0] & ~3) | bits[2] # blue band
		cnt+=1

	# save back
	resultImage = 'ResultImg.png'
	cv2.imwrite(resultImage, image)

def extract(resultImage):
	image = cv2.imread(resultImage, cv2.IMREAD_COLOR)
	if image is None:
		print(resultImage, 'not found')
		return

	extractFrom = getEmbeddingPoints()

	cnt = 0
	sign = ''
	for x, y in extractFrom:
		bit1 = (image[x][y][2] & 7) # red band
		bit2 = (image[x][y][1] & 7) # green band
		bit3 = (image[x][y][0] & 3) # blue band
		data = getByte([bit1,bit2,bit3])
		sign = sign+ chr(data)     # chr converts ASCII to text
		cnt+=1

	return sign.strip('*') 		   # removes the padding and returns the signature

embed('D:\Python\Digital Signature\srcImg.png', 'This image belongs to Iarshed')
signature = extract('D:\Python\Digital Signature\ResultImg.png')
print(signature)