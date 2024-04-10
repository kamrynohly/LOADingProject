# Welcome to our CS 276 Project.
### We are working to create an interface with generative AI that encourages deeper congitive engagement with content, leveraging pedagogical techniques like encouraging **productive struggle**. 

### How to Run Our Project
First, you must download the necessary dependencies for the project. Once you have downloaded the repository, you must also install openai and flask. You must also have an updated version of Python.

If you are using a Mac, try running
```
pip install openai
pip install flask
pip install Flask-Session
```

Once these have been successfully installed, you must also generate an OpenAI API key. Do not share this with anyone! You can create your API key by visiting this website about [OpenAI's API](https://openai.com/blog/openai-api).

Once you have created your API key, you must add it within a new file. Open up the repository folder within whatever IDE or text editor that you prefer. Within the folder on your local machine, create an `.env` file and include the following code, substituting `YOUR_KEY_HERE` for your own API key.
```
OPENAI_API_KEY=YOUR_KEY_HERE
```

When you have accomplished the above steps, you can run the project by opening up a terminal and running:
```
flask run
```

You should see a link created within your terminal, which gives you access to our project site. The site includes both our baseline AI tool, as well as our experimental tool. The experimental tool leverages two key design differences in its prompt-engineering, focusing on transferability of knowledge and building resiliency.