#!/usr/bin/env python3
import time
import json
from playwright.sync_api import sync_playwright

URL = 'http://127.0.0.1:8000/games/cookie-clicker.html'

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print('Opening', URL)
        page.goto(URL, timeout=60000)
        time.sleep(0.5)
        initial = int(page.inner_text('#count'))
        print('Initial count:', initial)
        # click cookie a bunch
        for _ in range(20):
            page.click('#cookie')
        time.sleep(0.4)
        after_click = int(page.inner_text('#count'))
        print('After clicking 20 times:', after_click)
        # read cursor cost
        cost = page.evaluate("""() => {
            const up = document.querySelectorAll('.upgrade')[0];
            if(!up) return null;
            const txt = up.innerText;
            const m = txt.match(/Cost:\s*(\d+)/i);
            return m? Number(m[1]) : null;
        }""")
        print('Detected cursor cost:', cost)
        if cost and after_click >= cost:
            print('Attempting to buy first upgrade')
            page.click('.upgrade button')
            time.sleep(0.3)
            print('Clicked buy')
        else:
            print('Not enough cookies yet to buy, continuing to click...')
            for _ in range(100): page.click('#cookie')
            time.sleep(0.5)
            print('New count:', page.inner_text('#count'))
            # try buy again
            try:
                page.click('.upgrade button')
                print('Clicked buy after extra clicks')
            except Exception as e:
                print('Buy still failed:', e)
        # save
        page.click('#saveBtn')
        time.sleep(0.2)
        raw = page.evaluate("localStorage.getItem('cookieDemo')")
        print('localStorage cookieDemo:', raw)
        # basic assertions
        ok = raw is not None
        try:
            data = json.loads(raw) if raw else None
        except Exception:
            data = None
        if data and ('items' in data):
            print('Smoke test passed: data has items:', data.get('items'))
        else:
            print('Smoke test warning: saved data missing or malformed')
        browser.close()

if __name__ == '__main__':
    run()
