import streamlit as st
from modules.openai_query_handler import OpenAIQueryHandler
from modules.argocd import argocd_functions, argocd_function_definitions
from modules.github import github_functions, github_function_definitions
from modules.harbor import harbor_functions, harbor_function_definitions

# Combine all the functions from different modules
custom_toolkit_functions = {**argocd_functions, **github_functions, **harbor_functions}
openai_function_definitions = argocd_function_definitions + github_function_definitions + harbor_function_definitions

llm = OpenAIQueryHandler(custom_toolkit_functions, openai_function_definitions)

# Initialize the conversation history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title("ChatOps")

# Input field for the user to input their query
user_input = st.text_input("You: ")


# Custom function to display messages with markdown support
def markdown_message(content, is_user=False, key=None):
    if is_user:
        st.markdown(f"<div style='text-align: right; color: white;'>You: {content}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color: green;'>Assistant: {content}</div>", unsafe_allow_html=True)


if st.button("Send"):
    # Add the user's query to the conversation history
    st.session_state['messages'].append({"role": "user", "content": user_input})

    # Get the bot's response
    bot_response = llm.construct_openai_query_response(user_input)

    # Add the bot's response to the conversation history
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})

    # Display the conversation history
    for msg in st.session_state['messages']:
        if msg["role"] == "user":
            markdown_message(msg["content"], is_user=True)
        else:
            markdown_message(msg["content"])

# Sidebar for additional options
# st.sidebar.title("Options")
# if st.sidebar.button("Clear Conversation"):
#     st.session_state['messages'] = []
