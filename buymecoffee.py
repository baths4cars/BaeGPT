import streamlit as st
from typing import Literal
from streamlit.components.v1 import html

Font = Literal['Cookie', 'Lato', 'Arial', 'Comic', 'Inter', 'Bree', 'Poppins']

def button(
    username: str,
    floating: bool = True,
    text: str = "Buy me a coffee",
    emoji: str = "",
    bg_color: str = "#FFDD00",
    font: Font = "Cookie",
    font_color: str = "#000000",
    coffee_color: str = "#000000",
    width: int = 220,
):
    button = f"""
        <script type="text/javascript"
            src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js"
            data-name="bmc-button"
            data-slug="{username}"
            data-color="{bg_color}"
            data-emoji="{emoji}"
            data-font="{font}"
            data-text="{text}"
            data-outline-color="#000000"
            data-font-color="{font_color}"
            data-coffee-color="{coffee_color}" >
        </script>
    """

    html(button, height=70, width=width)

    if floating:
        st.markdown(
            f"""
            <style>
                iframe[width="{width}"] {{
                    position: fixed;
                    bottom: 60px;
                    right: 40px;
                    background: transparent;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )