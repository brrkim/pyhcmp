from app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    
# def test_create_item():
#     body = {
#         "name": "testname",
#         "description": "testdescription",
#         "price": 2000,
#         "tax": 2000
#     }
#     response = client.post('/items',json=body)
#     assert response.status_code == 200
#     assert response.json() == body

def test_read_item():
    response = client.get('/items')
    assert response.status_code == 200
    assert response.json()