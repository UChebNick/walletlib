import pip._internal as pip

def import_lib(name):
    try:
        return __import__(name)
    except ImportError:
        pip.main(['install', name])
    return __import__(name)


requests = import_lib('requests')






import requests as r
from waletlib.error import *


#http://79.174.80.32:22354/wallet/create/?wallet_type=0.01
def create_wallet(wallet_type="0.01") -> tuple:
    # function for creating a wallet
    payloud = {"wallet_type": wallet_type}
    callback = r.get("http://127.0.0.1:8080" + "/wallet/create/", params=payloud)
    if callback.json()["code"] == 200:
        return {"pub": callback.json()["pub"], "priv": callback.json()["priv"]}

    elif callback.json()["code"] == 520:
        raise UnknownError()

    else:
        if callback.json()["error"] == "invalid wallet":
            raise InvalidType(callback)
        elif callback.json()["error"] == "invalid type":
            raise InvalidType(callback)



class wallet:
    def __init__(self, pub: str, priv: str) -> None:
        self.pub = pub
        self.priv = priv
        self.link = "http://127.0.0.1:8080"
        self.wallet_type = "0.01"

    def check_amount(self) -> int:
        # function for checking amount

        payload = {"pub": self.pub, "priv": self.priv}
        callback = r.get(self.link + "/wallet/amount/", params=payload)

        if callback.json()["code"] == 200:
            return callback.json()["amount"]

        elif callback.json()["code"] == 520:
            raise UnknownError()

        else:
            if callback.json()["error"] == "there is no such wallet":
                raise NonExistentWallet(callback)
            elif callback.json()["error"] == "invalid type":
                raise InvalidType(callback)



    def send_amount(self, to: str, amount: int) -> None:
        # function for making transfers

        payload = {"to_pub": to, "from_pub": self.pub, "from_priv": self.priv, "amount": amount}
        callback = r.get(self.link + "/amount/send/", params=payload)

        if callback.json()["code"] == 200:
            return payload

        elif callback.json()["code"] == 520:
            raise UnknownError()

        else:
            if callback.json()["error"] == "invalid to_pub wallet code":
                raise InvalidPubCode(callback)
            elif callback.json()["error"] == "invalid amount":
                raise InvalidAmount(callback)
            elif callback.json()["error"] == "not enough amount":
                raise NotEnoughAmount(callback)
            elif callback.json()["error"] == "invalid type":
                raise InvalidType(callback)





    def check_transaction(self):
        # function for check transaction

        payload = {"priv": self.priv}
        callback = r.get(self.link + "/wallet/transactions/", params=payload)

        if callback.json()["code"] == 200:
            ret = []
            for i in callback.json()["transaction"]:
                ret.append({"to_pub": i[0], "from_priv": i[1], "amount": i[2], "time": i[3][:-1]})
            return ret


        elif callback.json()["code"] == 520:
            raise UnknownError()

        else:
            if callback.json()["error"] == "invalid type":
                raise InvalidType(callback)
