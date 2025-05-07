# recovery.py
import os
import sys
import json
import time
import logging
from datetime import datetime

# --- Configuration ---
ENCRYPTED_EXTENSION = ".enc"
RANSOM_NOTE_FILENAME = "RECOVER_YOUR_FILES.txt"
MANIFEST_FILENAME = ".__ransom_manifest__.json"
LOCKDOWN_FLAG_FILE = "system_lockdown.flag"
RECOVERY_KEY = "duck"  # Hardcoded key for the simulation
LOG_FILE = "recovery.log"

# --- Setup Logging ---
def setup_logging():
    """Set up detailed logging to file and console."""
    # Create logger
    logger = logging.getLogger('recovery')
    logger.setLevel(logging.DEBUG)
    
    # Create console handler and set level
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # Create file handler and set level
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters
    console_format = logging.Formatter('[RECOVERY] %(message)s')
    file_format = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    
    # Add formatters to handlers
    console.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    # Add handlers to logger
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    return logger

# --- Core Recovery Functions ---

def xor_crypt_bytes(data_bytes, key_str):
    """XOR decrypts data with the given key."""
    logger.debug(f"Applying XOR decryption with key length: {len(key_str)}")
    key_bytes = key_str.encode('utf-8')
    key_len = len(key_bytes)
    return bytes([data_byte ^ key_bytes[i % key_len] for i, data_byte in enumerate(data_bytes)])

def get_manifest_path(target_dir):
    """Get the path to the manifest file."""
    return os.path.join(target_dir, MANIFEST_FILENAME)

def load_manifest(manifest_path):
    """Load the recovery manifest file."""
    logger.info(f"Attempting to load manifest from: {manifest_path}")
    
    if not os.path.exists(manifest_path):
        logger.error(f"Manifest file not found at: {manifest_path}")
        return []
    
    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            logger.info(f"Manifest loaded successfully. {len(data)} files to recover.")
            logger.debug(f"Manifest content: {data[:5]}...")
            return data
        else:
            logger.error("Manifest has invalid format (not a list)")
            return []
    except json.JSONDecodeError:
        logger.error("Failed to parse manifest - invalid JSON format")
        return []
    except IOError as e:
        logger.error(f"I/O error reading manifest: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error loading manifest: {e}")
        return []

