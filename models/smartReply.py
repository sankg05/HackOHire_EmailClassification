import streamlit as st
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

# Configure the generative model
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro')

# Function to convert text to Markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Function to generate response
def gem_output(input_text):
    safety_settings = [
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    prompt = "Please write an appropriate response for the following mail\n" + input_text
    response = model.generate_content(prompt, safety_settings=safety_settings)
    return response.text if response else ''

# Streamlit app
def main():
    st.title('Smart Reply Generator')

    # Input text area
    input_text = st.text_area("Enter the mail content")

    # Button to generate response
    if st.button("Generate Response"):
        if input_text:
            response = gem_output(input_text)
            if response:
                st.markdown(response)
            else:
                st.error("Failed to generate response. Please try again.")

if __name__ == "__main__":
    main()
