# ============================================================
# Excel + Power BI Learning App (Colorful One-Page Tabs)
# Author: Ashwik Bire
# Description: Advanced Streamlit app for learning Excel & Power BI
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image

# Page config
st.set_page_config(
    page_title="Excel + Power BI Learning Hub",
    page_icon="📊",
    layout="wide"
)

# Title Section
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1;'>📘 Excel + Power BI Learning Hub</h1>
    <p style='text-align: center; color: #566573;'>Learn Microsoft Excel & Power BI with interactive tutorials, quizzes, and projects.</p>
    """,
    unsafe_allow_html=True
)