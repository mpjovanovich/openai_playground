import argparse
import openai
import os


SYSTEM_PROMPT = '''
I'm a college processor writing an exam for an intro level computing logic course. 
I will prompt with a question that I would like to appear on the exam. 
The system shall output four multiple choice answers to this question, only one of which is correct. 
The correct answer shall be marked with an asterisk (*). 
Answers shall be approriate for a first year college course.
The system shall also output a rationale for why the correct answer is correct. The rationale shall be a sentence or two long.
'''
conversation = [
	## Provide the model with a high level context.
    {"role": "system", "content": SYSTEM_PROMPT},
]

## Get initial message from user.
question = input( 'Question: ' )
while question != 'exit' and question != 'quit':
    ## Add new user message to end of conversation.
    conversation.append(
    {
        "role": "user", 
        "content": question
    })

    ## Query the API
    ## Change the model to whatever you want to use.
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        temperature=0.1, #default
        messages=conversation
    )

    ## Save response and print
    message = chat_completion.choices[0].message
    conversation.append(message);
    print(message.content)

    ## Get next input
    question = input( 'Question: ' )