from httpx import AsyncClient


async def test_docs(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")
    assert response.status_code == 200, response.text
