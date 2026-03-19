import argparse
import urllib.request

def download_file(url, out_name):
    if not out_name:
        out_name = url.split('/')[-1]
        if not out_name:
            out_name = "downloaded_file"
            
    print(f"Target URL: {url}")
    print(f"Saving file as: {out_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Wget Clone - Stage 2")
    default_url = "https://www.python.org/static/img/python-logo.png"
    parser.add_argument("url", nargs='?', default=default_url, help="The URL to download")
    parser.add_argument("-o", "--output", help="Custom output filename")
    
    args = parser.parse_args()
    
    download_file(args.url, args.output)