import openai

OUTPUT_FILE = '/mnt/c/Users/mpjov/Desktop/quiz_generator.txt'
SYSTEM_PROMPT = '''
The user shall input a document, and the system shall provide multiple-choice 
test questions for a college exam based on the provided document.
'''

conversation = [
	## Provide the model with a high level context.
    {"role": "system", "content": SYSTEM_PROMPT},
]

with open('/home/mpjovanovich/git/course_notes/SDEV120/m06.md', 'r') as file:
    data = file.read()
    conversation.append({"role": "user", "content": data})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        temperature=0.1, #default
        messages=conversation
    )
    message = completion.choices[0].message.content
    print(message)
