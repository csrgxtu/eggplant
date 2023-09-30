import pytest

from eggplant import EggPlant, Source
from errors import Exceptions


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
