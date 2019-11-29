def test_request(client):
    response = client.get('/queries', query_string={'type': 'appliances'})

    assert 'whisk' in response.json
