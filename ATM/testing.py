import requests
from interface import ATMClient
from time import sleep
accounts = []
BASE_ADDRESS = "http://localhost:"
IP="localhost"
PORTS = ["8081", "8082", "8083", "8084"]
server_address = [BASE_ADDRESS + port for port in PORTS]
success = 0
def create_account():
    for send_url in server_address:
        send_url += "/create"
        try:
            r = requests.post(send_url)
            # print("sending beat")
            r.raise_for_status()
            response = r.json()
            if response["status"] == "Success":
                return response["account_id"]
            else:
                print("Response  : Failed to create account")
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
    return None

def deposit(atm_clients, amount):
    for cli in atm_clients:
        try:
            response = cli.deposit(amount)
            if response == "Success":
                return response
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
    return "Failure"

def withdraw(atm_clients, amount):
    for cli in atm_clients:
        try:
            response = cli.withdraw(amount)
            if response == "Success":
                return response
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
    return "Failure"

def transfer(atm_clients, to_account_id, amount):
    for cli in atm_clients:
        try:
            response = cli.transfer(to_account_id, amount)
            if response == "Success":
                return response
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
    return "Failure"

def balance(atm_clients):
    sleep(.5)
    for cli in atm_clients:
        try:
            response = cli.balance()
            if response != "Failure":
                return response
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
    return "Failure"
# init two accounts

account1 = create_account()
account2 = create_account()

if account1 is not None and account2 is not None:
    print("Test 1 Passed | successfully created accounts")
    success += 1
else:
    print("Test 1 Failed | Account creation failed")
    exit(0)

print("Account 1 : " + account1)
print("Account 2 : " + account2)

account1_clients = [ATMClient(IP, port) for port in PORTS]
for cli in account1_clients:
    cli.login(account1)

account2_clients = [ATMClient(IP, port) for port in PORTS]
for cli in account2_clients:
    cli.login(account2)

# deposit some cash
print("Depositing some cash (1500)")
deposit(account1_clients, 1500)

cur_balance = balance(account1_clients)
print("Balance : " + str(cur_balance))
try:
    assert 1500 == (int(cur_balance))
    success += 1
except Exception as e:
    print("Exception : " + str(e))
print("Shut down atm_three(press enter to continue)")
_ = input()

print("Attempting to withdraw cash (250) via atm_two")

# withdraw
withdraw(account1_clients[1:], 250)
sleep(1)
cur_balance = balance(account1_clients[1:])
print("Balance : " + str(cur_balance))
try:
    assert 1250 == (int(cur_balance))
    success += 1
except Exception as e:
    print("Exception : " + str(e))
print("First restart atm_three to let them sync\nThen shut down all atms(press enter to continue)")
_ = input()

# transfer

print("Attempting to transfer cash (60) from "+str(account1) + " to "+str(account2))

print("This should ideally fail and should not tranfer money")
# withdraw
transfer(account1_clients, account2, 60)
cur_balance = balance(account1_clients)
print("Balance : " + str(cur_balance))
try:
    assert "Failure" == cur_balance
    success += 1
except Exception as e:
    print("Exception : " + str(e))
cur_balance = balance(account2_clients)
print("Balance : " + str(cur_balance))
try:
    assert "Failure" == cur_balance
    success += 1
except Exception as e:
    print("Exception : " + str(e))

print("Restart all the atms(press enter to continue)")
_ = input()
cur_balance = balance(account1_clients)
print("Balance : " + str(cur_balance))
print(str(account1) + " balance : "+ str(cur_balance))

cur_balance = balance(account2_clients)
print("Balance : " + str(cur_balance))
print(account2 + " balance : "+ str(cur_balance))
print("Again attempting to transfer cash (60) from "+str(account1) + " to "+str(account2))

# withdraw
transfer(account1_clients, account2, 60)
cur_balance = balance(account1_clients)
print("Balance : " + str(cur_balance))
try:
    assert 1190 == (int(cur_balance))
    success += 1
except Exception as e:
    print("Exception : " + str(e))
cur_balance = balance(account2_clients)
print("Balance : " + str(cur_balance))
try:
    assert 60 == (int(cur_balance))
    success += 1
except Exception as e:
    print("Exception : " + str(e))
print("Test passed " + str(success) + " / 7")

# restart the corresponding server

