from flask import Flask, redirect, render_template, request
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values 


# Configure application
app = Flask(__name__)

# Auto reload when changes are made.
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Load necessary variables from .env file
#     Includes API_KEY
load_dotenv() 

# Start client
client = OpenAI()

# Make sure the session isn't stored in our cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# index()
# Allows the choice of two buttons
#       The first button directs the user to the experimental tool.
#       The second button directs the user to the baseline tool.
@app.get("/")
@app.route("/", methods=["GET", "POST"])
def index():
    # If we've selected a button, direct us to the proper tool.
    if request.method == "POST":
        if "experimental-btn" in request.form:
            return redirect("/experimental")
        # Otherwise, direct us to the baseline tool.
        return redirect("/baseline")
    # If we are requesting the page, load index.html.
    return render_template("index.html")



# baseline()
# Loads the baseline tool's opening page.
# Allows for the page to be retrieved with no beginning information,
# or can POST a prompt to the baseline AI functionalities.
# Only uses functions from `baseline_helpers.py`

@app.route("/baseline", methods=["GET", "POST"])
def baseline():
    # If the user submits a prompt, then verify it and load the AI response.
    if request.method == "POST":
        # Validate our input to avoid an unnecessary API call.
        prompt = request.form.get("prompt")
        if not prompt:
            print("You forgot the prompt!")
            return redirect("/baseline")
        
        # If our prompt is non-empty, then define the start of the AI conversation.
        conversation = [{"role": "user", "content": prompt}]
        output = baselineAskAI(conversation)                        # Generate a response with baseline AI
        response = {"role": "assistant", "content" : output}        # Store the response
        conversation.append(response)                               # Add the response to the conversation
        # Load our response into the explanation page.
        return render_template("baseline-response.html", promptResponse=output, conversation=conversation)
    # If not submitting the form, return the page like normal.
    return render_template("baseline.html")



# baseline_response()
# If the user posts an additional question to the original, then continues the conversation.
# Only uses functions from `baseline_helpers.py`

@app.route("/baseline-response", methods=["POST"])
def baseline_response():
    # Validate our input to avoid an unnecessary API call.
    prompt = request.form.get('secondary-prompt')
    if not prompt:
        print("You forgot the prompt!")
        return redirect("/baseline")

    # Get conversation history from the form.
    conversation = request.form.get("conversation")
    if not conversation:
        print("Error geting conversation history in baseline tool.")
        return redirect("/baseline")

    # Convert string into a list of dictionary elements
    conversation = eval(conversation)

    # Prior to calling the baseline AI, update the conversation context.
    conversation.append({"role": "user", "content": prompt})         # Add prompt to the conversation
    output = baselineAskAI(conversation)                             # Generate a response with baseline AI
    conversation.append({"role": "assistant", "content" : output})   # Add the response to the conversation

    # Return our response.
    return render_template("baseline-response.html", promptResponse=output, conversation=conversation)
    


# experimental()
# Loads the experimental tool's opening page.
# Allows for the page to be retrieved with no beginning information,
# or can POST a prompt to the experimental AI functionalities.
# Only uses functions from `experimental_helpers.py`
    
@app.route("/experimental", methods=["GET", "POST"])
def experimental():
    # If the user submits a prompt, then verify it and load the AI response.
    if request.method == "POST":
        # Validate our input to avoid an unnecessary API call.
        prompt = request.form.get("prompt")
        if not prompt:
            print("You forgot the prompt!")
            return redirect("/experimental")
        
        # If our prompt is non-empty, then define the start of the AI conversation.
        conversation = [{"role": "user", "content": prompt}]
        output = experimentalAskAI(conversation)                            # Generate a response with experimental AI
        conversation.append({"role": "assistant", "content" : output})      # Add the response to the conversation
        
        # Load response.
        return render_template("experimental-response.html", promptResponse=output, conversation=conversation)
    # If not submitting the form, return the page like normal.
    return render_template("experimental.html")



# experimental_response()
# If the user posts an additional question to the original, then continues the conversation.
# Only uses functions from `experimental_helpers.py`

@app.route("/experimental-response", methods=["POST"])
def experimental_response():
    # Validate our inputs to avoid an unnecessary API call.
    prompt = request.form.get('secondary-prompt')
    if not prompt:
        print("You forgot the prompt!")
        return redirect("/experimental")
    
    # Get conversation history from the form.
    conversation = request.form.get("conversation")
    if not conversation:
        print("Error geting conversation history.")
        return redirect("/experimental")

    # Convert string into a list of dictionary elements
    conversation = eval(conversation)
    conversation.append({"role": "user", "content": prompt})            # Add prompt to the conversation
    output = experimentalAskAI(conversation)                            # Generate a response with experimental AI
    conversation.append({"role": "assistant", "content" : output})      # Add the response to the conversation
    
    # Return the outputs.
    return render_template("experimental-response.html", promptResponse=output, conversation=conversation)



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



# experimentalAskAI(conversation)
#     Inputs a conversation from the user as a list of dictionary elements.
#     Outputs the response of the conversation completion as a string.

def experimentalAskAI(conversation):
  # Still testing!
  print(f"Starting conversations: {conversation}")

  # Define system instructions to prompts. 
  #     This is the section where we facilitate productive struggle through two main forms.
  #     1. Indicating to the AI to respond with analogous examples translates to transferability of knowledge.
  #     2. Stating not to give away the answer builds off of resiliency.

  systemPrompt = {
    "role": "system", 
    "content": "You are a tutor helping students learning about computer science. Do not give away the answer. Instead, guide students to answer their own question. Provide an example from an adjacent context to their question but never the identical answer. After the example, ask at least one guiding question. Be concise and use headings."
    } 

  checkUnderstandingInstr = {
    "role": "system",
    "content": "You are a tutor helping students learning about computer science. You do not give away the answer. Ask the students helpful guiding questions to see if they can transfer the knowledge from one example to help answer the question they've just asked. Ask them to explain their thought process, and then elaborate on whether or not their previous thoughts were correct or incorrect, kindly."
  }

  if (len(conversation) == 1):
    conversation.insert(0, systemPrompt)
  elif (len(conversation) == 4):
    conversation.insert(3, checkUnderstandingInstr)

  # Still testing!
  print(f"Experimental conversations: {conversation}")
  
  completion = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=conversation
  )
  # Confirm successful response, otherwise return an error.
  if not completion.choices[0].message.content:
    return "Failed to load AI response... please try again later."
  # Return response!
  return completion.choices[0].message.content