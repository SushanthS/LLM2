from pyt2s.services import stream_elements

data = stream_elements.requestTTS('Everything louder than everything else.')

with open('/Users/maheshsrinivas/LLM-Work/notebook-lm/output/output.mp3', '+wb') as file:
    file.write(data)
