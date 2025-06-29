from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True
)
server = app.server

# 전역 네비게이션 및 푸터 import
from assets.footer import _footer
from assets.nav import _nav

# 레이아웃 구성
app.layout = html.Div([
    # 상단 네비게이션
    html.Div(_nav, style={'zIndex': 2, 'position': 'relative'}),

    # globe.html iframe
    html.Div([
        html.Iframe(
            src='/assets/globe.html',
            style={
                'width': '100%',
                'height': '92vh',
                'border': 'none',
                'zIndex': 1,
                'position': 'relative'
            }
        )
    ]),

    # 하단 푸터
    html.Div(_footer, style={'zIndex': 2, 'position': 'relative'}),

    # 상태 저장
    dcc.Store(id='browser-memo', data={}, storage_type='session')
], style={
    'margin': '0',
    'padding': '0',
    'overflow': 'hidden',
    'backgroundColor': '#000'
})

# 실행
if __name__ == '__main__':
    app.run_server(debug=False, port=8080)
