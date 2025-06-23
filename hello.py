from playwright.sync_api import sync_playwright
import time

def open_browser():

    print("브라우저를 열고 있어요.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)

        page = browser.new_page()
        page.goto("https://www.google.com")
        print("브라우저가 열렸습니다.")
        print("10초 후에 자동으로 닫힙니다.")

        time.sleep(10)

        browser.close()
        print("브라우저가 닫혔습니다.")

def search_naver_map():
    print("네이버 지도로 이동해요.")

    search_word = input("어떤 맛집을 찾을까요? (예 : 광진구)")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)

        page = browser.new_page()
        search_url = f"https://map.naver.com/p/search/{search_word}"
        page.goto(search_url)
        
        print(f"{search_word}페이지로 이동했어요")
        print("검색 결과 로딩중....")
        time.sleep(10)
        print("검색 결과를 확인하세요")
        time.sleep(20)

        browser.close()
        print("브라우저가 닫혔습니다.")


if __name__ == "__main__":
    search_naver_map()
