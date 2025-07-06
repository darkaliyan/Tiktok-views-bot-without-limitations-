
try:
    import requests
except ImportError:
    import os
    print("📦 'requests' not found. Installing...")
    os.system("pip install requests")
    import requests

import re
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

def send_view(video_id):
    url = f"https://api.tiktok.com/aweme/v1/aweme/stats/?aweme_id={video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(url, headers=headers, timeout=5)
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

    print("🚀 Sending views... Press Ctrl+C to stop.\n")

    while True:
        send_view(video_id)
        time.sleep(1)

if __name__ == "__main__":
    main()