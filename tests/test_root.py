def test_request(client):
    response = client.get('/queries', query_string={'type': 'utensils'})

    assert 'whisk' in response.json
