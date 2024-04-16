from flask import Flask, redirect, render_template, request
from baseline_helpers import baselineAskAI
from experimental_helpers import experimentalAskAI



# Configure application
app = Flask(__name__)

# Auto reload when changes are made.
app.config["TEMPLATES_AUTO_RELOAD"] = True

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