import pandas as pd
import random

# 기존 채굴 데이터 로드
df_existing = pd.read_csv('data/mining_locations.csv')

# 전세계 도시 데이터 로드 (Simplemaps world cities 예시)
df_cities = pd.read_csv('data/world_cities.csv')

# 필요한 컬럼만 선택 (필요에 따라 컬럼명 조정)
df_cities = df_cities[['city', 'lat', 'lng', 'country']]

# 1000개 도시 무작위 샘플링 (기존에 겹치지 않는 도시로)
existing_cities = set(df_existing['city'].str.lower())
df_cities_filtered = df_cities[~df_cities['city'].str.lower().isin(existing_cities)]
df_sampled = df_cities_filtered.sample(n=1000, random_state=42).reset_index(drop=True)

# 임의 채굴량 및 기업명 부여
def generate_mining_volume():
    return random.randint(1000, 10000)

def generate_company(city):
    suffixes = ['Mining Co', 'Crypto Miners', 'Blockchain Ltd', 'Digital Mine', 'Mining Group']
    return f"{city} {random.choice(suffixes)}"

df_sampled['mining_volume'] = df_sampled['city'].apply(lambda _: generate_mining_volume())
df_sampled['company'] = df_sampled['city'].apply(generate_company)

# 컬럼명 맞추기 (lon, lat, city, mining_volume, company, country)
df_sampled = df_sampled.rename(columns={'lng': 'lon'})

# 기존 데이터에 company 컬럼 없으면 생성
if 'company' not in df_existing.columns:
    df_existing['company'] = None
if 'country' not in df_existing.columns:
    df_existing['country'] = None

# 기존 데이터와 합치기
df_combined = pd.concat([df_existing, df_sampled], ignore_index=True)

# 저장
df_combined.to_csv('data/mining_locations_expanded.csv', index=False)
print("1000개 도시 추가된 mining_locations_expanded.csv 생성 완료")
