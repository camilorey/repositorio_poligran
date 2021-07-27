from helpers.controladores import Dropdown
import pandas as pandas

QUERY_TABLA_BASE = "SELECT * FROM <nom_tabla>"

class ControladoresFactory:
    def __init__(self,back):
        self.back = back

    def crear_opciones_dropdown(self,dataframe,nom_campo,nom_val):
        opciones = {}
        for idx,fila in dataframe.iterrows():
            nombre = fila[nom_campo]
            valor = fila[nom_val]
            opciones[nombre] = valor
        return opciones

    def crear_dropdown(self,nom_tabla=None,query=None,nom_drop=None,drop_id=None):
        drop = None
        nom_d = 'drop-x'
        d_id = 'drop-x-id'
        if nom_drop is not None:
            nom_d = nom_drop
        if nom_tabla is not None:
            q = QUERY_TABLA_BASE.replace('<nom_tabla>',nom_tabla)
            nom_d = nom_tabla
            drop_id = nom_tabla+"-drop-id"
        if drop_id is not None:
            d_id = drop_id
        if query is not None:
            q = query
        result = self.back.hacer_query(q)
        nom_op = result.columns[1]
        nom_val = result.columns[0]
        ops = self.crear_opciones_dropdown(result,nom_op,nom_val)
        drop = Dropdown(drop_label=nom_d,
                        id=d_id,
                        opciones_dict=ops)
        print(drop_id)
        drop_comp = drop.crear_container()

        return drop_comp
