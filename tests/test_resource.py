def test_resource_automatically_decorates_get_handlers(client):
    # Given that I have a GET handler for /people
    # When I request that resource
    response = client.simulate_get("/people")

    # Then I should get back a successful response
    assert response.status_code == 200

    # And it should contain a JSON response
    assert response.json == {"people": []}


def test_resource_handlers_can_return_custom_status_codes(client):
    # Given that I have a POST handler for /people that returns a 201
    # When I request that resource
    response = client.simulate_post("/people")

    # Then I should get back a 201
    assert response.status_code == 201

    # And it should contain a JSON response
    assert response.json == {}


def test_resource_handlers_can_return_no_content(client):
    # Given that I have a DELETE handler for /people/{pk} that returns nothing
    # When I request that resource
    response = client.simulate_delete("/people/foo")

    # Then I should get back a 204
    assert response.status_code == 204

    # And it should contain no response
    assert response.content == b""

def test_resource_handlers_can_return_no_content_with_nativ_error(client):
    # Given that I have a DELETE handler for /people/{pk} that fails
    # When I request that resource
    response = client.simulate_post("/butterfly")

    # Then I should get back a 400
    assert response.status_code == 400

    # And it should contain no response
    assert response.content == b""
