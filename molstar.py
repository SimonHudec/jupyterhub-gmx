import streamlit as st
import os
from streamlit_molstar import st_molstar
from streamlit_molstar.auto import st_molstar_auto
import time
# --- Config ---
st.set_page_config(layout="wide")
DATA_FOLDER = "/home/jovyan"  # your server-side folder for structure/sim data

# --- Helpers ---
@st.cache_data
def list_structure_files():
    """Cached listing of files."""
    try:
        files = os.listdir(DATA_FOLDER)
        return sorted([f for f in files if f.endswith(('.pdb', '.gro', '.xtc'))])
    except FileNotFoundError:
        return []

def format_file_info(file):
    path = os.path.join(DATA_FOLDER, file)
    stats = os.stat(path)
    size_kb = stats.st_size / 1024
    mod_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(stats.st_mtime))
    return f"{file} ({size_kb:.1f} KB, modified {mod_time})"

def get_selected_path(file_label):
    return os.path.join(DATA_FOLDER, file_label.split(" (")[0])  # extract filename

# --- Layout ---
st.title("Molecular Viewer with Streamlit Mol*")

# Tabs
tab_default, tab_custom = st.tabs(["🔬 Default View", "📁 Custom File Selection"])

# --- Tab 1: Default view ---
with tab_default:
    st.subheader("Default Visualization (Fixed Files)")

    default_structure = '6pxm.pdb'
    default_topology = '6pxm.gro'
    default_trajectory = 'pbc.xtc'

    st.write("**Structure only**")
    st_molstar_auto([default_structure], key="auto_default", height="600px")

    st.write("**Topology + Trajectory**")
    st_molstar(default_topology, default_trajectory, key="traj", height="600px")

# --- Tab 2: Custom file selection from server ---
with tab_custom:
    st.subheader("Select Topology and Trajectory from Server")

    all_files = list_structure_files()
    pdb_gro_labels = [format_file_info(f) for f in all_files if f.endswith(('.pdb', '.gro'))]
    xtc_labels = [format_file_info(f) for f in all_files if f.endswith('.xtc')]

    selected_top = st.selectbox("Topology file (.pdb or .gro)", pdb_gro_labels, key="topo_select") if pdb_gro_labels else None
    selected_xtc = st.selectbox("Trajectory file (.xtc)", xtc_labels, key="xtc_select") if xtc_labels else None

    # Horizontal buttons
    b1, b2 = st.columns([1, 1])
    with b1:
        click_traj = st.button("📽️ Load with Trajectory", key="load_traj")
    with b2:
        click_top = st.button("📄 Load Topology Only", key="load_top")

    # Persistent Mol* viewer that only updates on button click
    if "viewer_mode" not in st.session_state:
        st.session_state.viewer_mode = None
        st.session_state.top_path = None
        st.session_state.xtc_path = None

    # Update state only when buttons are clicked
    if click_traj:
        if selected_top and selected_xtc:
            st.session_state.viewer_mode = "traj"
            st.session_state.top_path = get_selected_path(selected_top)
            st.session_state.xtc_path = get_selected_path(selected_xtc)
            st.success(f"Loaded: {os.path.basename(st.session_state.top_path)} + {os.path.basename(st.session_state.xtc_path)}")
        else:
            st.error("Please select both topology and trajectory files.")

    elif click_top:
        if selected_top:
            st.session_state.viewer_mode = "top"
            st.session_state.top_path = get_selected_path(selected_top)
            st.session_state.xtc_path = None
            st.success(f"Loaded: {os.path.basename(st.session_state.top_path)} (topology only)")
        else:
            st.error("Please select a topology file.")

    # Display the viewer based on stored state
    if st.session_state.viewer_mode == "traj":
        st_molstar(
            st.session_state.top_path,
            st.session_state.xtc_path,
            key="molstar_viewer",
            height="600px"
        )
    elif st.session_state.viewer_mode == "top":
        st_molstar_auto(
            [st.session_state.top_path],
            key="molstar_viewer",
            height="600px"
        )
