# Fantastic 4
from Login import *
from HomePage import *
from ForgotPassword import *


choice = 0
if "Forgot Password" in st.session_state:
    ForgotPassword()
elif "logged in" in st.session_state:
    homePage()
else:
    login()


