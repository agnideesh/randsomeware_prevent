# main_controller.py
import os
import sys
import subprocess
import time
import signal
import psutil
from datetime import datetime

# --- Configuration ---
HARDCODED_KEY = "duck"  # Central place for the key
ATTACK_AGENT_SCRIPT = "attack_agent.py"
RECOVERY_UTILITY_SCRIPT = "recovery.py"
SECURITY_MONITOR_SCRIPT = "security_monitor.py"
LOCKDOWN_FLAG_FILE = "system_lockdown.flag"

# --- Process Management ---
security_process = None
security_target_dir = None

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def is_process_running(process):
    """Check if a subprocess is still running."""
    if process is None:
        return False
    
    try:
        # Check if process is still running
        return process.poll() is None
    except:
        return False

def find_monitor_process():
    """Find if security_monitor.py is running as a separate process."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and len(cmdline) > 1 and SECURITY_MONITOR_SCRIPT in cmdline[1]:
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def is_security_monitor_active():
    """Check if the security monitor is running."""
    global security_process
    
    # First check our tracked process
    if security_process and is_process_running(security_process):
        return True
    
    # If our tracked process is not running, search for any security monitor process
    monitor_proc = find_monitor_process()
    if monitor_proc:
        return True
    
    return False

def get_lockdown_status(directory=None):
    """Check if a lockdown is active in the specified directory."""
    if directory and os.path.isdir(directory):
        lockdown_path = os.path.join(directory, LOCKDOWN_FLAG_FILE)
        if os.path.exists(lockdown_path):
            try:
                with open(lockdown_path, 'r') as f:
                    lockdown_info = f.read().strip()
                    return True, lockdown_info
            except:
                return True, "Lockdown active (could not read details)"
    
    # Check the security target directory if one is set
    if not directory and security_target_dir and os.path.isdir(security_target_dir):
        lockdown_path = os.path.join(security_target_dir, LOCKDOWN_FLAG_FILE) 
        if os.path.exists(lockdown_path):
            try:
                with open(lockdown_path, 'r') as f:
                    lockdown_info = f.read().strip()
                    return True, lockdown_info
            except:
                return True, "Lockdown active (could not read details)"
    
    return False, None

def display_main_menu():
    """Display the main menu and get user choice."""
    clear_screen()
    print("Ransomware Advanced Simulation Controller")
    print("=========================================")
    print(f"IMPORTANT: Uses a FIXED internal key: '{HARDCODED_KEY}' for all operations.")
    print("-----------------------------------------")
    
    # Get security monitor status
    security_active = is_security_monitor_active()
    security_status = "ACTIVE - Monitoring" if security_active else "INACTIVE"
    
    # Check if there's a lockdown
    is_locked, lockdown_info = get_lockdown_status()
    if is_locked:
        security_status += " [LOCKDOWN IN EFFECT]"
    
    if security_target_dir:
        print(f"Currently monitoring: {security_target_dir}")
    
    print("Menu:")
    print(f"1. Security Monitor Status: [{security_status}]")
    print(f"2. {'Stop' if security_active else 'Start'} Security Monitor")
    print("3. Launch Ransomware Attack Simulation")
    print("4. Launch Recovery Utility")
    print("5. Clear System Lockdown (if active)")
    print("6. Exit")
    print("-----------------------------------------")
    return input("Enter your choice (1-6): ").strip()

def start_security_monitor():
    """Start the security monitor as a background process."""
    global security_process, security_target_dir
    
    clear_screen()
    print("\n--- Starting Security Monitor ---")
    
    if is_security_monitor_active():
        print("Security Monitor is already running!")
        return
    
    target_dir = input("Enter the directory to monitor for ransomware activity: ").strip()
    if not target_dir or not os.path.isdir(target_dir):
        print("Error: Invalid directory.")
        return
    
    abs_target_dir = os.path.abspath(target_dir)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    if abs_target_dir == script_dir:
        print("Warning: Monitoring the script directory itself may cause false positives.")
        confirm = input("Are you sure you want to monitor this directory? (yes/no): ").lower()
        if confirm != 'yes':
            print("Security Monitor startup aborted.")
            return
    
    print(f"\nStarting Security Monitor to protect: {abs_target_dir}")
    
    try:
        # Start the security monitor as a separate process
        cmd = [sys.executable, SECURITY_MONITOR_SCRIPT, abs_target_dir]
        security_process = subprocess.Popen(cmd)
        security_target_dir = abs_target_dir
        
        time.sleep(2)  # Give it a moment to start
        
        if is_process_running(security_process):
            print("Security Monitor successfully started and is now active!")
            print("It will run in the background and monitor for suspicious encryption activity.")
            print("You can now return to the main menu and launch an attack simulation to test it.")
        else:
            print("Warning: Security Monitor process started but may have terminated.")
            print("Check for errors in security_monitor.log")
    except Exception as e:
        print(f"Error starting Security Monitor: {e}")

def stop_security_monitor():
    """Stop the running security monitor process."""
    global security_process, security_target_dir
    
    print("\n--- Stopping Security Monitor ---")
    
    if not is_security_monitor_active():
        print("No Security Monitor is currently running.")
        return
    
    try:
        # First try with our tracked process
        if security_process and is_process_running(security_process):
            print("Terminating Security Monitor process...")
            
            if os.name == 'nt':  # Windows
                security_process.terminate()
            else:  # Unix-like systems
                os.kill(security_process.pid, signal.SIGTERM)
            
            # Wait a bit for termination
            time.sleep(2)
            
            if not is_process_running(security_process):
                print("Security Monitor successfully stopped.")
                security_process = None
                security_target_dir = None
                return
        
        # If we're here, our tracked process wasn't running or couldn't be terminated
        # Try to find and kill any security monitor processes
        monitor_proc = find_monitor_process()
        if monitor_proc:
            print(f"Found Security Monitor process (PID: {monitor_proc.info['pid']}), terminating...")
            
            try:
                monitor_proc.terminate()
                time.sleep(2)
                if not monitor_proc.is_running():
                    print("Security Monitor successfully stopped.")
                    security_process = None
                    security_target_dir = None
                    return
            except:
                print("Could not terminate the Security Monitor process.")
                print("You may need to terminate it manually from your task manager.")
    except Exception as e:
        print(f"Error stopping Security Monitor: {e}")

def show_security_status():
    """Display detailed information about the Security Monitor's status."""
    clear_screen()
    print("\n--- Security Monitor Status ---")
    
    security_active = is_security_monitor_active()
    if security_active:
        print("Security Monitor is: ACTIVE")
        if security_target_dir:
            print(f"Monitoring directory: {security_target_dir}")
        
        # Check for lockdowns
        is_locked, lockdown_info = get_lockdown_status()
        if is_locked:
            print("\n[!] SYSTEM LOCKDOWN DETECTED [!]")
            print("Lockdown details:")
            print(f"{lockdown_info[:500]}..." if len(lockdown_info) > 500 else lockdown_info)
            print("\nUse menu option 5 to clear the lockdown if needed.")
        else:
            print("No lockdown is currently active.")
    else:
        print("Security Monitor is: INACTIVE")
        print("No active protection is running.")
        
        # Check if there's still a lockdown somewhere
        if security_target_dir:
            is_locked, lockdown_info = get_lockdown_status()
            if is_locked:
                print("\n[!] SYSTEM LOCKDOWN IS STILL ACTIVE [!]")
                print("Even though the monitor is not running, a lockdown is still in effect.")
                print("Use menu option 5 to clear the lockdown if needed.")

