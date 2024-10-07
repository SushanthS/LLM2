import PyPDF2
import dspy
import os
from openai import OpenAI

# enter key here
OPENAI_API_KEY=""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from elevenlabs import set_api_key
set_api_key(getpass('sk_98d0df11a6a364ebefd46201edc35a1f7cedac2ffb1a14cd'))

PDF_DIR = '/home/mahesh/LLM/notebook-lm/data'
PDF_FILE_NAME = 'eliud_kipchoge_sub2.pdf'
PDF_TO_READ = f'{PDF_DIR}/{PDF_FILE_NAME}'
OUTPUT_DIR = '/home/mahesh/LLM/notebook-lm/output'


def read_pdf_to_text(file_path):
    # Initialize a string to hold the text
    text = ""

    # Open the PDF file
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Loop through all the pages in the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the page
            page = pdf_reader.pages[page_num]
            # Extract text from the page
            text += page.extract_text()

    return text


def write_string_to_file(text_string, file_path):
    try:
        # Open the file in write mode ('w')
        with open(file_path, 'w') as file:
            # Write the text string to the file
            file.write(text_string)
        print(f"Text successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':

    pdf_text = read_pdf_to_text(PDF_TO_READ)
    print(pdf_text)
    print(len(pdf_text))

    write_string_to_file(pdf_text, f'{OUTPUT_DIR}/{PDF_FILE_NAME}.txt')

    # Set up the LM.
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)

    summarize = dspy.ChainOfThought('document -> summary')
    summary_txt = summarize(document=pdf_text)

    print("*********************SUMMARY******************")
    print(summary_txt)
    print(len(summary_txt.summary))
    print("*********************END SUMMARY******************")

    podcast_name = "Loneliness of a Long Distance Runner"
    podcastPrompt = f"""
    You are a writer creating the script for the another episode of a podcast {podcast_name} hosted by \"Tom\" and \"Jerry\".
    Use \"Tom\" as the person asking questions and \"Jerry\" as the person providing interesting insights to those questions.
    Always specify speaker name as  \"Tom\" or \"Jerry\" to identify who is speaking.
    Make the convesation casual and interesting.
    Extract relevant information for the podcast conversation from the Result delimited by triple quotes.
    Use the below format for the podcast conversation.
    1. Introduction about the topic and welcome everyone for another episode of the podcast {podcast_name}.
    2. Tom is the main host.
    2. Introduce both the speakers in brief.
    3. Then start the conversation.
    4. Start the conversation with some casual discussion like what they are doing right now at this moment.
    5. End the conversation with thank you speech to everyone.
    6. Do not use the word \"conversation\" response.

    """

    requestMessage = podcastPrompt + f"Result: ```{pdf_text}```"
    client = OpenAI()


    finalOutput = client.chat.completions.create(model="gpt-4o-mini",
                                               messages=[{"role": "system", "content": "You are a helpful assistant."},
                                                         {"role": "user", "content": requestMessage}
                                                         ],
                                               temperature=0.7
                                               )
    print(finalOutput.choices[0].message.content)

    print("***DONE!!***")

