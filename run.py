import os
from google.cloud import storage
import csv
import sys
import time

OUTPUT_DATA = {}

INPUT_DIR = "upload/"
GOOGLE_STORAGE_BUCKET=''
PUBLIC = True


def upload_file(file_data, path="/"):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GOOGLE_STORAGE_BUCKET)
        file = bucket.blob(path)
        file.upload_from_filename(file_data)    

        if PUBLIC:
            file.make_public()

        return file.public_url
    except Exception as e:
        print(e)

def get_list_of_files(dirName):
    list_of_files = os.listdir(dirName)
    all_files = list()
    for entry in list_of_files:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            all_files = all_files + get_list_of_files(fullPath)
        else:
            all_files.append(fullPath) 
    return all_files 

index = 1
list_of_files = get_list_of_files(INPUT_DIR)
total_progress_length = 50

for file in list_of_files:
    file_paths = file.split("/",1)
    
    progress_percentage = index * 100/ len(list_of_files) 
    progress = int((progress_percentage/100) * total_progress_length)
    sys.stdout.write('\rUploading [{completed}{remaining}] {progress_percentage}% ({file_name})'.format(
        progress_percentage=int(progress_percentage),
        completed='=' * progress,
        remaining=' ' * (total_progress_length - progress),
        file_name=file_paths[1]
    ))
    sys.stdout.flush()
    time.sleep(0.05)  

    url = "test"
    url = upload_file(file_data=file, path=file_paths[1])   
    index += 1
    OUTPUT_DATA[file] = {
        "file_path": str(file),
        "url": url,
    }

sys.stdout.write('\rCompleted [{completed}{remaining}] {progress_percentage}% {file_name}'.format(
    progress_percentage=int(100),
    completed='=' * total_progress_length,
    remaining=' ' * 0,
    file_name=' ' * int(len(list_of_files))
))


with open('result.csv', 'w') as fp:
    data_writer = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(["File Path", "Public", "URL"])
    for key in OUTPUT_DATA.keys():
        data_writer.writerow([key, PUBLIC, OUTPUT_DATA[key]["url"]])

print("\nOutput: result.csv")