def clear_lockdown():
    """Clear a system lockdown by removing the lockdown flag file."""
    clear_screen()
    print("\n--- Clear System Lockdown ---")
    
    # First check if there's a lockdown in the security target directory
    if security_target_dir:
        is_locked, _ = get_lockdown_status()
        if is_locked:
            print(f"Lockdown detected in monitored directory: {security_target_dir}")
            confirm = input("Do you want to clear this lockdown? (yes/no): ").lower()
            if confirm == 'yes':
                try:
                    lockdown_path = os.path.join(security_target_dir, LOCKDOWN_FLAG_FILE)
                    if os.path.exists(lockdown_path):
                        os.remove(lockdown_path)
                        print("Lockdown successfully cleared.")
                    else:
                        print("Lockdown flag file not found.")
                except Exception as e:
                    print(f"Error clearing lockdown: {e}")
            else:
                print("Lockdown clearing aborted.")
            return
    
    # If no lockdown in the security target directory or it's not set, ask for a directory
    print("No lockdown detected in currently monitored directory.")
    target_dir = input("Enter the directory where you want to clear a lockdown: ").strip()
    if not target_dir or not os.path.isdir(target_dir):
        print("Error: Invalid directory.")
        return
    
    abs_target_dir = os.path.abspath(target_dir)
    lockdown_path = os.path.join(abs_target_dir, LOCKDOWN_FLAG_FILE)
    
    if os.path.exists(lockdown_path):
        try:
            os.remove(lockdown_path)
            print(f"Lockdown successfully cleared from: {abs_target_dir}")
        except Exception as e:
            print(f"Error clearing lockdown: {e}")
    else:
        print(f"No lockdown flag found in: {abs_target_dir}")

