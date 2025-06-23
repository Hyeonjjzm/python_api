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

def explore_page_data():
    """페이지 데이터 탐색하기"""
    
    print("네이버 지도 페이지의 데이터를 탐색해봐요!")
    
    search_word = input("어떤 맛집을 찾을까요? (예: 강남역 맛집): ")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        # 검색 페이지로 이동
        search_url = f"https://map.naver.com/p/search/{search_word}"
        page.goto(search_url)
        print(f"'{search_word}' 검색 페이지로 이동!")
        
        # 페이지 로딩 대기
        time.sleep(10)
        
        print("\n=== 페이지 데이터 분석 시작! ===")
        
        # 1. 페이지 제목 확인
        title = page.title()
        print(f"📄 페이지 제목: {title}")
        
        # 2. 현재 URL 확인
        current_url = page.url
        print(f"🔗 현재 URL: {current_url}")
        
        # 3. li 요소가 몇 개 있는지 확인
        li_elements = page.locator("li").all()
        print(f"📋 페이지에서 찾은 li 요소 개수: {len(li_elements)}개")
        
        # 4. div 요소가 몇 개 있는지 확인  
        div_elements = page.locator("div").all()
        print(f"📦 페이지에서 찾은 div 요소 개수: {len(div_elements)}개")
        
        # 5. iframe이 있는지 확인
        iframe_elements = page.locator("iframe").all()
        print(f"🖼️ 페이지에서 찾은 iframe 개수: {len(iframe_elements)}개")
        
        if len(iframe_elements) > 0:
            print("   ✅ iframe을 발견했어요! 맛집 정보가 이 안에 있을 수 있어요.")
            
            # iframe의 id 확인
            for i, iframe in enumerate(iframe_elements):
                iframe_id = iframe.get_attribute("id")
                iframe_src = iframe.get_attribute("src")
                
                # iframe_id가 None이면 "없음"으로 표시
                if iframe_id is None:
                    iframe_id = "없음"
                
                # iframe_src가 None이면 "없음"으로 표시
                if iframe_src is None:
                    iframe_src = "없음"
                else:
                    # src가 너무 길면 앞 50글자만 보여주기
                    iframe_src = iframe_src[:50] + "..." if len(iframe_src) > 50 else iframe_src
                
                print(f"   iframe {i+1}: id='{iframe_id}', src='{iframe_src}'")
        
        print("\n=== 30초 동안 페이지를 자세히 관찰해보세요! ===")
        print("💡 F12를 눌러서 개발자 도구도 열어보세요!")
        time.sleep(30)
        
        browser.close()
        print("🔚 데이터 탐색 완료!")

def check_iframe_data():
    """iframe 안의 데이터 확인하기"""
    
    print("iframe 안의 맛집 데이터를 확인해봐요!")
    
    search_word = input("어떤 맛집을 찾을까요? (예: 강남역 맛집): ")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        
        # 검색 페이지로 이동
        search_url = f"https://map.naver.com/p/search/{search_word}"
        page.goto(search_url)
        print(f"'{search_word}' 검색!")
        
        # 페이지 로딩 대기
        time.sleep(10)
        
        try:
            print("\n🎯 iframe 안으로 들어가기 시도!")
            
            # iframe 안으로 들어가기
            iframe_box = page.frame_locator("#searchIframe")
            print("✅ iframe 안에 들어갔어요!")
            
            # iframe 안에서 데이터 확인
            time.sleep(5)
            
            # iframe 안의 li 요소 개수 확인
            iframe_li_elements = iframe_box.locator("li").all()
            print(f"📋 iframe 안의 li 요소 개수: {len(iframe_li_elements)}개")
            
            # 처음 5개 li 요소의 텍스트 확인
            print("\n📝 처음 5개 li 요소의 내용:")
            for i, li_element in enumerate(iframe_li_elements[:5]):
                try:
                    text = li_element.inner_text()
                    # 텍스트가 너무 길면 앞 부분만 보여주기
                    short_text = text[:60] + "..." if len(text) > 60 else text
                    print(f"   {i+1}. {short_text}")
                    print(f"      (전체 길이: {len(text)}글자)")
                except:
                    print(f"   {i+1}. 텍스트를 가져올 수 없음")
            
            # 맛집 정보 같은 요소 찾기
            print("\n🔍 맛집 정보 같은 요소 찾기:")
            restaurant_count = 0
            
            for i, li_element in enumerate(iframe_li_elements[:20]):  # 20개만 확인
                try:
                    text = li_element.inner_text()
                    # 충분한 정보가 있고 여러 줄인 경우를 맛집 정보로 판단
                    if len(text) > 50 and len(text.split('\n')) >= 3:
                        restaurant_count += 1
                        lines = text.split('\n')
                        restaurant_name = lines[0]  # 첫 번째 줄을 이름으로 추정
                        print(f"   🍽️ 맛집 {restaurant_count}: {restaurant_name}")
                except:
                    continue
            
            print(f"\n✅ 맛집으로 보이는 정보 {restaurant_count}개 발견!")
            
        except Exception as e:
            print(f"❌ iframe 접근 실패: {e}")
            print("💡 iframe이 없거나 구조가 다를 수 있어요.")
        
        print("\n=== 30초 동안 결과를 확인해보세요! ===")
        time.sleep(30)
        
        browser.close()
        print("🔚 iframe 데이터 확인 완료!")


if __name__ == "__main__":
    check_iframe_data()