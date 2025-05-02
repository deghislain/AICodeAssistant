import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from llm_calls import get_unit_test_feedback, generate_improved_unit_tests, generate_unit_test

reviewing_model = ""
write_code_model = ""
# Initialize the Dash app
app = dash.Dash(__name__)

# Create a DataFrame
df = pd.DataFrame({
    'first column': ["granite3.3:2b", "llama3.2:latest"],
    'second column': ["llama3.2:latest", "granite3.3:2b"]
})

app.layout = html.Div([
    html.Div([
        html.H2('Select LLMs'),
        html.Div([
            html.Div([
                html.Label('Select testing LLM'),
                dcc.Dropdown(
                    id='testing-llm',
                    options=[{'label': i, 'value': i} for i in df['first column']],
                    value=df['first column'][0]
                ),
                html.P(id='testing-llm-selected')
            ], style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select reviewing LLM'),
                dcc.Dropdown(
                    id='reviewing-llm',
                    options=[{'label': i, 'value': i} for i in df['second column']],
                    value=df['second column'][0]
                ),
                html.P(id='reviewing-llm-selected')
            ], style={'width': '20%', 'float': 'right'})
        ])
    ]),
    html.Div([
        html.Div([
            html.Div([
                html.Label('Code'),
                dcc.Textarea(
                    id='coding-notes',
                    style={'width': '100%', 'height': 400}
                ),
                html.Button('Get Unit Test', id='get-unit-test-button', n_clicks=0,
                            style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                                   'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            ], style={'width': '49%', 'height': '100px', 'display': 'inline-block'}),
            html.Div([
                html.Label('Unit Test'),
                dcc.Textarea(
                    id='unit-test-notes',
                    style={'width': '100%', 'height': 400}
                ),
                html.Button('Get Feedback', id='get-feedback-button', n_clicks=0,
                            style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                                   'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            ], style={'width': '49%', 'float': 'right'})
        ]),
        html.Div([
            html.Label('Review feedback'),
            dcc.Textarea(
                id='reviewing-notes',
                style={'width': '100%', 'height': 200}
            ),
            html.Button('Fix it', id='fix-it-button', n_clicks=0,
                        style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                               'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
        ], style={'width': '100%', 'float': 'right'})
    ]),

    html.Div(id='code-content'),
    html.Div(id='unit-test-content'),
    html.Div(id='review-content')
])


# Define callback functions
@app.callback(
    Output('testing-llm-selected', 'children'),
    [Input('testing-llm', 'value')]
)
def update_coding_llm_selected(value):
    global write_code_model
    write_code_model = value
    return f'You selected: {value}'


@app.callback(
    Output('reviewing-llm-selected', 'children'),
    [Input('reviewing-llm', 'value')]
)
def update_reviewing_llm_selected(value):
    global reviewing_model
    reviewing_model = value
    return f'You selected: {value}'


@app.callback(
    Output('unit-test-notes', 'value'),
    [Input('get-unit-test-button', 'n_clicks'),
     Input('fix-it-button', 'n_clicks')],
    [State('coding-notes', 'value'),
     State('unit-test-notes', 'value'),
     State('reviewing-notes', 'value')
     ]
)
def update_unit_test_notes(get_unit_test_clicks, get_feedback_clicks, code, unit_test, feedback):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ''

    prop_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if prop_id == 'get-unit-test-button':
        if get_unit_test_clicks is not None and get_unit_test_clicks > 0:
            return generate_unit_test(code, reviewing_model)
    elif prop_id == 'fix-it-button':
        if get_feedback_clicks is not None and get_feedback_clicks > 0:
            return generate_improved_unit_tests(unit_test, write_code_model, feedback)

    return unit_test if unit_test else ''


@app.callback(
    Output('reviewing-notes', 'value'),
    [Input('get-feedback-button', 'n_clicks')],
    [State('coding-notes', 'value'),
     State('unit-test-notes', 'value')]
)
def provide_unit_test_review_feedback(n_clicks, code, unit_test):
    if n_clicks is not None and n_clicks > 0:
        return get_unit_test_feedback(code, unit_test, reviewing_model)
    return ''


if __name__ == '__main__':
    app.run(debug=True)
