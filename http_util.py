import aiohttp
from typing import Union
from errors import Exceptions


class HttpProxy:
    def __init__(self) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
    
    async def get(self, url: str) -> Union[str, bytes]:
        """get method, download url source code

        Args:
            url (str): _description_

        Returns:
            Union[str, bytes]: err-msg, content
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                content = await response.read()
                return Exceptions.OK, content
