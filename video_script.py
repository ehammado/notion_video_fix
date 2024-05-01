# USAGE: 
    # Option 1 (cmd line): python ./video_script.py <notion_export_dir_name>
    # Option 2: python ./video_script.py
        # and manually input notion export directory (line 12)
# IMPORTANT: must have notion export and python script in the same directory

from bs4 import BeautifulSoup
import sys
import os
import re

directory = "" # input notion export directory here
if len(sys.argv) > 1:
    directory = sys.argv[1]
if directory == "":
    print("Error: Directory not specified")
    exit()

video_formats = ["mov", "mp4", "qt"]

for root, dirs, files in os.walk(directory):
    for filename in files:
        if ".html" in filename:
            full_path = os.path.join(root, filename)
            page = open(full_path, encoding="utf8")
            soup = BeautifulSoup(page.read(), features="html.parser")

            formats = '|'.join(video_formats)
            regexp = re.compile(fr"(\.{formats}$)")
           
            videos = soup.find_all(href=regexp)
            for video in videos:
                k,v = "class", ["source"]
                p = video.parent.attrs
                if k in p and v == p[k]:
                    p[k] = ""
                
                video.name = "video"
                video['src'] = video['href']
                del video['href']
                video['style'] = "width:100%"
                video['controls'] = ""            

            page.close()
            with open(full_path, "w", encoding="utf8") as output:
                output.write(str(soup))