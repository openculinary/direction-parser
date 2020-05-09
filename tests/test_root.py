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
        'Pre-heat the oven to 250 degrees F.': {
            'markup': 'Pre-heat the <mark>oven</mark> to 250 degrees F.',
            'appliances': [{'appliance': 'oven'}],
        },
        'leave the Slow cooker, on a low heat': {
            'markup': 'leave the <mark>Slow cooker</mark>, on a low heat',
            'appliances': [{'appliance': 'slow cooker'}],
        },
        'place casserole dish in oven': {
            'markup': 'place <mark>casserole dish</mark> in <mark>oven</mark>',
            'appliances': [{'appliance': 'oven'}],
            'vessels': [{'vessel': 'casserole dish'}],
        },
        'empty skewer into the karahi': {
            'markup': 'empty <mark>skewer</mark> into the <mark>karahi</mark>',
            'utensils': [{'utensil': 'skewer'}],
            'vessels': [{'vessel': 'karahi'}],
        },
    }

    response = client.post('/', data={
        'descriptions[]': list(description_equipment.keys())
    })
    for result in response.json:
        assert result['description'] in description_equipment
        for key, value in description_equipment[result['description']].items():
            assert result[key] == value
