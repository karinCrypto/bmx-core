# pages/step1.py

import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

# 파일 경로
csv_path = '../data/mining_locations.csv'
json_path = '../assets/mining_locations.json'

# CSV → JSON 변환 (앱 실행 시 자동 변환)
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df.to_json(json_path, orient='records')
else:
    df = pd.DataFrame(columns=['city', 'lat', 'lon', 'mining_volume'])

# Dash 페이지 등록
dash.register_page(__name__, path='/', name='비트코인 탄소 발자국', title='BITMaster')

# 레이아웃 구성
layout = html.Div([
    dcc.Store(id='browser-memo'),
    html.Iframe(
        src='/assets/globe.html',
        style={
            'width': '100vw',
            'height': '100vh',
            'border': 'none',
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'zIndex': '1',
            'overflow': 'hidden'
        }
    )
], style={
    'position': 'relative',
    'overflow': 'hidden',
    'backgroundColor': '#000',
    'width': '100vw',
    'height': '100vh',
    'margin': '0',
    'padding': '0'
})
