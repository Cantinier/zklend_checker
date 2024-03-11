import time

import requests
from requests.exceptions import RequestException

main_url = "https://data.app.zklend.com/airdrop/"
payload = {}


def req_api(address, proxy):
    url = main_url + address
    proxies = None
    if proxy is not None:
        proxies = {"http": "socks5://" + proxy, "https": "socks5://" + proxy}
    try:
        response = requests.request("GET", url, data=payload, proxies=proxies)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        print(f"Error requesting data from {url}: {e}")
        return None


def req_api_http(address, proxy, max_retries=3, retry_delay=1):
    print(address)
    url = main_url + address
    proxies = None

    if proxy is not None:
        proxy_parts = proxy.split('@')  # Splitting proxy into credentials and address
        if len(proxy_parts) == 2:
            credentials, proxy_address = proxy_parts
            proxies = {
                "http": f"{credentials}@{proxy_address}",
                "https": f"{credentials}@{proxy_address}"
            }
        else:
            proxy_address = proxy
            proxies = {
                "http": f"{proxy_address}",
                "https": f"{proxy_address}"
            }

    for attempt in range(max_retries):
        try:
            response = requests.request("GET", url, data=payload, proxies=proxies)
            if response.status_code == 200:
                return response.status_code, response.text
            else:
                print(f"Received non-200 status code: {response.status_code}. Retrying...")
        except RequestException as e:
            print(f"Error requesting data from {url}: {e}")

        # If not successful, wait and retry
        time.sleep(retry_delay)

    print(f"Failed to retrieve data from {url} after {max_retries} attempts.")
    return response.status_code, None


if __name__ == "__main__":
    print(req_api_http("0x0752d1b6c098F5c6a6",None))
