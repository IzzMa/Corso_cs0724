#decriptare il cifrario di Cesare
def cesare_decrypt(ciphertext, shift):
    alphabet = "ABCDEFGHILMNOPQRSTUVWXYZ"
    decrypted = ""
    for char in ciphertext:
        if char in alphabet:
            index = (alphabet.index(char) - shift) % len(alphabet)
            decrypted += alphabet[index]
        else:
            decrypted += char  #caratteri non alfabetici
    return decrypted

#messaggio cifrato e tentativi con tutte le chiavi possibili
ciphertext = "HSNFRGH"
decryptions = {shift: cesare_decrypt(ciphertext, shift) for shift in range(1, 26)}

#stampa i risultati
for shift, decryption in decryptions.items():
    print(f"Shift {shift}: {decryption}")
