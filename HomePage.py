from Functions import *
import streamlit as st
import pandas as pd
from math import pow


def homePage():

    if st.button("Log Out"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image('https://www.mmipromo.com/commercebankstore/images/themes/CommerceBank.jpg', width=200)
    with col3:
        st.write('')

    add_select = st.sidebar.selectbox(
        "Select an option: ",
        ("Home", "Add Transactions", "View Transactions", "Loan Calculator")
    )

    if add_select == "Home":

        st.markdown("<h1 style='text-align: center; color: Grey; font-size: 40px'> Home </h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: white; font-size: 20px'> Select an option in the sidebar </h1>", unsafe_allow_html=True)


    if add_select == "Add Transactions":
        st.markdown("<h1 style='text-align: center; color: black; font-size: 40px'> Add Transactions </h1>", unsafe_allow_html=True)

        email = st.text_input("Enter Email: ")

        menu = ['--', 'Utilities', 'Groceries', 'Transportations', 'Subscriptions', 'Misc']
        trans = st.selectbox("What is the category of transaction", menu)

        amount = st.text_input('Amount: ')

        if st.button("Submit"):
            flag = False
            try:
                int(amount)
            except ValueError:
                flag = True
            if flag:
                st.write('Input must be a number')
            elif check_repeat(email) == True:
                st.write("Incorrect Email")
            elif trans == '--':
                st.write("Category cannot be blank")
            elif amount == '':
                st.write("Amount cannot be blank")
            elif int(amount) < 0:
                st.write("Amount cannot be negative")
            else:
                st.write("Transaction accepted and added to transaction history")
                addTransaction(email, trans, amount)

    if add_select == "View Transactions":
        st.markdown("<h1 style='text-align: center; color: black; font-size: 40px'> View Transactions </h1>", unsafe_allow_html=True)
        st.write("Enter email and hit enter to view transaction history")
        email = st.text_input("Email: ")
        if st.button("Enter"):
            if check_repeat(email) == True:
                st.write("Incorrect Email")
            else:
                cats = []
                amounts = []
                cats, amounts = getLists(email)
                df = pd.DataFrame(
                    {
                        "categories": cats,
                        "amounts": amounts
                    }
                )
                st.dataframe(
                    df,
                    column_config={
                        "categories": "Categories",
                        "amounts": "Amounts"
                    },
                    hide_index=True,
                )


    if add_select == "Loan Calculator":
        st.markdown("<h1 style='text-align: center; color: black; font-size: 40px'> Loan Calculator </h1>", unsafe_allow_html=True)

        loan_amount = (st.text_input("Loan Amount: "))
        length = (st.text_input("Loan Term (in years)"))
        interest = (st.text_input("Interest Rate"))
        options = ['Monthly', 'Quarterly', 'Yearly']
        compound = st.selectbox("Compound", options)

        if st.button("Enter"):
            flag = False
            try:
                float(loan_amount)
                float(length)
                float(interest)
            except ValueError:
                flag = True
            if flag:
                st.write(':red[Inputs must be a number]')
            elif float(loan_amount) <= 0 or float(length) <= 0 or float(interest) <= 0:
                st.write("Amounts cannot be less than or equal to 0")
            else:
                cost = 0
                n = 0
                if compound == 'Monthly':
                    n = 12
                elif compound == 'Quarterly':
                    n = 4
                elif compound == 'Yearly':
                    n = 1

                cost = float(loan_amount) * pow((1 + ((float(interest)/100) / n)), (n * float(length)))

                st.write("Total cost after " + str(length) + " years would be: $" + "{:.2f}".format(cost))
                interestG = cost - float(loan_amount)
                st.write("$" + "{:.2f}".format(interestG) + " would be the interest gained over the span of the loan")

# final = P * (((1 + (r/n)) ** (n*t)))