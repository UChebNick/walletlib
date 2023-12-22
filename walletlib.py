import requests as r

#http://79.174.80.32:22354/wallet/create/?wallet_type=0.01
def create_wallet(wallet_type: str) -> tuple:
    # function for creating a wallet
    payloud = {"wallet_type": wallet_type}
    callback = r.get("http://79.174.80.32:22354" + "/wallet/create/", params=payloud)
    return {"pub": callback.json()["pub"], "priv": callback.json()["priv"]}


class wallet:
    def __init__(self, pub: str, priv: str) -> None:
        self.pub = pub
        self.priv = priv
        self.link = "http://79.174.80.32:22354"
        self.wallet_type = "0.01"

    def check_amount(self) -> int:
        # function for checking amount

        payload = {"pub": self.pub, "priv": self.priv}
        callback = r.get(self.link + "/wallet/amount/", params=payload)

        if callback.json()["code"] == 200:
            return callback.json()["amount"]

        elif callback.json()["code"] == 520:
            return unknown_error()

        else:
            return error(callback.json()["error"])

    def send_amount(self, to: str, amount: int) -> None:
        # function for making transfers

        payload = {"to_pub": to, "from_pub": self.pub, "from_priv": self.priv, "amount": amount}
        callback = r.get(self.link + "/amount/send/", params=payload)

        if callback.json()["code"] == 200:
            pass

        elif callback.json()["code"] == 520:
            return unknown_error()

        else:
            return error(callback.json()["error"])

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
            return unknown_error()

        else:
            return error(callback.json()["error"])


# functions for calling errors
def unknown_error():
    raise Exception("unknown error")


def error(er):
    raise Exception(f"{er} error")
