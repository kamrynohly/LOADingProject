from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 

# Load necessary variables from .env file
#     Includes API_KEY
load_dotenv() 

# Start client
client = OpenAI()

# baselineAskAI(conversation)
#     Inputs a conversation from the user as a list of dictionary elements.
#     Outputs the response of the conversation completion as a string.

def baselineAskAI(conversation):
  completion = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=conversation
  )
  # Confirm successful response, otherwise return an error.
  if not completion.choices[0].message.content:
    return "Failed to load AI response... please try again later."
  # Return response!
  return completion.choices[0].message.content