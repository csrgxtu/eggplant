import uuid
from typing import Union, Awaitable
from http_util import HttpProxy
from errors import Exceptions

class SourceHelper:
    @classmethod
    async def download_video(cls, origin_url: str, video_link: str, pw_cookies: Awaitable) -> Union[str, str]:
        """use http client download the video file

        Args:
            origin_url (str): _description_
            video_link (str): _description_
            pw_cookies (Awaitable): _description_

        Returns:
            Union[str, str]: _description_
        """
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': origin_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': 'macOS',
            'Sec-Fetch-Dest': 'empty'
        }
        request_cookies = {}
        for cookie in await pw_cookies:
            request_cookies.update({
                cookie.get('name'): cookie.get('value')
            })

        err, content = await HttpProxy.get(video_link, headers, request_cookies)
        if err != Exceptions.OK:
            return err, ""

        filename = f'/tmp/{uuid.uuid4()}.mp4'
        with open(filename, 'wb') as f:
            f.write(content)

        return Exceptions.OK, filename
