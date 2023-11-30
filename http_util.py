import httpx
from typing import Union
from errors import Exceptions

class HttpProxy:
    @classmethod
    async def get(self, url: str, headers: dict, cookies: dict, proxy: str) -> Union[str, bytes]:
        """get method, download url source code

        Args:
            url (str): _description_
            headers (dict): _description_
            cookies (dict): _description_
            proxy (str): http/https/socks5 proxy, like socks5://127.0.0.1:1080

        Returns:
            Union[str, bytes]: err-msg, content
        """
        if proxy:
            client = httpx.AsyncClient(proxies=proxy)
        else:
            client = httpx.AsyncClient()

        async with client:
            res = await client.get(url, headers=headers, cookies=cookies)
            if res.status_code == 200:
                return Exceptions.OK, res.content
            
            return Exceptions.DependencyError, ""
