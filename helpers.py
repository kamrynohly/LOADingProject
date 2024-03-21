from openai import OpenAI
import time
import os
from dotenv import load_dotenv, dotenv_values 

# loading variables from .env file
load_dotenv() 

# initialize client
client = OpenAI()

# Inputs a prompt from the user as a string. Returns the content of the response as a string.
def askAI(prompt):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are an optimistic, friendly tutor helping students learning about computer science. You do not give away the answer. You guide students to find the proper answer by providing analogous examples and guiding questions."},
      {"role": "user", "content": prompt}
    ]
  )
  print(completion.choices[0].message.content)
  return completion.choices[0].message.content