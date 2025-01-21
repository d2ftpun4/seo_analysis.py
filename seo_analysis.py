import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def analyze_seo(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        seo_report = {}

        # Title 태그 확인
        title_tag = soup.find('title')
        seo_report['Title'] = {
            'content': title_tag.text if title_tag else 'Missing',
            'length': len(title_tag.text) if title_tag else 0,
            'status': 'OK' if title_tag and len(title_tag.text) <= 40 else 'Too Long or Missing'
        }

        # Meta Description 확인
        meta_description = soup.find('meta', attrs={'name': 'description'})
        seo_report['Meta Description'] = {
            'content': meta_description['content'] if meta_description and 'content' in meta_description.attrs else 'Missing',
            'length': len(meta_description['content']) if meta_description and 'content' in meta_description.attrs else 0,
            'status': 'OK' if meta_description and len(meta_description['content']) <= 50 else 'Too Long or Missing'
        }

        # H1 태그 확인
        h1_tags = soup.find_all('h1')
        seo_report['H1 Tags'] = {
            'count': len(h1_tags),
            'status': 'OK' if len(h1_tags) == 1 else 'Multiple or Missing'
        }

        # H2 태그 확인
        h2_tags = soup.find_all('h2')
        seo_report['H2 Tags'] = {
            'count': len(h2_tags),
            'status': 'OK' if len(h2_tags) > 0 else 'Missing'
        }

        # 이미지 Alt 속성 확인
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        seo_report['Images'] = {
            'total_images': len(images),
            'missing_alt': len(images_without_alt),
            'status': 'OK' if len(images_without_alt) == 0 else 'Missing Alt Attributes'
        }

        # Open Graph 태그 확인
        og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
        seo_report['Open Graph Tags'] = {
            'count': len(og_tags),
            'status': 'OK' if len(og_tags) > 0 else 'Missing'
        }

        # Canonical URL 확인
        canonical_tag = soup.find('link', rel='canonical')
        seo_report['Canonical URL'] = {
            'status': 'OK' if canonical_tag else 'Missing'
        }

        # Robots.txt 확인
        robots_url = urljoin(url, '/robots.txt')
        try:
            robots_response = requests.get(robots_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            seo_report['Robots.txt'] = {
                'status': 'OK' if robots_response.status_code == 200 else f'Error {robots_response.status_code}',
                'content': robots_response.text[:200] if robots_response.status_code == 200 else '403 Forbidden: Access Denied'
            }
        except requests.exceptions.RequestException as e:
            seo_report['Robots.txt'] = {'status': 'Error', 'content': str(e)}

        # Sitemap.xml 확인
        sitemap_url = urljoin(url, '/sitemap.xml')
        try:
            sitemap_response = requests.get(sitemap_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            seo_report['Sitemap.xml'] = {
                'status': 'OK' if sitemap_response.status_code == 200 else f'Error {sitemap_response.status_code}',
                'content': sitemap_response.text[:200] if sitemap_response.status_code == 200 else '403 Forbidden: Access Denied'
            }
        except requests.exceptions.RequestException as e:
            seo_report['Sitemap.xml'] = {'status': 'Error', 'content': str(e)}

        return seo_report

    except Exception as e:
        return {'error': str(e)}

# Streamlit App
st.title("SEO Analysis Tool")
st.write("Enter a URL to analyze its SEO performance:")

url = st.text_input("Website URL (e.g., https://example.com)")
if url:
    report = analyze_seo(url)

    st.subheader("SEO Analysis Report")
    for key, value in report.items():
        st.write(f"### {key}")
        st.json(value)
