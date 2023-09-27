import pytest

from eggplant import EggPlant, Source
from errors import Exceptions


@pytest.mark.asyncio
async def test_download_douyin_video():
    eggplant = EggPlant(Source.DouYin)
    # https://v.douyin.com/ievRk7uf/
    # https://www.douyin.com/video/7281881306265341247
    err, video_file_path = await eggplant.download_video("https://v.douyin.com/ievRk7uf/")
    assert err == Exceptions.OK
