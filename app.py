from flask import Flask, redirect, render_template, request
from helpers import askAI

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Track current number of prompts that have been asked...
count = 0

# Load home page!
@app.route("/", methods=["GET", "POST"])
def index():
    # If the user submits a prompt...
    if request.method == "POST":
        # Validate input isn't empty to avoid an unnecessary API call.
        prompt = request.form.get("prompt")
        if not prompt:
            print("You forgot the prompt!")
            return redirect("/")
        
        # Otherwise, ask the AI the prompt!
        output = askAI(prompt)
        return render_template("explanations.html", topic=prompt, promptResponse=output)
    else:
        # If not submitting the form, return the page like normal.
        return render_template("index.html")
    

@app.route("/explanation", methods=["GET", "POST"])
def explanation():
    if request.method == "POST":
        # Validate input isn't empty to avoid an unnecessary API call.
        prompt = request.form.get("prompt")
        if not prompt:
            print("You forgot the prompt!")
            return redirect("/")

        if count == 1:
            add_to_prompt = "Start by asking me a few guiding questions about an analogous example."
        elif count == 2:
            add_to_prompt = "Provide an explanation of the previous questions about the analogous example."
        elif count == 3:
            add_to_prompt = "And be sure to ask my understanding and be supportive. Don't give away the answers."

        # Otherwise, ask the AI the prompt!
        print(prompt + add_to_prompt)
        output = askAI(prompt + add_to_prompt)
        count += 1
        return render_template("explanations.html", topic=prompt, promptResponse=output)
    else:
        # If not submitting the form, return the page like normal.
        return render_template("explanations.html")