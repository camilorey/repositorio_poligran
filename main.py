import pandas as pd
from datetime import date
import dash_uploader as du
import dash_daq as daq
from pathlib import Path
import dash_html_components as html
from app import app,back
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from helpers.back_end_controladores_factory import ControladoresFactory
from helpers.queries_especiales import query_grps_esc_facs_proy_id
from helpers.queries_especiales import query_linea_area_todos

control_factory = ControladoresFactory(back)


drop_programa = control_factory.crear_dropdown(nom_tabla='programa_academico')

back.get_periodo_actual_id()


drop_proyecto_drop = control_factory.crear_dropdown(nom_tabla='proyecto',drop_id ='proyecto-drop-id')
drop_proyecto = html.Div(id='drop-proyecto-comp-id',
                         children=[html.H2('Escoja el proyecto para asociar todo en el formulario'),
                                   drop_proyecto_drop])

drop_periodo_drop = control_factory.crear_dropdown(nom_tabla='periodo',drop_id='periodo-drop-id')
drop_periodo = html.Div(id='drop-periodo-comp-id',
                         children=[html.H2('Escoja el periodo al que quiere asociar el proyecto'),
                                   html.P('Por defecto se fija en ESTE periodo'),
                                   drop_periodo_drop])

def print_listado_como_string(valores):
    info = ''
    for i,val in enumerate(valores):
        info += val
        if i < len(valores)-1:
            info +=','

    return info

#-----------------------------------------------------------------------------------------
#Este es el store para poner la información del proyecto
#-----------------------------------------------------------------------------------------

@app.callback(Output('store-info-proyecto','data'),
              Input('proyecto-drop-id','value'))
def get_info_proyecto(proyecto_id):
    if proyecto_id is not None:
        query = query_grps_esc_facs_proy_id.replace('<proy_id>',str(proyecto_id))
        df = back.hacer_query(query)
        return df.to_json(orient='records')

#-----------------------------------------------------------------------------------------
#Estos son los bloques de texto que muestran la información de escuelas y facultades
#-----------------------------------------------------------------------------------------
@app.callback(Output('texto-facultades-id','children'),
              Input('store-info-proyecto','data'))
def actualizar_info_facultades(data_json):
    if data_json is None:
        return [html.H4('Facultades (No hay selección)')]
    else:
        df = pd.read_json(data_json)
        facs = df[['facultad']].drop_duplicates()
        lista_facs = []
        for idx,fac in facs.iterrows():
            fac_item = html.Li(fac['facultad'])
            lista_facs.append(fac_item)

        return html.Div(children=[html.H4('Facultades'),
                                  html.Ul(children=lista_facs)])

@app.callback(Output('texto-escuelas-id','children'),
              Input('store-info-proyecto','data'))
def actualizar_info_escuelas(data_json):
    if data_json is None:
        return [html.H4('Escuelas (No hay selección)')]
    else:
        df = pd.read_json(data_json)
        facs = df[['escuela']].drop_duplicates()
        lista_facs = []
        for idx,fac in facs.iterrows():
            fac_item = html.Li(fac['escuela'])
            lista_facs.append(fac_item)

        return html.Div(children=[html.H4('Escuelas'),
                                  html.Ul(children=lista_facs)])

@app.callback(Output('texto-grupos-id','children'),
              Input('store-info-proyecto','data'))
def actualizar_info_grupos(data_json):
    if data_json is None:
        return [html.H4('Grupos (No hay selección)')]
    else:
        df = pd.read_json(data_json)
        facs = df[['grupo']].drop_duplicates()
        lista_facs = []
        for idx,fac in facs.iterrows():
            fac_item = html.Li(fac['grupo'])
            lista_facs.append(fac_item)

        return html.Div(children=[html.H4('Grupos'),
                                  html.Ul(children=lista_facs)])

@app.callback(Output('texto-fechas-id','children'),
              Input('proyecto-drop-id','value'))
