import argparse
import urllib.request
import sys

def download_file(url, out_name):
    if not out_name:
        out_name = url.split('/')[-1]

    print(f"Target URL: {url}")
    print(f"Saving file as: {out_name}")
    response = urllib.request.urlopen(url)
    total_size = int(response.getheader('content-length', 0))
    downloaded = 0
    with open(out_name, 'wb') as f:
        while True:
            chunk = response.read(8192) 
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                sys.stdout.write(f"\rProgress: [{percent:.1f}%] - {downloaded}/{total_size} bytes")
                sys.stdout.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_url = "https://www.python.org/static/img/python-logo.png"
    parser.add_argument("url", nargs='?', default=default_url)
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    
    download_file(args.url, args.output)