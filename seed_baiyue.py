import requests
from bs4 import BeautifulSoup
from app.models.mountain import Mountain
import re

def seed_baiyue():
    url = "https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E7%99%BE%E5%B2%B3"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Fetching Wikipedia page...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')
    
    # Usually the main table has > 100 rows
    target_table = None
    for table in tables:
        rows = table.find_all('tr')
        if len(rows) >= 100:
            target_table = table
            break
            
    if not target_table:
        print("Could not find the target table.")
        return

    rows = target_table.find_all('tr')
    
    # Extract headers to find the indices
    headers_elements = rows[0].find_all(['th', 'td'])
    headers_text = [h.text.strip() for h in headers_elements]
    
    try:
        # Find index for 山名, 標高, 行政區劃
        name_idx = next(i for i, h in enumerate(headers_text) if '山名' in h)
        alt_idx = next(i for i, h in enumerate(headers_text) if '標高' in h or '高度' in h)
        loc_idx = next(i for i, h in enumerate(headers_text) if '行政區劃' in h or '位置' in h)
    except StopIteration:
        # Hardcode fallback for Wikipedia format as of 2024
        name_idx = 1
        alt_idx = 2
        loc_idx = 4
        
    count = 0
    for row in rows[1:]:
        cols = row.find_all(['th', 'td'])
        if len(cols) < max(name_idx, alt_idx, loc_idx) + 1:
            continue
            
        name = cols[name_idx].text.strip()
        # Remove reference tags like [1]
        name = re.sub(r'\[.*?\]', '', name)
        
        altitude_str = cols[alt_idx].text.strip().replace(',', '')
        # Extract digits
        alt_match = re.search(r'\d+', altitude_str)
        if not alt_match:
            continue
        altitude = int(alt_match.group())
        
        location = cols[loc_idx].text.strip()
        location = re.sub(r'\[.*?\]', '', location)
        
        # Insert into DB
        mountain_data = {
            "name": name,
            "altitude": altitude,
            "location": location,
            "description": f"台灣百岳之一，標高 {altitude} 公尺。",
            "safety_warning": "高山地區氣候變化大，請隨時注意天氣預報與自身保暖，防範高山症。",
            "equipment_list": "- 基本百岳登山裝備\n- 兩截式雨衣褲\n- 保暖衣物\n- 充足的行動糧與飲水\n- 個人急救包與常備藥品\n- 離線地圖與導航設備",
            "trail_timeline": "百岳路線通常需安排多日行程，請依個人體能與路線難度妥善規劃時間與住宿點。"
        }
        
        # Check if already exists to prevent duplicates
        existing = Mountain.search(name)
        if not any(m['name'] == name for m in existing):
            Mountain.create(mountain_data)
            count += 1
            
    print(f"Successfully inserted {count} mountains from 台灣百岳!")

if __name__ == '__main__':
    seed_baiyue()
