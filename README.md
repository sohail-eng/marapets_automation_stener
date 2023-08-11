# Title

### Marapets Automation Tool

# Description

This tool is used to automate the Marapets, just few more description will be writen by another developer. . .

# Install Python

[Follow this link to download python](https://www.python.org/downloads/)

# Install pip

[follow this link to install pip](https://pip.pypa.io/en/stable/installation/)

# Create Virtual Environment

```commandline
python -m venv venv
```

Windows

```commandline
./venv/Scripts/activate
```

Linux

```commandline
source venv/bin/activate
```

[Follow this link if you face any problem](https://realpython.com/lessons/creating-virtual-environment/)

# Install Requirements

```commandline
bash ./setup.sh
```

# Run Project

```commandline
python main.py
```

## Note

for the very first time, you need to enter username and password on the console. after successful login, it will login
automatically whenever you run it again until the credential fails. if you wanna change username password,
delete `creds_cookie.pkl` file from project directory and then run the project again, it will ask for the new username
and password
