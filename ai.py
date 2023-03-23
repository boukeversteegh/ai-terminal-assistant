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

# =============================================================================
# CONFIGURATION
# =============================================================================

# Set up OpenAI API
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define the keyboard controller
kbd = Controller()

# Define ANSI colors
yellow = "\033[93m"
dark_green = "\033[32m"
reset = "\033[0m"
color_comment = dark_green
color_command = yellow

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_system_info():
    os_name = os.name
    platform_system = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    platform_machine = platform.machine()
    platform_processor = platform.processor()
    platform_wsl = os.environ.get('WSL_DISTRO_NAME') is not None

    return f"operating system: {os_name}\n" + \
        f"platform: {platform_system}\n" + \
        f"release: {platform_release}\n" + \
        f"version: {platform_version}\n" + \
        f"machine: {platform_machine}\n" + \
        f"processor: {platform_processor}\n" + \
        f"wsl: {'yes' if platform_wsl else 'no'}"


def get_shell():
    # return first non python parent process, and remove .exe
    for process in psutil.Process(os.getppid()).parents():
        if "python" not in process.name().lower():
            return process.name().lower().replace(".exe", "")


def get_shell_version(shell):
    if shell == "powershell":
        return os.popen("powershell -Command $PSVersionTable.PSVersion").read()
    else:
        return os.popen(f"{shell} --version").read()


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

# =============================================================================
# CHATGPT FUNCTIONS
# =============================================================================


def generate_chat_gpt_messages(user_input):
    shell = get_shell()
    shell_version = get_shell_version(shell)
    system_info = get_system_info()
    working_directory = get_working_directory()
    package_managers = get_package_managers()
    sudo = sudo_available()

    example = "# Show all files (including hidden ones) in the current directory.\nls -lah\n"
    if shell == "powershell":
        example = "# Show all files and folders in the current directory (including hidden ones).\nGet-ChildItem"

    return [
        {"role": "system", "content":
         f"You're a {shell} terminal assistant, and your job is to translate natural language instructions to a single raw, executable {shell} command.\n" +
         "It has to be a single command on one line, or multiple commands spread out over multiple lines (without separators like ; or &&)\n" +
         f"The shell is {shell} {shell_version}.\n"
         f"Give a short explanation in {shell} comments before the command. Use the most human-friendly version of the command.\n" +
         "If you need to use a command that is not available on the system, explain in a comment what it does and suggest to install it.\n" +
         "If the instruction is not clear, use a comment to ask for clarification.\n" +
         "If you need to output a literal string that the user needs to write, which isn't a command or comment, prefix it with #> .\n" +
         "Use cli tools where possible (such as gh, aws, azure).\n" +
         f"The shell is running on the following system:\n" +
         f"{system_info}.\n" +
         f"The user is in the {working_directory} directory.\n" +
         f"If installing a package is required, use one of the following managers: {', '.join(package_managers)}. These are already installed for this user.\n" +
         f"The user has {'sudo' if sudo else 'no'} sudo access.\n"
         },
        {"role": "user", "content": "list files"},
        {"role": "assistant", "content": example},
        {"role": "user", "content": "play a game with me"},
        {"role": "assistant", "content": f"# I'm sorry, but I can only provide you with {shell} commands. I can't play games with you."},
        # {"role": "user", "content": "show me how to add a host name alias for my local ip address"},
        # {"role": "assistant", "content": f"# To add a host name for your local ip, open the hosts file /etc/hosts and add a line as follows\n# 127.0.0.1 youralias.\ncode /etc/hosts"},
        {"role": "user", "content": user_input},
    ]


def get_bash_command(messages):
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
        request_timeout=30
    )

    bash_command = response['choices'][0]['message']['content'].strip()
    return bash_command

# =============================================================================
# MAIN FUNCTION
# =============================================================================


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
            print(
                f"{color_comment}{message['role']}: {message['content']}{reset}")
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
    
    def get_executable_commands(command):
        #return [normalize_command(command) for command in bash_command.splitlines() if not command.startswith('#') and len(normalize_command(command))]
        # rewrite as loop:
        commands = []
        for command in bash_command.splitlines():
            if command.startswith('#'):
                continue
            normalized_command = normalize_command(command)

            if len(normalized_command) > 0:
                commands.append(normalized_command)
        return commands

    executable_commands = get_executable_commands(bash_command)

    for line in bash_command.splitlines():
        if len(line.strip()) == 0:
            continue

        # Print out any comments in yellow
        if line.startswith('#'):
            comment = textwrap.fill(
                line, width=80, initial_indent='  ', subsequent_indent='  ')
            print(f"{color_comment}{comment}{reset}")
        # Print out the executable command in yellow, if there are multiple commands
        elif len(line) and len(executable_commands) > 1:
            print(f"  {color_command}{line}{reset}")

    sys.stdout.flush()

    type_commands(executable_commands)


def type_commands(executable_commands):
    # powershell
    if get_shell() == 'powershell':
        # if its a single command, just type it
        if len(executable_commands) == 1:
            pyautogui.typewrite(executable_commands[0])
            return

        # Wrap everything in the Do alias
        pyautogui.typewrite("AiDo {\n")
        for command_index, command in enumerate(executable_commands):
            pyautogui.typewrite(command)
            pyautogui.typewrite("\n")
        pyautogui.typewrite("}")
    else:
        for command_index, command in enumerate(executable_commands):
            pyautogui.typewrite(command)
            if command_index < len(executable_commands) - 1 and not command.endswith('\\'):
                pyautogui.typewrite(" && \\\n")


if __name__ == "__main__":
    main()
