import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from python_scripts.utils import extract_first_match

def test_extract_first_match():
    texto = "PRUEBA 1 1234|34567|34567-1|5|2 PRUEBA ASUNTO"
    resultado = extract_first_match("(\d{1,})( ?\| ?\d{1,}){0,} ?- ?(\d{1,3} ?\| ?\d{1,3})||" + texto)
    assert resultado == "1234|34567|34567-1|5"

def test_flirt_match_no_match():
    texto = "Esto es un ejemplo de texto con palabras cortas como gato, perro, casa, sol."
    resultado = extract_first_match(("(\d{1,})( ?\| ?\d{1,}){0,} ?- ?(\d{1,3} ?\| ?\d{1,3})||" + texto))
    assert resultado == "No se encontraron coincidencias."

def test_flirt_match_error_regex():
    texto = "Esto es un ejemplo de texto con palabras cortas como gato, perro, casa, sol."
    resultado = extract_first_match(f"('||{texto}")
    print(f"||||{resultado = }||||")
    assert 'unterminated subpattern",\nre.error: missing ), unterminated subpattern at position 0\n' in resultado
