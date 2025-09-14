import requests

def test_techniques_endpoint():
    resp = requests.get('http://localhost:8000/techniques')
    assert resp.status_code == 200
    assert 'techniques' in resp.json()
