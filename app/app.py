# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import page_layout as pl

# using dash-bootstrap-components for our external stylesheets
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.scripts.config.serve_locally = True

# setup container for our page-content that will be called based on the url/pathname
dynamic_body_content = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
]) 

# initiate the app layout which consists of navbar and dinamically loaded body content
app.layout = html.Div([pl.navbar, dynamic_body_content])

# setup the callback for each page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/kebijakan-privasi':
    	return pl.body_kebijakan_privasi, pl.body_footer
    elif pathname == '/tos':
    	return pl.body_tos, pl.body_footer
    elif pathname == '/disclaimer':
    	return pl.body_disclaimer, pl.body_footer
    # elif pathname == '/dataviz':
    # 	return pl.body_selected_file, pl.body_display_datatable
    # elif pathname == '/details':
    # 	return pl.body_display_details
    elif pathname == '/dashboard':
        return pl.body_grafana, pl.body_footer
    elif pathname == '/about':
        return pl.body_about, pl.body_footer
    elif pathname == '/':
    	return pl.body_index, pl.body_footer
    else:
    	return pl.body_index, pl.body_footer


# Start the app server
if __name__ == '__main__':
    app.run_server(debug=True)