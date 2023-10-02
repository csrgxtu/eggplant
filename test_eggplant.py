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
    cookie_path = "/Users/minyakonga/Downloads/www.tiktok.com_cookies.json"
    urls = [
        'https://www.tiktok.com/@fiqzlirik/video/7278256015328496914',
        'https://www.tiktok.com/@neto_song/video/7283228578618035462',
        'https://www.tiktok.com/@runningspeed0/video/7271406113080282373'
    ]
    for url in urls:
        eggplant = EggPlant(Source.TikTok, cookie_path)
        err, video_file_path = await eggplant.download_video(url)
        assert err == Exceptions.OK
        assert ".mp4" in video_file_path

@pytest.mark.asyncio
async def test_tiktok():
    # url = 'https://www.tiktok.com/@neto_song/video/7283228578618035462'
    url = 'https://www.tiktok.com/@runningspeed0/video/7271406113080282373'
    async with TikTok("/Users/minyakonga/Downloads/www.tiktok.com_cookies.json") as tiktok:
        err, video_file_path = await tiktok.download_video(url)
        assert err == Exceptions.OK
        assert ".mp4" in video_file_path
