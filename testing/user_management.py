import json
import unittest

import flask_unittest

from yinpay import create_app


class UserManagementTestCase(flask_unittest.ClientTestCase):
    args = {"selector": "bdf7fe91-20d0-4820-a930-6a7d93837b1d"}
    app = create_app()
    token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMTg1MTM4NywianRpIjoiZDQ0MjhhYjctODc4NC00YmY2LTgwOWQtYWFhYzRhNDdhODMwIiwibmJmIjoxNjIxODUxMzg3LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwiZXhwIjoxNjIxOTk1Mzg3LCJub3RlcyI6bnVsbCwicGF5cm9sbF9zdXBwb3J0Ijp0cnVlLCJsYXN0X25hbWUiOiJzdHJpbmciLCJzdXBlcnVzZXIiOnRydWUsInVzZXJfbWV0YSI6bnVsbCwiaW1nIjpudWxsLCJ1c2VybmFtZSI6InN0cmluZyIsInJvbGUiOiJBRE1JTiIsInVwZGF0ZWQiOiIyMDIxLTA1LTIyVDA5OjAzOjQ4IiwiY3JlYXRlZCI6IjIwMjEtMDUtMjBUMTc6MjM6NTciLCJpZCI6IjZiNWQ1ODkyLWVmMmMtNGU1MS1hMWExLWNjOTEyZTdkNmU1OSIsImhybV9zdXBwb3J0Ijp0cnVlLCJwaG9uZV9udW1iZXIiOiIwNTU0MTM4OTg5IiwiZW1haWxfYWRkcmVzcyI6InViaWRzbWlzQGdtYWlsLmNvbSIsImxhc3RfbG9nZ2VkX2luIjpudWxsLCJmaXJzdF9uYW1lIjoic3RyaW5nIiwiZGlzYWJsZWQiOmZhbHNlLCJidXNpbmVzcyI6W3sicGhvbmVfbnVtYmVyIjoiMDU1NDEzODk4OSIsInN1cHBvcnRfZW1haWwiOiJzdHJpbmdAZ21haS5jb20iLCJkZXNjcmlwdGlvbiI6InN0cmluZyIsImJ0eXBlIjoiTm9ucHJvZml0IE9yZ2FuaXphdGlvbiIsImxvZ28iOm51bGwsImFkZHJlc3MiOiJzdHJpbmciLCJpZCI6ImJkZjdmZTkxLTIwZDAtNDgyMC1hOTMwLTZhN2Q5MzgzN2IxZCIsInVwZGF0ZWQiOiIyMDIxLTA1LTIyVDExOjAyOjUzIiwidXNlcl9pZCI6IjZiNWQ1ODkyLWVmMmMtNGU1MS1hMWExLWNjOTEyZTdkNmU1OSIsImNyZWF0ZWQiOiIyMDIxLTA1LTIyVDA5OjAzOjM0IiwibmFtZSI6IldvcmtlciAzIn0seyJwaG9uZV9udW1iZXIiOiIwNTU0MTM4OTg5Iiwic3VwcG9ydF9lbWFpbCI6InN0cmluZ0BnbWFpLmNvbSIsImRlc2NyaXB0aW9uIjoic3RyaW5nIiwiYnR5cGUiOiJOb25wcm9maXQgT3JnYW5pemF0aW9uIiwibG9nbyI6bnVsbCwiYWRkcmVzcyI6InN0cmluZyIsImlkIjoiZmEyNGU2N2YtZGEyZS00NDgwLWE0N2ItZDQ4YTU4YjI2NTlkIiwidXBkYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJ1c2VyX2lkIjoiNmI1ZDU4OTItZWYyYy00ZTUxLWExYTEtY2M5MTJlN2Q2ZTU5IiwiY3JlYXRlZCI6IjIwMjEtMDUtMjJUMDk6MDM6NDgiLCJuYW1lIjoic3RyaW4xMjIzZyJ9XX0._DOD3BOZ-nXi40m0A3xJcdrz6dCfLtDGB9zcz23FpHA"

    def test_get_users(self, client):
        request = client.get('http://127.0.0.1:5000/users/', query_string=self.args,
                             headers={'Authorization': self.token})
        assert request.status != 200

    def test_post_user(self, client):
        data = json.dumps(dict(
            first_name="Apana",
            phone_number="0554138989",
            last_name="Yinime",
            password="test@123",
            email_address="011034@gmail.com",
            username="ppappa",
            user_meta=dict(
                tin="30399494",
                ssn="3991-10020-299",
                religion="Christian",
                marital_status="Married",
                gender="Male",
                department_id='4908712a-e7af-4b23-9951-f6f5031aeee9',
                personnel_group_id="1f22ac4a-d341-4775-b6b2-82de66223a41"
            ),

        ))
        request = client.post('http://127.0.0.1:5000/users/', query_string=self.args,
                              headers={'Authorization': self.token}, data=data,
                              content_type='application/json')
        # print(request.json)

    def test_get_pk(self, client):
        request = client.get('http://127.0.0.1:5000/users/8b8b5364-64d6-437a-9a1f-467ccc1e51e7',
                             query_string=self.args,
                             headers={'Authorization': self.token})
        # print(request.json)

    def test_put_pk(self, client):
        data = json.dumps(dict(
            first_name="Apana",
            phone_number="0554138989",
            last_name="Yinime",
            password="test@123",
            email_address="0034@gmail.com",
            username="app1233",
            user_meta=dict(
                tin="A22",
                ssn="3991-10020-299",
                religion="Christian",
                marital_status="Married",
                gender="Female",
                department_id='4908712a-e7af-4b23-9951-f6f5031aeee9',
                personnel_group_id="1f22ac4a-d341-4775-b6b2-82de66223a41"
            ),

        ))
        request = client.put('http://127.0.0.1:5000/users/7c63d4f9-ac39-4610-9725-6a56b092da1b',
                             query_string=self.args,
                             headers={'Authorization': self.token}, data=data,
                             content_type='application/json')
        # print(request.json)

    def test_delete_pk(self, client):
        request = client.delete('http://127.0.0.1:5000/users/88b6dfe2-3b21-4629-a97d-4bc5ef41717c',
                                query_string=self.args,
                                headers={'Authorization': self.token})
        # print(request.json)

    def test_change_user_pwd(self, client):
        data = json.dumps(dict(
            password='password'
        ))
        request = client.put('http://127.0.0.1:5000/users/8df9acb5-8926-4f7a-aad2-565a3c630247/change-pwd',
                             query_string=self.args, data=data,
                             headers={'Authorization': self.token}, content_type='application/json')
        # print(request.json)

    def test_change_email(self, client):
        data = json.dumps(dict(
            email_address='password@gmail.com'
        ))
        request = client.put('http://127.0.0.1:5000/users/8df9acb5-8926-4f7a-aad2-565a3c630247/change-email-address',
                             query_string=self.args, data=data, content_type='application/json',
                             headers={'Authorization': self.token})
        # print(request.json)


if __name__ == '__main__':
    unittest.main()
