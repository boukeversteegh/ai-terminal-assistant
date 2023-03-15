import io
import re
import openai
import os
import sys
from pynput.keyboard import Controller
import textwrap
import psutil
import platform
import shutil
import time
import pyautogui

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

def get_working_directory():
    return os.getcwd()

def get_last_commands():
    return os.popen('history').read()

def get_package_managers():
    package_managers = [
        "pip",
        "conda",
        "npm",
        "yarn",
        "gem",
        "apt",
        "dnf",
        "yum",
        "pacman",
        "zypper",
        "brew",
        "choco",
        "scoop",
    ]

    installed_package_managers = []

    for pm in package_managers:
        if shutil.which(pm):
            installed_package_managers.append(pm)

    return installed_package_managers

def sudo_available():
    return shutil.which("sudo") is not None

# Define a function to generate the prompt
def generate_chat_gpt_messages(user_input):
    system_info = get_system_info()
    shell = get_shell()
    working_directory = get_working_directory()
    package_managers = get_package_managers()
    sudo = sudo_available()

    return [
        {"role": "system", "content":
         f"You're a {shell} terminal assistant, and your job is to translate natural language instructions to a single raw, executable {shell} command.\n" +
         "It has to be a single command on one line, or multiple commands combined with && (be sure to escape the newline)\n"+
         f"Give a short explanation in {shell} comments before the command. Use the most human-friendly version of the command.\n"+
         "If you need to use a command that is not available on the system, explain in a comment what it does and suggest to install it.\n" +
         "If the instruction is not clear, use a comment to ask for clarification.\n"+
         "Use cli tools where possible (such as gh, aws, azure).\n" + 
         f"The user is running {system_info}.\n"+
         f"The user is in the {working_directory} directory.\n" +
         f"If installing a package is required, use one of the following managers: {', '.join(package_managers)}. These are already installed for this user.\n" +
         f"The user has {'sudo' if sudo else 'no'} sudo access.\n"
         },
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
        max_tokens=1000,
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
color_command = yellow

def main():
    if len(sys.argv) != 2:
        print("Usage: python ai.py \"<natural language command>\"")
        sys.exit(1)

    user_input = sys.argv[1]

    options = []

    # remove flags from the start of the input and add them to the options list
    while user_input.startswith('-'):
        option, user_input = user_input.split(' ', 1)
        options.append(option)
    # Prepend stdin to the user input, if present
    if sys.stdin.isatty():
        pass
    else:
        stdin = sys.stdin.read().strip()
        if len(stdin):
            user_input = f"{user_input}. Use the following additional context to improve your suggestion:\n\n---\n\n{stdin}\n"


    

    os.system('')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    messages = generate_chat_gpt_messages(user_input)

    if '--debug' in options:
        # print the role and content of each message if debugging
        for message in messages:
            print(f"{color_comment}{message['role']}: {message['content']}{reset}")
        sys.exit(0)




    print(f"{color_comment}🤖 Thinking ...{reset}", end='')
    sys.stdout.flush()
    bash_command = get_bash_command(messages)
    # Overwrite the "thinking" message
    print(f"\r{' ' * 80}\r", end='')
    os.system('')
    print('🤖')

    # Get all lines that are not comments    
    def normalize_command(command):
        return re.sub(r'\s*&& \\\s*$', '', command.strip(';').strip())
    
    executable_commands = [normalize_command(command) for command in bash_command.splitlines() if not command.startswith('#') and len(normalize_command(command))]

    for line in bash_command.splitlines():
        if len(line.strip()) == 0:
            continue

        # Print out any comments in yellow
        if line.startswith('#'):
            comment = textwrap.fill(line, width=80, initial_indent='  ', subsequent_indent='  ')
            print(f"{color_comment}{comment}{reset}")
        # Print out the executable command in yellow, if there are multiple commands
        elif len(line) and len(executable_commands)>1:
            print(f"  {color_command}{line}{reset}")

    sys.stdout.flush()

    # print(executable_commands)

    # Simulate typing the executable commands, with index
    for command_index, command in enumerate(executable_commands):
        pyautogui.typewrite(command)
        if command_index < len(executable_commands) - 1 and not command.endswith('\\'):
            pyautogui.typewrite(" && \\\n")

if __name__ == "__main__":
    main()