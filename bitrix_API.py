import requests

async def insert_lead(ans1, ans2, ans3, username, user_fname):
    url = "https://b24-cndeea.bitrix24.ru/rest/1/m82yk2nacc8ywbhh/crm.lead.add.json"

    headers = {'Content-Type': 'application/json'}

    lead_data = {
        "fields":
        {
            "TITLE": user_fname,
            "UF_CRM_1688138290551": ans1,
            "UF_CRM_1688138303629": ans3,
            "NAME": username,
            "EMAIL": [{"VALUE": ans2, "VALUE_TYPE": "WORK"}],
        },
    }

    response = requests.post(url, headers=headers, json=lead_data)
    return response.status_code == 200



