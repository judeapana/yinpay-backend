import json
import unittest

import flask_unittest

from yinpay import create_app


class BusinessAccountsTestCase(flask_unittest.ClientTestCase):
    args = {"selector": "bdf7fe91-20d0-4820-a930-6a7d93837b1d"}
    app = create_app()
    token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMTg1MTM4NywianRpIjoiZDQ0MjhhYjctODc4NC00YmY2LTgwOWQtYWFhYzRhNDdhODMwIiwibmJmIjoxNjIxODUxMzg3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwiZXhwIjoxNjIxOTk1Mzg3LCJub3RlcyI6bnVsbCwicGF5cm9sbF9zdXBwb3J0Ijp0cnVlLCJsYXN0X25hbWUiOiJzdHJpbmciLCJzdXBlcnVzZXIiOnRydWUsInVzZXJfbWV0YSI6bnVsbCwiaW1nIjpudWxsLCJ1c2VybmFtZSI6InN0cmluZyIsInJvbGUiOiJBRE1JTiIsInVwZGF0ZWQiOiIyMDIxLTA1LTIyVDA5OjAzOjQ4IiwiY3JlYXRlZCI6IjIwMjEtMDUtMjBUMTc6MjM6NTciLCJpZCI6IjZiNWQ1ODkyLWVmMmMtNGU1MS1hMWExLWNjOTEyZTdkNmU1OSIsImhybV9zdXBwb3J0Ijp0cnVlLCJwaG9uZV9udW1iZXIiOiIwNTU0MTM4OTg5IiwiZW1haWxfYWRkcmVzcyI6InViaWRzbWlzQGdtYWlsLmNvbSIsImxhc3RfbG9nZ2VkX2luIjpudWxsLCJmaXJzdF9uYW1lIjoic3RyaW5nIiwiZGlzYWJsZWQiOmZhbHNlLCJidXNpbmVzcyI6W3sicGhvbmVfbnVtYmVyIjoiMDU1NDEzODk4OSIsInN1cHBvcnRfZW1haWwiOiJzdHJpbmdAZ21haS5jb20iLCJkZXNjcmlwdGlvbiI6InN0cmluZyIsImJ0eXBlIjoiTm9ucHJvZml0IE9yZ2FuaXphdGlvbiIsImxvZ28iOm51bGwsImFkZHJlc3MiOiJzdHJpbmciLCJpZCI6ImJkZjdmZTkxLTIwZDAtNDgyMC1hOTMwLTZhN2Q5MzgzN2IxZCIsInVwZGF0ZWQiOiIyMDIxLTA1LTIyVDExOjAyOjUzIiwidXNlcl9pZCI6IjZiNWQ1ODkyLWVmMmMtNGU1MS1hMWExLWNjOTEyZTdkNmU1OSIsImNyZWF0ZWQiOiIyMDIxLTA1LTIyVDA5OjAzOjM0IiwibmFtZSI6IldvcmtlciAzIn0seyJwaG9uZV9udW1iZXIiOiIwNTU0MTM4OTg5Iiwic3VwcG9ydF9lbWFpbCI6InN0cmluZ0BnbWFpLmNvbSIsImRlc2NyaXB0aW9uIjoic3RyaW5nIiwiYnR5cGUiOiJOb25wcm9maXQgT3JnYW5pemF0aW9uIiwibG9nbyI6bnVsbCwiYWRkcmVzcyI6InN0cmluZyIsImlkIjoiZmEyNGU2N2YtZGEyZS00NDgwLWE0N2ItZDQ4YTU4YjI2NTlkIiwidXBkYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJ1c2VyX2lkIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwiY3JlYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJuYW1lIjoic3RyaW4xMjIzZyJ9XX0._DOD3BOZ-nXi40m0A3xJcdrz6dCfLtDGB9zcz23FpHA"

    def test_get(self, client):
        request = client.get('http://127.0.0.1:5000/ba/', query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_post(self, client):
        data = json.dumps(dict(
            account_number="0449949940303",
            currency="GHS",
            code="",
            account_name="Apana Jude",
        ))
        request = client.post('http://127.0.0.1:5000/ba/', query_string=self.args,
                              headers={'Authorization': self.token}, data=data,
                              content_type='application/json')
        # print(request.json)

    def test_get_pk(self, client):
        request = client.get('http://127.0.0.1:5000/ba/2930bdab-9014-4fff-b42d-ee8dca0af606', query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_put_pk(self, client):
        data = json.dumps(dict(
            account_number="0449949940303",
            currency="GHS",
            code="",
            account_name="Apana Jude 0034",
        ))
        request = client.put('http://127.0.0.1:5000/ba/2930bdab-9014-4fff-b42d-ee8dca0af606', query_string=self.args,
                              headers={'Authorization': self.token}, data=data,
                              content_type='application/json')
        # print(request.json)

    def test_delete_pk(self, client):
        request = client.delete('http://127.0.0.1:5000/ba/2930bdab-9014-4fff-b42d-ee8dca0af606', query_string=self.args,
                             headers={'Authorization': self.token})
        print(request.json)


if __name__ == "__main__":
    unittest.main()
