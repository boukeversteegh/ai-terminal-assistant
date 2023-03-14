import openai
import os
import sys
from pynput.keyboard import Controller
import textwrap
import psutil
import platform

# Set up OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get System Information
def get_system_info():
    os_name = os.name
    platform_system = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    platform_machine = platform.machine()
    platform_processor = platform.processor()
    return f"{os_name} {platform_system} {platform_release} {platform_version} {platform_machine} {platform_processor}"

def get_shell():
    parent_process = psutil.Process(os.getppid())
    return parent_process.name().lower().replace(".exe", "")

# Define a function to generate the prompt
def generate_chat_gpt_messages(user_input):
    system_info = get_system_info()
    shell = get_shell()

    return [
        {"role": "system", "content":
         f"Your a {shell} terminal assistant, and your job is to translate natural language instructions to a single {shell} command\n" + 
         "It has to be a single command, but can be multiple lines, as long as the line endings are properly escaped).\n"+
         f"Give a short explanation in {shell} comments before the command. Use the most human-friendly version of the command.\n"+
         "If you need to use a command that is not available on the system, use a comment to explain what it does.\n" +
         "If the instruction is not clear, use a comment to ask for clarification.\n"+
         "Use cli tools where possible (such as gh, aws, azure).\n" + 
         f"The user is running {system_info}.\n"},
        {"role": "user", "content": "list files"},
        {"role": "assistant", "content": "# Show all files (including hidden ones) in the current directory.\nls -lah"},
        {"role": "user", "content": "play a game with me"},
        {"role": "assistant", "content": f"# I'm sorry, but I can only provide you with {shell} commands. I can't play games with you."},
        {"role": "user", "content": user_input},
    ]

# Define a function to make a request to ChatGPT 3.5-turbo and parse the response
def get_bash_command(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    bash_command = response['choices'][0]['message']['content'].strip()
    return bash_command

# Define the keyboard controller
kbd = Controller()

# Define ansi colors
yellow = "\033[93m"
dark_green = "\033[32m"
reset = "\033[0m"
color_comment = dark_green

def main():
    if len(sys.argv) != 2:
        print("Usage: python ai.py \"<natural language command>\"")
        sys.exit(1)
    
    user_input = sys.argv[1]

    os.system('')
    print(f"{color_comment}🤖 Thinking ...{reset}", end='')
    sys.stdout.flush()

    messages = generate_chat_gpt_messages(user_input)
    bash_command = get_bash_command(messages)
    # Overwrite the "thinking" message
    print(f"\r{' ' * 80}\r", end='')
    os.system('')
    print('🤖 ', end='')
    executable_commands = []
    for line in bash_command.splitlines():  
        if line.startswith('#'):
            # Print out any comments in yellow
            comment = textwrap.fill(line.lstrip('#').strip(), width=80)
            print(f"{color_comment}{comment}{reset}")
        else:
            executable_commands.append(line)

    sys.stdout.flush()

    # Simulate typing the executable commands, separated by ;
    kbd.type(";".join(executable_commands))

if __name__ == "__main__":
    main()