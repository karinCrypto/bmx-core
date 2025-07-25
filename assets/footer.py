from dash import html
import dash_bootstrap_components as dbc

_footer = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Hr([], className = 'hr-footer footer-fixed')], width = 12)
        ]),
        dbc.Row([
	        dbc.Col([], width = 1),
            dbc.Col(['Created with LEEEUNJI'], width = 3),
            dbc.Col([], width =6),
	        dbc.Col([
                html.Ul([
                    html.Li([
                        html.A([ html.I(className="fa-brands fa-github me-3 fa-1x")], href='https://github.com/karinCrypto'),
                        html.A([ html.I(className="fa-brands fa-linkedin me-3 fa-1x")], href='https://www.linkedin.com/in/karincrypto/'),
                        html.A([ html.I(className="fa-brands fa-medium me-3 fa-1x")], href='https://medium.com/@Karinnovation')
                    ])
                ], className='list-unstyled d-flex justify-content-center justify-content-md-start')
            ], width = 2)
        ])
    ], fluid=True)
], className = 'footer')