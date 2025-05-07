# security_monitor.py
import os
import sys
import time
import argparse
import platform
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
ENCRYPTED_EXTENSION = ".enc"
MAX_FILES_FOR_ALERT = 3  # Threshold for triggering simulated defense
ALERT_TIME_WINDOW = 5  # Time window in seconds to count suspicious file operations
LOCKDOWN_FLAG_FILE = "system_lockdown.flag"  # File created to signal system lockdown
LOG_FILE = "security_monitor.log"  # Log file for security events

# --- Global Variables ---
suspicious_files = []  # List to track recently encrypted files with timestamps
lockdown_active = False  # Flag to track if lockdown has been initiated

def log_event(message):
    """Log security events to both console and log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}"
    print(log_message)
    
    try:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def lock_windows_system():
    """Lock the Windows workstation when ransomware is detected"""
    if platform.system() == "Windows":
        try:
            log_event("[SECURITY MONITOR] LOCKING WINDOWS WORKSTATION FOR PROTECTION!")
            # Use rundll32 to lock the workstation - this is the standard Windows lock command
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
            return True
        except Exception as e:
            log_event(f"[SECURITY MONITOR] Error locking workstation: {e}")
            return False
    else:
        log_event("[SECURITY MONITOR] System lock requested but not on Windows platform")
        return False

class RansomwareDetector(FileSystemEventHandler):
    """Handler for file system events to detect potential ransomware activity"""
    
    def __init__(self, monitored_directory):
        super().__init__()
        self.monitored_directory = os.path.abspath(monitored_directory)
        log_event(f"[SECURITY MONITOR] Initializing protection for: {self.monitored_directory}")
        log_event(f"[SECURITY MONITOR] Alert threshold: {MAX_FILES_FOR_ALERT} encrypted files in {ALERT_TIME_WINDOW} seconds")
    
    def on_created(self, event):
        """Handle file creation events"""
        global suspicious_files, lockdown_active
        
        if lockdown_active:
            return  # If lockdown is already active, no need to process more events
        
        # Skip directory events and check if it's a file with .enc extension
        if not event.is_directory and event.src_path.endswith(ENCRYPTED_EXTENSION):
            file_path = event.src_path
            current_time = time.time()
            
            # Log the suspicious file
            log_event(f"[SECURITY MONITOR] Detected potential encrypted file: {file_path}")
            
            # Add to suspicious files list with timestamp
            suspicious_files.append((file_path, current_time))
            
            # Remove files older than the time window
            current_time = time.time()
            suspicious_files = [(f, t) for f, t in suspicious_files if current_time - t <= ALERT_TIME_WINDOW]
            
            # Check if we've exceeded the threshold for alert
            if len(suspicious_files) >= MAX_FILES_FOR_ALERT:
                self.trigger_lockdown()
    
    def on_deleted(self, event):
        """Handle file deletion events - often ransomware deletes original files"""
        # This is simplified - real systems would analyze patterns of deletions and creations
        pass
    
    def trigger_lockdown(self):
        """Simulate a system lockdown when ransomware is detected"""
        global lockdown_active
        
        if lockdown_active:
            return  # Prevent multiple lockdowns
        
        lockdown_active = True
        
        log_event("\n[SECURITY MONITOR] CRITICAL ALERT - Potential Ransomware Activity Detected!")
        log_event(f"[SECURITY MONITOR] {len(suspicious_files)} encrypted files detected in {ALERT_TIME_WINDOW}s time window")
        for file_path, _ in suspicious_files[:5]:  # Show first 5 suspicious files
            log_event(f"[SECURITY MONITOR] Suspicious file: {file_path}")
        
        log_event("[SECURITY MONITOR] Threat signature match: MAL/Ransom-Generic Variant DUCK001")
        log_event("[SECURITY MONITOR] ACTION: Isolating affected processes...")
        log_event("[SECURITY MONITOR] Deploying countermeasures...")
        log_event("[SECURITY MONITOR] Network quarantine initiated for affected endpoint.")
        log_event("[SECURITY MONITOR] SYSTEM LOCKDOWN ENGAGED! Blocking further unauthorized file encryption.")
        log_event("[SECURITY MONITOR] Incident report generated. Security team alerted.")
        
        # Create lockdown flag file to signal other processes
        try:
            lockdown_path = os.path.join(self.monitored_directory, LOCKDOWN_FLAG_FILE)
            with open(lockdown_path, 'w') as f:
                f.write(f"SYSTEM LOCKED: Potential ransomware detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"DO NOT REMOVE THIS FILE UNTIL INVESTIGATION IS COMPLETE\n")
                for file_path, _ in suspicious_files:
                    f.write(f"Suspicious file: {file_path}\n")
            
            log_event(f"[SECURITY MONITOR] Lockdown flag created at: {lockdown_path}")
            log_event("[SECURITY MONITOR] Monitoring will continue to track further malicious activity")
        except Exception as e:
            log_event(f"[SECURITY MONITOR] Error creating lockdown flag: {e}")
            
        # Actually lock the Windows system
        lock_windows_system()


def start_monitoring(target_directory):
    """Start the continuous monitoring process"""
    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory")
        return False
    
    # Initialize log file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"\n--- Security Monitor Session Started: {datetime.now()} ---\n")
    
    # Check if there's already a lockdown flag
    lockdown_path = os.path.join(target_directory, LOCKDOWN_FLAG_FILE)
    if os.path.exists(lockdown_path):
        log_event(f"[SECURITY MONITOR] WARNING: Lockdown flag already exists at {lockdown_path}")
        log_event("[SECURITY MONITOR] System is already in lockdown state")
        log_event("[SECURITY MONITOR] To reset, manually delete the lockdown flag file and restart the monitor")
        global lockdown_active
        lockdown_active = True
    
    # Set up the observer with our custom event handler
    event_handler = RansomwareDetector(target_directory)
    observer = Observer()
    observer.schedule(event_handler, target_directory, recursive=True)
    
    try:
        log_event("[SECURITY MONITOR] Starting continuous background monitoring...")
        log_event(f"[SECURITY MONITOR] Watching directory: {target_directory}")
        log_event("[SECURITY MONITOR] Press Ctrl+C to stop monitoring")
        observer.start()
        
        # Keep the script running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        log_event("[SECURITY MONITOR] Stopping monitoring (user interrupt)")
        observer.stop()
    
    except Exception as e:
        log_event(f"[SECURITY MONITOR] Error in monitoring: {e}")
        observer.stop()
        raise
    
    finally:
        observer.join()
        log_event("[SECURITY MONITOR] Monitoring stopped")
    
    return True


def clear_lockdown(target_directory):
    """Clear lockdown status by removing the flag file"""
    lockdown_path = os.path.join(target_directory, LOCKDOWN_FLAG_FILE)
    if os.path.exists(lockdown_path):
        try:
            os.remove(lockdown_path)
            print(f"Lockdown flag removed from: {lockdown_path}")
            return True
        except Exception as e:
            print(f"Error removing lockdown flag: {e}")
            return False
    else:
        print(f"No lockdown flag found at: {lockdown_path}")
        return True


def main():
    """Main function to parse args and start monitoring"""
    parser = argparse.ArgumentParser(description="Security Monitor - Ransomware Activity Detector")
    parser.add_argument("directory", help="Directory to monitor for suspicious activity")
    parser.add_argument("--clear-lockdown", action="store_true", 
                        help="Clear existing lockdown status before starting monitoring")
    
    args = parser.parse_args()
    
    if args.clear_lockdown:
        clear_lockdown(args.directory)
    
    # Start the continuous monitoring process
    start_monitoring(args.directory)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: No directory specified for monitoring")
        print("Usage: python security_monitor.py [directory_to_monitor]")
        print("       python security_monitor.py [directory_to_monitor] --clear-lockdown")
        sys.exit(1)
    
    main() 