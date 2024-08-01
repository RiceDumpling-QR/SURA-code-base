import subprocess


def check_duration(url):
    command = [
        "yt-dlp", 
        "-v", 
        "--cookies-from-browser", 
        "chrome", 
        "--get-duration",
        url
    ]
    try:
        result = subprocess.run(command, capture_output = True, text = True, check = True)
        return result.stdout
    except subprocess.CalledProcessError as e:
            return None
            print(f"Failed to check: {url}")

def convert_time(time):
    time_list = time.split(":")
    for i in range(len(time_list)):
        time_list[i] = int(time_list[i])
    if len(time_list) == 3:
        return 3600*time_list[0] + 60*time_list[1] + time_list[2]
    elif len(time_list) == 2:
        return 60*time_list[0] + time_list[1]
    elif len(time_list) == 1:
        return time_list[0]
    else:
        print("err")
        return 0 
    
    

with open("video_urls.txt","r") as file:
    urls = []
    for line in file:
        urls.append(line.strip())

selected = []
num = 0

for url in urls:
    duration = check_duration(url)
    if duration:
        if 1800 <= convert_time(duration) <= 18000:
            print("selected", url)
            num += 1
            selected.append(url)

with open('selected_url.txt', 'w') as file:
    for url in selected:
        file.write(url + '\n')

print("all done, selected ",num)
    
    