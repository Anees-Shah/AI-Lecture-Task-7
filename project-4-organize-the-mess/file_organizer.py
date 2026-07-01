import os
import shutil
import hashlib

# ==========================================
# CONFIGURATION & SAFETY SETTINGS
# ==========================================
# IMPORTANT: This MUST be the path to your BACKUP COPY!
SOURCE_FOLDER = "./messy_folder_backup" 
DESTINATION_FOLDER = "./organized_files"

# SAFETY SWITCH: Set to True to just print the plan. 
# ONLY change to False after you approve the plan!
DRY_RUN = True 

# Files larger than this (in MB) will be flagged as "Large"
LARGE_FILE_THRESHOLD_MB = 0.05 # Set low for testing; change to 50 for real use

# ==========================================
# FILE CATEGORIES
# ==========================================
CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.json']
}

def get_file_hash(filepath):
    """Calculates the MD5 hash of a file to check for exact content duplicates."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        # Read in chunks to handle large files without crashing memory
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return 'Miscellaneous'

def organize_files():
    if not os.path.exists(SOURCE_FOLDER):
        print(f"Error: Source folder '{SOURCE_FOLDER}' not found.")
        return

    if DRY_RUN:
        print("="*50)
        print("🛑 DRY RUN MODE: NO FILES WILL BE MOVED 🛑")
        print("="*50 + "\n")
    else:
        print("="*50)
        print("✅ EXECUTING ORGANIZATION ✅")
        print("="*50 + "\n")
        os.makedirs(DESTINATION_FOLDER, exist_ok=True)

    # Dictionary to track file hashes and find exact duplicates
    seen_hashes = {}
    action_plan = []

    # Walk through the source folder and all subfolders
    for root, dirs, files in os.walk(SOURCE_FOLDER):
        for file in files:
            if file.startswith('.'): continue # Skip hidden system files

            src_path = os.path.join(root, file)
            file_hash = get_file_hash(src_path)
            file_size_mb = os.path.getsize(src_path) / (1024 * 1024)
            category = get_category(file)
            
            action = {'file': file, 'src': src_path, 'size_mb': file_size_mb}

            # 1. Check for exact content duplicates
            if file_hash in seen_hashes:
                action['type'] = 'DUPLICATE'
                action['dest_folder'] = 'Duplicates'
                action['note'] = f"Exact copy of '{seen_hashes[file_hash]}'"
            else:
                seen_hashes[file_hash] = file
                action['type'] = 'MOVE'
                action['dest_folder'] = category
                
                # 2. Check for large files
                if file_size_mb > LARGE_FILE_THRESHOLD_MB:
                    action['note'] = f"LARGE FILE ({file_size_mb:.4f} MB)"
                else:
                    action['note'] = ""

            action_plan.append(action)

    # Print the proposed plan
    print(f"Scanned {len(action_plan)} files.\n")
    
    for action in action_plan:
        dest_folder = action['dest_folder']
        note = f" | Note: {action['note']}" if action['note'] else ""
        
        if action['type'] == 'DUPLICATE':
            print(f"👉 [DUPLICATE] '{action['file']}' -> '{dest_folder}/'{note}")
        else:
            print(f"👉 [MOVE] '{action['file']}' -> '{dest_folder}/'{note}")

    # Execute the moves ONLY if DRY_RUN is False
    if not DRY_RUN:
        print("\nExecuting moves...")
        for action in action_plan:
            dest_dir = os.path.join(DESTINATION_FOLDER, action['dest_folder'])
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, action['file'])
            
            # Safety: Prevent overwriting if a file with the same name exists in destination
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(action['file'])
                dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                counter += 1
                
            shutil.move(action['src'], dest_path)
        print("\n✅ Done! Check the 'organized_files' folder.")
    else:
        print("\n" + "="*50)
        print("🛑 DRY RUN COMPLETE 🛑")
        print("Review the plan above. If it looks correct, change DRY_RUN = False")
        print("in the script and run it again to execute the moves.")
        print("="*50)

if __name__ == "__main__":
    organize_files()