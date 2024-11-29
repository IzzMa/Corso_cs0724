import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import csv
from datetime import datetime
from queue import Queue
from tkinter import messagebox
import logging
import ipaddress
from scapy.all import sniff, ARP, DNS, IP, TCP, UDP, Raw

ALLOWED_IPS = ["192.168.1.1", "127.0.0.1"]
ALLOWED_PORTS = [80, 443]

logging.basicConfig(
    filename="sniffer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.master.title("Login")
        self.on_success = on_success

        self.username_label = ttk.Label(master, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(master)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(master, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(master, text="Login", command=self.authenticate)
        self.login_button.pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "securepassword":
            self.master.destroy()
            self.on_success()
        else:
            messagebox.showerror("Errore", "Credenziali non valide.")


class PacketSnifferApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Packet Sniffer")
        self.master.geometry("800x600")

        self.sniffing = False
        self.captured_packets = []

        self.create_widgets()

    def create_widgets(self):
        self.config_frame = ttk.LabelFrame(self.master, text="Configurazione")
        self.config_frame.pack(fill="x", padx=10, pady=5)

        self.ip_label = ttk.Label(self.config_frame, text="Indirizzo IP (0.0.0.0 per tutta la rete):")
        self.ip_label.pack(side="left", padx=5)

        self.ip_entry = ttk.Entry(self.config_frame, width=15)
        self.ip_entry.insert(0, "0.0.0.0")
        self.ip_entry.pack(side="left", padx=5)

        self.port_label = ttk.Label(self.config_frame, text="Porta (singola o range, es. 80 o 80-90):")
        self.port_label.pack(side="left", padx=5)

        self.port_entry = ttk.Entry(self.config_frame, width=20)
        self.port_entry.insert(0, "80")
        self.port_entry.pack(side="left", padx=5)

        self.start_button = ttk.Button(self.config_frame, text="Start", command=self.start_sniffing)
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(self.config_frame, text="Stop", command=self.stop_sniffing, state="disabled")
        self.stop_button.pack(side="left", padx=5)

        self.output_frame = ttk.LabelFrame(self.master, text="Output")
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.output_text = scrolledtext.ScrolledText(self.output_frame, state="disabled", width=80, height=20)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.export_button = ttk.Button(self.master, text="Esporta in CSV", command=self.export_to_csv, state="disabled")
        self.export_button.pack(pady=5)

    def log(self, message):
        self.master.after(0, self._log_message, message)

    def _log_message(self, message):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.config(state="disabled")
        self.output_text.yview(tk.END)
        logging.info(message)

    def is_allowed(self, ip, port):
        return ip in ALLOWED_IPS and port in ALLOWED_PORTS

    def start_sniffing(self):
        ip = self.ip_entry.get()
        port_input = self.port_entry.get()

        # Gestione delle porte (singola o range)
        try:
            if '-' in port_input:
                start_port, end_port = map(int, port_input.split('-'))
                ports = list(range(start_port, end_port + 1))
            else:
                ports = [int(port_input)]
        except ValueError:
            self.log("Errore: la porta deve essere un numero intero o un range.")
            return

        self.sniffing = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.export_button.config(state="disabled")

        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
        self.captured_packets = []

        self.log("Avvio dello sniffer...")
        threading.Thread(target=self.sniff_packets, args=(ip, ports), daemon=True).start()

    def stop_sniffing(self):
        self.sniffing = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.export_button.config(state="normal")
        self.log("Sniffer fermato.")

    def sniff_packets(self, ip, ports):
        def packet_callback(pkt):
            if self.sniffing:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if pkt.haslayer(ARP):
                    self.handle_arp(pkt, timestamp)
                elif pkt.haslayer(DNS):
                    self.handle_dns(pkt, timestamp)
                elif pkt.haslayer(TCP):
                    self.handle_tcp(pkt, timestamp, ports)
                elif pkt.haslayer(UDP):
                    self.handle_udp(pkt, timestamp)
                elif pkt.haslayer(Raw):
                    self.handle_raw(pkt, timestamp)

        if ip == "0.0.0.0":
            sniff(prn=packet_callback, filter="ip", store=0)
        else:
            sniff(prn=packet_callback, filter=f"ip host {ip}", store=0)

    def handle_arp(self, pkt, timestamp):
        packet_info = {
            "timestamp": timestamp,
            "source": pkt[ARP].psrc,
            "port": None,  # ARP non ha porte
            "data": None
        }
        self.captured_packets.append(packet_info)
        self.log(f"[ARP] {timestamp} Da {pkt[ARP].psrc} a {pkt[ARP].pdst}")

    def handle_dns(self, pkt, timestamp):
        if pkt.haslayer(DNS):
            packet_info = {
                "timestamp": timestamp,
                "source": pkt[IP].src,
                "port": None,  # DNS non ha porte
                "data": pkt[DNS].qd.qname.decode()
            }
            self.captured_packets.append(packet_info)
            self.log(f"[DNS] {timestamp} Query: {pkt[DNS].qd.qname.decode()}")

    def handle_tcp(self, pkt, timestamp, ports):
        if pkt.haslayer(TCP):
            if pkt[TCP].dport in ports or pkt[TCP].sport in ports:
                packet_info = {
                    "timestamp": timestamp,
                    "source": f"{pkt[IP].src}:{pkt[TCP].sport}",
                    "port": pkt[TCP].sport,
                    "data": pkt[TCP].payload.hex()
                }
                self.captured_packets.append(packet_info)
                self.log(f"[TCP] {timestamp} Da {pkt[IP].src}:{pkt[TCP].sport} a {pkt[IP].dst}:{pkt[TCP].dport} - Dati: {pkt[TCP].payload}")

    def handle_udp(self, pkt, timestamp):
        if pkt.haslayer(UDP):
            packet_info = {
                "timestamp": timestamp,
                "source": f"{pkt[IP].src}:{pkt[UDP].sport}",
                "port": pkt[UDP].sport,
                "data": None
            }
            self.captured_packets.append(packet_info)
            self.log(f"[UDP] {timestamp} Da {pkt[IP].src}:{pkt[UDP].sport} a {pkt[IP].dst}:{pkt[UDP].dport}")

    def handle_raw(self, pkt, timestamp):
        packet_info = {
            "timestamp": timestamp,
            "source": pkt[IP].src,
            "port": None,
            "data": pkt[Raw].load.hex()
        }
        self.captured_packets.append(packet_info)
        self.log(f"[Raw] {timestamp} Dati: {pkt[Raw].load.hex()}")

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ["timestamp", "source", "port", "data"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for packet in self.captured_packets:
                        writer.writerow(packet)
                self.log(f"Esportazione in CSV completata: {filename}")
            except Exception as e:
                self.log(f"Errore nell'esportazione del CSV: {e}")


def on_login_success():
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()


if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root, on_success=on_login_success)
    login_root.mainloop()
