from requests import post
from json import dumps


STATUS_SUCCESS = "success"
STATUS_FAILED = "failed"

PAYMENT_SUCCESS = 201
VERIFY_SUCCESS = 200
INQUIRY_SUCCESS = 200


class IDPayAPI:
    def __init__(self, api_key: str, callback: str, sandbox: bool = False):
        self.callback = callback

        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": api_key,
            "X-SANDBOX": "1" if sandbox else "0",
        }

        self.payment_url = "https://api.idpay.ir/v1.1/payment"
        self.verify_url = "https://api.idpay.ir/v1.1/verify"
        self.inquiry_url = "https://api.idpay.ir/v1.1/inquiry"

    def _send(self, url: str, data: dict, success_code: int) -> dict:
        response = post(url, data=dumps(data), headers=self.headers)

        answer = {"status": STATUS_FAILED, "response": response.json()}
        if response.status_code == success_code:
            answer["status"] = STATUS_SUCCESS

        return answer

    def payment(self, order_id: str, amount: int, payer: dict = {}) -> dict:
        data = {
            "order_id": order_id,
            "amount": amount,
            "callback": self.callback,
            "name": payer.get("name", ""),
            "phone": payer.get("phone", ""),
            "mail": payer.get("mail", ""),
            "desc": payer.get("desc", ""),
        }
        return self._send(self.payment_url, data, PAYMENT_SUCCESS)

    def verify(self, id: str, order_id: str) -> dict:
        data = {"id": id, "order_id": order_id}
        return self._send(self.verify_url, data, VERIFY_SUCCESS)

    def inquiry(self, id: str, order_id: str) -> dict:
        data = {"id": id, "order_id": order_id}
        return self._send(self.inquiry_url, data, INQUIRY_SUCCESS)

    @staticmethod
    def get_status(status: int) -> str | None:
        states = {
            1: "Transaction created",
            2: "Transaction failed",
            3: "An error has occurred",
            4: "Transaction blocked",
            5: "Transaction rejected to payer",
            6: "Transaction rejected",
            7: "Transaction canceled",
            8: "Redirected to IPG",
            10: "Verify pending",
            100: "Transaction verified",
            101: "Verified again",
            200: "Transaction settled",
        }

        return states.get(int(status), None)
