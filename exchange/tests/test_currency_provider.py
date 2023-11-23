import responses

from exchange.currency_provider import (
    MonoProvider,
    SellBuy,
    PrivatbankProvider,
    VkurseProvider,
    NbuProvider,
    MinfinProvider,
)


@responses.activate
def test_mono_provider():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=[
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateSell": 28.0,
                "rateBuy": 27.0,
            }
        ],
    )
    provider = MonoProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=27.0)


@responses.activate
def test_private_provider():
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        json=[
            {
                "ccy": "USD",
                "base_ccy": "UAH",
                "sale": 28.0,
                "buy": 27.0,
            }
        ],
    )
    provider = PrivatbankProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=27.0)


@responses.activate
def test_vkurse_provider():
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json={"Dollar": {"buy": "27.0", "sale": "28.0"}},
    )
    provider = VkurseProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=27.0)


@responses.activate
def test_nbu_provider():
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=[
            {
                "r030": 840,
                "txt": "Долар США",
                "rate": 28.0,
                "cc": "USD",
                "exchangedate": "23.11.2023",
            }
        ],
    )
    provider = NbuProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=28.0)


@responses.activate
def test_minfin_provider():
    responses.get(
        "https://api.minfin.com.ua/mb/66f790e025508e750d572640c13a9d70fe362b50/",
        json=[
            {
                "id": "186572",
                "pointDate": "2023-11-23 11:15:02",
                "date": "2023-11-23 11:00:00",
                "ask": "28.0",
                "bid": "27.0",
                "trendAsk": "-0.0002",
                "trendBid": "0.0034",
                "currency": "usd",
            },
            {
                "id": "186567",
                "pointDate": "2023-11-23 10:45:03",
                "date": "2023-11-23 10:30:00",
                "ask": "39.3433",
                "bid": "39.3214",
                "trendAsk": "-0.0289",
                "trendBid": "-0.0326",
                "currency": "usd",
            },
        ],
    )
    provider = MinfinProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=28.0, buy=27.0)