def launch_attack_simulation():
    """Launch the ransomware attack simulation."""
    clear_screen()
    print("\n--- Launching Ransomware Attack Simulation ---")
    
    target_dir = input("Enter the target directory for the attack: ").strip()
    if not target_dir or not os.path.isdir(target_dir):
        print("Error: Invalid target directory.")
        return
    
    abs_target_dir = os.path.abspath(target_dir)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    if abs_target_dir == script_dir:
        print("Error: Cannot target the script's own directory for safety reasons.")
        return

    # Check if directory is already locked down
    is_locked, lockdown_info = get_lockdown_status(abs_target_dir)
    if is_locked:
        print(f"\n[!] WARNING: Target directory is already in LOCKDOWN state!")
        print("The attack will not be able to proceed if the directory is locked.")
        print(f"Lockdown details: {lockdown_info[:100]}...")
        confirm = input("\nDo you still want to attempt the attack? (yes/no): ").lower()
        if confirm != 'yes':
            print("Attack simulation aborted by user.")
            return
    
    # Check if Security Monitor is active
    security_active = is_security_monitor_active()
    if security_active:
        if security_target_dir and os.path.samefile(abs_target_dir, security_target_dir):
            print("\n[!] NOTE: Security Monitor is ACTIVE and monitoring this directory!")
            print("If the Security Monitor detects the attack, it will lock the system and prevent encryption.")
        else:
            print("\n[!] NOTE: Security Monitor is ACTIVE but monitoring a different directory.")
            print("This attack will NOT be detected by the Security Monitor.")
    else:
        print("\n[!] NOTE: Security Monitor is INACTIVE.")
        print("No protection is active - the attack will be able to encrypt all files.")
    
    print(f"\nTargeting directory: {abs_target_dir}")
    print("This will simulate encrypting files. Original files will be modified/deleted.")
    print("Ensure this is a safe, designated test environment.")

    confirm = input("\nProceed with attack simulation? (yes/no): ").lower()
    if confirm != 'yes':
        print("Attack simulation aborted by user.")
        return
    
    try:
        print("\n[CONTROLLER] Initiating attack agent...")
        cmd = [sys.executable, ATTACK_AGENT_SCRIPT, abs_target_dir]
        process = subprocess.Popen(cmd)
        process.wait()
        print("\n[CONTROLLER] Attack agent has finished.")
    except FileNotFoundError:
        print(f"Error: {ATTACK_AGENT_SCRIPT} not found. Make sure it's in the same directory.")
    except Exception as e:
        print(f"Error launching attack agent: {e}")

