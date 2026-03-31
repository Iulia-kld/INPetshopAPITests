import allure
import jsonschema
import pytest
import requests

from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_a_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/99999")
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, "Code status is not as expected"
        with allure.step("Проверка текстого сообщения"):
            assert response.text == "Pet deleted", "The text is not what is expected"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_a_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 404, "Code status is not as expected"

        with allure.step("Проверка текстового сообщения"):
            assert response.text == "Pet not found", "The text is not what is expected"

    @allure.title("Получить информацию о несуществующем питомце")
    def test_get_information_about_a_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Code status is not as expected"
        with allure.step("Проверка текстового сообщения"):
            assert response.text == "Pet not found", "The text is not what is expected"

    @allure.title("Добавление нового питамца")
    def test_add_new_pet(self):
        with allure.step("Подготовка данных для добавления нового питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на добавление нового питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, "Code status is not as expected"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверить поля создания питомца"):
            assert response_json['id'] == payload['id'], "ID питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_new_pet_with_complete_data(self):
        with allure.step("Подготовка данных для отправки"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{
                    "id": 0, "name": "string"
                }],
                "status": "available"
            }

        with allure.step("Отправка запроса на добавление нового питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, "Code status is not as expected"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверить поля создания питомца"):
             assert response_json['id'] == payload['id'], "ID питомца не совпадает с ожидаемым"
             assert response_json['name'] == payload['name'], "Name питомца не совпадает с ожидаемым"
             assert response_json['status'] == payload['status'], "Status питомца не совпадает с ожидаемым"
             assert response_json['category'] == payload['category'], "Category питомца не совпадает с ожидаемым"
             assert response_json['photoUrls'] == payload['photoUrls'], "PhotoUrls питомца не совпадает с ожидаемым"
             assert response_json['tags'] == payload['tags'], "Tags питомца не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_on_id(self, create_pet):
        with allure.step("Получение id питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данные ответа"):
             assert  response.status_code == 200, "Code status is not as expected"
             assert  response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_info_about_pet(self, create_pet):

        with allure.step("Получение id питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для отправки"):
            payload_update = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
                }
        with allure.step("Отправить запрос на обновление"):
            response = requests.put(f"{BASE_URL}/pet", json=payload_update)

        with allure.step("Проверка статуса ответа и данные питомца"):
            assert response.status_code == 200, "Code status is not as expected"
            assert response.json()["id"] == payload_update["id"]
            assert response.json()["name"] == payload_update["name"]
            assert response.json()["status"] == payload_update["status"]

    @allure.title("Удаление информации о питомце")
    def test_delete_pet(self, create_pet):

        with allure.step("Получение id питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа после удаления"):
            assert response.status_code == 200, "Code status is not as expected"

        with allure.step("Отправка запроса после удаления питомца"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Code status is not as expected"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code, expected_type",
        [
            ("available", 200, list),
            ("pending", 200, list),
            ("sold", 200, list),
            ("@@@@@!!!!_____", 400, dict),
            ("", 400, dict),

        ]
    )
    def test_get_pets_by_status(self, status, expected_status_code, expected_type):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status":status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code, "Code status is not as expected"
            assert isinstance(response.json(), expected_type), "The data format does not match the expected format."
