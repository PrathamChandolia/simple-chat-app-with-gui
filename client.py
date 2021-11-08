import socket
import threading
import tkinter
from tkinter.constants import DISABLED
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.name = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.recieve)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chat")
        self.win.resizable(width=False, height=False)
        self.win.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = tkinter.Label(self.win, bg=BG_COLOR, fg=TEXT_COLOR,text="Welcome!", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = tkinter.Label(self.win, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.text_area = tkinter.Text(self.win, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,font=FONT, padx=5, pady=5)
        self.text_area.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_area.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = tkinter.Scrollbar(self.text_area)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_area.yview)

        # bottom label
        bottom_label = tkinter.Label(self.win, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = tkinter.Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self.write)

        self.input_area = tkinter.Text(self.msg_entry)
        self.input_area.place(relwidth=0.98, relheight=0.93, rely=0.008, relx=0.011)

        # send button
        self.send_button = tkinter.Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=self.write)
        self.send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.name}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def recieve(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.name.encode('utf-8'))
                else:
                    if self.gui_done:
                            self.text_area.config(state='normal')
                            self.text_area.insert('end', message)
                            self.text_area.yview('end')
                            self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client = Client(HOST,PORT)
