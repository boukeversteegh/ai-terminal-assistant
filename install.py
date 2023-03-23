import os
import re
import sys

import psutil


def get_shell():
    # return first non python parent process, and remove .exe
    for process in psutil.Process(os.getppid()).parents():
        if "python" not in process.name().lower():
            return process.name().lower().replace(".exe", "")


# Determine AI_TERMINAL_ASSISTANT_HOME based on the current python script location (full path)
def get_assistant_home():
    return os.path.dirname(os.path.realpath(__file__))


shell = get_shell()


def confirm(template, path):
    # Let user check and confirm
    yellow = "\033[93m"
    reset = "\033[0m"
    print(yellow + template + reset)
    print("The above functions will be merged into your PowerShell profile:")
    print(f"  {yellow}{path}{reset}")
    print("Press enter to continue, or Ctrl+C to cancel.")
    input()


if shell == "powershell":
    # Log
    print("Installing PowerShell profile...")

    # Read the $PROFILE variable with powershell
    profile_path = os.popen("powershell -Command $PROFILE").read().strip()

    # Read the profile content
    profile_content = open(profile_path, "r").read()


    # Use regex replace to remove function ai {...} and AiDo from the profile
    def remove_function(text, function_name):
        return re.sub(r"function " + function_name + r" {.*?^}\s*", "", text,
                      flags=re.DOTALL | re.MULTILINE)


    profile_content = remove_function(profile_content, "ai")
    profile_content = remove_function(profile_content, "AiDo")

    # Append content from the template to the profile
    profile_content_template_path = os.path.join(get_assistant_home(), "setup/Microsoft.PowerShell_profile.ps1")
    profile_content_template = open(profile_content_template_path, "r").read()
    profile_content_template = profile_content_template.replace("$AI_TERMINAL_ASSISTANT_HOME", get_assistant_home())

    confirm(profile_content_template, profile_path)

    profile_content += '\n' + profile_content_template

    # Write the profile content back to the profile
    open(profile_path, "w").write(profile_content)

elif shell == "bash":
    # Log
    print("Installing Bash profile...")

    # Support colors in Windows Terminal
    os.system('')

    # Read the .bash_profile file
    profile_path = os.path.expanduser("~/.bash_profile")
    profile_content = open(profile_path, "r").read()

    # Use regex replace to remove function ai() {...} from the profile
    profile_content = re.sub(r"function ai\(\) {.*?^}\s*", "", profile_content,
                             flags=re.DOTALL | re.MULTILINE)

    # Append content from the template to the profile
    # use / instead of \ in Windows path
    assistant_home = get_assistant_home().replace("\\", "/")

    profile_content_template_path = os.path.join(assistant_home, "setup/bash_profile.sh")
    profile_content_template = open(profile_content_template_path, "r").read()
    profile_content_template = profile_content_template.replace("$AI_TERMINAL_ASSISTANT_HOME", assistant_home)

    # Let user check and confirm
    confirm(profile_content_template, profile_path)

    profile_content += '\n' + profile_content_template

    # Write the profile content back to the profile
    open(profile_path, "w").write(profile_content)
else:
    print("Unsupported shell:", shell)
    sys.exit(1)