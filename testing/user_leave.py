import json
import unittest

import flask_unittest

from yinpay import create_app


class UserLeaveTestCase(flask_unittest.ClientTestCase):
    args = {"selector": "bdf7fe91-20d0-4820-a930-6a7d93837b1d"}
    app = create_app()
    token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMjExMDY3NCwianRpIjoiODZjZTIwMzItMTFiYy00MTM1LWE4Y2EtYTk3NDg1MzUyNWVhIiwibmJmIjoxNjIyMTEwNjc0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwiZXhwIjoxNjIyMjU0Njc0LCJmaXJzdF9uYW1lIjoic3RyaW5nIiwibGFzdF9sb2dnZWRfaW4iOm51bGwsImxhc3RfbmFtZSI6InN0cmluZyIsImVtYWlsX2FkZHJlc3MiOiJ1Ymlkc21pc0BnbWFpbC5jb20iLCJpbWciOm51bGwsInN1cGVydXNlciI6dHJ1ZSwicm9sZSI6IkFETUlOIiwidXBkYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJidXNpbmVzcyI6W3siZGVzY3JpcHRpb24iOiJzdHJpbmciLCJsb2dvIjpudWxsLCJuYW1lIjoiV29ya2VyIDMiLCJjcmVhdGVkIjoiMjAyMS0wNS0yMlQwOTowMzozNCIsInBob25lX251bWJlciI6IjA1NTQxMzg5ODkiLCJzdXBwb3J0X2VtYWlsIjoic3RyaW5nQGdtYWkuY29tIiwidXBkYXRlZCI6IjIwMjEtMDUtMjJUMTE6MDI6NTMiLCJpZCI6ImJkZjdmZTkxLTIwZDAtNDgyMC1hOTMwLTZhN2Q5MzgzN2IxZCIsImFkZHJlc3MiOiJzdHJpbmciLCJidHlwZSI6Ik5vbnByb2ZpdCBPcmdhbml6YXRpb24iLCJ1c2VyX2lkIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5In0seyJkZXNjcmlwdGlvbiI6InN0cmluZyIsImxvZ28iOm51bGwsIm5hbWUiOiJzdHJpbjEyMjNnIiwiY3JlYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJwaG9uZV9udW1iZXIiOiIwNTU0MTM4OTg5Iiwic3VwcG9ydF9lbWFpbCI6InN0cmluZ0BnbWFpLmNvbSIsInVwZGF0ZWQiOiIyMDIxLTA1LTIyVDA5OjAzOjQ4IiwiaWQiOiJmYTI0ZTY3Zi1kYTJlLTQ0ODAtYTQ3Yi1kNDhhNThiMjY1OWQiLCJhZGRyZXNzIjoic3RyaW5nIiwiYnR5cGUiOiJOb25wcm9maXQgT3JnYW5pemF0aW9uIiwidXNlcl9pZCI6IjZiNWQ1ODkyLWVmMmMtNGU1MS1hMWExLWNjOTEyZTdkNmU1OSJ9XSwidXNlcl9tZXRhIjpudWxsLCJjcmVhdGVkIjoiMjAyMS0wNS0yMFQxNzoyMzo1NyIsImRpc2FibGVkIjpmYWxzZSwiaWQiOiI2YjVkNTg5Mi1lZjJjLTRlNTEtYTFhMS1jYzkxMmU3ZDZlNTkiLCJ1c2VybmFtZSI6InN0cmluZyIsImhybV9zdXBwb3J0Ijp0cnVlLCJwYXlyb2xsX3N1cHBvcnQiOnRydWUsInBob25lX251bWJlciI6IjA1NTQxMzg5ODkiLCJub3RlcyI6bnVsbH0.GP2QXtJHbXll6b0kXe5W9w7gkLGXoLaB-gIF32y5pHs"

    def test_get(self, client):
        request = client.get('http://127.0.0.1:5000/user-leave/', query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_post(self, client):
        # data = json.dumps(dict(
        #     reason="To dream",
        #     from_date="01-01-1999",
        #     ltype="",
        #     to_date="01-01-1999",
        #     user_meta_id="014c7589-7ee7-4e86-83ef-82c23bb320c3"
        # ))
        # request = client.post('http://127.0.0.1:5000/user-leave/', query_string=self.args,
        #                       headers={'Authorization': self.token}, data=data,
        #                       content_type='application/json')
        # print(request.json)
        pass

    def test_get_pk(self, client):
        request = client.get('http://127.0.0.1:5000/user-leave/f8f368f9-1c9d-4141-a287-1738ca1b38f4',
                             query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_put_pk(self, client):
        data = json.dumps(dict(
            reason="To dream of 22",
            from_date="01-01-1999",
            ltype="",
            to_date="01-01-1999",
            user_meta_id="014c7589-7ee7-4e86-83ef-82c23bb320c3"
        ))
        request = client.put('http://127.0.0.1:5000/user-leave/f8f368f9-1c9d-4141-a287-1738ca1b38f4',
                             query_string=self.args,
                             headers={'Authorization': self.token}, data=data,
                             content_type='application/json')
        print(request.json)

    def test_delete_pk(self, client):
        request = client.delete('http://127.0.0.1:5000/user-leave/f8f368f9-1c9d-4141-a287-1738ca1b38f4',
                                query_string=self.args,
                                headers={'Authorization': self.token})
        print(request.json)


if __name__ == "__main__":
    unittest.main()
