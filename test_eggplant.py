import pytest

from eggplant import EggPlant, Source
from errors import Exceptions
from tiktok import TikTok
from douyin import DouYin


@pytest.mark.asyncio
async def test_download_douyin_video():
    cookie_path = "/Users/minyakonga/Downloads/www.douyin.com_cookies.json"
    urls = [
        # 'https://v.douyin.com/iecEVPQo/',
        # 'https://v.douyin.com/iecEgjLy/',
        # 'https://v.douyin.com/ieTs7nBH/',
        'https://v.douyin.com/iRS8TqSf/'
    ]
    for url in urls:
        eggplant = EggPlant(Source.DouYin, cookie_path)
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
    cookie_path = "/Users/minyakonga/Downloads/www.tiktok.com_cookies.json"
    # url = 'https://www.tiktok.com/@neto_song/video/7283228578618035462'
    url = 'https://www.tiktok.com/@runningspeed0/video/7271406113080282373'
    async with TikTok(cookie_path) as tiktok:
        err, video_file_path = await tiktok.download_video(url)
        assert err == Exceptions.OK
        assert ".mp4" in video_file_path

@pytest.mark.asyncio
async def test_douyin():
    cookie_path = "/Users/minyakonga/Downloads/www.douyin.com_cookies.json"
    url = 'https://v.douyin.com/id1agpHj/'
    async with DouYin(cookie_path) as dy:
        err, video_file_path = await dy.download_video(url)
        assert err == Exceptions.OK
        assert ".mp4" in video_file_path
