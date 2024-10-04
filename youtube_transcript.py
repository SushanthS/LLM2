from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
#import dspy
import pandas as pd
import dspy
import os

# enter key here
OPENAI_API_KEY=""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric

FILE_PATH = "/home/mahesh/LLM/notebook-lm/data"
YOUTUBE_URL = "https://www.youtube.com/watch?v=ZAf7FXih-Jc"


def extract_video_id(youtube_url):
    # Parse the video URL and extract the video ID
    parsed_url = urlparse(youtube_url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    else:
        raise ValueError("Invalid YouTube URL or missing video ID")


def get_transcript(video_url):
    try:
        # Extract the video ID from the YouTube URL
        video_id = extract_video_id(video_url)

        # Fetch the transcript using the video ID
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine the transcript into a single string
        transcript_text = ' '.join([entry['text'] for entry in transcript_list])

        return transcript_text
    except Exception as e:
        return str(e)


# Example usage

def write_string_to_file(text_string, file_path):
    try:
        # Open the file in write mode ('w')
        with open(file_path, 'w') as file:
            # Write the text string to the file
            file.write(text_string)
        print(f"Text successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



def summarize_transcript(transcript_path):
    """Summarizes a transcript using dspy.

    Args:
        transcript_path (str): Path to the transcript file.

    Returns:
        str: Summary of the transcript.
    """

    # Load the transcript using dspy
    transcript = dspy.load(transcript_path)

    # Extract relevant information from the transcript
    utterances = transcript.utterances
    speaker_labels = [utterance.speaker_label for utterance in utterances]
    text_content = [utterance.text_content for utterance in utterances]

    # Create a DataFrame for analysis
    transcript_df = pd.DataFrame({'speaker': speaker_labels, 'text': text_content})

    # Group utterances by speaker and concatenate text
    grouped_transcript = transcript_df.groupby('speaker')['text'].apply(lambda x: ' '.join(x))

    # Summarize each speaker's utterances using dspy's summarizer
    summarized_transcript = {}
    for speaker, text in grouped_transcript.items():
        summary = dspy.summarize(text)
        summarized_transcript[speaker] = summary

    # Combine summaries from all speakers into a single string
    final_summary = '\n'.join(f"{speaker}: {summary}" for speaker, summary in summarized_transcript.items())

    return final_summary

if __name__ == '__main__':
    transcript = get_transcript(YOUTUBE_URL)
    write_string_to_file(transcript, FILE_PATH) # transcript file

# Set up the LM.
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)

    summarize = dspy.ChainOfThought('document -> summary')
    response = summarize(document=transcript)

    print("***************TRANSCRIPT***************")
    print(transcript)
    print("\n")
    print(f"Transcript length: {len(transcript)}")
    print("****************************************")

    print("***************RATIONALE***************")
    print(response.rationale)
    print("\n")
    print(f"Rationale length: {len(response.rationale)}")
    print("****************************************")

    print("***************SUMMARY***************")
    print(response.summary)
    print("\n")
    print(f"Summary length: {len(response.summary)}")
    print("****************************************")



