import argparse
import openai
import os
import PyPDF2

## TODO: Might be worth looking into summarization pipelines
## https://huggingface.co/docs/transformers/tasks/summarization

SYSTEM_PROMPT = '''
The user shall input a document, and the system shall provide a minimum of 10 multiple-choice 
test questions, and 4 fill-in-the-blank questinos for a college exam based on the provided document.
Multiple choice questions may include a fill-in-the-blank component.
Questions shall be separated by a blank line.
Questions shall not be numbered. 
Responses shall not have letters in front.
In the case of multiple choice, the correct response shall be listed first, followed by three incorrect responses. Only the top response shall be correct.

Example multiple choice question and responses:
A subscript / index is a(n) _________.
number that indicates the position of an array element
element in the array
number that represents the highest value stored within an array
alternate name for an array

Example fill-in-the-blank question and responses:
The subscript or position within an array is also called the _________.
index
'''

conversation = [
	## Provide the model with a high level context.
    {"role": "system", "content": SYSTEM_PROMPT},
]

# Note that debugging with launch.json only works if you do the Run > Start Debugging command,
# not if you use the little bug icon.
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', type=str, required=True)
parser.add_argument('--output_file', type=str, required=True)
args = parser.parse_args()

print('Reading input file...')
text = ''
if args.input_file.endswith('.pdf'):
    with open(args.input_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            text += page.extract_text()
else:
    with open(args.input_file, 'r') as file:
        text = file.read()

conversation.append({"role": "user", "content": text})

print('Generating quiz...')
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    temperature=0.1, #default
    messages=conversation
)
message = completion.choices[0].message.content

print('Writing output file...')
with open(args.output_file, "w") as text_file:
    text_file.write(message)

print('Output file created.')