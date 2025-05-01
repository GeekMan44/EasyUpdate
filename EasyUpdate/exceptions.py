
class EasyUpdateError(Exception):
    pass

class FileDownloadError(EasyUpdateError):
    def __init__(self, url):
        super().__init__(f"""
Version file not found : {url}\n
    Make sure the file exist and the url is valid""")
    pass

class VersionFileFormatError(EasyUpdateError):
    def __init__(self, hint):
        super().__init__(f"""
The versions file is either incomplete or not formatted correctly.\n
    {hint}\n
    Please refer to the 'Version File' section in the documentation for more details.
""")
    pass

class PathFileError(EasyUpdateError):
    def __init__(self, path, hint):
        super().__init__(f"""
The path file is either incomplete or something block the creation of file/folder.\n
    The path: {path} return an error\n
    {hint}\n
""")
        pass

class UpdateFileError(EasyUpdateError):
    def __init__(self, file, hint):
        super().__init__(f"""
An error has occured when trying to execute '{file}'.\n
    {hint}\n
""")