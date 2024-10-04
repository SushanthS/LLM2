import dspy
import os

# enter key here
OPENAI_API_KEY=""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

class QA(dspy.Signature):
    """Given the question, generate an answer"""
    question = dspy.InputField(desc="User's question")
    essay = dspy.InputField(desc="User's essay")
#    answer = dspy.OutputField(desc="often between 1-5 words.")
    answer = dspy.OutputField(desc="An essay on the answer.")

class QA2(dspy.Signature):
    """Given the question, generate a podcast script with two hosts"""
    question = dspy.InputField(desc="essay")
    podcast_script = dspy.OutputField(desc="Podcast script")

# custom module
class ChainOfThoughtCustom(dspy.Module):
    def __init__(self):
        self.cot1 = dspy.ChainOfThought("question -> step_by_step_thought")
        self.cot2 = dspy.ChainOfThought("question, thought -> two_thousand_word_essay")
#        self.cot3 = dspy.ChainOfThought("question, thought, essay -> podcast_script")

    def forward(self, question):
        thought = self.cot1(question=question).step_by_step_thought
        essay = self.cot2(question=question, thought=thought).two_thousand_word_essay
#        script = self.cot3(question=question, thought=thought, essay=essay).podcast_script
        return dspy.Prediction(thought=thought, essay=essay)

if __name__ == '__main__':

# Set up the LM.
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)

    question = "what influence has ritchie blackmore had on rock and metal guitar?"
    COTCustom = ChainOfThoughtCustom()
    prediction = COTCustom(question=question)
    print(prediction.essay)
    print(len(prediction.essay))
    print("************************************************")
#    turbo.inspect_history(n=3)

    COTCustom = ChainOfThoughtCustom()
    script = COTCustom(question=prediction.essay)
    print(script)
    print(len(script))
    print("************************************************")