def save_manifest(manifest_path, data):
    """Save the updated manifest file."""
    logger.debug(f"Saving updated manifest with {len(data)} files remaining")
    try:
        with open(manifest_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        logger.error(f"I/O error writing manifest: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error saving manifest: {e}")
        return False

def remove_ransom_note(target_dir):
    """Remove the ransom note file."""
    note_path = os.path.join(target_dir, RANSOM_NOTE_FILENAME)
    if os.path.exists(note_path):
        try:
            os.remove(note_path)
            logger.info(f"Ransom note removed: {note_path}")
            return True
        except OSError as e:
            logger.error(f"Error removing ransom note: {e}")
            return False
    else:
        logger.debug(f"No ransom note found at: {note_path}")
        return True

def remove_lockdown_flag(target_dir):
    """Remove the lockdown flag if it exists."""
    flag_path = os.path.join(target_dir, LOCKDOWN_FLAG_FILE)
    if os.path.exists(flag_path):
        try:
            os.remove(flag_path)
            logger.info(f"Lockdown flag removed: {flag_path}")
            return True
        except OSError as e:
            logger.error(f"Error removing lockdown flag: {e}")
            return False
    return True

def recover_files(target_dir):
    """Main recovery function - decrypts files based on manifest."""
    logger.info("Starting file recovery process...")
    
    manifest_path = get_manifest_path(target_dir)
    manifest_data = load_manifest(manifest_path)
    
    if not manifest_data:
        logger.warning("No files to recover - empty or missing manifest")
        return 0, 0, 0
    
    # Statistics
    total_files = len(manifest_data)
    recovered_files = 0
    failed_files = 0
    
    logger.info(f"Found {total_files} files to recover in {target_dir}")
    
    # Print recovery details
    logger.info("-" * 60)
    logger.info("RECOVERY DETAILS:")
    logger.info(f"Target Directory: {os.path.abspath(target_dir)}")
    logger.info(f"Recovery Key: '{RECOVERY_KEY}'")
    logger.info(f"Files to Process: {total_files}")
    logger.info("-" * 60)
    
    start_time = time.time()
    
    # Create a copy of manifest_data to iterate over, as we'll modify the original
    files_to_recover = list(manifest_data)
    
    # Recover each file
    for index, record in enumerate(files_to_recover):
        encrypted_filepath = record.get("encrypted_path")
        original_filepath = record.get("original_path")
        
        # Validate record
        if not encrypted_filepath or not original_filepath:
            logger.warning(f"Invalid manifest record (skipping): {record}")
            failed_files += 1
            continue
        
        # Check if encrypted file exists
        if not os.path.exists(encrypted_filepath):
            logger.warning(f"Encrypted file not found (skipping): {encrypted_filepath}")
            failed_files += 1
            continue
        
        # Log progress every 5 files or for the first/last file
        if index % 5 == 0 or index == 0 or index == total_files - 1:
            logger.info(f"Progress: {index+1}/{total_files} files ({((index+1)/total_files)*100:.1f}%)")
        
        # Detailed logging for each file
        logger.debug(f"Processing file {index+1}/{total_files}: {encrypted_filepath}")
        
        try:
            # Read encrypted content
            with open(encrypted_filepath, 'rb') as f_in:
                encrypted_content = f_in.read()
            
            # Decrypt content
            start_decrypt = time.time()
            decrypted_content = xor_crypt_bytes(encrypted_content, RECOVERY_KEY)
            decrypt_time = time.time() - start_decrypt
            
            # Ensure directory exists for original file
            os.makedirs(os.path.dirname(original_filepath), exist_ok=True)
            
            # Save decrypted content
            with open(original_filepath, 'wb') as f_out:
                f_out.write(decrypted_content)
            
            # Remove encrypted file
            os.remove(encrypted_filepath)
            
            # Detail logging for successful recovery
            logger.debug(f"File recovered: {encrypted_filepath} -> {original_filepath} (Size: {len(decrypted_content)} bytes, Time: {decrypt_time:.3f}s)")
            
            # Remove this record from manifest_data
            for i, m_record in enumerate(manifest_data):
                if m_record.get("original_path") == original_filepath:
                    manifest_data.pop(i)
                    break
            
            recovered_files += 1
            
        except Exception as e:
            logger.error(f"Failed to recover file: {encrypted_filepath}")
            logger.error(f"Error details: {str(e)}")
            failed_files += 1
    
    # Save updated manifest (should be empty if all files were recovered)
    if save_manifest(manifest_path, manifest_data):
        logger.info("Manifest updated successfully")
        # Remove manifest if empty
        if not manifest_data:
            try:
                os.remove(manifest_path)
                logger.info("Empty manifest file removed")
            except Exception as e:
                logger.warning(f"Could not remove empty manifest: {e}")
    
    # Remove ransom note if all files recovered
    if not manifest_data:
        remove_ransom_note(target_dir)
        remove_lockdown_flag(target_dir)
    
    # Calculate statistics
    total_time = time.time() - start_time
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("RECOVERY SUMMARY:")
    logger.info("=" * 60)
    logger.info(f"Total files processed:      {total_files}")
    logger.info(f"Successfully recovered:     {recovered_files}")
    logger.info(f"Failed to recover:          {failed_files}")
    logger.info(f"Success rate:               {(recovered_files/total_files)*100:.1f}%")
    logger.info(f"Total recovery time:        {total_time:.2f} seconds")
    if recovered_files > 0:
        logger.info(f"Average time per file:      {total_time/recovered_files:.2f} seconds")
    logger.info("=" * 60)
    
    if failed_files > 0:
        logger.warning("Some files could not be recovered. Check the log for details.")
    elif recovered_files == total_files:
        logger.info("RECOVERY COMPLETED SUCCESSFULLY - All files restored!")
    
    return total_files, recovered_files, failed_files

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Error: No target directory specified.")
        print("Usage: python recovery.py [directory_to_recover]")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)
    
    print("\n===== RANSOMWARE RECOVERY UTILITY =====")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: {os.path.abspath(target_dir)}")
    print(f"Logging to: {os.path.abspath(LOG_FILE)}")
    print("=======================================\n")
    
    # Recover files
    total, recovered, failed = recover_files(target_dir)
    
    print("\n===== RECOVERY PROCESS COMPLETE =====")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Files Processed: {total}")
    print(f"Successfully Recovered: {recovered}")
    print(f"Failed: {failed}")
    print(f"Detailed log available at: {os.path.abspath(LOG_FILE)}")
    print("====================================\n")


# Initialize logger
logger = setup_logging()

if __name__ == "__main__":
    logger.info(f"Recovery utility started at {datetime.now()}")
    main()
    logger.info(f"Recovery utility completed at {datetime.now()}") 