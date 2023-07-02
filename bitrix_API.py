import requests

async def insert_lead(ans1, ans2, ans3, username, user_fname):
    url = "https://kingdomuniversity.bitrix24.ru/rest/25/2pcf4gb5vno4ojt0/crm.lead.add.json"

    headers = {'Content-Type': 'application/json'}

    lead_data = {
        "fields":
        {
            "TITLE": user_fname,
            "UF_CRM_1688153622107": ans1,
            "UF_CRM_1688153632970": ans3,
            "NAME": username,
            "EMAIL": [{"VALUE": ans2, "VALUE_TYPE": "WORK"}],
        },
    }

    response = requests.post(url, headers=headers, json=lead_data)
    return response.status_code == 200