def actualizar_fechas_proyecto(proyecto_id):
    fecha_ini = 'NO SE HA ESCOGIDO'
    fecha_cie = '-'
    estado = 'EN CURSO'
    if proyecto_id is not None:
        fecha_ini,fecha_cierre = back.get_fechas_proyecto(proyecto_id)
        fecha_ini = str(fecha_ini)
        if fecha_cierre is not None:
            fecha_cie = str(fecha_cie)
            estado = 'FINALIZADO'
    inicio_fin =[html.Li("Inicio del Proyecto: "+fecha_ini)]
    inicio_fin.append(html.Li("Fin del proyecto: "+fecha_cie))
    inicio_fin.append(html.Li("Estado del proyecto: "+estado))
    return html.Div(children=[html.H4("Fechas importantes del proyecto"),
                              html.Ul(children=inicio_fin)])

@app.callback(Output('periodo-drop-id','value'),
              Input('proyecto-drop-id','value'))
def poner_periodo_actual(proyecto_id):
    per_actual = back.get_periodo_actual_id()

    return per_actual
#-----------------------------------------------------------------------------------------
#Este es el drop para asociar programas académicos
#-----------------------------------------------------------------------------------------
programas = back.get_programas_academicos()
ops = []
for idx,prog in programas.iterrows():
    prog_id = prog['programa_academico_id']
    prog_nombre = prog['programa_academico']
    ops.append({'label':prog_nombre,'value':prog_id})

programas_drop = dcc.Dropdown(id='drop-programas-proyecto-id',
                             options = ops,
                             multi=True)

@app.callback(Output('drop-programas-proyecto-id','value'),
              Input('store-info-proyecto','data'))
def actualizar_info_programas(data_json):
    if data_json is None:
        return []
    else:
        df = pd.read_json(data_json)
        escuelas = list(df['escuela_id'].unique())
        progs_seleccionados = programas.loc[programas['escuela_id'].isin(escuelas)]
        return list(progs_seleccionados['programa_academico_id'].unique())

#-----------------------------------------------------------------------------------------
#Vamos a poner un text area para poner el nombre del producto
#-----------------------------------------------------------------------------------------
input_nom_producto = dcc.Textarea(id='nom-producto-input-id',
                                   value='Ingrese el nombre de su producto',
                                  style={"width":"100%","height":"200"})
nom_producto = html.Div(id='nom-producto-id',
                        children=[html.H4("Ingrese el nombre del producto"),
                                  input_nom_producto])

input_cod_cvlac = dcc.Textarea(id='cod-cvlac-input-id',
                               style={"width":"100%"})
cod_cvlac = html.Div(id='cod-cvlac-id',
                     children=[html.H4("Ingrese el Código CVLac de su producto"),
                               input_cod_cvlac])
input_cod_investigacion = dcc.Textarea(id='cod-investigacion-input-id',
                                    style={'width':'100%'})
cod_investigacion = html.Div(id='cod-investigacion-id',
                             children=[html.H4("Ingrese Código del Departamento de Investigación"),
                                       input_cod_investigacion])
input_num_convocatoria = dcc.Textarea(id='num-convocatoria-input-id',
                                      style={"width":"100%"})
num_convocatoria = html.Div(id='num-convocatoria-id',
                            children=[html.H4("Ingrese número de la convocatoria"),
                                      input_num_convocatoria])

fecha_convocatoria = dcc.DatePickerSingle(
        id='fecha-convocatoria-input-id',
        min_date_allowed=date(1995, 8, 5),
        initial_visible_month=date(2017, 8, 5),
        date=date.today(),
        style={"width":"100%"})
fecha_convocatoria = html.Div(id='fecha-convocatoria-id',
                              children=[html.H4("Ingrese la Fecha de Convocatoria"),
                                        fecha_convocatoria])
paises = back.get_paises()
ops_paises = []

id_colombia = 157
for idx, pais in paises.iterrows():
    clase_id = pais['pais_id']
    clase_nombre = pais['pais']
    if clase_nombre == 'COLOMBIA':
        id_colombia = clase_id
    ops_paises.append({'label': clase_nombre, 'value': clase_id})
pais_drop = dcc.Dropdown(id='pais-drop-id',
                         options=ops_paises,
                         multi=True,
                         value=id_colombia)
