import unittest
import re
import sys
import os
from unittest.mock import patch, MagicMock

# Agregar el directorio raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validations.user_validations import (
    limit_length,
    allow_permitted_characters,
    capitalize_first_letter,
    validate_username,
    validate_password,
    validate_credentials,
    validate_name,
    validate_apellido,
    validate_cedula,
    is_cedula_registered,
    is_cedula_unique_for_user,
    validar_campos
)

class TestValidations(unittest.TestCase):

    def test_limit_length(self):
        self.assertEqual(limit_length("1234567890", 5), "12345")
        self.assertEqual(limit_length("123", 5), "123")

    def test_allow_permitted_characters(self):
        self.assertEqual(allow_permitted_characters("user@name!"), "username")
        self.assertEqual(allow_permitted_characters("abc123_ABC"), "abc123_ABC")

    def test_capitalize_first_letter(self):
        self.assertEqual(capitalize_first_letter("john"), "John")
        self.assertEqual(capitalize_first_letter("DOE"), "Doe")

    def test_validate_username(self):
        self.assertFalse(validate_username("john")[0])
        self.assertTrue(validate_username("JohnDoe")[0])

    def test_validate_password(self):
        self.assertFalse(validate_password("pass")[0])
        self.assertTrue(validate_password("Passw0rd!")[0])

    def test_validate_credentials(self):
        self.assertFalse(validate_credentials("", "")[0])
        self.assertTrue(validate_credentials("username", "password")[0])

    def test_validate_name(self):
        self.assertFalse(validate_name("")[0])
        self.assertTrue(validate_name("John")[0])

    def test_validate_apellido(self):
        self.assertFalse(validate_apellido("a")[0])
        self.assertTrue(validate_apellido("Doe")[0])

    def test_validate_cedula(self):
        self.assertFalse(validate_cedula("123")[0])
        self.assertTrue(validate_cedula("1234567")[0])

    def test_is_cedula_registered(self):
        # Simular la conexión a la base de datos y los resultados
        with patch('validations.user_validations.establecer_conexion') as mock_establecer_conexion:
            mock_conexion = MagicMock()
            mock_establecer_conexion.return_value = mock_conexion
            mock_cursor = MagicMock()
            mock_conexion.cursor.return_value = mock_cursor

            mock_cursor.fetchone.return_value = [1]
            self.assertFalse(is_cedula_registered("1234567")[0])

            mock_cursor.fetchone.return_value = [0]
            self.assertTrue(is_cedula_registered("1234567")[0])

    def test_is_cedula_unique_for_user(self):
        with patch('validations.user_validations.establecer_conexion') as mock_establecer_conexion:
            mock_conexion = MagicMock()
            mock_establecer_conexion.return_value = mock_conexion
            mock_cursor = MagicMock()
            mock_conexion.cursor.return_value = mock_cursor

            # Caso donde la cédula es la misma que la original
            mock_cursor.fetchone.side_effect = [["1234567"], ["1234567"]]
            self.assertTrue(is_cedula_unique_for_user("1234567", 1)[0])

            # Resetear el side_effect para la siguiente prueba
            mock_cursor.reset_mock()
            mock_cursor.fetchone.side_effect = [["1234567"], ["2"]]
            
            # Caso donde la cédula está en uso por otro usuario
            self.assertFalse(is_cedula_unique_for_user("1234567", 2)[0])


if __name__ == '__main__':
    unittest.main()
