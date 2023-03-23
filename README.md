# 🤖 AI Terminal Assistant

AI Terminal Assistant is a command-line tool that allows you to interact with your terminal using natural language. It leverages the power of OpenAI's GPT-3.5-turbo model to convert your natural language instructions into shell commands for Bash and PowerShell.

## Features

- Translate natural language instructions into Bash or PowerShell commands
- Provide human-friendly explanations in the form of comments
- Automatically type the generated commands into the terminal
- You can edit the command before executing, or cancel with ctrl+c
- Suggested commands fully integrated in the terminal, bash expansion, history, pipes, etcetera
- Cross-platform support for Bash and PowerShell

## Examples

### Bash

```bash
$ ai find files containing the text hello world
# 🤖 Search for files containing the text "hello world" recursively in the current directory.
$ grep -rli "hello world" .
```

```bash
$ ai list files by size
# 🤖 List all files in the current directory sorted by size (largest to smallest).
$ ls -lS
```

```bash
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

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/boukeversteegh/ai-terminal-assistant.git
    cd ai-terminal-assistant
    ```
1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
1. Set up your OpenAI API key as an environment variable:
    ```bash
    export OPENAI_API_KEY="your_api_key_here"
    ```

    For PowerShell, use the following command:

    ```powershell
    $env:OPENAI_API_KEY = "your_api_key_here"
    ```

### Set up the `ai` alias

```shell
python install.py
```

Restart your terminal to use the `ai` alias.

## Usage

To use the AI Terminal Assistant, type the `ai` command followed by your natural language instruction:

```shell
$ ai list all files in the current directory
```

The AI Terminal Assistant will generate a shell command based on your instruction and automatically type it into your terminal.

You can also pipe additional context to the AI through the use of stdin, for example:

```shell
$ ls | ai organize these files semantically
🤖
  # Based on the file names, I suggest the following directory structure:
  mkdir Documents Media Pictures Programs
  mkdir Documents/Work Documents/Personal
  mkdir Media/Movies Media/TV\ Shows Media/Videos Media/Music
  mkdir Pictures/Family Pictures/Vacation Pictures/Wedding
  mkdir Programs/Installers Programs/Cracks Programs/Extensions
  # Then, move each file to its appropriate directory.
  mv Resume.pdf Documents/Work/
  mv Data_Analysis_Report.docx Documents/Work/
  mv Python_Tutorial.pdf Documents/Work/
  mv Tax_Return_2022.pdf Documents/Personal/
  mv Webinar_Slides.pptx Documents/Work/
  mv Invoice_12345.pdf Documents/Work/
  mv Birthday_Party_Invite.docx Documents/Personal/
  mv eBook_Title.epub Documents/Personal/
  mv Mobile_App_Prototype.sketch Documents/Work/
  mv Unsorted_Notes.txt Documents/Work/
  mv Budget_Spreadsheet.xlsx Documents/Work/
  mv Business_Proposal.docx Documents/Work/
  mv House_Plans.pdf Documents/Personal/
  mv Financial_Statement_Q3.pdf Documents/Work/
  mv Movie_Title_720p.mkv Media/Movies/
  mv TV_Show_S01E01.mkv Media/TV\ Shows/
  mv Cat_Video.mp4 Media/Videos/
  mv Travel_Vlog.mp4 Media/Videos/
  mv Music_Album.zip Media/Music/
  mv Article_Title.pdf Pictures/
  mv Family_Reunion.jpg Pictures/Family/
  mv Vacation_Photos.zip Pictures/Vacation/
  mv Wedding_Photos.tar.gz Pictures/Wedding/
  mv Desktop_Wallpaper.png Pictures/
  mv Game_Title_Setup.exe Programs/Installers/
  mv setup_software.exe Programs/Installers/
  mv Browser_Setup.dmg Programs/Installers/
  mv Software_Crack.zip Programs/Cracks/
  mv Browser_Extension.crx Programs/Extensions/
  # I'm assuming that random_file.tmp is not important, so it can be deleted.
  rm random_file.tmp

$ mkdir Documents && \
> mv Resume.pdf Data_Analysis_Report.docx Python_Tutorial.pdf Tax_Return_2022.pdf \Webinar_Slides.pptx eBook_Title.epub Article_Title.pdf Business_Proposal.docx \House_Plans.pdf Financial_Statement_Q3.pdf Budget_Spreadsheet.xlsx Documents/ && \
> mkdir Photos && \
> mv Vacation_Photos.zip Family_Reunion.jpg Wedding_Photos.tar.gz Photos/ && \
> mkdir Videos && \
```

## Contributing

We welcome contributions from the community! Whether it's bug fixes, improvements, new features, or anything else that can enhance the AI Terminal Assistant, we would love to have you on board.

Here are some ways you can contribute:

- Report bugs and issues

- Suggest improvements or new features
- Contribute to the codebase by fixing bugs or implementing new features
- Help with testing and documentation
- Share your feedback and experiences using the AI Terminal Assistant

## Limitations

Please note that while AI Terminal Assistant aims to provide accurate and useful shell commands, it relies on an AI model that may occasionally produce incorrect or unexpected output. Always review the generated commands and comments before executing them, especially when using commands that could modify or delete important data.