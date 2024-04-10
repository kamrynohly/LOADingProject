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

def experimentalAskAI(conversation):
  # Still testing!
  print(f"Starting conversations: {conversation}")

  # Define system instructions to prompts. 
  #     This is the section where we facilitate productive struggle through two main forms.
  #     1. Indicating to the AI to respond with analogous examples translates to transferability of knowledge.
  #     2. Stating not to give away the answer builds off of resiliency.
  analogousExampleInstr = {
    "role": "system", 
    "content": "You are a tutor helping students learning about computer science. You do not give away the answer, but you can give analogous code examples that do NOT give away the answer. You guide students to find the proper answer by providing analogous examples and guiding questions. Start by providing an analogous example."
  }
  checkUnderstandingInstr = {
    "role": "system",
    "content": "You are a tutor helping students learning about computer science. You do not give away the answer. Ask the students helpful guiding questions to see if they can transfer the knowledge from one example to help answer the question they've just asked. Ask them to explain their thought process, and then elaborate on whether or not their previous thoughts were correct or incorrect, kindly."
  }

  if (len(conversation) == 1):
    conversation.insert(0, analogousExampleInstr)
  elif (len(conversation) == 4):
    conversation.insert(3, checkUnderstandingInstr)

  # Still testing!
  print(f"Experimental conversations: {conversation}")
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=conversation
  )
  # Confirm successful response, otherwise return an error.
  if not completion.choices[0].message.content:
    return "Failed to load AI response... please try again later."
  # Return response!
  return completion.choices[0].message.content