import requests

async def insert_lead(number, ans1, ans2, ans3, user_fname, user_lname):
    url_contact = "https://kingdomuniversity.bitrix24.ru/rest/25/ppvmuxdgyk440qm7/crm.contact.add.json"

    params = {
        'fields': {
            'NAME': user_fname,
            'LAST_NAME': user_lname,
            'PHONE': [{'VALUE': number, 'VALUE_TYPE': 'WORK'}],
            'EMAIL': [{'VALUE': ans2, 'VALUE_TYPE': 'WORK'}],
            'SOURCE_ID': "OTHER",
            'SOURCE_DESCRIPTION': "Telegram",
            'UF_CRM_64A1AF824FDDB': ans1,
            'UF_CRM_64A1AF825DE57': ans3
        },
        'params': {'REGISTER_SONET_EVENT': 'Y'}
    }
    response1 = requests.post(url_contact, json=params)
    contact_id = response1.json()['result']

    url_deal = "https://kingdomuniversity.bitrix24.ru/rest/25/bri44f78o7dlfn2k/crm.deal.add.json"

    params2 = {
        'fields': {
            'TITLE': user_fname,
            'CONTACT_ID': contact_id,
            'UF_CRM_64A1AF8268BCF': ans1,
            'UF_CRM_64A1AF827392A': ans3
        }
    }
    response2 = requests.post(url_deal, json=params2)



