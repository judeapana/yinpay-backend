import json
import unittest

import flask_unittest

from yinpay import create_app


class UserEarningTestCase(flask_unittest.ClientTestCase):
    args = {"selector": "bdf7fe91-20d0-4820-a930-6a7d93837b1d"}
    app = create_app()
    token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMjE5NDU2MCwianRpIjoiNDA1ZWI1ZTEtNzdkOC00NzYyLThiNzYtZjQ4NGMzYzk3OTAyIiwibmJmIjoxNjIyMTk0NTYwLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwiZXhwIjoxNjIyMzM4NTYwLCJ1cGRhdGVkIjoiMjAyMS0wNS0yMlQwOTowMzo0OCIsIm5vdGVzIjpudWxsLCJpbWciOm51bGwsImlkIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwibGFzdF9uYW1lIjoic3RyaW5nIiwiYnVzaW5lc3MiOlt7InBob25lX251bWJlciI6IjA1NTQxMzg5ODkiLCJidHlwZSI6Ik5vbnByb2ZpdCBPcmdhbml6YXRpb24iLCJjcmVhdGVkIjoiMjAyMS0wNS0yMlQwOTowMzozNCIsImxvZ28iOm51bGwsInVwZGF0ZWQiOiIyMDIxLTA1LTIyVDExOjAyOjUzIiwiZGVzY3JpcHRpb24iOiJzdHJpbmciLCJ1c2VyX2lkIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5Iiwic3VwcG9ydF9lbWFpbCI6InN0cmluZ0BnbWFpLmNvbSIsImlkIjoiYmRmN2ZlOTEtMjBkMC00ODIwLWE5MzAtNmE3ZDkzODM3YjFkIiwibmFtZSI6IldvcmtlciAzIiwiYWRkcmVzcyI6InN0cmluZyJ9LHsicGhvbmVfbnVtYmVyIjoiMDU1NDEzODk4OSIsImJ0eXBlIjoiTm9ucHJvZml0IE9yZ2FuaXphdGlvbiIsImNyZWF0ZWQiOiIyMDIxLTA1LTIyVDA5OjAzOjQ4IiwibG9nbyI6bnVsbCwidXBkYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJkZXNjcmlwdGlvbiI6InN0cmluZyIsInVzZXJfaWQiOiI2YjVkNTg5Mi1lZjJjLTRlNTEtYTFhMS1jYzkxMmU3ZDZlNTkiLCJzdXBwb3J0X2VtYWlsIjoic3RyaW5nQGdtYWkuY29tIiwiaWQiOiJmYTI0ZTY3Zi1kYTJlLTQ0ODAtYTQ3Yi1kNDhhNThiMjY1OWQiLCJuYW1lIjoic3RyaW4xMjIzZyIsImFkZHJlc3MiOiJzdHJpbmcifV0sInBob25lX251bWJlciI6IjA1NTQxMzg5ODkiLCJjcmVhdGVkIjoiMjAyMS0wNS0yMFQxNzoyMzo1NyIsImhybV9zdXBwb3J0Ijp0cnVlLCJ1c2VybmFtZSI6InN0cmluZyIsImVtYWlsX2FkZHJlc3MiOiJ1Ymlkc21pc0BnbWFpbC5jb20iLCJ1c2VyX21ldGEiOm51bGwsInN1cGVydXNlciI6dHJ1ZSwiZGlzYWJsZWQiOmZhbHNlLCJmaXJzdF9uYW1lIjoic3RyaW5nIiwibGFzdF9sb2dnZWRfaW4iOm51bGwsInBheXJvbGxfc3VwcG9ydCI6dHJ1ZSwicm9sZSI6IkFETUlOIn0.sfg255YvJlYU-erwrAKip5In2-cIL45l4TzDu7SdPu4"

    def test_get(self, client):
        request = client.get('http://127.0.0.1:5000/user-deduction/', query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_post(self, client):
        data = json.dumps(dict(
            user_meta_id='014c7589-7ee7-4e86-83ef-82c23bb320c3',
            deduction_group_id="6503f210-9987-4c0d-9a20-f15ff09a7766",
        ))
        request = client.post('http://127.0.0.1:5000/user-deduction/', query_string=self.args,
                              headers={'Authorization': self.token}, data=data,
                              content_type='application/json')
        # print(request.json)

    def test_get_pk(self, client):
        request = client.get('http://127.0.0.1:5000/user-deduction/152108dc-8e8b-4994-a615-343b308bf9dd',
                             query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_put_pk(self, client):
        data = json.dumps(dict(
            user_meta_id='014c7589-7ee7-4e86-83ef-82c23bb320c3',
            deduction_group_id="6503f210-9987-4c0d-9a20-f15ff09a7766",
        ))
        request = client.put('http://127.0.0.1:5000/user-deduction/152108dc-8e8b-4994-a615-343b308bf9dd',
                             query_string=self.args,
                             headers={'Authorization': self.token}, data=data,
                             content_type='application/json')
        print(request.json)

    def test_delete_pk(self, client):
        request = client.delete('http://127.0.0.1:5000/user-deduction/152108dc-8e8b-4994-a615-343b308bf9dd',
                                query_string=self.args,
                                headers={'Authorization': self.token})
        # print(request.json)


if __name__ == "__main__":
    unittest.main()
