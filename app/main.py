import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Model options with their base URLs
model_options = {
    "Phi-4 Q5_K_M": "http://llm:8080/v1/",
    "Phi-4 Q4_K_M": "http://llm2:8080/v1/"
}

# Streamlit UI
st.title("Local LLM Chat")

# Model selection
selected_model = st.selectbox("Select Model", list(model_options.keys()))

prompt = st.text_area("Enter your prompt:", "")

if st.button("Send"):
    with st.spinner("Getting response..."):
        # Add reasoning instruction to the prompt
        reasoning_instruction = "\n\nPlease think step by step and provide your reasoning before giving the final answer."
        full_prompt = prompt + reasoning_instruction
        
        # Initialize client with selected model's base URL
        client = OpenAI(base_url=model_options[selected_model], api_key=os.getenv("API_KEY"))
        
        messages = [
            {"role": "user", "content": full_prompt}
        ]
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),  # This might need adjustment if models have different names
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
