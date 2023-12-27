import sqlite3
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(6))
    return random_string




class DbOperations:
    def connect_to_db(self):
        conn=sqlite3.connect('password_records.db')
        return conn
    
    def create_table(self,table_name="password_info"):
        conn=self.connect_to_db()
        query=f'''
        CREATE TABLE IF NOT EXISTS {table_name}(
            ID VARCHAR(7) PRIMARY KEY NOT NULL ,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            website TEXT NOT NULL,
            username VARCHAR(200),
            password VARCHAR(50)
        );
        '''
        query2=f'''
        CREATE TABLE IF NOT EXISTS CIPHER(
            ID VARCHAR(7) PRIMARY KEY NOT NULL ,
            KEY VARCHAR(50),
            TAG VARCHAR(50),
            NONCE VARCHAR(50)
        );
        '''
        
        with conn as conn:
            cursor=conn.cursor()
            cursor.execute(query)
            cursor.execute(query2)
            
    def create_record(self,data,table_name="password_info"):
        website=data['website']
        username=data['username']
        password=data['password']
        key=data['key']
        tag=data['tag']
        nonce=data['nonce']
        random_string = generate_random_string()
        conn=self.connect_to_db()
        query=f'''
        INSERT INTO {table_name}('ID','website','username','password') VALUES
        ( ?,?,?,?);
        '''
        query2=f'''
        INSERT INTO CIPHER ('ID','key','tag','nonce') VALUES
        ( ?,?,?,?);
        '''
        with conn as conn:
            cursor=conn.cursor()
            cursor.execute(query,(random_string,website,username,password))
            cursor.execute(query2,(random_string,key,tag,nonce))
            
    def show_records(self,table_name="password_info"):
        conn=self.connect_to_db()
        query=f'''
        SELECT * FROM {table_name};
        '''
        with conn as conn:
            cursor=conn.cursor()
            list_records=cursor.execute(query)
            return list_records
        print(list_records)
    
    def update_record(self,data , table_name="password_info"):
        ID=data['ID']
        website=data['website']
        username=data['username']
        password=data['password']
        key=data['key']
        tag=data['tag']
        nonce=data['nonce']
        conn=self.connect_to_db()
        query=f'''
        UPDATE {table_name} SET website=?, username=?,
        password=? WHERE ID=?;
        '''
        query2=f'''
        UPDATE CIPHER SET key=?, tag=?,
        nonce=? WHERE ID=?;
        '''
        with conn as conn:
            cursor=conn.cursor()
            cursor.execute(query,(website,username,password,ID))
            cursor.execute(query2,(key,tag,nonce,ID))
    
    def delete_record(self,ID , table_name="password_info"):
        conn=self.connect_to_db()
        query=f'''
        DELETE FROM {table_name} WHERE ID=?;
        '''
        with conn as conn:
            cursor=conn.cursor()
            cursor.execute(query,(ID,))
    def decrypt(self,id):
        connection = self.connect_to_db()
        cursor = connection.cursor()

        query = f"""
        SELECT cipher.*, password_info.password
        FROM cipher
        INNER JOIN password_info ON cipher.id = password_info.id
        WHERE cipher.id = ?
        """
        cursor.execute(query, (id,))
        results = cursor.fetchall()
        for row in results:
            cipher = AES.new(row[1], AES.MODE_EAX, row[3])
            data = cipher.decrypt_and_verify(row[4], row[2])
            data2=data.decode('utf-8')
            return data2
    def search_records(self, search_term, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name}
        WHERE website LIKE ? OR username LIKE ? OR password LIKE ?;
        '''
        with conn as conn:
            cursor = conn.cursor()
            list_records = cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            return list_records
            
        