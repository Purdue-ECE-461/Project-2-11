import sys

from numpy import true_divide
sys.path.insert(0, '/home/mert/Desktop/Berkay/Project-2-11/project-1/')
# sys.path.append('/home/mert/Desktop/Berkay/Project-2-11/project-1/')
from proj1 import *
 

# def testt():
#     with open("dict.txt") as fptr:
#         dict_resp = json.loads(fptr.read())
#     print(dict_resp) 

def run_scoring():
    main(['package_url.txt'])

def write_url(url):
    with open('package_url.txt', 'w') as url_file:
        url_file.write(str(url))

def ingestibilty(dict):
    values = dict.values()
    final_score = 0
    if final_score > 0.5:
        return True
    else:
        return False

if __name__ == '__main__':
    url = 'https://github.com/cloudinary/cloudinary_npm'
    write_url(url)