pais = html.Div(id='pais-id',
                children=[html.H4("Ingrese el país de la convocatoria"),
                          pais_drop])
componente_campos =[dbc.Row(dbc.Col(nom_producto,width=12),no_gutters=True)]

#-----------------------------------------------------------------------------------------
#Vamos a poner una caja de diálogo para las clases de productos
#-----------------------------------------------------------------------------------------
clase_productos = back.get_clase_producto()
ops = []
for idx,clase in clase_productos.iterrows():
    clase_id = clase['clase_producto_id']
    clase_nombre = clase['clase_producto']
    ops.append({'label':clase_nombre,'value':clase_id})


clase_producto = html.Div([html.H4("Escoja una clase de producto"),
                           dcc.Dropdown(id='clase-producto-id',
                                        placeholder='Escoja una clase de producto',
                                        options=ops)])

tipo_producto = html.Div([html.H4("Escoja el tipo producto"),
                           dcc.Dropdown(id='tipo-producto-drop-id',
                                        placeholder='Escoja primero una clase de producto')])

@app.callback(Output('tipo-producto-drop-id','options'),
              Input('clase-producto-id','value'))
def actualizar_tipo_producto(clase_prod):
    if clase_prod is None:
        return []
    clase_productos = back.get_tipo_producto(clase_prod)
    ops=[]
    for idx, clase in clase_productos.iterrows():
        clase_id = clase['tipo_producto_id']
        clase_nombre = clase['tipo_producto']
        ops.append({'label': clase_nombre, 'value': clase_id})
    return ops

#-----------------------------------------------------------------------------------------
#Vamos a poner una caja para las personas
#-----------------------------------------------------------------------------------------
personas_drop = dcc.Dropdown(id='personas-drop-id')
#drop para escoger personas que ya están en la DB
personas = back.get_personas()
ops = []
for idx,persona in personas.iterrows():
    clase_id = persona['persona_id']
    clase_nombre = persona['persona']
    ops.append({'label':clase_nombre,'value':clase_id})
personas_drop = dcc.Dropdown(id='personas-drop-id',
                             options=ops,
                             multi=True)

#-----------------------------------------------------------------------------------------
#Vamos a poner una caja para poner las personas asociadas al proyecto
#-----------------------------------------------------------------------------------------
campo_cedula = html.Div(id='nueva-cedula-id',
                        children=[html.H5('Identificacion de la persona'),
                                  dcc.Input(id='nueva-cedula-field-id')])
campo_nombre = html.Div(id='nuevo-nombre-id',
                        children=[html.H5('Nombre y Apellidos de la persona'),
                                  dcc.Input(id='nuevo-nombre-field-id')])
ops_tipo_persona = [{"label":'EXTERNO',"value":"EXTERNO"},
                    {"label":'ESTUDIANTE',"value":"ESTUDIANTE"},
                    {"label":'DOCENTE',"value":"DOCENTE"},]
campo_tipo = html.Div(id='nuevo-tipo-id',
                      children=[html.H5('Tipo de la persona'),
                                dcc.Checklist(id='tipo-nueva-persona-check-id',
                                              options=ops_tipo_persona)])
boton_agregar_persona = html.Div(html.Button('Agregar Persona',
                                             id='agregar-persona-boton-id',
                                             style={'backgroundColor': '#111100',
                                                    'color': 'white',
                                                    'width': '100%',
                                                    'border': '1.5px black solid',
                                                    'height': '50px',
                                                    'text-align': 'center',
                                                    'marginLeft': '20px',
                                                    'marginTop': 20}))
nueva_persona_div = html.Div([html.H4('Agregar nueva persona'),
                         html.P('Puede poner cédula de ciudadanía, de extranjería o pasaporte'),
                         dbc.Row([dbc.Col(campo_cedula,width=12),
                                  dbc.Col(campo_nombre,width=12),
                                  dbc.Col(campo_tipo,width=12),
                                  dbc.Col(boton_agregar_persona,width=12),
                                  dbc.Col(html.Div(id='persona-agregada-id'),width=12)],
                                 no_gutters=True)
                              ])
