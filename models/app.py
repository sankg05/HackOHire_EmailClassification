import streamlit as st
from transformers import pipeline
import requests

API_TOKEN = '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'

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def main():
    st.title("Sentiment Classification Demo")
    
    input_text = st.text_area("Enter text", "")

    pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    pipe1 = pipeline("summarization", model="facebook/bart-large-cnn")
    
    if st.button("Get Summary and Predict"):
        a = pipe1(input_text)
        summary_text = a[0]['summary_text']
        out = pipe(summary_text)
        
        output = query({
            "inputs": summary_text,
            "parameters": {"candidate_labels": ["Enquiry", "Escalation", "Dissatisfaction", "Concern", "Random"]},
        })
        
        st.write("Predicted Label:", out[0]['label'])
        st.write("Label with highest score:", output['labels'][output['scores'].index(max(output['scores']))])

if __name__ == "__main__":
    main()
