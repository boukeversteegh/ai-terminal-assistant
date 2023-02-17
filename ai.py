import openai
import os
import sys

# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define a function that uses GPT-3 to generate a Bash command based on natural language input
def translate_to_bash(instruction):
    prompt = "Translate the following natural language instruction to a Bash command: " + instruction + "\n\nBash command:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    # print(response)
    if response.choices[0].finish_reason == "error":
        raise ValueError("OpenAI API returned an error: " + response.choices[0].text)
    return response.choices[0].text.strip()


# Define a shell function that prompts the user for an instruction and generates a Bash command using GPT-3
def run(instruction):
    try:
        command = translate_to_bash(instruction)
        print(f"\033[36m{command}\033[0m", end='')
        input()
    except KeyboardInterrupt:
        print()
        print(f"\033[33m{'(cancelled)'}\033[0m")
        sys.exit(1)
    os.system(command)
    

# Define a main function that reads the natural language prompt from the command line arguments
def main():
    os.system('')
    instruction = " ".join(sys.argv[1:])
    run(instruction)

# Call the main function when the script is executed
if __name__ == "__main__":
    main()