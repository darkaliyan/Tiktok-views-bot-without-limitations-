
try:
    import requests
except ImportError:
    import os
    print("📦 'requests' not found. Installing...")
    os.system("pip install requests")
    import requests

import re
import random
import time

def resolve_redirect(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        print(f"❌ Failed to resolve URL: {e}")
        return None

def extract_video_id(url):
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)
    else:
        print("❌ Could not extract video ID.")
        return None

def load_proxies():
    try:
        with open("proxies.txt", "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def get_proxy(proxies):
    if not proxies:
        return None
    proxy = random.choice(proxies)
    return {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

def send_view(video_id, proxies):
    url = f"https://api.tiktok.com/aweme/v1/aweme/stats/?aweme_id={video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        proxy = get_proxy(proxies)
        response = requests.post(url, headers=headers, proxies=proxy, timeout=5)
        print(f"✅ View sent — Status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

def main():
    video_url = input("🔗 Enter TikTok video URL (short or full): ").strip()
    resolved_url = resolve_redirect(video_url)
    if not resolved_url:
        return

    video_id = extract_video_id(resolved_url)
    if not video_id:
        return

    proxies = load_proxies()

    print("🚀 Sending views... Press Ctrl+C to stop.\n")

    while True:
        send_view(video_id, proxies)
        time.sleep(1)

if __name__ == "__main__":
    main()
