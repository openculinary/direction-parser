def test_request(client, knowledge_graph_stub):
    description_equipment = {}
    response = client.post(
        "/", data={"descriptions[]": list(description_equipment.keys())}
    )
    assert response.status_code == 500
