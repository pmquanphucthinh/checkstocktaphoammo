import requests
import os
import subprocess

def send_telegram_message(bot_token, chat_id, message):
    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(api_url, data=params)
    return response.json()

def create_github_release(tag_name, body):
    github_token = os.getenv('GITHUB_TOKEN')
    repo_owner = os.getenv('GITHUB_REPOSITORY_OWNER')
    repo_name = os.getenv('GITHUB_REPOSITORY_NAME')

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases'
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        'tag_name': tag_name,
        'body': body
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def main():
    # API cho kho hàng 1
    api_url_1 = "https://taphoammo.net/api/getStock"
    api_params_1 = "kioskToken=3NCKIZQWT6TQ6C5T1E8G&userToken=VX642S9VPUYR308OTROAQOTEPEB2VEPNFUZL"

    # API cho kho hàng 2
    api_url_2 = "https://taphoammo.net/api/getStock"
    api_params_2 = "kioskToken=YXRH1M4QFDT0IRYOSFSQ&userToken=VX642S9VPUYR308OTROAQOTEPEB2VEPNFUZL"

    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Gửi request đến API cho kho hàng 1
    response_1 = requests.get(f'{api_url_1}?{api_params_1}')
    data_1 = response_1.json()

    # Gửi request đến API cho kho hàng 2
    response_2 = requests.get(f'{api_url_2}?{api_params_2}')
    data_2 = response_2.json()

    # Trích xuất giá trị stock từ cả hai kho hàng
    stock_1 = data_1.get('stock', 'N/A')
    stock_2 = data_2.get('stock', 'N/A')

    # Gửi dữ liệu về Telegram
    message = f"Gittechvn        - Kho hàng: {stock_1}\nShopgithubgiare - Kho hàng: {stock_2}"
    send_telegram_message(telegram_bot_token, telegram_chat_id, message)

    # Tạo GitHub release
    tag_name = f'v{stock_1}_{stock_2}'
    body = f"Gittechvn - Kho hàng 1: {stock_1}\nShopgithubgiare - Kho hàng 2: {stock_2}"
    create_github_release(tag_name, body)

if __name__ == "__main__":
    main()
