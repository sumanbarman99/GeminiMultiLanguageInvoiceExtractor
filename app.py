from dotenv import load_dotenv

# load all the environment variables from .env
load_dotenv()

# Import require libraries
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Get google api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


# convert image into bytes
def input_image_details(uploaded_file):
    # Read the image into bytes
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# Initilize streamlit app

st.set_page_config("MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload image of Invoice: ", type=["jpg", "jpeg", "png"])
image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Upload Image.", use_column_width=True)

submit = st.button("Tell me about the Invoice")

input_prompt = """
Yor are an expert in understanding imvoices. We will upload an image as invoice 
and you will answer any questions based on the uploaded invoice image."""

# If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is")
    st.write(response)

