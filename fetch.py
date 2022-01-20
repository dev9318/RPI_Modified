try:
    from urllib import urlopen, urlretrieve
except:
    from urllib.request import urlopen, urlretrieve

import json
import os
import datetime
import ssl
from PIL import Image


FROM = "hostel"
FROM += "16"
# BASEURL = 'http://noticeboard.wncc-iitb.org/'
INSTIURL = 'https://insti.app/api/events'
BASE_DIR = '/home/pi/Desktop/Downloads/'
Insti_dir = '/home/pi/Desktop/Downloads/InstiApp/'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args))


# def fetch_data():
#     url = urljoin(BASEURL, 'list/', '?from=' + FROM)
#     response = urlopen(url, context=ctx)
#     data = json.loads(response.read().decode('utf-8'))
#     return data

def fetchInsti():
    InstiResponse = urlopen(INSTIURL, context=ctx)
    Data = json.loads(InstiResponse.read().decode('utf-8'))
    return Data

def prepare_online_list(data):
    online_list = []
    directory_list = []

    # Iterate through all fetched galleries
    for g_index in data['galleries']:
        gallery = data['galleries'][g_index]
        title = gallery['title']

        # Add to directory list for all galleries
        directory_list.append(os.path.join(BASE_DIR, title))

        # Create directories for Galleries if they don't already exist
        if not os.path.exists(os.path.join(BASE_DIR, title)):
            os.makedirs(os.path.join(BASE_DIR, title))


        # Create list of tuples having (PHOTO_URL, DOWNLOAD_PATH)
        for p_index in gallery['photos']:
            photo = gallery['photos'][p_index]
            img_url = photo['url']
            # url = urljoin(BASEURL, img_url)
            name = photo['name']
            # online_list.append((url, os.path.join(BASE_DIR, title, name.replace('|',''))))s

    with open("/home/pi/Desktop/config.json", "r") as jsonFile:
        config = json.load(jsonFile)

    config["directories"] = directory_list

    with open("/home/pi/Desktop/config.json", "w") as jsonFile:
        json.dump(config, jsonFile, indent=2)
    return online_list

def InstiApp_online(InstiAppData):
    online_list = []
    directory_list = []
    title = 'InstiApp'
        # Add to directory list for all galleries
    directory_list.append(os.path.join(BASE_DIR, title))

        # Create directories for Galleries if they don't already exist
    if not os.path.exists(os.path.join(BASE_DIR, title)):
        os.makedirs(os.path.join(BASE_DIR, title))

    # Iterate through all fetched galleries
    number_of_events = InstiAppData['count']
    for x in range(number_of_events):
        gallery = InstiAppData['data'][x] 
        url = gallery['image_url']
        name = gallery['name']
        refined_name = name.replace('|','')
        refined_name = refined_name.replace(':','')
        refined_name = refined_name.replace('/','')
        online_list.append((url, os.path.join(BASE_DIR, title, refined_name)))

    with open("/home/pi/Desktop/config.json", "r") as jsonFile:
        config = json.load(jsonFile)

    config["directories"].append(directory_list[0])

    with open("/home/pi/Desktop/config.json", "w") as jsonFile:
        json.dump(config, jsonFile, indent=2)
    return online_list


def prepare_existing_list(online_list):
    files_to_delete = []
    existing_files = []

    # Find all files inside Downloads/
    for (dirpath, dirnames, filenames) in os.walk(BASE_DIR):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if "InstiApp" in str(file_path):
                continue
            existing_files.append(file_path)

            # If existing file doesn't exist in online list, delete
            found = False
            for online_file in online_list:
                if str(online_file[1]) == str(file_path[:-4]):
                    found = True
                    break
            if found is False:
                if(("Fetch" in file) or ("config" in file)):
                    continue
                os.remove(file_path) 
    return existing_files

def prepare_existing_Insti_list(online_list):
    files_to_delete = []
    existing_files = []

    # Find all files inside Downloads/
    for (dirpath, dirnames, filenames) in os.walk(Insti_dir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Add files present to existing_files list
            existing_files.append(file_path)
            # If existing file doesn't exist in online list, delete
            found = False
            for online_file in online_list:
                if str(online_file[1]) == str(file_path[:-4]):
                    found = True
                    break
            if found is False:
                if(("Fetch" in file) or ("config" in file)):
                    continue
                os.remove(file_path) 
    return existing_files


def download_files(online_list, existing_files):
    for file in online_list:
        if str(file[1])[1:] not in str(existing_files):
            try:
                urlretrieve(file[0], file[1]+".jpg")
                image_file = file[1]+".jpg"
                img_org = Image.open(image_file)
                width_org, height_org = img_org.size
                if (width_org/height_org > 1600/900) : factor = 1600/width_org
                else : factor = 900/height_org
                width = int(width_org * factor)
                height = int(height_org * factor)
                img_anti = img_org.resize((width, height), Image.ANTIALIAS)
                img_anti.save(image_file)
                print("Image Downloaded")
            except:
                print("error!")
                continue


if __name__ == '__main__':
    # data = fetch_data()
    InstiAppData = fetchInsti()

    print("Script running at- " + str(datetime.datetime.now()))

    # print("Hostel noticeboard urls")
    # online_list = prepare_online_list(data)
    # print("updating Hostel images")
    # existing_files = prepare_existing_list(online_list)
    # print("Downloading Hostel images")
    # download_files(online_list, existing_files)

    print("InstiApp urls")
    Insti_online_list = InstiApp_online(InstiAppData)
    print("updating InstiApp images")
    Insti_existing_files = prepare_existing_Insti_list(Insti_online_list)
    print("Downloading InstiApp images")
    download_files(Insti_online_list, Insti_existing_files)

    print("Success!")
