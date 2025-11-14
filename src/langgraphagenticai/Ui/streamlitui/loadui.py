import streamlit as st
import os
import datetime import date

from langchain_core.messages import AIMessage, HumanMessage
from src.langgraphagenticai.Ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config() #config
        self.user_controls = {}