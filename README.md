# eggplant
An SDK for tiktok and douyin which support download videos without water mark and upload videos. (upload videos not implement yet)

# How it works
By using `playwright` scrape the video page you specified, get the rendered source code, parse the source code and get the video file link, then use http client download the video file into your file system.  

*Note: Due to the anti-crawler policy, the video file link will change constantly, so sometimes this sdk won't get the video file. If you encounter this scenario, please let me know.*

# Get Started
## Requirements
1, Python3, network connectivity to tiktok.com or douyin.com  
2, clone the source code
```Bash
$ git clone git@github.com:csrgxtu/eggplant.git
```
3, install dependencies
```Bash
$ pip install -r requirements
```
4, prepare your cookie json file which will be used by script  
  * install chrome extension [Get cookies.txt locally](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc?pli=1)
  * access [tiktok.com](tiktok.com) or [douyin.com](douyin.com) in your chrome
  * in the extension, select `json` export format and then click `Export`  

5, create your script in source root dir like following:
```Bash
touch my_download_script.py
```
6, following two code snippet, the video file will be downloaded at your `/tmp/`

## Download From Douyin
```Python
from eggplant import EggPlant, Source
from errors import Exceptions
from douyin import DouYin

cookie_path = "/tmp/www.douyin.com_cookies.json"
url = 'https://v.douyin.com/id1agpHj/'
async with DouYin(cookie_path) as dy:
    err, video_file_path = await dy.download_video(url)
    assert err == Exceptions.OK
    assert ".mp4" in video_file_path
```

## Download From TikTok
```Python
from eggplant import EggPlant, Source
from errors import Exceptions
from tiktok import TikTok

cookie_path = "/tmp/www.tiktok.com_cookies.json"
url = 'https://www.tiktok.com/@runningspeed0/video/7271406113080282373'
async with TikTok(cookie_path) as tiktok:
    err, video_file_path = await tiktok.download_video(url)
    assert err == Exceptions.OK
    assert ".mp4" in video_file_path
```

## TODO
1, make eggplant `pip` installable  
2, support upload video
