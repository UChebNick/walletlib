import asyncio
import aiohttp
from walletlib.walletlib.error import *


hp = "127.0.0.1:8000"


async def create_wallet(wallet_type="0.01") -> tuple:
    # функция для создания кошелька
    payload = {"wallet_type": wallet_type}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{hp}/wallet/create/", params=payload) as response:
            if response.status == 429:
                raise TooManyRequest(response)
            elif response.status == 200:
                json_data = await response.json()
                if json_data["code"] == 200:
                    return (json_data["pub"], json_data["priv"])
                elif json_data["code"] == 520:
                    raise UnknownError()
                else:
                    if json_data["error"] == "invalid wallet":
                        raise InvalidType(response)
                    elif json_data["error"] == "invalid type":
                        raise InvalidType(response)


class wallet:
    def __init__(self, pub: str, priv: str):
        self.pub = pub
        self.priv = priv
        self.link = f"http://{hp}"
        self.wallet_type = "0.01"





    async def check_amount(self) -> int:
        # функция для проверки баланса

        payload = {"pub": self.pub, "priv": self.priv}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.link}/wallet/amount/", params=payload) as response:
                if response.status == 429:
                    raise TooManyRequest(response)
                elif response.status == 200:
                    json_data = await response.json()
                    if json_data["code"] == 200:
                        return json_data["amount"]
                    elif json_data["code"] == 520:
                        raise UnknownError()
                    else:
                        if json_data["error"] == "there is no such wallet":
                            raise NonExistentWallet(response)
                        elif json_data["error"] == "invalid type":
                            raise InvalidType(response)

    async def send_amount(self, to: str, amount: int) -> None:
        # функция для отправки средств

        payload = {"to_pub": to, "from_pub": self.pub, "from_priv": self.priv, "amount": amount}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.link}/amount/send/", params=payload) as response:
                if response.status == 429:
                    raise TooManyRequest(response)
                elif response.status == 200:
                    return payload
                elif response.status == 520:
                    raise UnknownError()
                else:
                    json_data = await response.json()
                    if json_data["error"] == "invalid to_pub wallet code":
                        raise InvalidPubCode(response)
                    elif json_data["error"] == "invalid amount":
                        raise InvalidAmount(response)
                    elif json_data["error"] == "not enough amount":
                        raise NotEnoughAmount(response)
                    elif json_data["error"] == "invalid type":

                        raise InvalidType(response)

                    async def check_transaction(self):
                        payload = {"priv": self.priv, "pub": self.pub}
                        async with aiohttp.ClientSession() as session:
                            async with session.get(f"{self.link}/wallet/transactions/", params=payload) as response:
                                if response.status == 429:
                                    raise TooManyRequest(response)
                                elif response.status == 200:
                                    json_data = await response.json()
                                    if json_data["code"] == 200:
                                        return json_data["transaction"]
                                    elif json_data["code"] == 520:
                                        raise UnknownError()
                                    else:
                                        if json_data["error"] == "invalid type":
                                            raise InvalidType(response)
