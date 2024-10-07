from os import listdir
from .base import Base
from .drive import Drive
from json import loads

DATA_PATH = "./.data"

def transfer_base(base_file):
    base_name = base_file.split(".")[0]
    base = Base(base_name)

    with open(f"{DATA_PATH}/drives/{base_file}", "r") as file:
        data = loads(file.read())
        for item in data:
            key = item["key"]
            del item["key"]
            base.put(item, key)

def transfer_bases():
    bases = listdir(f"{DATA_PATH}/bases")

    for base_file in bases:
        transfer_base(base_file)

def transfer_drive(drive_folder):
    drive = Drive(drive_folder)

    files = listdir(f"{DATA_PATH}/drives/{drive_folder}")
    skipped_count = 0

    for file in files:
        filepath = f"{DATA_PATH}/drives/{drive_folder}/{file}"
        with open(filepath, "rb") as content_file:
            data = content_file.read()

            try:
                drive.put(file, data)
            except Exception as exception:
                print(f"Skipped {file}: {exception.__class__.__name__}")
                skipped_count += 1
    
    print(f"Skipped {skipped_count} files in {drive_folder}")

def transfer_drives():
    drives = listdir(f"{DATA_PATH}/drives")

    for drive_folder in drives:
        transfer_drive(drive_folder)

