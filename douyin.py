from typing import Union
from bs4 import BeautifulSoup
from http_util import HttpProxy
from errors import Exceptions

class DouYin:
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
        proxy = HttpProxy()
        err, html = await proxy.get(url)
        if err != Exceptions.OK:
            return err, ""
        print(f'{html}')

        await self.__parse_video_url(html)
        
        return Exceptions.OK, html

    async def __parse_video_url(self, html: str) -> Union[str, str]:
        """parse and get video play link

        Args:
            html (str): html source code

        Returns:
            Union[str, str]: err-msg, video link
        """
        soup = BeautifulSoup(html, 'html.parser')
        video_tag = soup.find("xg-video-container")
        print('\n')
        print(video_tag.text)
