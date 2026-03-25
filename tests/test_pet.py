from http.client import responses

import allure
import requests

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