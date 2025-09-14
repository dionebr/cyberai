import requests

def test_generate_response():
    payload = {
        'prompt': 'Explique SQL Injection',
        'technique': 'sql_injection',
        'context': 'HTB',
        'target': '10.10.10.10'
    }
    resp = requests.post('http://localhost:8000/generate', json=payload)
    assert resp.status_code == 200
    assert 'response' in resp.json()
