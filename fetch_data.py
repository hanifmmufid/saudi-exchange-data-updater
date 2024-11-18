import requests
import json
import re


# Fungsi untuk mengambil data dari API
def fetch_data(start_date, end_date):
    # URL API
    url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/newsandreports/reports-publications/historical-reports/!ut/p/z1/lZFNU4NADIZ_Sw9cmwCyXb2hU6hOseCCwl4cqCswpcAs2zL668voxWLrR27JPG-SNwEOMfA63Zd5qsqmTqshTzh5tmyCxoLiChfhDRJkLolCqhvzC3g6BqjnEgzu7WBlzCx0HxH4v_TIfAsDx_fMJT6gi-RvejwT9q_zk0E_OwvoBBhw4J2oxFqJFy-VG6Eg8Zyv1XmtSvUGiW6aiNawEh9NDSI6mGLOtUXRQIZj4MTVRh2-n-UD-ME3EzXcAc-rJvv8o11nJs2BS_EqpJDTnRzKhVJtd6Whhn3fT3dt38jNdN1sNTwlKZpOQXxMQruNovg9FNnlbekX1X5pTyYHhH9KnQ!!/p0/IZ7_5A602H80O0HTC060SG6UT81216=CZ6_5A602H80O0HTC060SG6UT812E4=NJpopulateCompanyDetails=/"

    # Fungsi untuk mengonversi header dari string ke dictionary
    def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []):
        d = {}
        for kv in s.split('\n'):
            kv = kv.strip()
            if kv and sep in kv:
                k, v = kv.split(sep, 1)
                if v == "''":
                    v = ''
                if strip_cookie and k.lower() == 'cookie':
                    continue
                if strip_cl and k.lower() == 'content-length':
                    continue
                if k in strip_headers:
                    continue
                d[k] = v
        return d

    # Header request
    h2 = """accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
            accept-encoding: gzip, deflate, br, zstd
            accept-language: en-US,en;q=0.9,id;q=0.8
            cache-control: max-age=0
            cookie: BIGipServerSaudiExchange.sa.app~SaudiExchange.sa_pool=889131436.20480.0000; _ga=GA1.1.142069110.1731569516; com.ibm.wps.state.preprocessors.locale.LanguageCookie=en; JSESSIONID=!KM2DmYMiONKlRjTHYTs5PW+MzmvOZ+Wzu9vBxBWC/H+Z8XAxRjCKXDCy0Bu1efjICDDhVwP/tVwSn+ztZHrix0DwHBhbFrFziDOv; TS01fdeb15=0102d17fade8e92ee01e739f074f12e995584b94033c72f6654b180f0129c5083f84fc6831416339a6956baef4a4a6fb49129a005dfc323b11dc5d23ec851a064d93cfc98b959de08b84a4d3e1a04d5790628c683f64707087a8b299df947c0728ab2fd688; _ga_P0MCK0BGCX=GS1.1.1731569515.1.1.1731570192.0.0.0; _ga_DC6H7ZFCGP=GS1.1.1731569515.1.1.1731570192.0.0.0; RT="z=1&dm=www.saudiexchange.sa&si=d7ccedf6-04fa-4a5d-aa47-150e33635879&ss=m3h06lxg&sl=1&tt=0&obo=1&ld=rbx9&ul=rbxa"
            priority: u=0, i
            referer: https://tinyurl-checker.web.app/
            sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "Linux"
            sec-fetch-dest: document
            sec-fetch-mode: navigate
            sec-fetch-site: cross-site
            sec-fetch-user: ?1
            upgrade-insecure-requests: 1
            user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"""

    headers = get_headers(h2)

    # Payload untuk POST request
    payload = {
            "draw": str(1),
            "columns[0][data]": "transactionDateStr",
            "columns[0][searchable]": str(True),
            "columns[0][orderable]": str(False),
            "columns[0][search][value]": "",
            "columns[0][search][regex]": str(False),
            "columns[1][data]": "todaysOpen",
            "columns[1][searchable]": str(True),
            "columns[1][orderable]": str(False),
            "columns[1][search][value]": "",
            "columns[1][search][regex]": str(False),
            "columns[2][data]": "highPrice",
            "columns[2][searchable]": str(True),
            "columns[2][orderable]": str(False),
            "columns[2][search][value]": "",
            "columns[2][search][regex]": str(False),
            "columns[3][data]": "lowPrice",
            "columns[3][searchable]": str(True),
            "columns[3][orderable]": str(False),
            "columns[3][search][value]": "",
            "columns[3][search][regex]": str(False),
            "columns[4][data]": "previousClosePrice",
            "columns[4][searchable]": str(True),
            "columns[4][orderable]": str(False),
            "columns[4][search][value]": "",
            "columns[4][search][regex]": str(False),
            "columns[5][data]": "change",
            "columns[5][searchable]": str(True),
            "columns[5][orderable]": str(False),
            "columns[5][search][value]": "",
            "columns[5][search][regex]": str(False),
            "columns[6][data]": "changePercent",
            "columns[6][searchable]": str(True),
            "columns[6][orderable]": str(False),
            "columns[6][search][value]": "",
            "columns[6][search][regex]": str(False),
            "columns[7][data]": "volumeTraded",
            "columns[7][searchable]": str(True),
            "columns[7][orderable]": str(False),
            "columns[7][search][value]": "",
            "columns[7][search][regex]": str(False),
            "columns[8][data]": "turnOver",
            "columns[8][searchable]": str(True),
            "columns[8][orderable]": str(False),
            "columns[8][search][value]": "",
            "columns[8][search][regex]": str(False),
            "columns[9][data]": "noOfTrades",
            "columns[9][searchable]": str(True),
            "columns[9][orderable]": str(False),
            "columns[9][search][value]": "",
            "columns[9][search][regex]": str(False),
            "columns[10][data]": "nav",
            "columns[10][searchable]": str(True),
            "columns[10][orderable]": str(False),
            "columns[10][search][value]": "",
            "columns[10][search][regex]": str(False),
            "columns[11][data]": "aum",
            "columns[11][searchable]": str(True),
            "columns[11][orderable]": str(False),
            "columns[11][search][value]": "",
            "columns[11][search][regex]": str(False),
            "columns[12][data]": "12",
            "columns[12][searchable]": str(True),
            "columns[12][orderable]": str(True),
            "columns[12][search][value]": "",
            "columns[12][search][regex]": str(False),
            "start": str(0),
            "length": str(100),
            "search[value]": "",
            "search[regex]": str(False),
            "selectedMarket": "MF",
            "selectedSector": str(0),
            "selectedEntity": str(133005),
            "startDate": start_date,
            "endDate": end_date,
            "tableTabId": str(0),
            "startIndex": str(0),
            "endIndex": str(30)
        }

    # Mengirim request ke server
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed with status code {response.status_code}")
