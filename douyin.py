import asyncio
import uuid
from typing import Union
from bs4 import BeautifulSoup
from selenium import webdriver
from http_util import HttpProxy
from errors import Exceptions

class DouYin:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    async def download_video(self, url: str) -> Union[str, str]:
        """ download video from DouYin
        * download the url source html source code
        * parse and find the video file url
        * download the video into temp directory

        Args:
            url (str): DouYin video page url

        Returns:
            Union[str, str]: err-msg, video-file-path
        """
        err, rendered_html = await self.__get_rendered_src(url)
        if err != Exceptions.OK:
            return err, ""
        
        err, video_link = await self.__parse_video_url(rendered_html)
        if err != Exceptions.OK:
            return err, ""
        
        proxy = HttpProxy()
        err, content = await proxy.get(video_link)
        if err != Exceptions.OK:
            return err, ""

        filename = f'/tmp/{uuid.uuid4()}.mp4'
        with open(filename, 'wb') as f:
            f.write(content)

        return Exceptions.OK, filename

    async def __get_rendered_src(self, url: str) -> Union[str, str]:
        """DouYin's web is rendered on client side, so need use headless
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
        sources = soup.find_all('source')
        video_link = "https:" + sources[-1].attrs['src']
        print(f'Video Link: {video_link}')

        self.driver.get(video_link)
        await asyncio.sleep(3)
        cdn_link = self.driver.current_url
        self.driver.close()
        print(f'After 302: {cdn_link}')

        return Exceptions.OK, cdn_link
