from dataclasses import dataclass

import pytest
from httpx import AsyncClient


@dataclass
class Base:
    id: str
    title: str
    description: str


@dataclass
class MenuTempStorage(Base):
    submenus_count: int
    dishes_count: int


@dataclass
class SubmenuTempStorage(Base):
    dishes_count: int


@dataclass
class DishesTempStorage(Base):
    price: str


@pytest.mark.asyncio
class TestRestApi:
    LOCAL_URL = "/api/v1/{}"

    async def test_menus_list(self, async_client: AsyncClient):
        response = await async_client.get(self.LOCAL_URL.format("menus/"))

        assert response.status_code == 200
        assert response.json() == []

    async def test_create_menu(self, async_client: AsyncClient):
        data = {"title": "My menu 1", "description": "My menu description 1"}
        response = await async_client.post(
            self.LOCAL_URL.format("menus/"), json=data
        )
        response_json = response.json()

        assert response.status_code == 201

        assert response_json.get("id") is not None
        MenuTempStorage.id = response_json.get("id")

        assert response_json.get("title") is not None
        MenuTempStorage.title = response_json.get("title")

        assert response_json.get("description") is not None
        MenuTempStorage.description = response_json.get("description")

    async def test_menu_not_empty(self, async_client: AsyncClient):
        response = await async_client.get(self.LOCAL_URL.format("menus/"))

        assert response.status_code == 200
        assert response.json() != []

    async def test_target_menu(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}")
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("id") == MenuTempStorage.id
        assert response_json.get("title") == MenuTempStorage.title
        assert response_json.get("description") == MenuTempStorage.description

    async def test_update_menu(self, async_client: AsyncClient):
        data = {
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        }

        response = await async_client.patch(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}"), json=data
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("title") != MenuTempStorage.title
        assert response_json.get("description") != MenuTempStorage.description

        MenuTempStorage.title = response_json.get("title")
        MenuTempStorage.description = response_json.get("description")

        assert response_json.get("title") == MenuTempStorage.title
        assert response_json.get("description") == MenuTempStorage.description

        await self.test_target_menu(async_client)

    async def test_submenus_list(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}/submenus/")
        )

        assert response.status_code == 200
        assert response.json() == []

    async def test_create_submenu(self, async_client: AsyncClient):
        data = {
            "title": "My submenu 1",
            "description": "My submenu description 1",
        }
        response = await async_client.post(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}/submenus/"),
            json=data,
        )
        response_json = response.json()

        assert response.status_code == 201

        SubmenuTempStorage.id = response_json.get("id")
        SubmenuTempStorage.title = response_json.get("title")
        SubmenuTempStorage.description = response_json.get("description")

        assert SubmenuTempStorage.id == response_json.get("id")
        assert SubmenuTempStorage.title == response_json.get("title")
        assert SubmenuTempStorage.description == response_json.get(
            "description"
        )

    async def test_submenus_list_not_empty(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}/submenus/")
        )

        assert response.status_code == 200
        assert response.json() != []

    async def test_target_submenu(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/submenus/{SubmenuTempStorage.id}"
            )
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("id") == SubmenuTempStorage.id
        assert response_json.get("title") == SubmenuTempStorage.title
        assert (
            response_json.get("description") == SubmenuTempStorage.description
        )

    async def test_update_submenu(self, async_client: AsyncClient):
        data = {
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1",
        }
        response = await async_client.patch(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/submenus/{SubmenuTempStorage.id}"
            ),
            json=data,
        )
        response_json = response.json()

        assert response.status_code == 200

        assert response_json.get("title") != SubmenuTempStorage.title
        assert (
            response_json.get("description") != SubmenuTempStorage.description
        )

        SubmenuTempStorage.title = response_json.get("title")
        SubmenuTempStorage.description = response_json.get("description")

        assert response_json.get("title") == SubmenuTempStorage.title
        assert (
            response_json.get("description") == SubmenuTempStorage.description
        )

        await self.test_target_submenu(async_client)

    async def test_dishes_list(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}/"
                f"dishes/"
            )
        )

        assert response.status_code == 200
        assert response.json() == []

    async def test_create_dish(self, async_client: AsyncClient):
        data = {
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "12.50",
        }
        response = await async_client.post(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}/"
                f"dishes/"
            ),
            json=data,
        )
        response_json = response.json()

        assert response.status_code == 201

        DishesTempStorage.id = response_json.get("id")
        DishesTempStorage.title = response_json.get("title")
        DishesTempStorage.description = response_json.get("description")
        DishesTempStorage.price = response_json.get("price")

        assert DishesTempStorage.id == response_json.get("id")
        assert DishesTempStorage.title == response_json.get("title")
        assert DishesTempStorage.description == response_json.get(
            "description"
        )
        assert DishesTempStorage.price == response_json.get("price")

    async def test_dishes_list_not_empty(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}/"
                f"dishes/"
            )
        )

        assert response.status_code == 200
        assert response.json() != []

    async def test_target_dish(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}/"
                f"dishes/{DishesTempStorage.id}"
            )
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("id") == DishesTempStorage.id
        assert response_json.get("title") == DishesTempStorage.title
        assert (
            response_json.get("description") == DishesTempStorage.description
        )
        assert response_json.get("price") == DishesTempStorage.price

    async def test_update_dish(self, async_client: AsyncClient):
        data = {
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "14.50",
        }
        response = await async_client.patch(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}/"
                f"dishes/{DishesTempStorage.id}"
            ),
            json=data,
        )
        response_json = response.json()

        assert response.status_code == 200

        assert response_json.get("title") != DishesTempStorage.title
        assert (
            response_json.get("description") != DishesTempStorage.description
        )
        assert response_json.get("price") != DishesTempStorage.price

        DishesTempStorage.title = response_json.get("title")
        DishesTempStorage.description = response_json.get("description")
        DishesTempStorage.price = response_json.get("price")

        assert response_json.get("title") == DishesTempStorage.title
        assert (
            response_json.get("description") == DishesTempStorage.description
        )
        assert response_json.get("price") == DishesTempStorage.price

        await self.test_target_dish(async_client)

    async def test_menu_counters(self, async_client: AsyncClient):
        await self.test_create_dish(async_client)

        response = await async_client.get(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}")
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("id") == MenuTempStorage.id
        assert response_json.get("submenus_count") == 1
        assert response_json.get("dishes_count") == 2

    async def test_submenu_counter(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}"
            )
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("id") == SubmenuTempStorage.id
        assert response_json.get("dishes_count") == 2

    async def test_delete_submenu(self, async_client: AsyncClient):
        response = await async_client.delete(
            self.LOCAL_URL.format(
                f"menus/{MenuTempStorage.id}/"
                f"submenus/{SubmenuTempStorage.id}"
            )
        )

        assert response.status_code == 200
        await self.test_submenus_list(async_client)
        await self.test_dishes_list(async_client)

    async def test_menu_counter_after_delete_submenu(
        self, async_client: AsyncClient
    ):
        response = await async_client.get(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}")
        )
        response_json = response.json()

        assert response.status_code == 200
        assert response_json.get("id") == MenuTempStorage.id
        assert response_json.get("submenus_count") == 0
        assert response_json.get("dishes_count") == 0

    async def test_delete_menu(self, async_client: AsyncClient):
        response = await async_client.delete(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}")
        )

        assert response.status_code == 200
        await self.test_menus_list(async_client)

    async def test_target_menu_not_exists(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format(f"menus/{MenuTempStorage.id}")
        )
        response_json = response.json()

        assert response.status_code == 404
        assert response_json.get("detail") == "menu not found"

    async def test_check_not_valid_id_for_menu(
        self, async_client: AsyncClient
    ):
        response = await async_client.get(
            self.LOCAL_URL.format("menus/not_valid_id")
        )

        assert response.status_code == 422

    async def test_check_not_exists_menu(self, async_client: AsyncClient):
        response = await async_client.get(self.LOCAL_URL.format("menus/0"))

        assert response.status_code == 404
        assert response.json().get("detail") == "menu not found"

    async def test_check_not_exists_submenu(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format("menus/1/submenus/0")
        )

        assert response.status_code == 404
        assert response.json().get("detail") == "submenu not found"

    async def test_check_not_exists_dish(self, async_client: AsyncClient):
        response = await async_client.get(
            self.LOCAL_URL.format("menus/1/submenus/1/dishes/0")
        )

        assert response.status_code == 404
        assert response.json().get("detail") == "dish not found"
