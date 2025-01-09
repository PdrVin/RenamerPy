import os
import re
import shutil
from typing import Literal
import pandas as pd
from unidecode import unidecode

# Current Folder Path
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# Photo Folder Paths
PHOTOS = os.path.join(ROOT_PATH, "System_Photos") # Photos Folder
PHOTOS_ISOLATED = os.path.join(ROOT_PATH, "Isolated_Photos") # Photo Folder without Record
PHOTOS_FAILURES = os.path.join(ROOT_PATH, "Failures_Photos") # Photo Folder with Error

# Make sure the destination folders exist
for folder in [PHOTOS_ISOLATED, PHOTOS_FAILURES]:
    os.makedirs(folder, exist_ok=True)

# Function - Find the Most recent CSV file
def find_recent_csv(pattern: Literal['']) -> str | None:
    csv_files = [file for file in os.listdir(ROOT_PATH) if re.match(pattern, file)]
    csv_files.sort(reverse=True)
    return os.path.join(ROOT_PATH, csv_files[0]) if csv_files else None

# CSV files name pattern
PATTERN_CSV = r"Users_\d{6}_\d{4}.csv"

# Find the Most recent CSV file
recent_csv_file = find_recent_csv(PATTERN_CSV)

# Check for CSV Existence
if recent_csv_file is None:
    raise FileNotFoundError(
        "No CSV file found with the specified pattern.")

# Extract data from CSV file / Setting "Record" as string
df = pd.read_csv(recent_csv_file, dtype={"Record": str})

# Preparing data in DataFrame
df["Record"] = df["Record"].str.zfill(6)  # Ensures leading zeros
df["User"] = df["User"].str.strip().str.lower().apply(unidecode)

# Creating a dictionary to map Usernames to Records
name_to_record = dict(zip(df["User"], df["Record"]))

# Initializing Counters & Error list
transfered_rows, affected_rows, fail_rows = 0, 0, 0
list_failures = []

# Iterating through files in the Photo Folder
for file in os.listdir(PHOTOS):
    try:
        if file.lower().endswith(".jfif"):
            # Extract the Photo Name & Extension
            name_photo, extension = os.path.splitext(file)
            name_photo = unidecode(name_photo.lower()) # Remove accentuation
            
            # Extract Record from Username
            record = name_to_record.get(name_photo)
            
            # Original Path of each photo
            origin_path = os.path.join(PHOTOS, file)
            
            # Check for User without Record
            if record in ['000nan']:
                new_path = os.path.join(PHOTOS_ISOLATED, file)
                shutil.move(origin_path, new_path)
                transfered_rows += 1
            # Check for Photo without User
            elif record in [None, 'None']:
                new_path = os.path.join(PHOTOS_FAILURES, file)
                shutil.move(origin_path, new_path)
                fail_rows += 1
            else:
                new_name = f"{record}{extension}"
                new_path = os.path.join(PHOTOS, new_name)
                os.rename(origin_path, new_path)
                affected_rows += 1
    except Exception as e:
        # Add the file name and error message
        list_failures.append((file, str(e)))

# Report
print("Process completed.")
print(f"Renamed Photos: {affected_rows}")
print(f"Isolated Photos: {transfered_rows}")
print(f"Failed Photos: {fail_rows}")

# Error Report
print("Errors:", end=" ")
print(0) if not list_failures else print("\n")
for file, error in list_failures:
    print(f"File: {file} - Error: {error}")
