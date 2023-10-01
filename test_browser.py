from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
import requests
import json

def run(playwright):
    chrome = playwright.chromium
    browser = chrome.launch(
        proxy={
            "server": "socks5://127.0.0.1:1080",
        }
    )
    context = browser.new_context()
    page = context.new_page()

    with open('/Users/minyakonga/Downloads/www.tiktok.com_cookies.json', 'r') as f:
        cookies = json.loads(f.read())

    pw_cookies, request_cookies = [], {}
    for cookie in cookies:
        pw_cookies.append({
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'domain': cookie.get('domain'),
            'path': cookie.get('path'),
            'HttpOnly': False,
            'HostOnly': False,
            'Secure': False
        })
    context.clear_cookies()
    context.add_cookies(cookies=pw_cookies)

    url = "https://www.tiktok.com/@christikalttv/video/7272423353061887275"
    xpath = f'//*[@id="xgwrapper-4-{url.split("/")[-1]}"]/video'

    page.goto(url)
    expect(page.locator(xpath)).to_have_attribute(name="mediatype", value="video")
    video_link = page.locator(xpath).get_attribute('src')
    print(video_link + "\n")
    with open('./test.html', 'w') as f:
        f.write(page.content())

    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'macOS',
        'Sec-Fetch-Dest': 'empty'
    }

    for cookie in context.cookies():
        request_cookies.update({
            cookie.get('name'): cookie.get('value')
        })
    
    res = requests.get(video_link, headers=headers, cookies=request_cookies)
    print(f'requested: {res.status_code}')
    with open('./test.mp4', 'wb') as f:
        f.write(res.content)

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
