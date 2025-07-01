import asyncio

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from llm_calls import process_prompt

prompt_model = ""
selected_persona = ""
# Initialize the Dash app
app = dash.Dash(__name__)

# Create a DataFrame
df = pd.DataFrame({
    'first column': ["granite3.3:2b", "llama3.2:latest", "granite-code:8b", "codellama:7b", "", ""],
    'second column': ["prompt_engineer", "english_teacher", "software_engineer", "translator", "researcher", "writer"]
})

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H2('Select LLMs'),
        html.Div([
            html.Div([
                html.Label('Select LLM'),
                dcc.Dropdown(
                    id='prompt-llm',
                    options=[{'label': i, 'value': i} for i in df['first column']],
                    value=df['first column'][0]
                ),
                html.P(id='prompt-llm-selected')
            ], style={'width': '20%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select Persona'),
                dcc.Dropdown(
                    id='persona',
                    options=[{'label': i, 'value': i} for i in df['second column']],
                    value=df['second column'][0]
                ),
                html.P(id='selected_persona')
            ], style={'width': '20%', 'float': 'right'})
        ])
    ]),
    html.Div([
        html.Div([
            html.Div([
                html.Label('Prompt'),
                dcc.Textarea(
                    id='prompt-notes',
                    style={'width': '100%', 'height': 550}
                ),
                html.Button('Submit', id='submit-button', n_clicks=0,
                            style={'background-color': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                                   'border': 'none', 'border-radius': '5px', 'cursor': 'pointer'})
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Result'),
                dcc.Textarea(
                    id='reviewing-prompt-notes',
                    style={'width': '100%', 'height': 550}
                ),
            ], style={'width': '49%', 'float': 'right'})
        ])
    ]),
    html.Div(id='prompt-content'),
    html.Div(id='reviewed-prompt')
])


@app.callback(
    Output('prompt-llm-selected', 'children'),
    [Input('prompt-llm', 'value')]
)
def update_prompt_llm_selected(value):
    global prompt_model
    prompt_model = value
    return f'You selected: {value}'

@app.callback(
    Output('selected_persona', 'children'),
    [Input('persona', 'value')]
)
def update_reviewing_llm_selected(value):
    global selected_persona
    selected_persona = value
    return f'You selected: {value}'

@app.callback(
    Output('reviewing-prompt-notes', 'value'),
    [Input('submit-button', 'n_clicks')],
    [State('prompt-notes', 'value')]
)
def prompt_handler(n_clicks, prompt):
    if n_clicks is not None and n_clicks > 0:
        return asyncio.run(process_prompt(prompt, prompt_model, selected_persona))
    return ''


if __name__ == '__main__':
    app.run(debug=True)
