import pytest
from unittest.mock import patch, MagicMock
import HomePage as homePage  # Assuming your code is in 'your_module.py'

# Setup for Streamlit's session_state and other components
@pytest.fixture
def st_mock():
    with patch('streamlit.button'), \
         patch('streamlit.text_input', return_value=""), \
         patch('streamlit.write'), \
         patch('streamlit.selectbox', return_value="Home"), \
         patch('streamlit.columns', return_value=(MagicMock(), MagicMock(), MagicMock())), \
         patch('streamlit.session_state', new_callable=dict), \
         patch('streamlit.rerun'), \
         patch('streamlit.markdown'), \
         patch('streamlit.image'), \
         patch('streamlit.dataframe'), \
         patch('streamlit.pyplot'):
        import streamlit as st
        yield st

def test_logging_out(st_mock):
    st_mock.button.return_value = True  # Simulate button press
    homePage()
    assert 'email' not in st_mock.session_state  # Check if session is cleared
    st_mock.rerun.assert_called_once()  # Check if rerun is called

def test_home_page_loads(st_mock):
    st_mock.selectbox.return_value = "Home"
    homePage()
    st_mock.markdown.assert_any_call("<h1 style='text-align: center; color: white; font-size: 40px'> Home </h1>", unsafe_allow_html=True)

@patch('your_module.getUserInfo', return_value=("John", "Doe"))
def test_user_profile_page(get_user_info_mock, st_mock):
    st_mock.selectbox.return_value = "User Profile and Settings"
    homePage()
    st_mock.write.assert_any_call("First Name: ", "John")
    st_mock.write.assert_any_call("Last Name: ", "Doe")

def test_add_transactions(st_mock):
    st_mock.selectbox.return_value = "Add Transactions"
    st_mock.button.side_effect = [False, True]  # No submit button pressed, then submit pressed
    st_mock.text_input.side_effect = ['100']  # Valid amount entered
    homePage()
    st_mock.write.assert_called_with("Transaction accepted and added to transaction history")

@patch('your_module.loan_visualization')
def test_loan_calculator(loan_vis_mock, st_mock):
    st_mock.selectbox.return_value = "Loan Calculator"
    st_mock.button.return_value = True
    st_mock.text_input.side_effect = ['5000', '5', '5']  # Valid inputs for loan_amount, length, interest
    homePage()
    loan_vis_mock.assert_called_once()  # Check if visualization function is called
