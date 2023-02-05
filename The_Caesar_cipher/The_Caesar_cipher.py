"""
The Caesar cipher is an ancient encryption algorithm used by Julius Caesar. It 
encrypts letters by shifting them over by a 
certain number of places in the alphabet. We 
call the length of shift the key. For example, if the 
key is 3, then A becomes D, B becomes E, C becomes 
F, and so on. To decrypt the message, you must shift 
the encrypted letters in the opposite direction. This 
program lets the user encrypt and decrypt messages 
according to this algorithm.

When you run the code, the output will look like this:

Do you want to (e)ncrypt or (d)ecrypt?
> e
Please enter the key (0 to 25) to use.
> 4
Enter the message to encrypt.
> Meet me by the rose bushes tonight.
QIIX QI FC XLI VSWI FYWLIW XSRMKLX.


Do you want to (e)ncrypt or (d)ecrypt?
> d
Please enter the key (0 to 26) to use.
> 4
Enter the message to decrypt.
> QIIX QI FC XLI VSWI FYWLIW XSRMKLX.
MEET ME BY THE ROSE BUSHES TONIGHT.
"""
def main(key, index):
    task = ['encrypt', 'decrypt']

    # Handle exceptions for the key and message
    try:
        if key < 0 or key > 26:
            raise ValueError('Key must be between 0 and 26.')
        msg = input(f'Enter the message to {task[index]}.\n> ').upper()
        if not msg:
            raise ValueError('Message cannot be empty.')
    except ValueError as e:
        return e
    
    # Main code for encrypting or decrypting the message
    result = []
    for word in msg.split():
        new_word = ''
        for letter in word:
            new_letter = ord(letter) + key
            if index == 1:
                new_letter = ord(letter) - key
            if new_letter > ord('Z'):
                new_letter -= 26
            elif new_letter < ord('A'):
                new_letter += 26
            new_word += chr(new_letter)
        result.append(new_word)
    return ' '.join(result)

if __name__ == '__main__':
    # Keep prompting the user until they enter 'e' or 'd'
    while True:
        mode = input('Do you want to (e)ncrypt or (d)ecrypt?\n> ').lower()
        if mode in ['e', 'd']:
            break
        print('Please enter "e" or "d".')

    # Keep prompting the user until they enter a valid key
    while True:
        try:
            key = int(input('Please enter the key (0 to 26) to use.\n> '))
            if key >= 0 and key <= 26:
                break
        except ValueError:
            pass
        print('Key must be an integer between 0 and 26.')
   
    # Set the index based on the mode
    index = 0 if mode == 'e' else 1

    # Print the result
    print(main(key, index))
