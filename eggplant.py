from typing import Union
from tiktok import TikTok
from douyin import DouYin


class EggPlant:
    def __init__(self, source: str) -> None:
        """_summary_

        Args:
            source (str): refer class Source

        Raises:
            ValueError: _description_
        """
        if source == Source.TikTok:
            self.eggplant = TikTok(cookie_path="")
        elif source == Source.DouYin:
            self.eggplant = DouYin(cookie_path="")
        else:
            raise ValueError(f"Invalid Source {source}")
    
    async def download_video(self, url: str) -> Union[str, str]:
        """download video by url from sources

        Args:
            url (str): a source url

        Returns:
            Union[str, str]: err-msg, video-file-path
        """
        err, video_file_path = await self.eggplant.download_video(url)
        return err, video_file_path


class Source:
    """common sources that EggPlant supports
    """
    TikTok = "TikTok"
    DouYin = "DouYin"
