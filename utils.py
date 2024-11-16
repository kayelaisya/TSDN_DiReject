import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import base64
import pickle
import requests
import io
import joblib

@st.cache(ttl=12500, allow_output_mutation=True)
def load_model():
    model = pickle.load(open(r"https://raw.githubusercontent.com/kayelaisya/TSDN_DiReject/main/nb_tsdn.pkl", "rb"))
    return model
