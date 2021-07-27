from dash import Dash
from backend.back_end import BackEnd
import dash_bootstrap_components as dbc

app = Dash(__name__,
           suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

#creamos una sola instancia del backend
back = BackEnd()