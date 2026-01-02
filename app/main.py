import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

# Streamlit UI
st.title("Local LLM Chat")
prompt = st.text_area("Enter your prompt:", "")

if st.button("Send"):
    with st.spinner("Getting response..."):
        messages = [
            {"role": "user", "content": prompt}
        ]
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages
            )
            
            # Extract the text content from the response
            answer = response.choices[0].message.content
            
            # Display the result in the Streamlit UI
            st.markdown("### Response:")
            st.write(answer)

        except Exception as e:
            # Catch connection errors, API timeouts, or configuration issues
            st.error(f"An error occurred: {e}")
