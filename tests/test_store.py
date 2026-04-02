from http.client import responses
from symtable import Class

import requests
import pytest
import allure
import jsonschema
from tests.schemas.pet_schema import STORE_SCHEMA, INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_placing_an_order(self):
        with allure.step("Подготовка данных для отправки"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на отправку заказа"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, "Code status is not as expected"
            jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверить поля отправленного заказа"):
            assert response_json['id'] == payload['id'], "ID заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "PetId заказа не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "Quantity заказа не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "Complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_info_about_order(self, create_order):
        with allure.step("Получение id заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данныx ответа"):
            assert response.status_code == 200, "Code status is not as expected"
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self, create_order):
        with allure.step("Получение ID"):
            order_id = create_order["id"]

        with allure.step("Удаление заказа по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса кода ответа"):
            assert response.status_code == 200, "Code status is not as expected"
            assert response.json()["id"] == order_id

        with allure.step("Повторная отправка запроса на удаление"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, "Code status is not as expected"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_info_about_nonexistent_order(self):
        with allure.step("Отправка запроса о несущеструющем заказе"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 404, "Code status is not as expected"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory_data(self):
            with allure.step("Отпрвка запроса на получение инвентаря"):
                response = requests.get(f"{BASE_URL}/store/inventory")
                response_json = response.json()

            with allure.step("Проверить статус ответа и формат ответа"):
                assert response.status_code == 200, "Code status is not as expected"
                jsonschema.validate(response_json, INVENTORY_SCHEMA)
