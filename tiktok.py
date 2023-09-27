from typing import Union


class TikTok:
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
        pass

