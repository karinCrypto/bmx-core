import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from itertools import product
from assets.sarima_gridsearch import sarima_grid_search

dash.register_page(__name__, name='비트코인 사주(MBTI)', title='BITmaster')

_data_airp = pd.read_csv('data/AirPassengers.csv', usecols=[0, 1], names=['Time', 'Values'], skiprows=1)
_data_airp['Time'] = pd.to_datetime(_data_airp['Time'], errors='raise')

### PAGE LAYOUT ######

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3(['나는 비트코인 부자가 될 상인가?'])
        ], width=12, className='row-titles')
    ]),
    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([html.P(['Select the ', html.B(['train']), ' percentage: '], className='par')], width=4),
        dbc.Col([
            dcc.Slider(50, 95, 5, value=80, marks=None,
                       tooltip={"placement": "bottom", "always_visible": True},
                       id='train-slider', persistence=True, persistence_type='session')
        ], width=3),
        dbc.Col([], width=3),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col([], width=1),
                    dbc.Col([html.P(['Set ', ' 사주 입력 (생년, 월일)'], className='par')], width=10),
                    dbc.Col([], width=1),
                ]),
                dbc.Row([
                    dbc.Col([html.P([html.B(['사주']), ':'], className='par')], width=2),
                    dbc.Col([dcc.Dropdown(options=[], value='0', placeholder='생년', clearable=False, id='p-from')], width=4),
                    dbc.Col([], width=1),
                    dbc.Col([dcc.Dropdown(options=[], value='0', placeholder='월일', clearable=False, id='p-to')], width=4),
                    dbc.Col([], width=1)
                ]),
            ], className='div-hyperpar')
        ], width=6, className='col-hyperpar'),
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col([], width=1),
                    dbc.Col([html.P(['Set ', html.B(['P, D, Q, m']), ' seasonal parameters range (from, to)'], className='par')], width=10),
                    dbc.Col([], width=1),
                ]),
                *[
                    dbc.Row([
                        dbc.Col([html.P([html.B([label]), ':'], className='par')], width=2),
                        dbc.Col([dcc.Dropdown(options=[], value='0', placeholder='from', clearable=False, id=f'{id_}-from')], width=4),
                        dbc.Col([], width=1),
                        dbc.Col([dcc.Dropdown(options=[], value='0', placeholder='to', clearable=False, id=f'{id_}-to')], width=4),
                        dbc.Col([], width=1)
                    ]) for label, id_ in [('P', 'sp'), ('D', 'sd'), ('Q', 'sq'), ('m', 'sm')]
                ]
            ], className='div-hyperpar')
        ], width=6, className='col-hyperpar')
    ], style={'margin': '20px 0px 0px 0px'}),
    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([
            html.P(['Grid Search combinations: ', html.B([], id='comb-nr')], className='par')
        ], width=3),
        dbc.Col([
            html.Button('Start Grid Search', id='start-gs', n_clicks=0,
                        title='The grid search may take several minutes',
                        className='my-button')
        ], width=3),
        dbc.Col([], width=3)
    ]),
    dbc.Row([
        dbc.Col([], width=4),
        dbc.Col([
            dcc.Loading(id='gs-loading', type='circle', children=html.Div(id='gs-results'))
        ], width=4),
        dbc.Col([], width=4)
    ])
])

### CALLBACK ###################################################################################################################

@callback(
    Output('comb-nr', 'children'),
    Output('gs-results', 'children'),
    Output('browser-memo', 'data', allow_duplicate=True),
    Input('train-slider', 'value'),
    Input('start-gs', 'n_clicks'),
    Input('p-from', 'value'),
    Input('p-to', 'value'),
    Input('d-from', 'value'),
    Input('d-to', 'value'),
    Input('q-from', 'value'),
    Input('q-to', 'value'),
    Input('sp-from', 'value'),
    Input('sp-to', 'value'),
    Input('sd-from', 'value'),
    Input('sd-to', 'value'),
    Input('sq-from', 'value'),
    Input('sq-to', 'value'),
    Input('sm-from', 'value'),
    Input('sm-to', 'value'),
    State('browser-memo', 'data'),
    prevent_initial_call='initial_duplicate'
)
def grid_search_results(_trainp, _nclicks, p_from, p_to, d_from, d_to, q_from, q_to,
                        sp_from, sp_to, sd_from, sd_to, sq_from, sq_to, sm_from, sm_to, _memo):
    # None값 처리
    defaults = lambda v: v if v is not None else 0
    p_from, p_to = defaults(p_from), defaults(p_to)
    d_from, d_to = defaults(d_from), defaults(d_to)
    q_from, q_to = defaults(q_from), defaults(q_to)
    sp_from, sp_to = defaults(sp_from), defaults(sp_to)
    sd_from, sd_to = defaults(sd_from), defaults(sd_to)
    sq_from, sq_to = defaults(sq_from), defaults(sq_to)
    sm_from, sm_to = defaults(sm_from), defaults(sm_to)

    _p = list(range(p_from, p_to + 1))
    _d = list(range(d_from, d_to + 1))
    _q = list(range(q_from, q_to + 1))
    _P = list(range(sp_from, sp_to + 1))
    _D = list(range(sd_from, sd_to + 1))
    _Q = list(range(sq_from, sq_to + 1))
    _m = list(range(sm_from, sm_to + 1))
    _combs = list(product(_p, _d, _q, _P, _D, _Q, _m))

    if not _combs:
        return 0, None, _memo

    if _nclicks > 0:
        _data = _data_airp.copy()
        _data['Values'] = np.log(_data['Values'])
        idx = round(len(_data) * _trainp / 100)
        _datatrain = _data.iloc[:idx + 1]
        _datatest = _data.iloc[idx + 1:]

        if not _datatrain.empty and not _datatest.empty:
            _gs_res = sarima_grid_search(_data, _combs)
            _gs_res_tbl = _gs_res.iloc[:10].copy()
            _gs_res_tbl.columns = ['Parameters (p,d,q)(P,D,Q)m', 'AIC Score']
            _gs_res_tbl['AIC Score'] = _gs_res_tbl['AIC Score'].round(3)
            _memo['grid_search_results'] = _gs_res_tbl.to_dict('records')

            tbl = dbc.Table.from_dataframe(_gs_res_tbl, index=False, striped=False, bordered=True, hover=True, size='sm')
            return len(_combs), [html.Hr(), html.P(html.B('Top-10 models by AIC score')), tbl], _memo

    return len(_combs), None, _memo
