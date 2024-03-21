from flask import Flask, redirect, render_template, request
from helpers import askAI

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
        return render_template("index.html", prompt=prompt, promptResponse=output)
    else:
        # If not submitting the form, return the page like normal.
        return render_template("index.html")