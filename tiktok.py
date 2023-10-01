import asyncio
import uuid
import json
import time
from typing import Union
from selenium import webdriver
from bs4 import BeautifulSoup
from http_util import HttpProxy
from errors import Exceptions

class TikTok:
    def __init__(self, cookie_path: str) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("download.default_directory=/tmp")
        self.driver = webdriver.Chrome(options=options)
        # self.driver.get('https://www.tiktok.com')

    async def download_video(self, url: str) -> Union[str, str]:
        """ download video from TikTok
        * download the url source html source code
        * parse and find the video file url
        * download the video into temp directory

        Args:
            url (str): TikTok video page url

        Returns:
            Union[str, str]: err-msg, video-file-path
        """
        err, rendered_html = await self.__get_rendered_src(url)
        if err != Exceptions.OK:
            return err, ""
        
        err, video_link = await self.__parse_video_url(rendered_html)
        if err != Exceptions.OK:
            return err, ""
        
        print(f'Start download: {video_link}')
        await self.__nav_to_video(video_link)
        self.driver.quit()
        raise TimeoutError

        proxy = HttpProxy()
        err, content = await proxy.get(video_link, cookies_dict)
        if err != Exceptions.OK:
            return err, ""
        
        filename = f'/tmp/{uuid.uuid4()}.mp4'
        with open(filename, 'wb') as f:
            f.write(content)
        
        return Exceptions.OK, filename

    async def __get_rendered_src(self, url: str) -> Union[str, str]:
        """TikTok's web is rendered on client side, so need use headless
        chrome render the page and then get the source code

        Args:
            url (str): _description_

        Returns:
            Union[str, str]: err-msg, html source code
        """
        self.driver.get(url)
        await asyncio.sleep(5)
        return Exceptions.OK, self.driver.page_source

    async def __parse_video_url(self, html: str) -> Union[str, str]:
        """parse and get video play link

        Args:
            html (str): html source code

        Returns:
            Union[str, str]: err-msg, video link
        """
        soup = BeautifulSoup(html, 'html.parser')
        videos = soup.find_all('video')
        video_link = videos[0].attrs['src']
        print(f'Video Link: {video_link}')

        return Exceptions.OK, video_link

    async def __nav_to_video(self, video_link: str) -> Union[str, str]:
        """_summary_

        Args:
            video_link (str): _description_

        Returns:
            Union[str, str]: _description_
        """
        self.driver.get(video_link)
        # await asyncio.sleep(8)
        # js = f'''
        #  var a = document.createElement("a");
        #  a.href = "{video_link}";
        #  a.download = "test.mp4";
        #  document.body.appendChild(a); a.click();
        # '''
        # self.driver.execute_script(js)
        # print(f'Downloaded')
        await asyncio.sleep(300)
        return Exceptions.OK, ""
    
    async def upload_video(self, filename: str) -> Union[str, str]:
        """upload video in filename to tiktok

        Args:
            filename (str): _description_

        Returns:
            Union[str, str]: err-msg, _
        """
        pass
