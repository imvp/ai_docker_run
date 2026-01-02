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
        # Add reasoning instruction to the prompt
        reasoning_instruction = "\n\nPlease think step by step and provide your reasoning before giving the final answer."
        full_prompt = prompt + reasoning_instruction
        
        messages = [
            {"role": "user", "content": full_prompt}
        ]
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages
            )
            
            # Extract the text content from the response
            answer = response.choices[0].message.content
            
            # Try to parse reasoning and final answer
            # Look for common separators between reasoning and answer
            separators = ["Final answer:", "Answer:", "Conclusion:", "Therefore,"]
            reasoning = ""
            final_answer = answer
            
            for separator in separators:
                if separator in answer:
                    parts = answer.split(separator, 1)
                    reasoning = parts[0].strip()
                    final_answer = parts[1].strip()
                    break
            
            # Display reasoning in an expander if found
            if reasoning:
                with st.expander("Reasoning"):
                    st.write(reasoning)
            
            # Display the final answer
            st.markdown("### Answer:")
            st.write(final_answer)

        except Exception as e:
            # Catch connection errors, API timeouts, or configuration issues
            st.error(f"An error occurred: {e}")
