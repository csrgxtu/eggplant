import uuid
import json
from typing import Union
from http_util import HttpProxy
from errors import Exceptions
from playwright.async_api import async_playwright
from playwright.async_api import expect
import requests

class TikTok:
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
        self.browser = await pw.chromium.launch(
            proxy={
                "server": "socks5://127.0.0.1:1080",
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

        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': 'macOS',
            'Sec-Fetch-Dest': 'empty'
        }
        request_cookies = {}
        for cookie in await self.context.cookies():
            request_cookies.update({
                cookie.get('name'): cookie.get('value')
            })
        
        # err, data = await HttpProxy.get(video_link, headers=headers, cookies=request_cookies)
        # if err != Exceptions.OK:
        #     return err, ""
        
        res = requests.get(video_link, headers=headers, cookies=request_cookies)
        print(f'Requests: {res.status_code}')
        with open('./test.mp4', 'wb') as f:
            f.write(res.content)

        return Exceptions.OK, "./test.mp4"

    async def upload_video(self, filename: str) -> Union[str, str]:
        """upload video in filename to tiktok

        Args:
            filename (str): _description_

        Returns:
            Union[str, str]: err-msg, _
        """
        return Exceptions.OK, ""
