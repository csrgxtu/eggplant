import pytest

from eggplant import EggPlant, Source
from errors import Exceptions
from tiktok import TikTok


@pytest.mark.asyncio
async def test_download_douyin_video():
    urls = [
        # 'https://v.douyin.com/ievRk7uf/',
        # 'https://v.douyin.com/iecENcVj/',
        # 'https://v.douyin.com/iecEuGWp/',
        # 'https://v.douyin.com/iecEbWKX/',
        # 'https://v.douyin.com/iecEVPQo/',
        'https://v.douyin.com/iecEgjLy/',
        # 'https://v.douyin.com/ieTs7nBH/'
    ]
    for url in urls:
        eggplant = EggPlant(Source.DouYin)
        err, video_file_path = await eggplant.download_video(url)
        assert err == Exceptions.OK
        assert ".mp4" in video_file_path

@pytest.mark.asyncio
async def test_download_tiktok_video():
    urls = [
        'https://www.tiktok.com/@neto_song/video/7283228578618035462?is_from_webapp=1&sender_device=pc&web_id=7283401144314725931'
    ]
    for url in urls:
        eggplant = EggPlant(Source.TikTok)
        err, video_file_path = await eggplant.download_video(url)
        assert err == Exceptions.OK
        # assert ".mp4" in video_file_path

@pytest.mark.asyncio
async def test_tiktok():
    url = 'https://www.tiktok.com/@neto_song/video/7283228578618035462'
    async with TikTok("/Users/minyakonga/Downloads/www.tiktok.com_cookies.json") as tiktok:
        await tiktok.download_video(url)
