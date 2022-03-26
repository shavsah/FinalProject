import os
import time
import json
import requests
import threading

print('*********')
# Takes the json file path and name
json_name = input('Enter json file name. >>>  ')
print('*********')

# Takes the folder name to creat the folder in which the images will be saved
dir_name = input('Pleas enter your directory name for downloading pictures. >>> ')

# Start time of the program
t1 = time.time()

pic_names = []
urls_list = []
thread_list = []

# Takes json urls and defining image names
try:
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, dir_name) 
    os.mkdir(path)

    with open(json_name, "r") as f:
        data = json.load(f)
    for i in data.values():
        for j in i:
            a = list(j.values())[0]
            urls_list.append(a)

    for i in range(1, len(urls_list) + 1):
        name = 'picture_' + str(i) + '.jpeg'
        pic_names.append(name)

except FileExistsError:
    print('*********')
    print('Folder with the same name already exists.')

# Downloading images into the created folder
def download_images(url, name):
    try:
        r = requests.get(url)
        out = open(f'{path}/{name}', 'wb')
        out.write(r.content)
        out.close()
        print(f'{name} downloaded !')
    except requests.exceptions.RequestException as e:
        print('Somthing went wrong with URLs.')

# Uses threading
for i in range(0, len(urls_list)):
    t = threading.Thread(target = download_images, args = (urls_list[i], pic_names[i]))
    thread_list.append(t)
    t.start()
for j in thread_list:
    j.join()

# End time of the program
t2 = time.time()

print('*********')

# Calculating time of the program
print(f'The program ends in {t2 - t1} seconds.')

# Deletes the folder in case it is empty
if os.path.exists(path) and len(os.listdir(path)) == 0:
    print(f'Folder {dir_name} deleted because it is empty.')
    os.rmdir(path)