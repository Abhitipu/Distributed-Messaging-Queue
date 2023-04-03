import requests
import argparse

class ATMClient():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.id = None

    def login(self, account_id):
        url = f"http://{self.ip}:{self.port}/account/"
        try:
            response = requests.get(url,data = {"account_id": account_id})
            if response["status"] == "Success":
                self.id = account_id
                return "Success"
            else:
                return "Failure"
        except :
            return "Failure"        


    def deposit(self, amount):
        url = f"http://{self.ip}:{self.port}/account/deposit"
        response = requests.post(url, data={"amount": amount, "account_id": self.id})
        if response["status"] == "Success":
            return "Success"
        else:
            return "Failure"
        
    def withdraw(self, amount):
        url = f"http://{self.ip}:{self.port}/account/withdraw"
        response = requests.post(url, data={"amount": amount, "account_id": self.id})
        return response["status"]

    def transfer(self, to_account_id, amount):
        url = f"http://{self.ip}:{self.port}/account/transfer"
        response = requests.post(url, data={"to_account_id": to_account_id, "amount": amount, "account_id": self.id})
        if response["status"] == "Success":
            return "Success"
        else:
            return "Failure"
        

    def balance(self):
        url = f"http://{self.ip}:{self.port}/account/balance"
        response = requests.get(url, data={"account_id": self.id})
        if response["status"] == "Success": 
            return response["balance"]
        else:
            return "Failure"
    
    def create(self):
        url = f"http://{self.ip}:{self.port}/account/create"
        response = requests.post(url)
        if response["status"] == "Success":
            self.id = response["account_id"]
            return "Success", self.id
        else:
            return "Failure", -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port number",
                        type=int, default=5000)
    parser.add_argument("-ip", "--ip", help="ip address",
                        type=str, default="0.0.0.0")
    args = parser.parse_args()

    client = ATMClient(args.ip, args.port)
    # create an event loop to handle user input
    print("Welcome to the ATM!")
    print("Create an account or login")

    while True:
        print(">>> ", end="")
        command = input()
        if command == "create":
            response, account_id = client.create()
            if response == "Failure":
                print("Account creation failed")
            else:
                print(f"Account creation successful! Your account ID is {account_id}")
                break
        elif command == "login":
            print("account_id: ", end="")
            account_id = input()
            client.id = account_id
            response = client.login(account_id)
            if response == "Failure":
                print("Login failed")
            else:
                print("Login successful! Welcome to the ATM!")
                break
        else:
            print("Invalid command")
    
    print("Login successful! Welcome to the ATM!")

    while True:
        print(">>> ", end="")
        command = input()
        if command == "deposit":
            print("amount: ", end="")
            amount = input()
            response = client.deposit(amount)
            if response == "Success":
                print("Deposit successful")
            else:
                print("Deposit failed")
        elif command == "withdraw":
            print("amount: ", end="")
            amount = input()
            response = client.withdraw(amount)
            if response == "Success":
                print("Withdraw successful")
            else:
                print("Withdraw failed")
        elif command == "balance":
            response = client.balance()
            if response == "Failure":
                print("Balance failed")
            else:
                print(f"Balance: {response}")

        elif command == "transfer":
            print("to_account_id: ", end="")
            to_account_id = input()
            print("amount: ", end="")
            amount = input()
            response = client.transfer(to_account_id, amount)
            if response == "Success":
                print("Transfer successful")
            else:
                print("Transfer failed")

        elif command == "exit":
            break
        
        elif command == "help":
            print("Commands:")
            print("deposit")
            print("withdraw")
            print("balance")
            print("transfer")
            print("exit")

        else:
            print("Invalid command")

if __name__ == "__main__":
    main()


