from api import PetFriends
from settings import valid_email, valid_password
import os
pf = PetFriends()

class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_all_pets_with_valid_key(self, filter=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0
    def test_add_New_Pet_With_Valid_Data(self, name='Нео', animal_type='кот', age='4',
                                    pet_photo='images/Neo.jpeg'):
#        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def test_successful_delete_self_pet(self):
        """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        if len(my_pets['pets']) == 0:
            self.pf.add_new_pet(auth_key, "Хам", "хомяк", "1", "images/xam1.jpg")
            _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = self.pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
        _, my_pets = self.pf.get_list_of_pets(auth_key, "my_pets")

#    Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()

    def test_successful_Update_Self_Pet_Info(self, name='Микрочел', animal_type='Крыс', age=3):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
            raise Exception("There is no my pets")

# 10 штук
# 1
def test_set_photo_pet(pet_photo="images/Mikrochelik.jpeg"):
    """ Проверяем возможность добавления фото к информации о своем питомце """
# Запрашиваем ключ api и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
# Если список не пустой, то пробуем добавить фото к первому питомцу
    if len(my_pets["pets"]) > 0:
        status, result = pf.set_photo_pet(auth_key, my_pets["pets"][0]["id"], pet_photo)
# Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result["pet_photo"]
    else:
        # если список питомцев пустой, то выкидывает исключение с текстом об отсутствии своих питомцев
        raise Exception("No pets")
# 2
def test_add_new_pet_without_photo_valid_data(name="Квазимода", animal_type="двортерьер", age="6"):
    """ Проверяем возможность добавления питомца (без фото) с корректными данными """
# Запрашиваем ключ api
    _, auth_key = pf.get_api_key(valid_email, valid_password)
# Добавляем нового питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
# Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name
# 3
def test_add_new_pet_without_photo_empty_data(name="", animal_type="", age=""):
    """ Проверка с негативным сценарием . Проверяем возможность добавления питомца (без фото) с пустыми данными
    (баг) """
    # Запрашиваем ключ api
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем нового питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name
# 4
def test_add_pet_with_a_lot_of_numbers_in_variable_name(name="1234567891", animal_type='cat', age='2', pet_photo='images/Neo.jpeg'):
        '''Проверка с негативным сценарием. Добавления питомца имя которого состоит из 10 цифр'''
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result["name"] == name
# 5
def test_add_pet_with_a_lot_of_words_in_variable_age(name="Neo", animal_type='cat', age='сто ведер гвоздей вбили в забор',
                                                      pet_photo='images/Neo.jpeg'):
    '''Проверка с негативным сценарием. Добавления питомца возраст которого состоит из нескольких слов'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age
# 6
def test_add_pet_with_a_lot_of_numbers_in_variable_animal_type(name="Neo", animal_type='01234567890123456789', age='2',
                                                      pet_photo='images/Neo.jpeg'):
    '''Проверка с негативным сценарием. Добавления порода которого состоит 20 цифр'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type
# 7
def test_add_new_pet_uncorrect_age_number(name='Нона', animal_type='кошка', age='-1',
                                          pet_photo='images/Nona.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.'''
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age
# 8
def test_get_api_key_for_invalid_user_email(email='Name', password=valid_password):
    """Проверяем, что доступ к сайту не будет открыт при неверной почте, вернет статус 403
    и в результате не содержится слово key """
    status, result = pf.get_api_key(email, password)
 # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert "key" not in result
# 9
def test_get_api_key_for_invalid_user_password(email=valid_email, password='1111111'):
    """Проверяем, что доступ к сайту не будет открыт при неверном пароле и вернет статус 403
    и в результате не содержится слово key """
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result
# 10
def test_get_api_key_for_data_user_empty(email='', password=''):
    """ Проверяем что доступ к сайту при пустых значениях логина и пароля не будет открыт, вернет статус 403
    и в результате не содержится слово key """
# Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
# Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert "key" not in result