@app.callback(Output('persona-agregada-id','children'),
              Input('agregar-persona-boton-id','n_clicks'),
              State('nueva-cedula-field-id','value'),
              State('nuevo-nombre-field-id','value'),
              State('tipo-nueva-persona-check-id','value'))
def agregar_persona_boton(n_clicks,persona_id,persona_nombre,tipos):
    if persona_id is not None and persona_nombre is not None and tipos is not None:
        if len(tipos)==0:
            return "falta poner por lo menos un tipo de persona"
        else:
            persona_nombre = persona_nombre.upper()
            back.agregar_persona(persona_id,persona_nombre,tipos)
            return "persona agregada"
    else:
        return "Faltan campos por llenar"

@app.callback(Output('personas-drop-id','value'),
              Input('agregar-persona-boton-id','n_clicks'),
              State('nueva-cedula-field-id','value'),
              State('nuevo-nombre-field-id','value'),
              State('personas-drop-id','value'))
def agregar_persona_lista(n_clicks,persona_id,persona_nombre,personas_selec):
    if personas_selec is None:
        return [{"label":persona_id,'value':persona_id}]
    else:
        nuevas = personas_selec.append({"label":persona,'value':persona_id})
        return nuevas


@app.callback(Output('personas-drop-id','options'),
              Input('agregar-persona-boton-id','n_clicks'))
def actualizar_personas_lista(n_clicks):
    personas = back.get_personas()
    ops = []
    for idx, persona in personas.iterrows():
        clase_id = persona['persona_id']
        clase_nombre = persona['persona']
        ops.append({'label': clase_nombre, 'value': clase_id})
    return ops

personas = html.Div(id='info-personas-id',
                         children=[html.H4("Personas relacionadas al proyecto"),
                                   personas_drop,
                                   nueva_persona_div])
#-----------------------------------------------------------------------------------------
#Vamos a poner una caja para las áreas y líneas
#-----------------------------------------------------------------------------------------
areas_lineas_total = back.hacer_query(query_linea_area_todos)
ops_areas = []
ops_lineas = []
areas_total = areas_lineas_total[['area_id','area']].drop_duplicates()
for idx, area in areas_total.iterrows():
    clase_id = area['area_id']
    clase_nombre = area['area']
    ops_areas.append({'label': clase_nombre, 'value': clase_id})

lineas_total = areas_lineas_total[['linea_id','linea']].drop_duplicates()
for idx, linea in lineas_total.iterrows():
    clase_id = linea['linea_id']
    clase_nombre = linea['linea']
    ops_lineas.append({'label': clase_nombre, 'value': clase_id})

areas_drop = dcc.Dropdown(id='areas-drop-id',
                          multi=True)
lineas_drop = dcc.Dropdown(id='lineas-drop-id',
                           multi=True)

@app.callback(Output('areas-drop-id','options'),
              Input('proyecto-drop-id','value'))
def set_areas_proyecto_drop(proyecto_id):
    if proyecto_id is not None:
        areas_y_lineas = back.get_lineas_y_areas_de_proyecto(proyecto_id)
        areas = areas_y_lineas[['area_id','area']].drop_duplicates()
        ops = []
        for idx, area in areas.iterrows():
            clase_id = area['area_id']
            clase_nombre = area['area']
            ops.append({'label': clase_nombre, 'value': clase_id})
        return ops
    else:
        return ops_areas

@app.callback(Output('lineas-drop-id','options'),
              Input('proyecto-drop-id','value'),
              Input('areas-drop-id','value'))
