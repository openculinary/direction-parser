def test_appliance_query(client):
    response = client.get('/queries', query_string={'type': 'appliances'})

    assert 'blender' in response.json


def test_utensil_query(client):
    response = client.get('/queries', query_string={'type': 'utensils'})

    assert 'whisk' in response.json
