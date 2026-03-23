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


