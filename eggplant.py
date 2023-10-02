from typing import Union
from tiktok import TikTok
from douyin import DouYin


class EggPlant:
    def __init__(self, source: str, cookie_path: str) -> None:
        """_summary_

        Args:
            source (str): refer class Source
            cookie_path (str): cookies exported from chrome

        Raises:
            ValueError: _description_
        """
        self.cookie_path = cookie_path
        if source == Source.TikTok:
            self.eggplant = TikTok
        elif source == Source.DouYin:
            self.eggplant = DouYin
        else:
            raise ValueError(f"Invalid Source {source}")
    
    async def download_video(self, url: str) -> Union[str, str]:
        """download video by url from sources

        Args:
            url (str): a source url

        Returns:
            Union[str, str]: err-msg, video-file-path
        """
        async with self.eggplant(self.cookie_path) as eggplant:
            err, video_file_path = await eggplant.download_video(url)
        return err, video_file_path


class Source:
    """common sources that EggPlant supports
    """
    TikTok = "TikTok"
    DouYin = "DouYin"
