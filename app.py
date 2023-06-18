import requests
from flask import Flask, request, jsonify, render_template
import traceback
import os
import replicate

REPLICATE_API_TOKEN = input("Enter Replicate API Token: ")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/generate_image", methods=["POST"])
def generate_image():
    
    data = request.get_json()
    prompt = data["text"]
    print(prompt)
    output = replicate.run(
        "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
        input={"prompt": prompt}
    )
    print(output)
    image_url = output
    print(image_url)
    return jsonify({"image_url": image_url})
    

@app.route("/answer_question", methods=["POST"])
def answer_question():
    data = request.get_json()
    prompt = data["question"]
    print(prompt)
    output = replicate.run(
        "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
        input={"prompt": prompt}
    )
    output_list = list(output)  # Convert the generator to a list
    answer_string = " ".join(output_list)
    print(answer_string)  # Concatenate the strings into a single output string
    return jsonify({"answer_string": answer_string})

if __name__ == "__main__":
    app.run(debug=True)
