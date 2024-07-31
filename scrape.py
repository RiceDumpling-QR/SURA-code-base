import subprocess


def download_video(url):
    try:
        command = ["yt-dlp",
                "-vU",
                "-S",
                "res:160",
                url]
        result = subprocess.run(command, capture_output = True, text = True, check = True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to download: {url}")
        return None


with open("video_urls.txt","r") as file:
    urls = []
    for line in file:
        urls.append(line.strip())

for url in urls:
    print("processing", url)
    download_video(url)


