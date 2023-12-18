import json
from unittest.mock import Mock
from django.test import Client

import pytest
from freezegun import freeze_time

from exchange.views import exchange_rates


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_exchange_rates():
    response = exchange_rates(Mock())
    assert response.status_code == 200
    response_body = json.loads(response.content)
    assert response_body == {
        "current_rates": [
            {
                "buy": "30.0000",
                "currency_a": "USD",
                "currency_b": "UAH",
                "date": "2020-01-01",
                "id": 1,
                "sell": "29.0000",
                "vendor": "monobank",
            },
            {
                "buy": "34.0000",
                "currency_a": "EUR",
                "currency_b": "UAH",
                "date": "2020-01-01",
                "id": 2,
                "sell": "32.0000",
                "vendor": "monobank",
            },
            {
                "buy": "31.0000",
                "currency_a": "USD",
                "currency_b": "UAH",
                "date": "2020-01-01",
                "id": 3,
                "sell": "30.0000",
                "vendor": "privatbank",
            },
            {
                "buy": "35.0000",
                "currency_a": "EUR",
                "currency_b": "UAH",
                "date": "2020-01-01",
                "id": 4,
                "sell": "33.0000",
                "vendor": "privatbank",
            },
        ]
    }


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_calculator_usd_in_uah():
    client = Client()
    data = {"currency_sell": "USD", "currency_buy": "UAH", "suma": 100}

    response = client.post("", data)

    assert response.status_code == 200

    response_body = response.context
    result = response_body["result"]

    assert result == 3100


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_calculator_eur_in_uah():
    client = Client()
    data = {"currency_sell": "EUR", "currency_buy": "UAH", "suma": 100}

    response = client.post("", data)

    assert response.status_code == 200

    response_body = response.context
    result = response_body["result"]

    assert result == 3500


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_calculator_uah_in_eur():
    client = Client()
    data = {"currency_sell": "UAH", "currency_buy": "EUR", "suma": 3200}

    response = client.post("", data)

    assert response.status_code == 200

    response_body = response.context
    result = response_body["result"]

    assert result == 100


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_calculator_eur_in_eur():
    client = Client()
    data = {"currency_sell": "EUR", "currency_buy": "EUR", "suma": 3200}

    response = client.post("", data)

    assert response.status_code == 200

    response_body = response.context
    result = response_body["field_errors"]

    assert result == ["Неможливо конвертувати однакові валюти!"]


@freeze_time("2020-01-01")
@pytest.mark.django_db
def test_calculator_usd_in_eur():
    client = Client()
    data = {"currency_sell": "USD", "currency_buy": "EUR", "suma": 3200}

    response = client.post("", data)

    assert response.status_code == 200

    response_body = response.context
    result = response_body["field_errors"]

    assert result == ["Наш обмінник не може конвертувати USD в EUR"]


@freeze_time("2010-01-01")
@pytest.mark.django_db
def test_calculator_empty():
    client = Client()
    data = {"currency_sell": "UAH", "currency_buy": "EUR", "suma": 3200}

    response = client.post("", data)

    assert response.status_code == 200

    response_body = response.context
    result = response_body["error"]

    assert result == "База даних порожня обмін не можливий"
