# 📊 StatScience

**StatScience** is a powerful, flexible statistics tracking system designed to let users define and monitor their own custom statistics in real time. Whether you're tracking sales, user growth, productivity metrics, or any stat that matters to *you*, StatScience gives you insight into trends and performance using statistical technology.

## 🚀 Features

* 📈 **UNLIMITED CONTROL**: Create and manage custom statistics for your unique needs.
* 🧠 **INTELLIGENT INSIGHT**: Harness the power of statistical conditions technology.
* ✍️ **INSTANT ACTION**: Enter data on the fly—**no BS external APIs**.
* 🔎 **DEEP INSPECTION**: Dive into the decision of the machine. ***SEE*** what it thinks.
* 📊 **CLEAR VISUALS**: Not only read, but SEE your data with a graph.

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
