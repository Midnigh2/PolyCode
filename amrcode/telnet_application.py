import tkinter as tk
import telnetlib

class TelnetClient:
    def __init__(self):
        self.host = None
        self.port = None
        self.tn = None

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.tn = telnetlib.Telnet(host, port)

    def disconnect(self):
        self.tn.close()

    def send_message(self, message):
        self.tn.write(message.encode('ascii'))

class TelnetApplication:
    def __init__(self, master):
        self.master = master
        self.telnet_client = TelnetClient()

        self.create_widgets()

    def create_widgets(self):
        self.host_label = tk.Label(self.master, text='Host')
        self.host_label.grid(row=0, column=0)

        self.host_entry = tk.Entry(self.master)
        self.host_entry.grid(row=0, column=1)

        self.port_label = tk.Label(self.master, text='Port')
        self.port_label.grid(row=1, column=0)

        self.port_entry = tk.Entry(self.master)
        self.port_entry.grid(row=1, column=1)

        self.connect_button = tk.Button(self.master, text='Connect', command=self.connect)
        self.connect_button.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S)

        self.disconnect_button = tk.Button(self.master, text='Disconnect', command=self.disconnect)
        self.disconnect_button.grid(row=0, column=3, rowspan=2, sticky=tk.N+tk.S)

        self.message_label = tk.Label(self.master, text='Message')
        self.message_label.grid(row=2, column=0)

        self.message_entry = tk.Entry(self.master)
        self.message_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W+tk.E)

        self.send_button = tk.Button(self.master, text='Send', command=self.send_message)
        self.send_button.grid(row=2, column=3, sticky=tk.W+tk.E)

        self.output_label = tk.Label(self.master, text='Output')
        self.output_label.grid(row=4, column=0, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

        self.output_text = tk.Text(self.master, width=4, height=15)
        self.output_text.grid(row=5, column=0, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)

    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        self.telnet_client.connect(host, port)
        self.output_text.insert(tk.END, f'Connected to {host}:{port}\n')

    def disconnect(self):
        self.telnet_client.disconnect()
        self.output_text.insert(tk.END, 'Disconnected\n')

    def send_message(self):
        message = self.message_entry.get()
        self.telnet_client.send_message(message + '\r\n')
        self.output_text.insert(tk.END, f'Sent message: {message}\n')

root = tk.Tk()
root.title("Telnet Application")
root.geometry("325x295+400+200")
app = TelnetApplication(root)
root.mainloop()