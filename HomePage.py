from matplotlib import pyplot as plt
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
        ("Home","User Profile and Settings", "Add Transactions", "View Transactions", "Loan Calculator")
    )

    if add_select == "Home":

        st.markdown("<h1 style='text-align: center; color: white; font-size: 40px'> Home </h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: white; font-size: 20px'> Select an option in the sidebar </h1>", unsafe_allow_html=True)


    if add_select == "User Profile and Settings":

        firstName, lastName = getUserInfo(st.session_state.email)

        st.markdown("<h1 style='text-align: center; color: white; font-size: 40px'> User Profile </h1>", unsafe_allow_html=True)
        st.write("First Name: ", firstName)
        st.write("Last Name: ", lastName)

        changed_password = st.text_input("Password")
        if st.button("Change Password"):
            change_password(changed_password, st.session_state.email)


    if add_select == "Add Transactions":
        st.markdown("<h1 style='text-align: center; color: white; font-size: 40px'> Add Transactions </h1>", unsafe_allow_html=True)

        menu = ['--', 'Utilities', 'Groceries', 'Transportations', 'Subscriptions','Housing','Entertainment','Misc']
        trans = st.selectbox("What is the category of transaction", menu)

        amount = st.text_input('Amount: ')

        if st.button("Submit"):
            flag = False
            try:
                int(amount)
            except ValueError:
                flag = True
            if flag:
                st.write(':red[Input must be a number]')
            elif trans == '--':
                st.write(":red[Category cannot be blank]")
            elif amount == '':
                st.write(":red[Amount cannot be blank]")
            elif int(amount) < 0:
                st.write(":red[Amount cannot be negative]")
            else:
                st.write("Transaction accepted and added to transaction history")
                addTransaction(st.session_state.email, trans, amount)

    if add_select == "View Transactions":
        st.markdown("<h1 style='text-align: center; color: white; font-size: 40px'> View Transactions </h1>", unsafe_allow_html=True)
        cats = []
        amounts = []
        dates= []
        cats, amounts, dates = getLists(st.session_state.email)
        df = pd.DataFrame(
            {
                "categories": cats,
                "amounts": amounts, 
                "dates": dates
            }
        )

        sort_option = st.selectbox("Sort by", ("Category", "Amounts", "Date Entered, Year-Month-Day"))

        if sort_option == "Category":
            df = df.sort_values(by=['categories'])
        elif sort_option == "Amounts":
            df = df.sort_values(by=['amounts'])
        else:
            df['dates'] = pd.to_datetime(df['dates'])
            df = df.sort_values(by=['dates'])

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(
                df,
                column_config={
                    "categories": "Categories",
                    "amounts": "Amounts",
                    "dates": "Date Entered, Year-Month-Day"
                },
                hide_index=True,
            )
            
        with col2:
            display_option = st.selectbox("Spending Statistics:", ("Most Frequent Category", "Monthly Total", "Category with Most Spent"))
            if display_option == "Most Frequent Category":
                most_frequent_category = df['categories'].mode()[0]
                st.write(f"Most frequent category: **{most_frequent_category}**")
            elif display_option == "Monthly Total":
                total_spent = df['amounts'].sum()   
                st.write(f"Spent this month: $**{str(total_spent)}**")
            else:
                category_with_most_spent = df.groupby('categories')['amounts'].sum().idxmax()
                st.write(f"Category with most spent: **{category_with_most_spent}**")


    if add_select == "Loan Calculator":
        st.markdown("<h1 style='text-align: center; color: white; font-size: 40px'> Loan Calculator </h1>", unsafe_allow_html=True)

        loan_amount = (st.text_input("Loan Amount: "))
        length = (st.text_input("Loan Term (in years)"))
        interest = (st.text_input("Interest Rate"))
        options = ['Monthly', 'Quarterly', 'Yearly']
        compound = st.selectbox("Compound", options)

        def loan_visualization(loan_amount, length, interest, compound):
            total_cost = cost
            interest_gain = total_cost - float(loan_amount)

            # Plotting
            labels = ['Loan Amount', 'Interest Gain']
            sizes = [float(loan_amount), interest_gain]
            explode = (0.1, 0)  # explode the 1st slice (Loan Amount)
            colors = ['#ff9999','#66b3ff']

            fig1, ax1 = plt.subplots(facecolor='#006649')
            ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.pyplot(fig1)
        
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
                loan_visualization(loan_amount, length, interest, compound)

# final = P * (((1 + (r/n)) ** (n*t)))