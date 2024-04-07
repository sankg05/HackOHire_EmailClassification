import streamlit as st
from transformers import pipeline

# Load the summarization pipeline
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def main():
    # Set title and description
    st.title("Text Summarization Demo")
    st.write("This app summarizes input text using the BART-large-CNN model.")

    # Input text area for user to enter text
    input_text = st.text_area("Enter text:", "")

    # Button to trigger summarization
    if st.button("Summarize"):
        # Check if input text is provided
        if input_text.strip() == "":
            st.warning("Please enter some text.")
        else:
            # Summarize the input text
            summary = summarization_pipeline(input_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            
            # Display the summary
            st.subheader("Summary:")
            st.write(summary)

if __name__ == "__main__":
    main()