def launch_recovery_utility():
    """Launch the recovery utility."""
    clear_screen()
    print("\n--- Launching Recovery Utility ---")
    
    target_dir = input("Enter the target directory for recovery: ").strip()
    if not target_dir or not os.path.isdir(target_dir):
        print("Error: Invalid target directory.")
        return
    
    abs_target_dir = os.path.abspath(target_dir)
    print(f"\nTargeting directory for recovery: {abs_target_dir}")
    confirm = input("\nProceed with recovery? (yes/no): ").lower()
    if confirm != 'yes':
        print("Recovery aborted by user.")
        return
    
    try:
        print("\n[CONTROLLER] Initiating recovery utility...")
        cmd = [sys.executable, RECOVERY_UTILITY_SCRIPT, abs_target_dir]
        process = subprocess.Popen(cmd)
        process.wait()
        print("\n[CONTROLLER] Recovery utility has finished. Check recovery.log for details.")
    except FileNotFoundError:
        print(f"Error: {RECOVERY_UTILITY_SCRIPT} not found. Make sure it's in the same directory.")
    except Exception as e:
        print(f"Error launching recovery utility: {e}")

def main_loop():
    """Main control loop for the application."""
    while True:
        choice = display_main_menu()
        
        if choice == '1':
            show_security_status()
        elif choice == '2':
            if is_security_monitor_active():
                stop_security_monitor()
            else:
                start_security_monitor()
        elif choice == '3':
            launch_attack_simulation()
        elif choice == '4':
            launch_recovery_utility()
        elif choice == '5':
            clear_lockdown()
        elif choice == '6':
            print("\nExiting Ransomware Advanced Simulation Controller.")
            
            # Confirm if we should stop the security monitor before exiting
            if is_security_monitor_active():
                confirm = input("Security Monitor is still running. Stop it before exiting? (yes/no): ").lower()
                if confirm == 'yes':
                    stop_security_monitor()
                else:
                    print("Security Monitor will continue running in the background.")
            
            print("Stay vigilant!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")
        
        print("\n-----------------------------------------")
        input("Press Enter to return to the main menu...")

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import psutil
        return True
    except ImportError:
        print("Missing required dependency: psutil")
        print("Please install it using: pip install psutil")
        print("Then restart this application.")
        return False

def check_required_files():
    """Check if all required script files are present."""
    required_files = [SECURITY_MONITOR_SCRIPT, ATTACK_AGENT_SCRIPT, RECOVERY_UTILITY_SCRIPT]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("Missing required files:")
        for f in missing_files:
            print(f"- {f}")
        print("Please ensure all script files are in the same directory.")
        return False
    return True

if __name__ == "__main__":
    clear_screen()
    print("Initializing Ransomware Advanced Simulation Controller...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-----------------------------------------")
    
    # Check dependencies and required files
    if not check_dependencies() or not check_required_files():
        print("\nCannot start controller due to missing dependencies or files.")
        sys.exit(1)
    
    # Show disclaimer
    print("\nDISCLAIMER: This tool is for educational and simulation purposes ONLY.")
    print("DO NOT use it on important data or without explicit permission.")
    print("The author is not responsible for any misuse or data loss.")
    print("Always test in a safe, isolated environment.")
    
    input("\nPress Enter to continue to the main controller...")
    
    # Handle potential errors gracefully
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n\nController terminated by user (Ctrl+C).")
        
        # Try to clean up security monitor process if it's running
        if is_security_monitor_active():
            print("Attempting to stop Security Monitor before exiting...")
            try:
                stop_security_monitor()
            except:
                print("Could not stop Security Monitor. It may continue running.")
                
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")
    
    finally:
        print("\nExiting Ransomware Advanced Simulation Controller.")
        sys.exit(0) 