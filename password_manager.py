from tkinter import CENTER, Tk, Label, Button, Entry, Frame, END, Toplevel
from tkinter import ttk
from db_operations import DbOperations
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sqlite3
from tkinter import *
import random
import string
import zxcvbn  

class root_window:
    def __init__(self, root, db):
        self.db = db
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("900x550+40+40")

        head_title = Label(self.root, text="Password Manager", width=40,
        bg="purple", font=("Nexa Heavy", 20), padx=10, pady=10).grid(columnspan=4, padx=105, pady=20)

        self.crud_frame = ttk.Frame(self.root)
        self.crud_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        self.search_entry = Entry(self.crud_frame, width=30, font=("Nexa Heavy", 12))
        self.search_entry.grid(row=self.row_no, column=self.col_no)
        self.col_no += 1
        Button(self.crud_frame, text="Search", bg="yellow", font=("Nexa Heavy", 12), width=20,
               command=self.search_records).grid(row=self.row_no, column=self.col_no, padx=5, pady=5)
        self.create_extra_buttons()  
        self.create_records_tree()

    def create_extra_buttons(self):
        self.row_no += 1
        self.col_no = 0
        Button(self.crud_frame, text="Generate Password", bg="cyan", fg='white', font=("Nexa Heavy", 12),
               padx=2, pady=1, width=20, command=self.generate_password).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)

        self.col_no += 1
        Button(self.crud_frame, text="Strength Analysis", bg="orange", fg='white', font=("Nexa Heavy", 12),
               padx=2, pady=1, width=20, command=self.strength_analysis).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)

    def create_records_tree(self):
        columns = ('ID', 'Website', 'Username', 'Password')
        self.records_tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.records_tree.heading('ID', text="ID")
        self.records_tree.heading('Website', text="Website Name")
        self.records_tree.heading('Username', text="Username")
        self.records_tree.heading('Password', text="Password")
        self.records_tree['displaycolumns'] = ('ID', 'Website', 'Username', 'Password')

        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item = self.records_tree.item(selected_item)
                print(item)

                record = item['values']
                print(record[0])
                de = self.db.decrypt(record[0])
                print(de)
                record[3] = de

                print(record)
                for entry_box, item in zip(self.entry_boxes, record):
                    entry_box.delete(0, END)
                    entry_box.insert(0, item)

        self.records_tree.bind('<<TreeviewSelect>>', item_selected)
        self.records_tree.grid()

    def create_entry_labels(self):
        self.col_no, self.row_no = 0, 0
        labels_info = ('ID', 'Website', 'Username', 'Password')
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg='grey', fg='white', font=
            ("Nexa Heavy", 12), padx=5, pady=2).grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no += 1

    def create_crud_buttons(self):
        self.row_no += 1
        self.col_no = 0
        buttons_info = (('Save', 'green', self.save_record), ('Update', 'blue',
                                                              self.update_record), ('Delete', 'red', self.delete_record),
                         ('Copy Password', 'violet', self.copy_password),
                         ('Show All Records', 'purple', self.show_records))
        for btn_info in buttons_info:
            if btn_info[0] == 'Show All Records':
                self.row_no += 1
                self.col_no = 0
            Button(self.crud_frame, text=btn_info[0], bg=btn_info[1],
                   fg='white', font=("Nexa Heavy", 12), padx=2, pady=1, width=20,
                   command=btn_info[2]).grid(row=self.row_no, column=self.col_no, padx=5, pady=10)
            self.col_no += 1

    def create_entry_boxes(self):
        self.row_no += 1
        self.entry_boxes = []
        self.col_no = 0
        for i in range(4):
            show = ""
            if i == 3:
                show = "*"
            entry_box = Entry(self.crud_frame, width=20, background="lightgrey", font=
            ("Nexa Heavy", 12), show=show)
            entry_box.grid(row=self.row_no, column=self.col_no, padx=20, pady=2)
            self.col_no += 1
            self.entry_boxes.append(entry_box)
            

    # CRUD functions
    
    SAVE_MESSAGE = "Successfully Saved"
    UPDATE_SAVE_TIME = 900 

    def save_record(self):
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()

        # Check if password meets the minimum requirements

        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        bytes_data = password.encode('utf-8')
        ciphertext, tag = cipher.encrypt_and_digest(bytes_data)
        nonce = cipher.nonce

        data = {'website': website, 'username': username, 'password': ciphertext, 'key': key, 'tag': tag, 'nonce': nonce}
        self.db.create_record(data)
        self.show_records()
        self.show_update_saved_message()
        
        
    SUCCESS_MESSAGE = "Successfully Updated"
    UPDATE_SUCCESS_TIME = 900 

    def update_record(self):
        ID = self.entry_boxes[0].get()
        website = self.entry_boxes[1].get()
        username = self.entry_boxes[2].get()
        password = self.entry_boxes[3].get()

        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        bytes_data = password.encode('utf-8')
        ciphertext, tag = cipher.encrypt_and_digest(bytes_data)
        nonce = cipher.nonce

        data = {'ID': ID, 'website': website, 'username': username, 'password': ciphertext, 'key': key, 'tag': tag,
                'nonce': nonce}
        self.db.update_record(data)
        self.show_records()
        self.show_update_success_message()
        

    def delete_record(self):
        ID = self.entry_boxes[0].get()
        self.db.delete_record(ID)
        self.show_records()

    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        records_list = self.db.show_records()

        for record in records_list:
            self.records_tree.insert('', END, values=(record[0], record[3], [record[4]], record[5]))
            
    def search_records(self):
        search_term = self.search_entry.get()
        records_list = self.db.search_records(search_term)

        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        for record in records_list:
            self.records_tree.insert('', END, values=(record[0], record[3], [record[4]], record[5]))

    def generate_password(self):
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digits = random.choice(string.digits)
        special_characters = random.choice(string.punctuation)
        remaining_length = 8  

        password_list = [uppercase, lowercase, digits, special_characters]
        for _ in range(remaining_length):
            password_list.append(random.choice(string.ascii_letters + string.digits + string.punctuation))

        random.shuffle(password_list)
        password = ''.join(password_list)
        self.entry_boxes[3].delete(0, END)
        self.entry_boxes[3].insert(0, password)

    def strength_analysis(self):
        password = self.entry_boxes[3].get()
        result = zxcvbn.zxcvbn(password)
        strength_10 = int(result['score']*2.5)
        feedback = result['feedback']['suggestions']

        title_box = f"Password Strength: {strength_10}/10"
        self.showmessage(title_box, '\n'.join(feedback))


    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.entry_boxes[3].get())
        message = "Password Copied"
        title = "Copy"
        if self.entry_boxes[3].get() == "":
            message = "Box is Empty"
            title = "Error"
        self.showmessage2(title, message)

    def check_password_requirements(self, password):
        if any(char.isupper() for char in password) and \
                len(password) >= 1:
            return True
        else:
            return False

    def showmessage(self, title_box: str = None, message: str = None):
        root = Toplevel(self.root)
        background = 'green'
        if title_box == "Error":
            background = "red"
        root.geometry('400x150+600+200')
        root.title(title_box)
        Label(root, text=title_box, background=background, font=("Nexa Heavy", 15),
            fg='white').pack(padx=4, pady=2)

        message_label = Label(root, text=message, font=("Nexa Heavy", 12), fg='black')
        message_label.pack(padx=4, pady=2)

        ok_button = Button(root, text="OK", font=("Nexa Heavy", 12), command=root.destroy)
        ok_button.pack(pady=10)

        root.mainloop()
    
    def showmessage2(self, title_box:str=None, message:str=None):
        TIME_TO_WAIT=900
        root= Toplevel(self.root)
        background='green'
        if title_box=="Error":
            background="red"
        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root,text=message,background=background,font=("Nexa Heavy",15),
        fg='white').pack(padx=4,pady=2)
        try:
            root.after(TIME_TO_WAIT,root.destroy)
        except Exception as e:
            print("Error occured",e)

    def show_update_success_message(self):
        success_window = Toplevel(self.root)
        success_window.geometry('300x80+600+200')
        success_window.title("Update Success")
        Label(success_window, text=self.SUCCESS_MESSAGE, background='green', font=("Nexa Heavy", 15),
              fg='white').pack(padx=4, pady=2)

        success_window.after(self.UPDATE_SUCCESS_TIME, success_window.destroy)

        success_window.mainloop()
        
    def show_update_saved_message(self):
        save_window = Toplevel(self.root)
        save_window.geometry('300x80+600+200')
        save_window.title("Save Success")
        Label(save_window, text=self.SAVE_MESSAGE, background='green', font=("Nexa Heavy", 15),
        fg='white').pack(padx=4, pady=2)

        save_window.after(self.UPDATE_SAVE_TIME, save_window.destroy)

        save_window.mainloop()
        
if __name__ == "__main__":
    db_class = DbOperations()
    db_class.create_table()

    root = Tk()
    root_class = root_window(root, db_class)
    root.mainloop()
