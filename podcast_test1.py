import wikipedia
import tiktoken
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import openai
from getpass import getpass

# enter key here
openai.api_key = getpass('')

# Return a sentence-tokenized copy of text, using NLTK’s recommended sentence tokenizer (currently PunktSentenceTokenizer for the specified language).
def split_text (input_text):
  split_texts = sent_tokenize(input_text)
  return split_texts

def create_chunks(split_sents, max_token_len=2500):
  current_token_len = 0
  input_chunks = []
  current_chunk = ""
  for sents in split_sents:
    sent_token_len = len(enc.encode(sents))
    if (current_token_len + sent_token_len) > max_token_len:
      input_chunks.append(current_chunk)
      current_chunk = ""
      current_token_len = 0
    current_chunk = current_chunk + sents
    current_token_len = current_token_len + sent_token_len
  if current_chunk != "":
    input_chunks.append(current_chunk)
  return input_chunks



if __name__ == '__main__':
  input = wikipedia.page("Eliud Kipchoge", auto_suggest=False)
  wiki_input = input.content
  print(len(wiki_input))

  enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
  print("number of tokens in corpus ", len(enc.encode(wiki_input)))

  split_sents = split_text(wiki_input)
  input_chunks = create_chunks(split_sents, max_token_len=2500)
  print(f'Batch size: {len(input_chunks)}')


