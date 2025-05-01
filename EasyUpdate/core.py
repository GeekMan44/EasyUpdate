import requests
import json
import os
import sys
import subprocess
import time
import psutil
from .exceptions import FileDownloadError, VersionFileFormatError, PathFileError, UpdateFileError

def generate_temp_file(file: str = "") -> str:

        new_file = file.split(".")
        extension = ""
        if len(new_file) > 1:
            extension = "" + "." + new_file[-1]
            new_file.pop()
        new_file.insert(1, "_new")
        new_file = "".join(new_file) + extension
        return new_file

class UpdateManager:

    def __init__(self, version_file: str, version_url: str, updater_name: str = "update.exe"):
        self.version_url = version_url
        self.version_file = version_file
        self.needUpdate = False
        self.file_name = []
        self.new_name = []
        self.isCompiled = False
        self.updater_name = updater_name

    def search_update(self) -> bool:
        try:
            self.versions_url = requests.get(self.version_url).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            raise FileDownloadError(self.version_url)

        if "latest" in self.versions_url:
            if "version" in self.versions_url["latest"]:
                self.version_url = self.versions_url["latest"]["version"].split(".")
                self.version_file = self.version_file.split(".")
                version_lengh = len(self.version_url)
                
                i=0
                while version_lengh > i and self.needUpdate == False:

                    if int(self.version_url[i]) > int(self.version_file[i]):
                        self.needUpdate = True

                    elif int(self.version_url[i]) < int(self.version_file[i]):
                        self.needUpdate = False
                    i = i+1

                if self.needUpdate:
                    if "endpoint" in self.versions_url["latest"]:
                        self.endpoint = self.versions_url["latest"]["endpoint"]
                    else:
                        raise VersionFileFormatError("Missing 'endpoint' key in 'latest' section")
                    if "files" in self.versions_url["latest"]:
                        self.files = self.versions_url["latest"]["files"]
                        if not self.files:
                            raise VersionFileFormatError("'files' key is empty, can't download files")
                        return True
                    else:
                        raise VersionFileFormatError("Missing 'files' key in 'latest' section")
            else:
                raise VersionFileFormatError("Missing 'version' key in 'latest' section")
        else:
            raise VersionFileFormatError("'latest' section is missing in the versions file")
        return False


    def download_update(self, authorization: bool = False, updater: str = "update.exe") -> bool:
        if not self.needUpdate:
            return False
        else:
            if authorization == True:
                if getattr(sys, 'frozen', False):
                    
                    actual_dir = os.path.dirname(sys.executable)
                    self.actual_file = os.path.abspath(sys.executable)
                    self.isCompiled = True
                else:
                    actual_dir = os.path.dirname(sys.argv[0])

                    self.actual_file = os.path.abspath(sys.argv[0])
                
                for element in self.files:
                    if element["folder"]:
                        folder = element["folder"]
                    else:
                        folder = ""
                    
                    if "file" in element:
                        file = element["file"]
                        self.file_name.append(file)
                        url = f"{self.endpoint}{file}"
                    else:
                        raise VersionFileFormatError("Missing 'file' key in 'files' inside 'latest' section")

                    try:
                        response = requests.get(url)
                    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                        raise FileDownloadError(url)

                    save_path = os.path.join(actual_dir, folder)

                    try:
                        os.makedirs(save_path, exist_ok=True)
                    except FileExistsError:
                        raise PathFileError(save_path, f"Make sure no file has the same name as the folder '{folder}'")
                    

                    file = os.path.join(save_path, file)
                    
                    if self.isCompiled == True:
                        if file == self.actual_file:
                            file = generate_temp_file(file)

                    with open(os.path.join(save_path, file), "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)

                if self.isCompiled == True:
                    updater_path = os.path.join(actual_dir, self.updater_name)
                    subprocess.Popen(updater_path)
                    sys.exit()
            else:
                return False

def updater(main_name: str = "main.exe", waiting_time: int = 10):
    start_time = time.time()
    while (time.time()-start_time) <= waiting_time:
        en_cours = any(proc.info['name'] == main_name for proc in psutil.process_iter(['name']))
        if not en_cours:
            break
        time.sleep(1)

    if en_cours:
        sys.exit()

    if getattr(sys, 'frozen', False):
        actual_dir = os.path.dirname(sys.executable)
        actual_file = os.path.abspath(sys.executable)
    
    else:
        raise UpdateFileError(actual_file, "Make sure this file is a compiled file, either a '.exe' for windows or a executable file for linux")

    try:
        new_name = os.path.join(actual_dir, generate_temp_file(main_name))
        main_name = os.path.join(actual_dir, main_name)

        os.replace(new_name, main_name)
        subprocess.Popen(main_name)
        sys.exit()
    except:
        pass

    return True