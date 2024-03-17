import pytest

from api import PetFriends
from settings import valid_email, valid_password
from settings import unvalid_email, unvalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result





def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data_cat(name='Васька', animal_type='кот',
                                     age='1', pet_photo='images/cat.pet.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_update_pet_info_cat(name='Матрос', animal_type='cat', age='1.5'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')


    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Это не моё животное')

def test_successful_delete_pet_cat():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, '', '', '', '')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_with_valid_data_dog(name='Пёсбарбос', animal_type='собака',
                                     age='2', pet_photo='images/dog.pet.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_update_pet_info_dog(name='Волкодав', animal_type='Пёс', age=1):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')


    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name

def test_successful_delete_pet_dog():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "", "", "", "")
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_new_pet_with_invalid_photo(name='', animal_type='', age='', pet_photo='fotki/nofoto.jpg'):
    '''Проверяем, что неверный путь к файлу или несуществующий файл вызывают исключение'''

    '''Запрашиваем ключ api и сохраняем в переменную auth_key'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    try:
        '''Добавляем питомца с неверным путем к файлу или несуществующим файлом'''
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    except FileNotFoundError:
        '''Проверяем, что исключение FileNotFoundError было вызвано'''
        assert True
    else:
        '''Если исключение не было вызвано, то тест не прошел'''
        assert False

def test_post_create_pet_sipmle(name='Кузя', animal_type='Кот',age='9'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age )

    assert status == 200
    assert result['name'] == name

def test_post_set_pet_photo(pet_photo='images\kuzja.pet.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    # Проверяем, есть ли уже фотография у питомца
    if my_pets['pets'][0]['pet_photo'] == "":
        status, result = pf.set_pet_photo(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        print("Питомец имеет фото")

def test_unvalid_get_api_key_user(email=unvalid_email, password=unvalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_post_create_pet_simple_uncorrect_date(name=123, animal_type= 3235, age = 'gsag'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    with pytest.raises(AssertionError):
        assert status == 403
        assert result['name'] == name


