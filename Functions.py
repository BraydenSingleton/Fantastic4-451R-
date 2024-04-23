import mysql.connector
import bcrypt
from Login import *
import streamlit as st
from datetime import date

# To Do
# Disable Login option upon successful login
# When logging out, reset function to original state -> login()
# add drop bar to home page
# in function add connection to sql and add functions to check inputs for login
# recreate tables in sql database to match inputs of front end

salt = bcrypt.gensalt()

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='B@tman15',
    port='3306',
    database='bank_data'
)

mycursor = connection.cursor()
mycursor.execute("SELECT * FROM user_info")
users = mycursor.fetchall()


def change_password(password, email):
    userBytes = password.encode('utf-8')
    mycursor = connection.cursor()
    query = ("UPDATE user_info SET pword=%s WHERE email=%s;")
    record = (bcrypt.hashpw(userBytes,salt),email)
    mycursor.execute(query,record)
    connection.commit()
    st.write(":green[Password has successfully changed]")
    

def check_security_questions(a1,a2,a3):
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM user_info")
    users = mycursor.fetchall()

    for i in range(len(users)):
        if users[i][4] == a1:
            if users[i][5] == a2:
                if users[i][6] == a3:
                    return True
                
    return False


def check_login(uName, pword):
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM user_info")
    users = mycursor.fetchall()

    userBytes = pword.encode('utf-8')

    for i in range(len(users)):
        if users[i][2] == uName:
            if bcrypt.checkpw(userBytes, users[i][3].encode('utf-8')) == True:

                return users[i][0], users[i][1]
            else:
                return '0'

        elif i == len(users) - 1 and users[i][2] != uName:
            return '1'

def check_repeat(email):
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM user_info")
    users = mycursor.fetchall()

    for i in range(len(users)):
        if users[i][2] == email:
            return False
        elif i == len(users) - 1 and users[i][2] != email:
            return True

def add_to_database(first, last, email, password, a1, a2, a3):
    bytes = password.encode('utf-8')
    mycursor = connection.cursor()
    query = ("INSERT INTO user_info (fName, lName, email, pword, a1, a2, a3)"
             "VALUES(%s, %s, %s, %s, %s, %s, %s)")
    record = (first, last, email, bcrypt.hashpw(bytes,salt), a1, a2, a3)
    mycursor.execute(query, record)
    connection.commit()

def addTransaction(email, cat, amount):
    mycursor = connection.cursor()
    query = ("INSERT INTO user_transactions(email, category, amount, date)"
             "VALUES(%s, %s, %s,%s)")
    record = (email, cat, amount, date.today())
    mycursor.execute(query, record)
    connection.commit()

def getUser(email):
    print('hi')

def getLists(email):
    categories = []
    amounts = []
    dates = []
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM user_transactions")
    users = mycursor.fetchall()

    for i in range(len(users)):
        if users[i][0] == email:
            categories.append(users[i][1])
            amounts.append(users[i][2])
            dates.append(users[i][3])
    return categories, amounts, dates

def getUserInfo(email):
    firstName = ""
    lastName = ""
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM user_info")
    users = mycursor.fetchall()

    for i in range(len(users)):
        if users[i][2] == email:
            firstName = users[i][0]
            lastName = users[i][1]
    
    return firstName, lastName
