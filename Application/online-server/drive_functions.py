#google drive function for emotion detection program

import os
import os.path as path
import re

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials

gauth.LoadCredentialsFile(path.join(path.dirname(path.abspath(__file__)), "mycreds.txt"))

if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.CommandLineAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile(path.join(path.dirname(path.abspath(__file__)), "mycreds.txt"))
drive = GoogleDrive(gauth)
http = drive.auth.Get_Http_Object()
initial_folder = None

FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
   
def upload_file(title,filename,full_path='',folderID=0):
    """
    Upload a given file to Google Drive, optionally under a specific parent folder
    :param filename: The path to the file you wish to upload
    :param parent_folder: Optional parent folder override, defaults to root
    :return: file_id
    """
    if full_path != '':
        full_path = full_path+'\\'
    if not path.exists(full_path+filename):
        print(f"Specified filename {filename} does not exist!")
        return False
    file_params = {"title": filename}
    if folderID:
        file_params["parents"] = [{"kind": "drive#fileLink", "id": folderID}]
    file = drive.CreateFile(file_params)
    file.SetContentFile(full_path+filename)
    file.Upload(param={"http": http})
    file.FetchMetadata()
    file.InsertPermission({"type": "anyone", "role": "reader"})
    print(f"Get it with: {file['id']}")
    print(f"URL: {file['webContentLink']}")
    return file['id']

def list_files(parent_folder = "root", print_to_stdout = False):
    """
    List all files under a specific folder
    :param parent_folder: Optional folder ID to list files under, defaults to root
    :param print_to_stdout: While aggregating the list of files, also print to stdout, default false
    :return: A tuple of two lists, first of files and second of directories
    """
    file_list = drive.ListFile({"q": f"'{parent_folder}' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file["mimeType"] == FOLDER_MIME_TYPE:
            continue
        if print_to_stdout:
            print(f"Title: {file['title']}\tid: {file['id']}")

    parent_folder = drive.CreateFile({"id": parent_folder})
    parent_folder.FetchMetadata()
    title = parent_folder.metadata["title"]
    try:
        if initial_folder is not None:
            while (parent_folder.metadata["id"] != initial_folder.metadata["id"]):
                parent_folder = parent_folder.metadata["parents"][0]["id"]
                parent_folder = drive.CreateFile({"id": parent_folder})
                parent_folder.FetchMetadata()
                title = path.join(parent_folder.metadata["title"], title)
    except IndexError:
        title = path.join(initial_folder.metadata["title"], title)
    files_list, folders_list = [], []
    for file in file_list:
        file["title"] = path.join(title, file["title"])
        if file["mimeType"] != FOLDER_MIME_TYPE:
            files_list.append(file)
        else:
            folders_list.append(file)
    return files_list, folders_list

def download_file(file_id ,skip_existing = False,overwrite_existing = False) :
    """
    Download a given file
    :param overwrite_existing: Overwrite a file if it already exists
    :param skip_existing: Skip downloading the file if it already exists
    :param file_id: File ID to download
    :return: None
    """
    files_to_dl, folders_to_dl = [], []
    file = drive.CreateFile({"id": file_id})
    file.FetchMetadata()
    if file.metadata["mimeType"] == FOLDER_MIME_TYPE:
        print(f"{file.metadata['title']} is a folder, downloading recursively")
        files_to_dl, folders_to_dl = list_files(file_id)
        global initial_folder
        if initial_folder is None:
            initial_folder = file
            if not path.isdir(file.metadata["title"]):
                os.mkdir(file.metadata["title"])
    else:
        files_to_dl.append(file)
    for dl_file in files_to_dl:
        filename = dl_file["title"]
        if path.isfile(filename):
            if skip_existing:
                print(f"{filename} already exists, skipping.")
                continue
            elif overwrite_existing:
                print(f"{filename} already exists, overwriting.")
                os.remove(filename)
            else:
                raise IllegalStateException(
                    f"{filename} already exists but neither --skip nor --overwrite were "
                    f"passed!"
                    )
        print(f"Downloading {filename} -> {filename}")
        dl_file.GetContentFile(filename)
        print(f"Downloaded {filename}!")

    for folder in folders_to_dl:
        folder_name = folder["title"]
        folder_id = folder.metadata["id"]
        if not path.isdir(folder_name):
            os.makedirs(folder_name)
        download_file(folder_id)
    return True

def search_download(filename,folderID=0):
    """
    Search and download a file
    :param filename: name of the file
    :param folderID: enter the parent folderid if known
    :return: id or False
    """
    if folderID:
        files_list = drive.ListFile({'q':f"'{folderID}' in parents and trashed=false"}).GetList()
    else:
        files_list = drive.ListFile({'q':"'root' in parents and trashed=false"}).GetList()
    item = 0
    for files in files_list:
        if files['title'] == filename:
            item = files['id']
    if not item:
        print('No files found.')
        return False
    file = drive.CreateFile({"id":item})
    file.GetContentFile(filename)
    return item

def url_to_gdrive_id(url):
    """
    Parses the given Google Drive URL and extracts the file ID from it
    to be used by the Drive API client to download it.
    :param url: The Google Drive URL to parse, can also be an actual ID in case the user feels gracious.
    :return: file ID extracted from the URL
    """
    pattern = re.compile(r"[a-zA-Z0-9-_]{33}")
    return pattern.search(url).group(0)

def create_folder(folder_name):
    """
    Creates a folder with the title as folder_name
    :param folder_name: name of folder
    :return: folder_id
    """
    folder = drive.CreateFile({'title':folder_name,'mimeType':'application/vnd.google-apps.folder'})
    folder.Upload()
    return folder['id']

def check_folder_exists(folder_name,create=1):
    """
    Check if a folder name exists.
    if not create it
    :param folder_name: name of folder
    :param create: create a folder or not
    :return: folder_id or folder_id/False if create=0
    """
    list_of_file = drive.ListFile({'q':"'root' in parents and trashed=false"}).GetList()
    for drive_folder in list_of_file:
        if drive_folder['title'] == folder_name:
            return drive_folder['id']
    if create:
        folder_id = create_folder(folder_name)
        return folder_id
    else:
        return False

def upload_file_save_id(log,title,filename,full_path='',folderID=0):
    """
    Upload a given file to Google Drive, optionally under a specific parent folder
    :param filename: The path to the file you wish to upload
    :param parent_folder: Optional parent folder override, defaults to root
    :param log: a file object to which the folder id has to be written to
    :return: bool
    """
    id = upload_file(title,filename,full_path,folderID)
    try:
        log.write(filename+': '+str(id)+'\n')
        f = drive.CreateFile({"id":id})
        log.write(f'Url : {f["webContentLink"]}   \n\n')
        print('done writing')
    except:
        print(f'Unable to write to file {log}')
        print('use the upload_file function instead')
        return False
    return True

class IllegalStateException(Exception):
    pass




