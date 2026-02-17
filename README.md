## 📑 Contents

- [Overview](#-jericho--secure-login-monitor)
- [Features](#️-features)
- [Dependencies](#-dependencies)
- [Setup](#️-setup)
  - [Set Login Password](#-set-login-password)
  - [Set Telegram Bot Token](#-set-telegram-bot-token)
  - [Set Telegram Chat ID](#-set-telegram-chat-id)
  - [Creating the Windows .exe File](#-creating-the-windows-exe-file)
  - [Add Jericho to Windows Task Scheduler](#-add-jericho-to-windows-task-scheduler)
- [Modifications](#-modifications)

---

# 🔐 Jericho – Secure Login Monitor

Jericho is a **desktop security utility** that prompts for a password at startup.  
If an **incorrect password** is entered (or the time expires), it:

- 🚨 Sends an **unauthorized login alert** via **Telegram**
- 📸 Captures an image from the **webcam**
- 🕒 Logs the **timestamp** of the attempt

If the correct password is entered, a **welcome screen** is displayed.

This tool is ideal for:

- Personal laptop security
- Silent login monitoring
- Windows Task Scheduler–based startup protection

---


## ⚙️ Features

- ⏳ Password entry timeout (default: **30 seconds**)
- 👁️ Show / hide password toggle
- 📡 Internet availability check before alerting
- 🤖 Telegram bot integration
- 📷 Webcam capture on unauthorized attempt
- 🔐 Secure credential storage using **Windows Credential Manager**
- 🧊 Packaged as a **single EXE** using PyInstaller

---

## 🧩 Dependencies

Install **Python 3.9 or later**, then install required packages:

```bash
pip install customtkinter requests keyring pillow opencv-python
```

### Telegram Requirements

Jericho requires a Telegram bot to send login alerts and images.

- <a href="https://core.telegram.org/bots/tutorial">Guide to create a Telegram bot</a>  
- <a href="https://gist.github.com/nafiesl/4ad622f344cd1dc3bb1ecbe468ff9f8a#how-to-get-telegram-bot-chat-id">Guide to obtain a Telegram Chat ID</a>  
  

## ⚙️ Setup

Jericho securely stores credentials using **Windows Credential Manager** via the `keyring` library.  
These steps need to be done **once** before running the app or creating the `.exe`.

> **Note: Re-run the respective commands below to update any credentials**

### 1️⃣ Set Login Password

```python
import keyring
keyring.set_password("LN_APP", "PASSKEY", "your_password_here")
```

This is the password required when Jericho starts.

### 2️⃣ Set Telegram Bot Token

```python
import keyring
keyring.set_password("Jericho", "BOT_TOKEN", "your_telegram_bot_token")
```

Use the token obtained from BotFather here.

### 3️⃣ Set Telegram Chat ID

```python
import keyring
keyring.set_password("Jericho", "CHAT_ID", "your_telegram_chat_id")
```

### 4️⃣ Creating the Windows `.exe` File

> Follow the steps below to package Jericho as a standalone Windows executable.
>
> #### Install PyInstaller
>
> ```bash
> pip install pyinstaller
> ```
>
> #### Build the Executable
>
>Run the following command from the src directory:
>
> ```bash
> pyinstaller --onefile --noconsole ^
> --add-data "Jericho.PNG;." ^
> --add-data "show.png;." ^
> --add-data "hide.png;." ^
> main.py
> ```
>
> #### Locate the Executable
>
> After a successful build, the executable will be available at:
>
>> dist/main.exe
>
>
> You may rename it if required, for example:
>
>> Jericho.exe

### 5️⃣ Add Jericho to Windows Task Scheduler
>
>Follow these steps to run Jericho automatically at system startup or user login using **Windows Task Scheduler**.
>
>---
>
>#### Open Task Scheduler
>
> - Press **Win + R**
> - Type `taskschd.msc`
> - Press **Enter**
>
>---
>
>#### Create a New Task
>
>- Click **Create Task**
>- Name: `Jericho Security Monitor`
>- Check: ✅ **Run with highest privileges**
>
>---
>
>#### Configure Trigger
>
>- Go to the **Triggers** tab
>- Click **New**
>- **Begin the task:** `At log on`
>- Select: `Any user` or your specific user account
>- Click **OK**
>
>---
>
>#### Configure Action
>
>- Go to the **Actions** tab
>- Click **New**
>- **Action:** `Start a program`
>- **Program/script:** C:\Path\To\Jericho.exe
>
>---
>
>#### Conditions & Settings
>
>- Disable AC power restrictions
>- Disable auto-stop on long runtime
>- Allow task to run on demand
>- Add timeout for this task in the task scheduler

## 🛠 Modifications

You can customize Jericho by updating the following parameters in `main.py`:

- **`WAIT_TIME`** – Time (in seconds) allowed to enter the password  
- **`WELCOME_TIME`** – Duration (in seconds) of the welcome screen  
- **Camera Source** – Change `cv2.VideoCapture(0)` if using a different webcam  
- **UI Theme** – Modify `ctk.set_appearance_mode("system")` to `"dark"` or `"light"`  

Save the file and rebuild the `.exe` after making changes.

---

<a href="https://www.flaticon.com/free-icons/bot" title="bot icons">Bot icons created by Smashicons - Flaticon</a>