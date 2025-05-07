# 🔒 Ultimate Ransomware Simulator: Attack, Detection & Recovery System

![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Educational](https://img.shields.io/badge/purpose-educational-orange)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)

> **LOOKING FOR A RANSOMWARE SIMULATOR?** This project offers a comprehensive educational ransomware simulation tool featuring real-time detection, Windows workstation lockdown, and file recovery capabilities - all in ONE system!

The most complete open-source **ransomware simulation toolkit** for cybersecurity education and testing. Unlike other simulators, this project provides a full-cycle experience: realistic **attacks**, active **defense monitoring**, system **lockdown**, and complete **recovery** - making it perfect for security training, awareness programs, and defense validation.

> ⚠️ **EDUCATIONAL USE ONLY**: This simulator helps understand ransomware attack vectors, detection strategies and recovery procedures in a controlled environment. Never deploy on production systems.

## 🌟 What Makes This Tool Different?

Most ransomware simulators only perform encryption. Our system provides:

| Feature | This Tool | Other Simulators |
|---------|-----------|------------------|
| **Realistic Encryption** | ✅ Yes | ✅ Yes |
| **Real-time Detection** | ✅ Yes | ❌ No |
| **Active Defense** | ✅ Yes | ❌ No |
| **Windows Lockdown** | ✅ Yes | ❌ No |
| **Full Recovery** | ✅ Yes | ❌ Partial/No |
| **Unified Interface** | ✅ Yes | ❌ No |
| **Detailed Logging** | ✅ Yes | ❌ Limited |
| **Multi-Platform** | ✅ Yes | ❌ Varies |

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

- 🔒 **Complete Ransomware Attack Simulation**
  - XOR encryption with monitored progress
  - Ransom note creation with customizable messages
  - Manifest tracking of encrypted files
  - Realistic attack progression indicators
  
- 🛡 **Advanced Security Monitoring System**
  - Real-time directory monitoring using watchdog
  - ML-like detection of suspicious encryption patterns
  - Automatic system lockdown when attack detected
  - Windows workstation protection (locks screen on attack)
  
- 🔄 **Comprehensive Recovery Tools**
  - One-click file restoration with integrity verification
  - Detailed recovery statistics and reporting
  - Clean removal of attack artifacts
  - Automatic manifest processing
  
- 🎮 **Centralized Control Interface**
  - Menu-driven operation for all components
  - Status monitoring dashboard
  - Process management for background services
  - Command history and activity logging

## 🔥 Use Cases for Cybersecurity Professionals

1. **Security Team Training**
   - Simulate ransomware incidents for incident response training
   - Practice detection and containment procedures
   - Test recovery strategies and backup systems

2. **Security Control Validation**
   - Evaluate endpoint protection effectiveness
   - Test file monitoring and alerting systems
   - Validate security monitoring tools

3. **Awareness Programs**
   - Demonstrate ransomware impact safely
   - Educate users on detection signs
   - Show protection measures in action

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
- Windows (recommended for full functionality), macOS, or Linux

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

This project fills a critical gap in cybersecurity education and testing. While many standalone ransomware simulators exist, few provide the complete attack lifecycle with defensive capabilities. Our system offers:

1. **Realistic Attack Simulation** - The encryption process, file targeting, and ransom demands
2. **Active Defense Monitoring** - Real-time detection of suspicious file operations 
3. **Automated Response** - System lockdown and workstation protection
4. **Comprehensive Recovery** - Complete file restoration and system cleanup

Security professionals can use this system to improve ransomware preparedness, test detection systems, and practice recovery procedures in a controlled environment.

## 🛡️ Technical Implementation

- **Encryption**: XOR-based encryption with manifest tracking
- **Detection**: Watchdog-powered file system monitoring with threshold-based alerting
- **Protection**: Windows API lockdown via user32.dll LockWorkStation
- **Recovery**: Key-based decryption with verification and cleanup

## 🔐 Security Considerations

- **ONLY** use in a controlled, isolated environment
- **NEVER** run on systems containing important data
- **ALWAYS** create backups before testing
- **DO NOT** modify the code to use stronger encryption
- Consider running in a virtual machine for additional isolation

## ❓ Frequently Asked Questions

### How is this different from other ransomware simulators?
Unlike most simulators that only encrypt files, our system provides the full ransomware experience: attack, detection, protection, and recovery. The real-time security monitoring and Windows workstation lockdown features make this a uniquely comprehensive educational tool.

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

## 🔍 Keywords

ransomware, ransomware simulator, encryption simulator, cybersecurity training, security monitoring, ransomware detection, file recovery, incident response training, security tools, python security, educational hacking, penetration testing, red team tools, blue team training, ransomware protection, XOR encryption, security simulation

---

**Created for educational purposes. Stay cyber-safe!** 