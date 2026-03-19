import argparse
import urllib.request
import urllib.error
import sys
import time
import base64

def download_file(url, out_name, retries, user, password, headers):
    if not out_name:
        out_name = url.split('/')[-1]
        if not out_name:
            out_name = "downloaded_file"

    print(f"Target URL: {url}")
    req = urllib.request.Request(url)

    if headers:
        for h in headers:
            if ':' in h:
                k, v = h.split(':', 1)
                req.add_header(k.strip(), v.strip())
    if user and password:
        auth_string = f"{user}:{password}"
        b64_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        req.add_header('Authorization', f'Basic {b64_auth}')

    attempt = 0
    while attempt <= retries:
        try:
            response = urllib.request.urlopen(req, timeout=10)
            total_size = response.getheader('content-length')
            if total_size is None:
                with open(out_name, 'wb') as f:
                    f.write(response.read())
                print(f"\n[Success] Downloaded {out_name} (Unknown size)")
                return
            
            total_size = int(total_size)
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
                        
            print(f"\n[Success] File saved as: {out_name}")
            return

        except urllib.error.HTTPError as e:
            print(f"\n[HTTP Error] Code: {e.code} - {e.reason}")
            break
            
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"\n[Network Error]: {e.reason}")
            attempt += 1
            if attempt <= retries:
                print(f"Retrying... ({attempt}/{retries})")
                time.sleep(2)
            else:
                print("[Failed] Max retries reached. Download aborted.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_url = "http://httpbin.org/basic-auth/user/passwd"
    parser.add_argument("url", nargs='?', default=default_url)
    parser.add_argument("-o", "--output", default="auth_result.json")
    parser.add_argument("--retry", type=int, default=0)
    parser.add_argument("--user", help="Username for Basic Auth")
    parser.add_argument("--password", help="Password for Basic Auth")
    parser.add_argument("--header", action='append', help="Custom headers")
    
    args = parser.parse_args()
    
    download_file(args.url, args.output, args.retry, args.user, args.password, args.header)