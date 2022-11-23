from flask import Flask, request
import africastalking
import pymongo
import os

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["transactiondb"]
mycol = mydb["transactions"]

app = Flask(__name__)
username = "sandbox" 
api_key = "7efba7847bef001e94f78b37bdf5b1aa1aca1c3ffa2111d1ed8769221ae9e152" 
africastalking.initialize(username, api_key)

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    global amount 
    global acc_number
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    
    if text == "":
        response = "CON Enter 1 to transfer money."
    elif text == "1":
        response = "CON Enter the account number you would like to transfer to."
        acc_number = text.split("*")[1]
    elif text == f"1*{acc_number}":
        response = "CON Enter the amount you would like to send"
        amount = text.split("*")[2]    
    elif text == f"1*{acc_number}*{amount}":
        response = "CON Select the bank\n"
        response += "1 ACCESS (DIAMOND)"
        response += "2 HERITAGE BANK"
        response += "3 JAIZ BANK"
        response += "4 KEYSTONE BANK"
    elif text == f"1*{acc_number}*{amount}*1":
        bank = "ACCESS (DIAMOND)"
        response = f"CON Enter 1 to confirm payment of NGN{amount} to {acc_number}, ACCESS (DIAMOND)"
    elif text == f"1*{acc_number}*{amount}*2":
        bank = "HERITAGE BANK"
        response = f"CON Enter 1 to confirm payment of NGN{amount} to {acc_number}, {bank}"
    elif text == f"1*{acc_number}*{amount}*3":
        bank = "JAIZ BANK"
        response = f"CON Enter 1 to confirm payment of NGN{amount} to {acc_number}, {bank}"
    elif text == f"1*{acc_number}*{amount}*4":
        bank = "KEYSTONE"
        response = f"CON Enter 1 to confirm payment of NGN{amount} to {acc_number}, {bank}"
    elif text == f"1*{acc_number}*{amount}*1*1":
        response = "END Transaction processing.... Developed by Franklyn Ukwueze."
        details = mycol.insert_one({"Account number":acc_number, "Amount":amount, "Bank":bank})
    elif text == f"1*{acc_number}*{amount}*2*1":
        response = "END Transaction processing.... Developed by Franklyn Ukwueze."
        details = mycol.insert_one({"Account number":acc_number, "Amount":amount, "Bank":bank})    
    elif text == f"1*{acc_number}*{amount}*3*1":
        response = "END Transaction processing.... Developed by Franklyn Ukwueze."
        details = mycol.insert_one({"Account number":acc_number, "Amount":amount, "Bank":bank})
    elif text == f"1*{acc_number}*{amount}*1*1":
        response = "END Transaction processing.... Developed by Franklyn Ukwueze."
        details = mycol.insert_one({"Account number":acc_number, "Amount":amount, "Bank":bank})
    else:
        response = "END Transaction failed."
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))            