def set_lineas_proyecto_drop(proyecto_id,areas):
    if proyecto_id is None and areas is None:
        return ops_lineas
    elif areas is not None and proyecto_id is None:
        sub_lineas = areas_lineas_total.loc[areas_lineas_total['area_id'].isin(areas)]
        ops_sub_lineas = []
        for idx, linea in sub_lineas.iterrows():
            clase_id = linea['linea_id']
            clase_nombre = linea['linea']
            ops_sub_lineas.append({'label': clase_nombre, 'value': clase_id})
        return ops_sub_lineas
    else:
        areas_y_lineas = back.get_lineas_y_areas_de_proyecto(proyecto_id)
        lineas = areas_y_lineas[['linea_id', 'linea']].drop_duplicates()
        ops = []
        for idx, linea in lineas.iterrows():
            clase_id = linea['linea_id']
            clase_nombre = linea['linea']
            ops.append({'label': clase_nombre, 'value': clase_id})
        return ops

    if proyecto_id is not None and areas is not None:
        areas_y_lineas = back.get_lineas_y_areas_de_proyecto(proyecto_id)
        areas = areas_y_lineas[['area_id','area']]
        lineas = areas_y_lineas[['linea_id','linea','area_id']].drop_duplicates()
        ops = []
        for idx, linea in lineas.iterrows():
            clase_id = linea['linea_id']
            clase_nombre = linea['linea']
            area_id = linea['area_id']
            if area_id in areas:
                ops.append({'label': clase_nombre, 'value': clase_id})
        return ops

instis = back.get_instituciones()
ops = []
for idx, insti in instis.iterrows():
        clase_id = insti['instituciones_id']
        clase_nombre = insti['instituciones']
        ops.append({'label': clase_nombre, 'value': clase_id})

instituciones_drop = dcc.Dropdown(id='instituciones-drop-id',
                                  options=ops,
                                  multi=True)

campo_nom_institucion = html.Div(id='nombre-nueva-institucion-id',
                        children=[html.H5('Nombre de la Institución'),
                                  dcc.Input(id='nueva-institucion-input-id')])
boton_agregar_institucion = html.Div(html.Button('Agregar Institución',
                                             id='agregar-institucion-boton-id',
                                             style={'backgroundColor': '#111100',
                                                    'color': 'white',
                                                    'width': '100%',
                                                    'border': '1.5px black solid',
                                                    'height': '50px',
                                                    'text-align': 'center',
                                                    'marginLeft': '20px',
                                                    'marginTop': 20}))
nueva_institucion_div = html.Div([html.H4('Agregar nueva Institución'),
                         html.P('Puede poner nombre de la institucion'),
                         dbc.Row([dbc.Col(campo_nom_institucion,width=12),
                                  dbc.Col(boton_agregar_institucion,width=12),
                                  dbc.Col(html.Div(id='institucion-agregada-id'),width=12)],
                                 no_gutters=True)
                              ])
instituciones = html.Div(id='info-instituciones-id',
                    children=[html.H4("Instituciones relacionadas"),
                              instituciones_drop,
                              nueva_institucion_div])

@app.callback(Output('institucion-agregada-id','children'),
              Input('agregar-institucion-boton-id', 'n_clicks'),
              State('nueva-institucion-input-id', 'value'))
def agregar_nueva_institucion(n_clicks,nom_institucion):
    if nom_institucion is not None:
        back.agregar_nueva_institucion(nom_institucion.upper())
        return "Nueva institución agregada, refresque"
    else:
        return "no se ha agregado ninguna institución"

@app.callback(Output('instituciones-drop-id','children'),
              Input('agregar-institucion-boton-id', 'n_clicks'))
def actualizar_instituciones(n_clicks):
    instis = back.get_instituciones()
    ops = []
    for idx, insti in instis.iterrows():
        clase_id = insti['instituciones_id']
        clase_nombre = insti['instituciones']
        ops.append({'label': clase_nombre, 'value': clase_id})


areas_y_lineas = html.Div(id='areas-y-lineas-id',
                          children=[html.H4("Áreas y Líneas de investigación"),
                                    html.Div(children=[html.H5('Áreas de Investigación'),
                                                       areas_drop]),
                                    html.Div(children=[html.H5('Líneas de Investigación'),
                                                       lineas_drop]),
                                    html.Div(children=[html.H5('Instituciones asociadas'),
                                                       instituciones])])

#-----------------------------------------------------------------------------------------
#Vamos a poner una caja de diálogo para subir el archivo
#-----------------------------------------------------------------------------------------
tipos_archivo_permitidos = ['rar','zip','doc','docx','xls','xlsx',
                            'pdf','tex','png','jpg']
