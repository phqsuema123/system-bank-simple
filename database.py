import mysql.connector
from abc import ABCMeta, abstractmethod
import secrets

class ACC(metaclass=ABCMeta):
    @abstractmethod
    def createacc(self):
        pass

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def withdraw(self):
        pass

    @abstractmethod
    def deposit(self):
        pass

    @abstractmethod
    def displayBalance(self):
        pass

    @abstractmethod
    def transfer(self):
        pass

class SACC(ACC):
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="asdzxc123",
                database="bank2"
            )
            self.cursor = self.db.cursor()
            self.create_table()
        except mysql.connector.Error as err:
            print("Error connecting to MySQL:", err)

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS accounts (
                accid INT AUTO_INCREMENT,
                name VARCHAR(200),
                last_name VARCHAR(200),
                age INT,
                idcard VARCHAR(13),
                pinnumber INT,
                balance DECIMAL(10, 2),
                PRIMARY KEY (accid)
            )
        """
        self.cursor.execute(create_table_query)
        self.db.commit()

    def createacc(self, name, last_name, age, idcard, pinnumber, money):
        accid = secrets.randbelow(100000000)
        sql = "INSERT INTO accounts (name, last_name, age, idcard, pinnumber, balance, accid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, last_name, age, idcard, pinnumber, money, accid)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("Your account has been created successfully")
        print("your id account -->{}".format(accid))

    def check(self, accid, pinnumber):
        self.cursor.execute("SELECT * FROM accounts WHERE accid = %s AND pinnumber = %s", (accid, pinnumber))
        account = self.cursor.fetchone()
        if account:
            print("Check successful")
            return True
        else:
            print("Check failed: Incorrect account ID or PIN")
            return False

    def withdraw(self, accid, withdraw_amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE accid = %s", (accid,))
        balance = self.cursor.fetchone()[0]
        if withdraw_amount > balance:
            print("Insufficient balance")
        else:
            new_balance = balance - withdraw_amount
            self.cursor.execute("UPDATE accounts SET balance = %s WHERE accid = %s", (new_balance, accid))
            self.db.commit()
            print("Withdrawal successful")
            self.displayBalance(accid)

    def deposit(self, accid, deposit_amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE accid = %s", (accid,))
        balance = self.cursor.fetchone()[0]
        new_balance = balance + deposit_amount
        self.cursor.execute("UPDATE accounts SET balance = %s WHERE accid = %s", (new_balance, accid))
        self.db.commit()
        print("Deposit successful")
        self.displayBalance(accid)

    def displayBalance(self, accid):
        self.cursor.execute("SELECT balance FROM accounts WHERE accid = %s", (accid,))
        balance = self.cursor.fetchone()
        if balance:
            print("Available balance: {}".format(balance[0]))
        else:
            print("Account not found")

    def transfer(self, accid, receiver_accid, amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE accid = %s", (accid,))
        sender_balance = self.cursor.fetchone()[0]

        if amount > sender_balance:
            print("Insufficient balance for transfer")
            return

        sender_new_balance = sender_balance - amount
        self.cursor.execute("UPDATE accounts SET balance = %s WHERE accid = %s", (sender_new_balance, accid))

        self.cursor.execute("SELECT balance FROM accounts WHERE accid = %s", (receiver_accid,))
        receiver_balance = self.cursor.fetchone()[0]
        receiver_new_balance = receiver_balance + amount
        self.cursor.execute("UPDATE accounts SET balance = %s WHERE accid = %s", (receiver_new_balance, receiver_accid))
        self.cursor.execute("INSERT INTO transfers (sender_accid, receiver_accid, amount) VALUES (%s, %s, %s)",
                            (accid, receiver_accid, amount))

        self.db.commit()


           


    

saveacc = SACC()

while True:
    while True:
        try:
            print("Welcome to Mumu Bank")
            print("Press 1 to create your account")
            print("Press 2 to login to your account")
            print("Press 3 to exit")

            menu_options = [1, 2, 3]
            choose1 = int(input("--> "))

            if choose1 not in menu_options:
                print("Please press only numbers in the menu.")
            else:
                break
        except ValueError as e:
            print("Invalid input. Please enter a number.")

    if choose1 == 1:
        while True:
            try:
                name = input("Name: ")
                if name.isalpha() and len(name) <= 200:
                    break
                else:
                    print("Please enter a valid name containing only alphabets and up to 200 characters.")
            except ValueError:
                print("Invalid input. Please try again.")


        while True:
            try:
                last_name = input("Last Name: ")
                if last_name.isalpha() and len(last_name) <= 200:
                    break
                else:
                    print("please check your info")
            except ValueError:
                print("please check your info")

        while True:
            try:
                age = int(input("Age: "))
                if 1 <= age <= 200:
                    break
                else:
                    print("age is wrong")
            except ValueError:
                print("please check your info ")

        while True:
            try:
                idcard = input("ID Card: ")
                if idcard.isdigit() and len(idcard) == 13:
                    break
                else:
                    print("Please enter a 13-digit number.")
            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                pinnumber = int(input("Set your PIN (6 numbers): "))
                if str(pinnumber).isdigit() and len(str(pinnumber)) == 6:
                    break
                else:
                    print("Please enter a 6-digit number.")
            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                money = int(input("Initial deposit: "))
                break
            except ValueError:
                print("please check your info")
        saveacc.createacc(name, last_name, age, idcard, pinnumber, money)

    elif choose1 == 2:
        name = input("Enter name: ")
        accid = int(input("Enter account ID: "))
        pinnumber = int(input("Enter your PIN: "))
        auth = saveacc.check(accid, pinnumber)

        if auth:
            while True:
                try:
                    print("Press 1 to withdraw")
                    print("Press 2 to deposit")
                    print("Press 3 to display balance")
                    print("press 4 to transfer")
                    print("Press 5 to exit")
                    menu_options = [1, 2, 3, 4,5]
                    choose = int(input("--> "))

                    if choose not in menu_options:
                        print("Please press only numbers in the menu.")
                    else:
                        if choose == 1:
                            while True:
                                try:
                                    withdraw_amount = int(input("Enter withdrawal amount: "))
                                    saveacc.withdraw(accid, withdraw_amount)
                                    break
                                except ValueError:
                                    print("Invalid withdrawal amount. Please enter a valid number.")

                        elif choose == 2:
                            while True:
                                try:
                                    deposit_amount = int(input("Enter deposit amount: "))
                                    saveacc.deposit(accid, deposit_amount)
                                    break
                                except ValueError:
                                    print("Invalid deposit amount. Please enter a valid number.")
                        elif choose == 3:
                            saveacc.displayBalance(accid)

                        elif choose == 4:
                            while True:
                                try:
                                    receiver_accid = int(input("Enter receiver's account ID: "))
                                    amount = int(input("Enter transfer amount: "))
                                    saveacc.transfer(accid, receiver_accid, amount)
                                    break
                                except ValueError:
                                    print("Invalid input. Please enter valid account IDs and transfer amount.")


                        elif choose == 5:
                            break
                except ValueError:
                    print("Invalid input. Please enter a number.")

    elif choose1 == 3:
        break

