import asyncio
import uuid
import json
import time
from typing import Union
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from http_util import HttpProxy
from errors import Exceptions

class DouYin:
    def __init__(self, cookie_path: str) -> None:
        # options = ChromeOptions()
        # ## regular
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--profile-directory=Default')

        # ## experimental
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('useAutomationExtension', False)

        # options.add_argument('--headless=new')

        # login first, upload video will need login
        with open(cookie_path, 'r') as f:
            self.cookies = json.loads(f.read())

        self.driver = webdriver.Chrome()
        self.driver.get('https://www.douyin.com')
        for cookie in self.cookies:
            self.driver.add_cookie({
                'domain': '.douyin.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": cookie.get('value'),
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            })
        print('after setting cookies')
        self.driver.get('https://www.douyin.com')
        time.sleep(120)
        

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