UPLOAD_FOLDER = r"C:\Users\camil\Documents\repositorio_proyecto_dash\static\uploads"
du.configure_upload(app, UPLOAD_FOLDER)
upload_archivo_uploadbox = du.Upload(upload_id='upload-data-id',
                                     text='Arrastre y suelte sus archivos aquí',
                                     text_completed='Completado:',
                                     pause_button=False,
                                     cancel_button=True,
                                     max_file_size=200, #200MB en tamaños,
                                     filetypes=tipos_archivo_permitidos)
upload_archivos_div = html.Div(upload_archivo_uploadbox,
                               style={'textAlign': 'center','width': '100%',
                                      'padding': '10px','display': 'inline-block'})
confirmacion_archivo_subido = html.Div(id='confirmacion-dialogo-id')
upload_archivo = html.Div(id='upload-archivo',
                          children=[html.H4("Subir archivos al repositorio"),
                                    upload_archivos_div,
                                    confirmacion_archivo_subido])

@app.callback(Output('confirmacion-dialogo-id','children'),
              Input('upload-data-id','isCompleted'),
              State('upload-data-id','fileNames'))
def imprimir_confirmacion(completo,nom_archivos):
    if nom_archivos is not None:
        out = []
        for archivo in nom_archivos:
            #file = Path(UPLOAD_FOLDER) / archivo
            out.append(archivo)
        return html.Ul([html.Li(str(x)) for x in out])
    else:
        return html.Ul(html.Li("Ningún archivo para subir!"))

#-----------------------------------------------------------------------------------------
#Ahora ponemos el botón de enviar
#-----------------------------------------------------------------------------------------
boton_enviar_comp = html.Button('Subir al Repositorio',
                                id='boton-subir',
                                n_clicks=0,
                                style={'backgroundColor': '#111100',
                                       'color':'white',
                                       'width':'100%' ,
                                       'border':'1.5px black solid',
                                       'height': '50px',
                                       'text-align':'center',
                                       'marginLeft': '20px',
                                       'marginTop': 20})

def generar_informe(nom_producto,cvlac,cod_invest,
                    num_convo,fecha_conv,paises,
                    clase,tipo,proy_id,perio_id,personas,instituciones):
    titulo_label = "Registro: "+nom_producto.title()
    titulo = html.H2(titulo_label)
    informacion_campos = [html.H3('Código CVLac: '+cvlac),
                          html.H3('Código Investigación: '+cod_invest),
                          html.H3('Número de Convocatoria: '+num_convo),
                          html.H3("Fecha de la Convocatoria: "+str(fecha_conv))]
    pais_string = ''
    if isinstance(paises, int):
        informacion_campos.append(html.H3('País ' + str(paises)))
    else:
        for i, p in enumerate(paises):
            pais_string += str(p)
            if i < len(paises) - 1:
                pais_string += ', '
    informacion_campos.append(html.H3('Países de la convocatoria: ' + pais_string))
    informacion_campos.append(html.H3('Clase de Producto: ' + str(clase)))
    informacion_campos.append(html.H3('Tipo de Producto: ' + str(tipo)))
    if personas is not None:
        lista_personas = html.Ul([html.Li(str(p)) for p in personas])
        informacion_campos.append(html.Div([html.H3('Personas:'),
                                            lista_personas]))
    else:
        informacion_campos.append(html.H3('Personas: None'))

    if instituciones is not None:
        lista_instituciones = html.Ul([html.Li(str(p)) for p in instituciones])
        informacion_campos.append(html.Div([html.H3('Instituciones:'),
                                            lista_instituciones]))
    else:
        informacion_campos.append(html.H3('Personas: None'))

    return html.Div(children=[titulo,
                              html.Div(html.H3('Proyecto ' + str(proy_id))),
                              html.Div(html.H3('Periodo ' + str(perio_id))),
                              html.Div([html.H2("Campos de texto"),
                                        html.Div(informacion_campos)
                                        ])
                              ]
                    )
