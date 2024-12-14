import pytest


@pytest.mark.respx(base_url="http://knowledge-graph-service", using="httpx")
def test_request(client, knowledge_graph_stub):
    description_equipment = {}
    response = client.post(
        "/",
        data={
            "language_code": "en",
            "descriptions[]": list(description_equipment.keys()),
        },
    )
    assert response.status_code == 500
