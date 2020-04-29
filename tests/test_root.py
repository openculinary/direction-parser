def test_appliance_queries(client):
    response = client.get('/queries', query_string={'type': 'appliances'})

    assert 'blender' in response.json


def test_utensil_queries(client):
    response = client.get('/queries', query_string={'type': 'utensils'})

    assert 'whisk' in response.json


def test_vessel_queries(client):
    response = client.get('/queries', query_string={'type': 'vessels'})

    assert 'dutch oven' in response.json


def test_description_parsing(client):
    description_equipment = {
        'pre-heat the oven to 300 degrees': {
            'appliances': ['oven'],
        },
        'leave the slow cooker on a low heat for three hours': {
            'appliances': ['slow cooker'],
        },
        'remove the casserole dish from the oven': {
            'appliances': ['oven'],
            'vessels': ['casserole dish'],
        },
        'place the skewers in the frying pan': {
            'utensils': ['skewer'],
            'vessels': ['frying pan'],
        },
    }

    response = client.post('/', data={
        'descriptions[]': list(description_equipment.keys())
    })
    for result in response.json:
        assert result['description'] in description_equipment
        for key, value in description_equipment[result['description']].items():
            assert result[key] == value
