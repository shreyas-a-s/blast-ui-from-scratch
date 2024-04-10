#!/usr/bin/env python3

import subprocess
from flask import Flask, request

def run_blastn(parameter):
    with open("sequence.txt", "w") as file:
        # Write the value of the variable to the file
        file.write(parameter)

    # Run the blast with the given parameter
    process = subprocess.Popen(['blastn', '-query', 'sequence.txt', '-db', 'azadirachta-indica-blast-test/azadirachta-indica', '-out', 'output_file.txt', '-max_target_seqs', '500', '-evalue', '0.001', '-word_size', '11', '-gapopen', '5', '-gapextend', '2', '-penalty', '-2', '-reward', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check if there was an error
    if process.returncode != 0:
        print("Error:", stderr.decode('utf-8'))
        return None

def read_file(file_path):
    # Open the text file in read mode
    with open(file_path, "r") as file:
        # Read the content of the file
        file_content = file.read()

    # Return the content of the file
    return file_content

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/run_blast', methods=['POST'])
def run_blast():
    parameter = request.form['text']
    run_blastn(parameter)
    return read_file('output_file.txt')

if __name__ == '__main__':
    app.run(debug=True)
