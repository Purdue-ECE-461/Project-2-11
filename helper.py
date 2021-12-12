import sys
import tempfile
from numpy import true_divide
pre_path = sys.path[0]
sys.path.insert(0, pre_path + '/project-1/')
# sys.path.append('/home/mert/Desktop/Berkay/Project-2-11/project-1/')
from proj1 import *
 

 

def run_scoring(path):
    dict_path = main([path])
    return dict_path

def write_url(url):
    # with open('package_url.txt', 'w') as url_file:
    #     url_file.write(str(url))
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as url_file:
        url_file.write(url)
    
    url_file_path = url_file.name

    return url_file_path

def ingestibilty(dict):
    values = dict.values()
    final_score = sum(values)
    # final_score = 0

    if final_score > 0.5:
        return True
    else:
        return False

if __name__ == '__main__':
    url = 'https://github.com/cloudinary/cloudinary_npm'
    write_url(url)
