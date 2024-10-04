from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
#import dspy
import pandas as pd
import dspy
import os
from pydantic import BaseModel, Field

# enter key here
OPENAI_API_KEY=""
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
#from dspy.datasets.gsm8k import GSM8K, gsm8k_metric


class QA(dspy.Signature):
    question = dspy.InputField(desc="User's question")
    answer = dspy.OutputField(desc="often between 1 and 5 words")


class DoubleChainOfThoughtModule(dspy.Module):
    def __init__(self):
        self.cot1 = dspy.ChainOfThought("question -> step_by_step_thought")
        self.cot2 = dspy.ChainOfThought("question, thought -> one_word_answer")

    def forward(self, question):
        thought = self.cot1(question=question).step_by_step_thought
        answer = self.cot2(question=question, thought=thought).one_word_answer
        return dspy.Prediction(thought=thought, answer=answer)

class AnswerConfidence(BaseModel):
    answer: str = Field("Answer. 1-5 words.")
    confidence: float = Field("Your confidence level between 0-1")

class QAWithConfidence(dspy.Signature):
    """Given user's question, answer it amd also give confidence level"""
    question = dspy.InputField()
    answer: AnswerConfidence = dspy.OutputField()

class FIFAAnswer(BaseModel):
    country: str = Field()
    year: int = Field()

class QAList(dspy.Signature):
    """Given user's question, answer with a JSON readable python list"""
    question = dspy.InputField()
    answer_list: list[FIFAAnswer] = dspy.OutputField()

if __name__ == '__main__':

# Set up the LM.
    turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
    dspy.settings.configure(lm=turbo)

#    QUESTION = 'what is the capital city of the birth state of the guitar player who succeeded ritchie blackmore in deep purple in the 1990s?'
    QUESTION = 'Generate a list of country and year of FIFA world cup winners from the 2002-present'

#    predict = dspy.TypedChainOfThought(QAList)
    predict = dspy.TypedChainOfThought(QAList)

    answer = predict(question=QUESTION)
    print("***************************************")
    print(answer.answer_list)
    print("***************************************")

#    generate_answer = dspy.ChainOfThought(QA)
#    prediction = generate_answer(question=QUESTION)

#    print("***************PREDICTION***************")
#    print(prediction)
#    print("****************************************")
#    print(turbo.inspect_history(n=1))

"""
    doubleCot = DoubleChainOfThoughtModule()
    doubleCotOutput = doubleCot(question=QUESTION)

    print("***************DOUBLE COT***************")
    print(doubleCotOutput)
    print("****************************************")
    print(turbo.inspect_history(n=2))

"""
"""
    predict = dspy.TypedChainOfThought(QAWithConfidence)
    TypedCotOutput = predict(question=QUESTION)

    print("***************TYPED COT***************")
    print(TypedCotOutput.answer)
    print(TypedCotOutput.answer.answer)
    print(TypedCotOutput.answer.confidence)
    print(type(TypedCotOutput.answer.confidence))
    print("****************************************")
    print(turbo.inspect_history(n=2))
"""

#    response = summarize(document=transcript)
"""
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
"""