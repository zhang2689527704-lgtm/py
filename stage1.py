import sys
import urllib.request

def download_file(url):
    filename = url.split('/')[-1]
    if not filename:
        filename = "downloaded_file"
    urllib.request.urlretrieve(url, filename)
    
    print(f"Success! File saved as: {filename}")


target_url = "https://www.python.org/static/img/python-logo.png"
        
download_file(target_url)