import asyncio

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from llm_calls import get_feedback, generate_improved_code

reviewing_model = ""
write_code_model = ""
# Initialize the Dash app
app = dash.Dash(__name__)

# Create a DataFrame
df = pd.DataFrame({
    'first column': ["granite3.3:2b", "llama3.2:latest"],
    'second column': ["llama3.2:latest", "granite3.3:2b"]
})

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H2('Select LLMs'),
        html.Div([
            html.Div([
                html.Label('Select coding LLM'),
                dcc.Dropdown(
                    id='coding-llm',
                    options=[{'label': i, 'value': i} for i in df['first column']],
                    value=df['first column'][0]
                ),
                html.P(id='coding-llm-selected')
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
                    style={'width': '100%', 'height': 550}
                ),
                html.Button('Get Feedback', id='get-feedback-button', n_clicks=0,
                            style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                                   'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Review feedback'),
                dcc.Textarea(
                    id='reviewing-notes',
                    style={'width': '100%', 'height': 550}
                ),
                html.Button('Fix it', id='fix-it-button', n_clicks=0,
                            style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                                   'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            ], style={'width': '49%', 'float': 'right'})
        ])
    ]),
    html.Div(id='code-content'),
    html.Div(id='review-content')
])


# Define callback functions
@app.callback(
    Output('coding-llm-selected', 'children'),
    [Input('coding-llm', 'value')]
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
    Output('reviewing-notes', 'value'),
    [Input('get-feedback-button', 'n_clicks')],
    [State('coding-notes', 'value')]
)
def provide_review_feedback(n_clicks, code):
    if n_clicks is not None and n_clicks > 0:
        return asyncio.run(get_feedback(code, reviewing_model))
    return ''


@app.callback(
    Output('coding-notes', 'value'),
    [Input('fix-it-button', 'n_clicks')],
    [State('reviewing-notes', 'value'),
     State('coding-notes', 'value')]
)
def fix_code(n_clicks, review, code):
    if n_clicks is not None and int(n_clicks) > 0:
        return asyncio.run(generate_improved_code(code, write_code_model, review))
    return code


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
