from Functions import *
from Functions import check_login, check_repeat
from Functions import add_to_database

def ForgotPassword():

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.image('https://www.mmipromo.com/commercebankstore/images/themes/CommerceBank.jpg', width=200)
    with col3:
        st.write('')
    
    userName = st.text_input("Email:")
    new_password = st.text_input("New Password:", type='password')
    confirm_new_password = st.text_input("Confirm Password:", type='password')

    if st.button('Change Password'):
        if new_password == confirm_new_password:
            change_password(new_password, userName)
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
        else:
            st.write(":red[Your new passwords don't match]")