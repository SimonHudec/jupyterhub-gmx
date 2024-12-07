# view https://github.com/pragmatic-streamlit/streamlit-molstar
# run with streamlit run pokus-molstar.py


import streamlit as st
from streamlit_molstar import st_molstar, st_molstar_rcsb, st_molstar_remote
from streamlit_molstar.auto import st_molstar_auto
import streamlit as st

import streamlit as st
from streamlit_molstar.auto import st_molstar_auto

import streamlit as st

from streamlit.runtime.scriptrunner import get_script_run_ctx

ctx = get_script_run_ctx()

st.set_page_config(layout="wide")

st.write("from remote url")
files = ["https://files.rcsb.org/download/3PTB.pdb", "https://files.rcsb.org/download/1LOL.pdb"]
st_molstar_auto(files, key="6", height="320px")

st.write("from local file")
files = ['6pxm.pdb']

st_molstar_auto(files, key="7", height="320px")
# don't close the streamlit app before interrupting the process in terminal