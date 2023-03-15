# AI Terminal Assistant

AI Terminal Assistant is a command-line tool that allows you to interact with your terminal using natural language. It leverages the power of OpenAI's GPT-3.5-turbo model to convert your natural language instructions into shell commands for Bash and PowerShell.

## Features

- Translate natural language instructions into Bash or PowerShell commands
- Provide human-friendly explanations in the form of comments
- Automatically type the generated commands into the terminal
- Cross-platform support for Bash and PowerShell

## Setup

1. Clone the repository:

```
bash
git clone https://github.com/boukeversteegh/ai-terminal-assistant.git
cd ai-terminal-assistant
```

1. Install the required dependencies:

```
bash
pip install -r requirements.txt
```

1. Set up your OpenAI API key as an environment variable:

```
bash
export OPENAI_API_KEY="your_api_key_here"
```

For PowerShell, use the following command:

```
powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

### Bash

To set up the AI Terminal Assistant alias for Bash, add the following function to your `.bashrc` or `.bash_profile` file:

```
bash
function ai() {
  python /path/to/ai-terminal-assistant/ai.py "$*"
}
```

Replace `/path/to/ai-terminal-assistant` with the actual path to the `ai-terminal-assistant` folder.

After adding the function, restart your terminal or run `source ~/.bashrc` (or `source ~/.bash_profile`).

### PowerShell

To set up the AI Terminal Assistant alias for PowerShell, add the following function to your PowerShell profile:

```
powershell
function ai {
  python C:\path\to\ai-terminal-assistant\ai.py ($args -join ' ')
}
```

Replace `C:\path\to\ai-terminal-assistant` with the actual path to the `ai-terminal-assistant` folder.

After adding the function, restart your PowerShell session or run `. $profile`.

## Usage

To use the AI Terminal Assistant, type the `ai` command followed by your natural language instruction:

```
bash
ai list all files in the current directory
```

The AI Terminal Assistant will generate a shell command based on your instruction and automatically type it into your terminal.

## Examples

### Bash

```shell
$ ai find files containing the text hello world
# 🤖 Search for files containing the text "hello world" recursively in the current directory.
$ grep -rli "hello world" .
```

```shell
$ ai list files by size
# 🤖 List all files in the current directory sorted by size (largest to smallest).
$ ls -lS
```

```shell
$ ai compress all png files in the current directory
# 🤖 Compress all PNG files in the current directory using tar and gzip.
$ tar -czf png_files.tar.gz *.png
```

### PowerShell

```powershell
PS C:\Users\Anonymous> ai how much free disk space in mb?
# 🤖 Display the amount of free disk space in MB for the C: drive.
PS C:\Users\Anonymous> (Get-PSDrive -PSProvider 'FileSystem').Free/1MB
6379.5546875
```

## Contributing

We welcome contributions from the community! Whether it's bug fixes, improvements, new features, or anything else that can enhance the AI Terminal Assistant, we would love to have you on board.

Here are some ways you can contribute:

    Report bugs and issues
    Suggest improvements or new features
    Contribute to the codebase by fixing bugs or implementing new features
    Help with testing and documentation
    Share your feedback and experiences using the AI Terminal Assistant

## Limitations

Please note that while AI Terminal Assistant aims to provide accurate and useful shell commands, it relies on an AI model that may occasionally produce incorrect or unexpected output. Always review the generated commands and comments before executing them, especially when using commands that could modify or delete important data.