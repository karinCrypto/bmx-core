# convert_to_json.py

import pandas as pd
import os

# 입력 CSV 경로
csv_path = 'data/mining_locations.csv'
# 출력 JSON 경로 (Dash의 assets 폴더)
json_path = 'assets/mining_locations.json'

# CSV 파일이 존재할 경우만 변환
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df.to_json(json_path, orient='records', force_ascii=False)
    print(f"✅ 변환 완료: {json_path}")
else:
    print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
