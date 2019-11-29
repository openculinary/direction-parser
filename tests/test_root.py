def test_appliance_query(client):
    response = client.get('/queries', query_string={'type': 'appliances'})

    assert 'blender' in response.json


def test_utensil_query(client):
    response = client.get('/queries', query_string={'type': 'utensils'})

    assert 'whisk' in response.json


def test_vessel_query(client):
    response = client.get('/queries', query_string={'type': 'vessels'})

    assert 'dutch oven' in response.json
