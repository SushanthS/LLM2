import streamlit as st
#import streamlit_lottie
import streamlit_scrollable_textbox as stx
from youtube_transcript_api import YouTubeTranscriptApi
import dspy

import pathlib
import requests
import json
import os
from urllib.parse import urlparse, parse_qs
import torch
from pyt2s.services import stream_elements

# enter key here before running
OPENAI_API_KEY=""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# mxs - looks like utils is a folder that is not available here.
#from utils import *


def extract_video_id(youtube_url):
    # Parse the video URL and extract the video ID
    parsed_url = urlparse(youtube_url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    else:
        raise ValueError("Invalid YouTube URL or missing video ID")


def get_transcript(yt_url):
    """
    Function to get the transcripts of the Youtube Video
    """
    try:
        # Extract the video ID from the YouTube URL
        video_id = extract_video_id(yt_url)

        # Fetch the transcript using the video ID
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine the transcript into a single string
        transcript_text = ' '.join([entry['text'] for entry in transcript_list])

        return transcript_text
    except Exception as e:
        return str(e)

def write_string_to_file(text_string, file_path):
    try:
        # Open the file in write mode ('w')
        with open(file_path, 'w') as file:
            # Write the text string to the file
            file.write(text_string)
        print(f"Text successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_summary(transcript):
    """
    Function to generate a summary of the transcript
    """
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)

    summarize = dspy.ChainOfThought('document -> summary')
    response = summarize(document=transcript)

    return response.summary

class QA2(dspy.Signature):
    """Given an essay, generate a podcast script on the answer"""
    essay = dspy.InputField(desc="User's essay")
    podcast_script = dspy.OutputField(desc="A podcast script based on the given essay. There are two hosts in the podcast - Ray and Tom.")



def create_podcast_file(transcript):
    """
    Function to return  podcast mp3 file from the transcript
    """
    # Set up the LM.
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)

    predict2 = dspy.Predict(QA2)
    script = predict2(essay=transcript)
    print(script.podcast_script)
    print(len(script.podcast_script))
    print("************************************************")
#    turbo.inspect_history(n=2)

    # TTS
    data = stream_elements.requestTTS(script.podcast_script)
    mp3_file = f'/Users/maheshsrinivas/LLM-Work/nlm/LLM2/output/pdc1.mp3'
    with open(mp3_file, '+wb') as file:
        file.write(data)

    print(f"GPU: {torch.cuda.is_available()}")

    return mp3_file


def main():
    """
    Main Function
    """
    st.set_page_config(
        page_title="AI Audio Transciber",
        layout= "centered",
        initial_sidebar_state="expanded",
        #menu_items={
        #'Get Help': 'https://github.com/smaranjitghose/AIAudioTranscriber',
        #'Report a bug': "https://github.com/smaranjitghose/AIAudioTranscriber/issues",
        #'About': "## A minimalistic application to generate transcriptions for audio built using Python"
        #} 
        )
    transcript = ""
    summary = ""
    podcast_mp3_file = "/Users/maheshsrinivas/LLM-Work/nlm/LLM2/output/podcast.mp3"
    st.title("AI Audio Transcriber")
    #Create a Input Form Component
    input_mode = st.sidebar.selectbox(
                                    label="Input Mode",
                                    options= ["Youtube Video URL","Quiz"])
    st.session_state["input_mode"] = input_mode

    # Create a Form Component on the Sidebar for accepting input data and parameters
    with st.sidebar.form(key="input_form",clear_on_submit=False):

        # Nested Component to take user input for audio file as per seleted mode
        if input_mode == "Youtube Video URL":
            yt_url = st.text_input(label="Paste URL for Youtube Video 📋")
        else:
            aud_url = st.text_input(label="Enter URL for Audio File 🔗 ")

        submitted = st.form_submit_button(label="Generate Transcript, Summary & Podcast✨")

        if(submitted):
            if yt_url:
                transcript = get_transcript(yt_url)
                summary = create_summary(transcript)
                video_id = extract_video_id(yt_url)
                podcast_mp3_file = create_podcast_file(transcript)
            else:
                st.warning("Please🙏 enter a valid URL for Youtube video")
         

    col1,col2 = st.columns([10,10],gap="large")
        
    # Display the generated Transcripts
    with col1:
        st.markdown("GENERATED TRANSCRIPT")
        # st.markdown(st.session_state["transcript"])
        stx.scrollableTextbox(transcript, height = 500)
        
    # Display the original Audio
    with col2:
        st.markdown("YouTube Video Summary")
        # st.markdown(st.session_state["transcript"])
        stx.scrollableTextbox(summary, height = 300)  
    
    with open(podcast_mp3_file,"rb") as f:
        st.audio(f.read())     
        
    st.balloons()
        


if __name__ == "__main__":
    main()