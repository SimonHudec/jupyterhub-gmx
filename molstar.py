# view https://github.com/pragmatic-streamlit/streamlit-molstar
# run with streamlit run molstar.py
import streamlit as st
from streamlit_molstar import st_molstar, st_molstar_rcsb, st_molstar_remote
from streamlit_molstar.auto import st_molstar_auto
import streamlit as st

st.set_page_config(layout="wide")
st.write("from local file")
files = ['6pxm.pdb']
st_molstar_auto(files, key="7", height="320px")

st.write("topology")
files = ['6pxm.gro','em-protein.xtc', 'pbc.xtc']
st_molstar(files[0], files[1], key="8", height="320px")
st_molstar(files[0], files[2], key="9", height="320px")

# don't close the streamlit app before interrupting the process in terminal