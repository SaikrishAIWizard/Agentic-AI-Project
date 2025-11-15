import streamlit as st
import json
from src.langgraphagenticai.Ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.Ui.streamlitui.display_result import DisplayResultsStreamlit


#MAIN FUNCTION START
def load_langgraph_agenticai_app():
    """
    Loads and run the LangGraph AgenticAI Application with Streamlit UI.
    This function Initializes the UI, handles user input, configure the LLM Model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness
    """

    #Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    #Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    elif st.session_state.IsSDLC:
        user_message = st.session_state.state
    else:
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            #configure LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error:LLM model could not be initialized.")
                return
            #Initialize and setup the graph based on use case
            usecase = user_input.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected")
                return
            ### Graph Builder
            graph_builder= GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultsStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return
        except Exception as e:
            raise ValueError(f"Error Occured with Exception: {e}")
