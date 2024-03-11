
import json
import pandas as pd

from request import req_api_http


def get_excel_data_json():
    df = pd.read_excel('table.xlsx')
    data_list = df.apply(lambda row: {"wallet": row['wallet'].lower(), "proxy": row['proxy']}, axis=1)
    return data_list.to_json(orient='records')


def get_wallets_status():
    data = json.loads(get_excel_data_json())
    results = []
    for wallet in data:
        proxy = wallet["proxy"] if wallet["proxy"] is not None else None
        code, response = req_api_http(wallet["wallet"], proxy)
        result = {
            "wallet": wallet['wallet'],
            "code":code,
            "status": json.loads(response) if response else None  # Assuming response is a JSON string
        }
        results.append(result)
    return results


def generate_excel():
    data = get_wallets_status()

    data_frames = []
    for item in data:
        address = item["wallet"]
        status = item["status"]
        code = item["code"]

        if code == 200:
            if status is not None:
                status_eligible = "Eligible"
            else:
                status_eligible = "Not Eligible"
        else:
            status_eligible = "Recheck"
        df = pd.DataFrame({
            'status': [status_eligible],
        }, index=[address])

        data_frames.append(df)

    result_df = pd.concat(data_frames)
    result_df.index.name = 'Address'
    result_df.to_excel('result.xlsx')


generate_excel()