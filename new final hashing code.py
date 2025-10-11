import random

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

capital = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '!', '@', '#', '$', '%','^', '&', '*', '(', ')', '_', '+', '{', '}', ':', '"', '<', '>', '?', '|']
small = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '`', '-', '=', '[', ']', '/','.', ',', ';','0','1','2','3','4','5','6','7','8','9']

while True:
    input_text = input("Enter text to convert to binary: ")
    binary_representation = text_to_binary(input_text)

    hashed_representation = []
    for bit in binary_representation:
        if bit == '1':
            hashed_representation.append(random.choice(capital))
        else:
            hashed_representation.append(random.choice(small))
    hashed_text = ''.join(hashed_representation)
    print("Hashed text:")
    print(hashed_text)

    input_hash = input("Enter text to convert to binary: ")
    binary_recovered = ''.join('1' if char in capital else '0' for char in input_hash)
    reversed_text = binary_to_text(binary_recovered)
    print("Reversed text:")
    print(reversed_text)
