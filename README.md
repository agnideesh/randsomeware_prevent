

**Ransomware Attack Simulation, Detection, and Recovery System (Python)**

This project is a comprehensive, educational ransomware simulation and recovery toolkit written in Python. It allows cybersecurity students, professionals, and educators to safely explore how ransomware attacks work, how real-time security monitoring can detect and halt them, and how encrypted files can be recovered—all in a controlled environment.

**Features:**
- Realistic ransomware attack simulation (XOR encryption, ransom notes, manifest tracking)
- Real-time security monitor with automatic system lockdown and Windows workstation lock
- Full-featured recovery utility to restore encrypted files and clean up after attacks
- Centralized menu-driven controller for easy operation and demonstration
- Detailed logging for both attack and recovery processes
- Designed for Windows (with partial support for Linux/macOS)

**Educational Use Only:**  
This tool is for learning, research, and demonstration purposes. It is NOT intended for malicious use or deployment on production systems.

**How it works:**
- Start the security monitor to protect a directory
- Simulate a ransomware attack and watch as the system detects and blocks it
- Use the recovery tool to restore your files
- All actions are managed from a single, user-friendly main controller

**Perfect for:**
- Cybersecurity training labs
- Demonstrating ransomware defense strategies
- Teaching file recovery and incident response
- Security awareness workshops

**Requirements:**  
Python 3.6+, `psutil`, `watchdog`

**Get Started:**  
1. Clone the repo  
2. Install dependencies: `pip install psutil watchdog`  
3. Run: `python main_controller.py`  

**Disclaimer:**  
This project is for educational purposes only. The authors are not responsible for misuse or any resulting damage.

---

**Keywords:**  
ransomware, simulation, detection, recovery, cybersecurity, python, security monitor, educational, incident response, file encryption, file recovery, system lockdown, Windows, training, demo


