import dspy
import os
from pyt2s.services import stream_elements

QUESTION = "How did Eliud Kipchoge break the sub-2 hour barrier in a full marathon distance? What were the training methods he used to achieve his groundbreaking feat?"

# enter key here
OPENAI_API_KEY=""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

class QA(dspy.Signature):
    """Given the question, generate an essay on the answer"""
    question = dspy.InputField(desc="User's question")
#    answer = dspy.OutputField(desc="often between 1-5 words.")
    answer = dspy.OutputField(desc="An essay on the answer up to 4000 words")

class QA2(dspy.Signature):
    """Given an essay, generate a podcast script on the answer"""
    essay = dspy.InputField(desc="User's essay")
    podcast_script = dspy.OutputField(desc="A podcast script based on the given essay. There are two hosts in the podcast - Ray and Tom.")

if __name__ == '__main__':

# Set up the LM.
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)


    predict = dspy.Predict(QA)
    prediction = predict(question=QUESTION)
    print(prediction.answer)
    print(len(prediction.answer))
    print("************************************************")
    predict2 = dspy.Predict(QA2)
    script = predict2(essay=prediction.answer)
    print(script.podcast_script)
    print(len(script.podcast_script))
    print("************************************************")
#    turbo.inspect_history(n=2)

    # TTS
    data = stream_elements.requestTTS(script.podcast_script)
    with open('/home/mahesh/LLM/notebook-lm/output/eliud.mp3', '+wb') as file:
        file.write(data)