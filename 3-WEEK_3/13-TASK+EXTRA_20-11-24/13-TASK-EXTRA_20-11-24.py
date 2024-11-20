from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

#caricare la chiave privata
def load_private_key(filepath):
    with open(filepath, 'rb') as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

#caricare la chiave pubblica
def load_public_key(filepath):
    with open(filepath, 'rb') as key_file:
        return serialization.load_pem_public_key(key_file.read())

#crittografa il messaggio e lo salva come file
def encrypt_message(public_key):
    message = input("Inserisci il messaggio da crittografare: ")
    encrypted = public_key.encrypt(
        message.encode(),
        padding.PKCS1v15()
    )
    filename = input("Inserisci il nome di outpt per salvare il messaggio crittografato: ") + ".enc"
    with open(filename, "wb") as file:
        file.write(base64.b64encode(encrypted))
    print(f"Messaggio crittografato salvato in: {filename}")

#decrittografa il messaggio dal file
def decrypt_message(private_key):
    filename = input("Inserisci il nome del file contenente il messaggio crittografato (senza estensione): ") + ".enc"
    try:
        with open(filename, "rb") as file:
            encrypted = base64.b64decode(file.read())
        decrypted = private_key.decrypt(
            encrypted,
            padding.PKCS1v15()
        )
        print("Messaggio decrittato:", decrypted.decode('utf-8'))
    except FileNotFoundError:
        print(f"Errore: Il file {filename} non esiste.")

#firma il messaggio e lo salva come file
def sign_message(private_key):
    message = input("Inserisci il messaggio da firmare: ")
    signed = private_key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    filename = input("Inserisci il nome di output per salvare la firma: ") + ".sig"
    with open(filename, "wb") as file:
        file.write(base64.b64encode(signed))
    print(f"Firma salvata in: {filename}")

#verifica la firma da testo imput e file di firma
def verify_signature(public_key):
    message = input("Inserisci il messaggio originale: ")
    filename = input("Inserisci il nome del file contenente la firma (senza estensione): ") + ".sig"
    try:
        with open(filename, "rb") as file:
            signature = base64.b64decode(file.read())
        try:
            public_key.verify(
                signature,
                message.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            print("La firma è valida.")
        except Exception as e:
            print("La firma NON è valida:", str(e))
    except FileNotFoundError:
        print(f"Errore: Il file {filename} non esiste.")

#procedure
if __name__ == "__main__":
    #carica le chiavi
    private_key = load_private_key('private_key.pem')
    public_key = load_public_key('public_key.pem')

    #operazioni possibili scritte a schermo
    while True:
        print("\nScegli un'operazione:")
        print("1. Crittografa il messaggio")
        print("2. Decrittografa il messaggio")
        print("3. Firma il messaggio")
        print("4. Verifica una firma")
        print("5. Esci")
        choice = input("Scegli l'operazione: ")

        if choice == '1':
            encrypt_message(public_key)
        elif choice == '2':
            decrypt_message(private_key)
        elif choice == '3':
            sign_message(private_key)
        elif choice == '4':
            verify_signature(public_key)
        elif choice == '5':
            print("Grazie! Program Shut Down.")
            break
        else:
            print("Scelta non valida! Riprova.")
