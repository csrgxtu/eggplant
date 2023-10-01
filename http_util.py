import aiohttp
from typing import Union
from errors import Exceptions

class HttpProxy:
    @classmethod
    async def get(self, url: str, headers: dict, cookies: dict) -> Union[str, bytes]:
        """get method, download url source code

        Args:
            url (str): _description_
            headers (dict): _description_
            cookies (dict): _description_

        Returns:
            Union[str, bytes]: err-msg, content
        """
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.get(url, headers=headers) as response:
                content = await response.read()
                return Exceptions.OK, content