'instituciones-drop-id'
@app.callback(Output('info-proyecto-id','children'),
              Input('boton-subir','n_clicks'),
              State('nom-producto-input-id','value'),State('cod-cvlac-input-id','value'),
              State('cod-investigacion-input-id','value'),State('num-convocatoria-input-id','value'),
              State('fecha-convocatoria-input-id','date'),State('pais-drop-id','value'),
              State('clase-producto-id','value'),State('tipo-producto-drop-id','value'),
              State('proyecto-drop-id','value'),State('periodo-drop-id','value'),
              State('personas-drop-id','value'),State('instituciones-drop-id','value'),
              State('drop-programas-proyecto-id','value'),State('lineas-drop-id','value'))
def agregar_al_repo(num_clicks,nom_producto,cvlac,cod_invest,num_convocatoria,
                    fecha_conv,paises,clase,tipo,proyecto_id,
                    periodo_id,personas,instituciones,programas,lineas):
    #insertamos el producto en la tabla
    prod_id = back.insertar_en_producto(nom_producto,tipo)
    #insertamos el registro y la convocatoria y asociamos el producto con el proyecto
    back.insertar_en_registro(prod_id,periodo_id,proyecto_id,
                              num_convocatoria,date.today(),fecha_conv)
    #ahora asociamos las personas con el producto
    if isinstance(personas,str):
        personas = [personas]

    back.asociar_producto_personas(prod_id,personas)
    if isinstance(paises,str):
        paises =[paises]
    #asociamos producto con paises
    back.asociar_producto_paises(prod_id,paises)
    if isinstance(instituciones,str):
        instituciones = [instituciones]
    back.asociar_producto_instituciones(prod_id,instituciones)
    if isinstance(lineas,str):
        lineas = [lineas]
    back.asociar_producto_lineas(prod_id,lineas)
    if programas is not None:
        if isinstance(programas,str):
            programas = [programas]
        back.asociar_producto_programas(prod_id,programas)

    return generar_informe(nom_producto,cvlac,cod_invest,
                           num_convocatoria,fecha_conv,paises,
                           clase,tipo,proyecto_id,periodo_id,personas,instituciones)

#-----------------------------------------------------------------------------------------
#Este es el layout de la aplicación en general
#-----------------------------------------------------------------------------------------
app.layout = html.Div([dcc.Store(id='store-info-proyecto'),
                       dbc.Container([html.H1("Este es el Formulario para subir Archivos"),
                                      html.Div([dbc.Row([dbc.Col(drop_proyecto, width=10),
                                                         dbc.Col(drop_periodo, width=2)],
                                                        no_gutters=True)]),
                                      dbc.Row([dbc.Col(html.Div(id='texto-facultades-id'),width=3),
                                                       dbc.Col(html.Div(id='texto-escuelas-id'),width=2),
                                                       dbc.Col(html.Div(id='texto-grupos-id'),width=2),
                                                       dbc.Col(html.Div(id='texto-fechas-id'),width=2),
                                                       dbc.Col(html.Div(id='caja-programas-id',
                                                                        children=[html.H4("Programas Académicos relacionados"),
                                                                                  programas_drop]),width=3)],
                                                      no_gutters=True),
                                      dbc.Row([dbc.Col(personas,width=6),
                                             dbc.Col(areas_y_lineas,width=6)],
                                            no_gutters=True),
                                      dbc.Row([dbc.Col(nom_producto,width=12)],
                                                      no_gutters=True),
                                      dbc.Row([dbc.Col(cod_cvlac),
                                             dbc.Col(cod_investigacion)],no_gutters=True),
                                      dbc.Row([dbc.Col(num_convocatoria),
                                              dbc.Col([fecha_convocatoria,pais]),
                                              dbc.Col([clase_producto,tipo_producto])],
                                              no_gutters=True),
                                      dbc.Row(dbc.Col(upload_archivo,width=12),
                                             no_gutters=True),
                                      dbc.Row([boton_enviar_comp],no_gutters=True),
                                      dbc.Row([html.Div(id='info-proyecto-id')],no_gutters=True)

                                      ],fluid=True)],
                      style={"padding-left":"0px"})

#-----------------------------------------------------------------------------------------
#Este es el layout de la aplicación en general
#-----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False,port=5080)


