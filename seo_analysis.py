import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def analyze_seo(url):
    try:
        # 웹사이트 HTML 가져오기
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        seo_report = {}

        # H1 태그 확인
        h1_tags = soup.find_all('h1')
        seo_report['H1 Tags'] = {
            'count': len(h1_tags),
            'status': 'OK' if len(h1_tags) == 1 else 'Too Many' if len(h1_tags) > 1 else 'Missing',
            'details': [tag.text.strip() for tag in h1_tags] if h1_tags else 'No H1 tags found'
        }

        # H2 태그 확인
        h2_tags = soup.find_all('h2')
        seo_report['H2 Tags'] = {
            'count': len(h2_tags),
            'status': 'OK' if len(h2_tags) > 0 else 'Missing',
            'details': [tag.text.strip() for tag in h2_tags] if h2_tags else 'No H2 tags found'
        }

        return seo_report

    except Exception as e:
        return {'error': str(e)}

# 테스트 실행
if __name__ == "__main__":
    url = input("Enter the URL to analyze (e.g., https://example.com): ")
    report = analyze_seo(url)

    print("\nSEO Analysis Report:\n")
    for key, value in report.items():
        print(f"{key}: {value}")
