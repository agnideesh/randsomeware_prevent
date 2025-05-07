# Ransomware Attack Simulation and Recovery System

![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Educational](https://img.shields.io/badge/purpose-educational-orange)

A comprehensive, **educational ransomware simulation** and **recovery toolkit** written in Python. This project allows cybersecurity students, professionals, and educators to safely explore how **ransomware attacks** work, how real-time **security monitoring** can detect and halt them, and how encrypted files can be **recovered**—all in a controlled environment.

> ⚠️ **IMPORTANT**: This tool is for **educational purposes ONLY**. Never use it on production systems or without proper authorization.

## 📋 Table of Contents

- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Screenshots](#-screenshots)
- [Detailed Usage](#-detailed-usage)
- [Why This Project?](#-why-this-project)
- [Security Considerations](#-security-considerations)
- [Frequently Asked Questions](#-frequently-asked-questions)
- [License](#-license)

## ✨ Features

- 🔒 **Complete Ransomware Simulation Environment**
  - Realistic attack simulation with XOR encryption
  - Automatic creation of ransom notes and encrypted file tracking
  - Detailed logging and statistics during attack and recovery
  
- 🛡 **Advanced Security Monitoring**
  - Real-time directory monitoring with watchdog
  - Suspicious file operation detection
  - Automatic system lockdown
  - Windows workstation protection (locks screen on attack detection)
  
- 🔄 **Comprehensive Recovery Tools**
  - One-click file restoration 
  - Recovery statistics and progress tracking
  - Cleanup of attack artifacts
  
- 🎮 **Unified Control Interface**
  - Menu-driven operation of all components
  - Status monitoring and reporting
  - Process management

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   main_controller.py                     │
│                                                         │
│              Central Command & Control                   │
└───────────────┬─────────────────┬─────────────────┬─────┘
                │                 │                 │
                ▼                 ▼                 ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ security_monitor.py │ │ attack_agent.py │ │   recovery.py   │
│                     │ │                 │ │                 │
│  • File monitoring  │ │  • Encryption   │ │  • Decryption   │
│  • Threat detection │ │  • Ransom notes │ │  • File recovery│
│  • System lockdown  │ │  • Manifests    │ │  • Statistics   │
└─────────────────────┘ └─────────────────┘ └─────────────────┘
```

## 📥 Installation

### Prerequisites

- Python 3.6 or higher
- Windows (recommended), macOS, or Linux

### Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ransomware-simulation-system.git
   cd ransomware-simulation-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Quick Start

1. **Create a test directory** with sample files (NEVER use important data)

2. **Run the main controller**
   ```bash
   python main_controller.py
   ```

3. **Start the security monitor** (option 2) on your test directory

4. **Launch an attack simulation** (option 3) on the same directory

5. **Observe the detection and system lockdown**

6. **Recover your files** (option 4)

## 📸 Screenshots

### Main Controller Interface
![Main Controller](screenshots/main-controller.png)
*The central command interface for managing all system components*

### Attack Simulation
![Attack in Progress](screenshots/attack-simulation.png)
*A ransomware attack in progress, encrypting files and creating a manifest*

### Security Monitor Alert
![Security Alert](screenshots/security-alert.png)
*The security monitor detecting suspicious activity and triggering a lockdown*

### Recovery Process
![Recovery Process](screenshots/recovery-process.png)
*File recovery in progress, restoring encrypted files to their original state*

## 📖 Detailed Usage

### Running Components Together (Recommended)

The main controller provides a unified interface:

```bash
python main_controller.py
```

### Running Components Separately (Advanced)

For more advanced testing, run components in separate terminals:

**Terminal 1: Security Monitor**
```bash
python security_monitor.py C:\path\to\test\folder
```

**Terminal 2: Attack Simulation**
```bash
python attack_agent.py C:\path\to\test\folder
```

**Terminal 3: Recovery**
```bash
python recovery.py C:\path\to\test\folder
```

See `guide.txt` for more detailed instructions.

## 🔍 Why This Project?

This project was created to help cybersecurity professionals, students, and educators understand:

1. **How ransomware works** - The encryption process, file targeting, and ransom demands
2. **Detection strategies** - Identifying suspicious file operations in real-time
3. **Recovery procedures** - Restoring systems after an attack
4. **Defensive measures** - How security monitoring can prevent full system compromise

By providing a safe, controlled environment to observe these processes, we aim to improve ransomware preparedness and response capabilities.

## 🔐 Security Considerations

- **ONLY** use in a controlled, isolated environment
- **NEVER** run on systems containing important data
- **ALWAYS** create backups before testing
- **DO NOT** modify the code to use stronger encryption
- Consider running in a virtual machine for additional isolation

## ❓ Frequently Asked Questions

### Is this actual ransomware?
No. While it simulates ransomware behavior, it uses a simple XOR encryption with a hardcoded key ("duck") that's visible in the code. Real ransomware uses much stronger encryption, remote key management, and is designed to be difficult to reverse.

### Is this legal to use?
Yes, when used for legitimate educational and research purposes in environments you own or have permission to test in. Never use on unauthorized systems.

### Can this help me understand real ransomware attacks?
Yes. While simplified, this simulation demonstrates core concepts of how ransomware targets files, encrypts them, creates ransom notes, and manages recovery keys.

### Will this work on my operating system?
The system is fully functional on Windows. Linux and macOS are supported but won't have the workstation locking feature.

### How can I contribute to this project?
Contributions are welcome! Please feel free to submit a pull request with improvements or additional features.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Created for educational purposes. Stay cyber-safe!** 