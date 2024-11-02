import pytest
from app import load_pdf_content
import requests
import os

# Test sprawdzający, czy plik PDF istnieje i jest prawidłowo wczytany
def test_load_pdf_content_exists():
    result = load_pdf_content('PDF/misjazgrzyby.pdf')
    assert result is not None

# Test sprawdzający, czy odpowiednio obsługiwany jest brak pliku PDF
def test_load_pdf_content_not_exists():
    result = load_pdf_content('nonexistent_file.pdf')
    assert result is None

# Test dostępności API OpenAI sprawdzający odpowiedź serwera
def test_api_availability():
    url = "https://api.openai.com/v1/engines"
    headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        assert response.status_code == 200
    except requests.ConnectionError:
        # Obsługuje sytuację, gdy wystąpił problem z połączeniem sieciowym
        pytest.fail("API OpenAI jest niedostępne - problem z połączeniem.")
    except requests.Timeout:
        # Obsługuje sytuację, gdy żądanie przekroczyło ustawiony limit czasu
        pytest.fail("Żądanie przekroczyło limit czasu - API OpenAI może być niedostępne.")
    except Exception as e:
        # Obsługuje inne nieoczekiwane wyjątki, które mogły wystąpić podczas wykonywania żądania
        pytest.fail(f"Wystąpił nieoczekiwany błąd: {e}")
