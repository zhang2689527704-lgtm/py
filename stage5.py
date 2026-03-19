import argparse
import urllib.request
import urllib.error
import sys
import time

def download_file(url, out_name):
    if not out_name:
        out_name = url.split('/')[-1]

    print(f"Target URL: {url}")
    print(f"Saving file as: {out_name}")
    
    try:
        response = urllib.request.urlopen(url)
        total_size = int(response.getheader('content-length', 0))
        downloaded = 0
        start_time = time.time()
        
        with open(out_name, 'wb') as f:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                
                elapsed = time.time() - start_time
                if elapsed > 0 and total_size > 0:
                    speed_kb = (downloaded / 1024) / elapsed
                    percent = (downloaded / total_size) * 100
                    remaining_bytes = total_size - downloaded
                    eta = remaining_bytes / (speed_kb * 1024) if speed_kb > 0 else 0
                    
                    sys.stdout.write(f"\rProgress: [{percent:.1f}%] | Speed: {speed_kb:.1f} KB/s | ETA: {eta:.1f}s ")
                    sys.stdout.flush()

    except urllib.error.HTTPError as e:
        print(f"\n[HTTP Error] Code: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"\n[Network Error]: {e.reason}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_url = "https://www.python.org/static/img/python-logo.png"
    parser.add_argument("url", nargs='?', default=default_url)
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    
    download_file(args.url, args.output)