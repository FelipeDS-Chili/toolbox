
from toolbox.operations import get_data, get_episodes
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pandas
import requests
import json
import os

#title = st.text_input('Nombre del Anime', 'naruto')

#st.table(get_data().head())





def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)
