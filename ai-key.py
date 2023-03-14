import openai
import sys
import time
from pynput.keyboard import Controller
import subprocess
import os

# Set up OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define a function to generate the prompt
def generate_prompt(user_input):
    return f"Translate the following natural language command to a bash/unix command: {user_input}"

# Define a function to make a request to ChatGPT 3.5-turbo and parse the response
def get_bash_command(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    bash_command = response.choices[0].text.strip()
    return bash_command

# Define the keyboard controller
kbd = Controller()

def main():
    if len(sys.argv) != 2:
        print("Usage: python ai.py \"<natural language command>\"")
        sys.exit(1)

    user_input = sys.argv[1]
    prompt = generate_prompt(user_input)
    bash_command = get_bash_command(prompt)
    print(f"Suggested bash command: {bash_command}")

    # Wait for the terminal to return to the command prompt
    time.sleep(1)

    # Simulate typing the generated command
    kbd.type(bash_command + '\n')

if __name__ == "__main__":
    main()
