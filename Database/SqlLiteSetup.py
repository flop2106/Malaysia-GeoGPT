from sqlalchemy import text, create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

DATABASE_URL = 'sqlite:///finance_tracking.db'
engine = create_engine(DATABASE_URL)
#Base = declarative_base(engine)
def execute_sql(statement):
    with engine.connect() as connection:
        result = connection.execute(text(statement))
        if 'select' in statement.lower():
            result = result.fetchall()

        #connection.commit()
    return result
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.set_password()

    @staticmethod
    def initialize_table():
        '''
        with engine.connect() as connection:
            connection.execute(text("""
                                    CREATE TABLE IF NOT EXISTS users (
                                   user_id INTEGER PRIMARY KEY,
                                   username TEXT UNIQUE NOT NULL,
                                   password_hash TEXT NOT NULL
                                   );
                              """))
        '''
        init_table_statement = """
                                CREATE TABLE IF NOT EXISTS users (
                               user_id INTEGER PRIMARY KEY,
                               username TEXT UNIQUE NOT NULL,
                               password_hash TEXT NOT NULL
                               );
                          """
        execute_sql(init_table_statement)

    def set_password(self):
        self.password_hash = generate_password_hash(self.password)

    def check_password(self, password_db):
        return check_password_hash(password_db, self.password)

    def check_userid(self, signup = False):
        check_user_statement = f"""
                                 SELECT
                                     *
                                 FROM
                                     users
                                WHERE
                                    username LIKE '{self.username}'
                                 """

        count_user = execute_sql(check_user_statement)
        #count_user = count_user.fetchall()
        if count_user: #To check password
            rows = count_user[0]
            user_id = rows[0]
            user_username = rows[1]
            self.password_db = rows[2]
            if signup == False:
                if self.check_password(self.password_db): #check if the password is right
                    return user_id
                else:
                    print('Wrong Password')
                    return False
            if signup == True:
                print('Username exsits! Change Username')
                return False
        else:
            #Create password
            self.set_password()
            self.insert_user()
            return True
            

    def insert_user(self):
        check_max_id_statement = '''
            SELECT
                MAX(user_id)
            FROM
                users
            LIMIT 1
            '''
        #max_id = execute_sql(check_max_id_statement).fetchall()[0][0]
        max_id = execute_sql(check_max_id_statement)[0][0]
        self.max_id = max_id
        if str(max_id) == "None":
            max_id = 0
        print(max_id)
        insert_statement = f"""
            INSERT INTO users (user_id, username, password_hash)
            VALUES ({max_id+1}, '{self.username}', '{self.password_hash}');
        """
        execute_sql(insert_statement)
        print(f"User {self.username} Added!")


class Item:
    @staticmethod
    def initialize_table():

        init_table_statement = """
                               CREATE TABLE IF NOT EXISTS items (
                                   item_id INTEGER PRIMARY KEY,
                                   category TEXT,
                                   item TEXT,
                                   price FLOAT,
                                   user_id INTEGER,
                                   input_date DATE DEFAULT CURRENT_DATE,
                                   FOREIGN KEY (user_id) REFERENCES users(user_id)
                                   );
                               """
        execute_sql(init_table_statement)
    @staticmethod
    def adding_item(user_id, category, item, price):
        insert_item_statement = f"""
        INSERT INTO items (user_id, category, item, price)
        VALUES ({user_id},'{category}','{item}',{price})
        """
        execute_sql(insert_item_statement)
        print(f'Item {item} inserted!')
    @staticmethod
    def delete_item(item_id):
        delete_item_statement = f"""
        DELETE FROM items WHERE item_id = {item_id}
        """
        execute_sql(delete_item_statement)
        print(f'Item {item_id} Deleted')
    @staticmethod
    def showing_item(user_id, date_from, date_to):
        show_item_statement = f"""
        SELECT
            *
        FROM
            items
        WHERE
                user_id = {user_id}
            AND
                (input_date BETWEEN '{date_from.date()}' AND '{date_to.date()}');

        """
        result = pd.read_sql(show_item_statement, con = engine)

        return result

if __name__ == '__main__':
    User.initialize_table()
    Item.initialize_table()