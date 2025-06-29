from dash import html
import dash_bootstrap_components as dbc
import dash

_nav = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.I(className="fa-solid fa-chart-simple fa-2x")
            ], className='logo')
        ], width=4),
        dbc.Col([
            html.H1([
                html.Span('Bit', style={'color': '#ffc107 !important'}), 
                html.Span('master')  # master 부분은 기본 색상 유지
            ], className='app-brand')
        ], width=8)
    ]),
    dbc.Row([
        dbc.Nav(
            [dbc.NavLink(page["name"], active='exact', href=page["path"]) for page in dash.page_registry.values()],
            vertical=True, pills=True, class_name='my-nav'
        )
    ])
])
