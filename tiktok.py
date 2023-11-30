import json
from typing import Union
from playwright.async_api import async_playwright, expect
from errors import Exceptions
from source_helper import SourceHelper


class TikTok:
    def __init__(self, cookie_path: str) -> None:
        """_summary_

        Args:
            cookie_path (str): _description_
        """
        # self.proxy = 'socks5://127.0.0.1:1080'
        self.proxy = ''
        with open(cookie_path, 'r') as f:
            self.cookies = json.loads(f.read())

    async def __aenter__(self) -> None:
        """async context manager, prepare the chrome instance
        """
        self.apw = async_playwright()
        pw = await self.apw.__aenter__()
        self.browser = await pw.chromium.launch(
            proxy={
                "server": self.proxy,
            }
        )
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
        """ download video from TikTok
        * download the url source html source code
        * parse and find the video file url
        * download the video into temp directory

        Args:
            url (str): TikTok video page url

        Returns:
            Union[str, str]: err-msg, video-file-path
        """
        await self.page.goto(url)

        xpath = f'//*[@id="xgwrapper-4-{url.split("/")[-1]}"]/video'
        await expect(self.page.locator(xpath)).to_have_attribute(name="mediatype", value="video")
        video_link = await self.page.locator(xpath).get_attribute('src')
        print(f'Extracted VideoLink: {video_link}\n')

        return await SourceHelper.download_video(url, video_link, self.context.cookies(), self.proxy)

    async def upload_video(self, filename: str) -> Union[str, str]:
        """upload video in filename to tiktok

        Args:
            filename (str): _description_

        Returns:
            Union[str, str]: err-msg, _
        """
        return Exceptions.OK, ""
