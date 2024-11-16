import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import base64
import pickle
import requests
import io

@st.cache(ttl=12500, allow_output_mutation=True)
def load_model():
    model = pickle.load(open(r"C:/Users/acer/Downloads/nb_tsdn.pkl", "rb"))
    return model
