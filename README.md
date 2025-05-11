# 📊 StatScience

**StatScience** is a powerful, flexible statistics tracking system designed to let users define and monitor their own custom statistics in real time. Whether you're tracking sales, user growth, productivity metrics, or any stat that matters to *you*, StatScience allows you to graph and get insight into trends and performance using statistical technology.

Originally, I had intended to design it just for myself, but I decided to also allow others to use it for their own purposes.

## 🚀 Features

* 📈 **UNLIMITED CONTROL**: Create and manage custom statistics for your unique needs.
* 🧠 **INTELLIGENT INSIGHT**: Learn what will happen to a statistic in the future and how to improve it.
* ✍️ **INSTANT ACTION**: Enter data on the fly—**no BS external APIs**.
* 🔎 **DEEP INSPECTION**: Dive into the decision of the machine. ***SEE*** what it thinks.
* 📊 **CLEAR VISUALS**: Not only read, but SEE your data with a graph.

## Privacy
StatScience is completely private. Nobody will know anything about anything unless you yourself directly tell them, or you give them access.

## Who's the Target?
This tool is for anyone and anything that needs to keep track of a number, such as:
- Teams that need to report and track metrics consistently
- Projects that need to track how many visitors their website had
- Projects that need a service to keep track of numbers
- Finance workers graphing money in/out
- Workers tracking how much time they've spent working
- Anyone tracking how much of something they've gotten in contrast to how many lost
And ad infinitum!

## 🛠️ Technology Stack

- **Backend**: Django + Python
- **Frontend**: (TBD. Likely just HTML/CSS)
- **Database**: (TBD. PostgreSQL probably)

## 📦 Installation

Windows users, run these commands in POWERSHELL to install
the project. Must have Docker installed.
```powershell
# Download the Windows PowerShell setup script
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Ames-hub/statscience/main/setupscripts/setup.ps1" -OutFile "setup.ps1"

# Then run it
.\setup.ps1
```

Linux users, run these commands in the terminal to install
the project. Must have docker installed.
```bash
# Download the Linux Bash setup script
curl -o setup.bash https://raw.githubusercontent.com/Ames-hub/statscience/main/setupscripts/setup.bash

# Make it executable and run it
chmod +x setup.bash
./setup.bash
```

You may have to delete the leftover file called "setup.bash" or "setup.ps1" 
