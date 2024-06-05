import subprocess
import time
import shutil
import os

def run_command(command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running command {' '.join(command)}: {e}")
            return None


def get_disk_usage(path):
    """Return the used disk space in bytes."""
    total, used, free = shutil.disk_usage(path)
    return used


def get_video_info(video_url):

    info = {}
    info['title'] = run_command(['yt-dlp', '--get-title', video_url])
    info['uploader'] = run_command(['yt-dlp', '--get-filename', '-o', '%(uploader)s', video_url])
    info['duration'] = run_command(['yt-dlp', '--get-duration', video_url])
    
    return info



def download_video(video_url):
    download_directory = os.getcwd()  # You can change this to your desired directory
    initial_disk_usage = get_disk_usage(download_directory)
    
    start_time = time.time()
    
    video_url_quoted = "\"video_url\""

    # Command to execute
    command = [
        "yt-dlp",
        #"-v",
        #"--cookies-from-browser",
        #"chrome",
        "-f",
        "bv[height<=360]+ba/b[height<=360]",
        video_url
    ]

    try:
        # Run the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        end_time = time.time()
        
        final_disk_usage = get_disk_usage(download_directory)
        time_taken = end_time - start_time
        space_used = final_disk_usage - initial_disk_usage
        
        print(result.stdout.decode())
        print("Video downloaded successfully!")
        print(f"Time taken: {time_taken:.2f} seconds")
        print(f"Disk space used: {space_used / (1024 * 1024):.2f} MB")
        
        return time_taken, space_used
    except subprocess.CalledProcessError as e:
        print("An error occurred while downloading the video:")
        print(e.stderr.decode())
        return None, None

if __name__ == "__main__":
    input_file = 'video_urls.txt'
    output_file = 'download_log.txt'
    
    with open(input_file, 'r') as file:
        video_urls = file.readlines()
    
    with open(output_file, 'w') as log_file:
        for url in video_urls:
            url = url.strip()
            if url:
                print(f"Processing {url}...")
                
                time_taken, space_used = download_video(url)
                info = get_video_info(url)
                if time_taken is not None and space_used is not None:
                    log_file.write(f"title: {info['title']} \n")
                    log_file.write(f"uploader: {info['uploader']} \n")
                    log_file.write(f"duration: {info['duration']} \n")
                    log_file.write(f"URL: {url}\n")
                    log_file.write(f"Time taken: {time_taken:.2f} seconds\n")
                    log_file.write(f"Space used: {space_used / (1024 * 1024):.2f} MB\n\n")                 
                else:
                    log_file.write(f"URL: {url}\n")
                    log_file.write("Failed to download\n\n")
                
                # Add a delay between processing each URL
                time.sleep(5)
