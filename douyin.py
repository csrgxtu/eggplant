import json
from typing import Union
from playwright.async_api import async_playwright, expect
from errors import Exceptions
from source_helper import SourceHelper


class DouYin:
    def __init__(self, cookie_path: str) -> None:
        """_summary_

        Args:
            cookie_path (str): _description_
        """
        with open(cookie_path, 'r') as f:
            self.cookies = json.loads(f.read())
    
    async def __aenter__(self) -> None:
        """async context manager, prepare the chrome instance
        """
        self.apw = async_playwright()
        pw = await self.apw.__aenter__()
        self.browser = await pw.chromium.launch()
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        # set chrome exported cookies into playwright
        pw_cookies = []
        for cookie in self.cookies:
            pw_cookies.append({
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                'domain': cookie.get('domain'),
                'path': cookie.get('path'),
                'HttpOnly': False,
                'HostOnly': False,
                'Secure': False
            })
        await self.context.clear_cookies()
        await self.context.add_cookies(cookies=pw_cookies)

        return self
    
    async def __aexit__(self, exc_type, exc, tb) -> None:
        """async context manager, release the instance

        Args:
            exc_type (_type_): _description_
            exc (_type_): _description_
            tb (_type_): _description_
        """
        await self.context.close()
        await self.browser.close()
        await self.apw.__aexit__()
        

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
        await self.page.goto(url)

        xpath = '//*[@id="douyin-right-container"]/div[2]/div/div[1]/div[2]/div/xg-video-container/video'
        # xpath = '//*[@id="douyin-right-container"]/div[3]/div/div[1]/div[2]/div/xg-video-container/video'
        await expect(self.page.locator(xpath)).to_have_attribute('mediatype', 'video')
        xpath_source = xpath + '/source[2]'
        video_link = await self.page.locator(xpath_source).get_attribute('src')
        video_link = f'https:{video_link}'
        print(f'Extracted VideoLink: {video_link}\n')
        
        return await SourceHelper.download_video(url, video_link, self.context.cookies())

    async def upload_video(self, filename: str) -> Union[str, str]:
        """upload video in filename to tiktok

        Args:
            filename (str): _description_

        Returns:
            Union[str, str]: err-msg, _
        """
        return Exceptions.OK, ""