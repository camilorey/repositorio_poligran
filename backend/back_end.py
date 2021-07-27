import pandas as pd
import psycopg2
from datetime import datetime
from helpers.queries_especiales import query_grps_esc_facs_proy_id
from helpers.queries_especiales import query_tipos_de_clase
from helpers.queries_especiales import insert_persona,insert_persona_tipo
from helpers.queries_especiales import query_grupo_linea_area_de_proyecto
from helpers.queries_especiales import insert_en_producto
from helpers.queries_especiales import insert_en_registro
from helpers.queries_especiales import insert_en_convocatoria
#Credenciales de la base de datos
db_params={'hostname':'kashin.db.elephantsql.com',
           'username':'rvsmzhyg',
           'password':'k_WJ12u1EYzXngB2uj2LLE9TtzOhd-FB',
           'database':'rvsmzhyg'}

#método para insertar una lista de comandos en la DB

class BackEnd:
    def __init__(self):
        self.params_db = db_params

        # método para hacer una consulta en la base de datos

    def hacer_query(self,query,insert=False):
        conexionDB = None
        resultado = None
        try:
            conexionDB = psycopg2.connect(host=self.params_db['hostname'],
                                          user=self.params_db['username'],
                                          password=self.params_db['password'],
                                          dbname=self.params_db['database'])
            resultado = pd.read_sql_query(query, conexionDB)
            if insert == True:
                conexionDB.commit()
            conexionDB.close()
            return resultado
        except (Exception, psycopg2.DatabaseError) as Error:
            print(Error)
        finally:
            if conexionDB is not None:
                conexionDB.close()
                print("DB Connection closed", "OK")

    def ejecutar_comandos(self,lista_comandos):
        conexionDB = None
        try:
            # vamos a hacer una conexión con la Base de Datos
            conexionDB = psycopg2.connect(host=self.params_db['hostname'],
                                          user=self.params_db['username'],
                                          password=self.params_db['password'],
                                          dbname=self.params_db['database'])
            # vamos a generar un cursor que ejecutará las instrucciones
            cursorDB = conexionDB.cursor()
            print("conexión estabalecida con la base de datos")
            for comando in lista_comandos:
                cursorDB.execute(comando)
            # hacemos cambios permanentes en la base de Datos
            conexionDB.commit()
            # cerramos la conexión con la base de Datos
            conexionDB.close()
        except (Exception, psycopg2.DatabaseError) as Error:
            print("algo salió mal", Error)
        finally:
            if conexionDB is not None:
                conexionDB.close()

    def get_escuelas_grupos_facultades(self,proyecto_id):
        print("Trayendo Escuelas Grupos y Facultades")
        query =query_grps_esc_facs_proy_id.replace('<proy_id>',str(proyecto_id))
        result = self.hacer_query(query)
        facultades = result[['facultad_id','facultad']].drop_duplicates()
        escuelas = result[['escuela_id','escuela']].drop_duplicates()
        grupos = result[['grupo_id','grupo']].drop_duplicates()
        return facultades,escuelas,grupos

    def get_programas_academicos(self,filtro_escuela=None):
        print("trayendo programas académicos y filtrando por escuelas")
        query = "SELECT * FROM programa_academico"
        result = self.hacer_query(query)
        if filtro_escuela is None:
            return result
        else:
            sub_result = result.loc[result['escuela_id'].isin(filtro_escuela)]
            return sub_result

    def get_personas(self):
        print("trayendo toda la lista de personas con tipo")
        query = """SELECT * 
                   FROM persona JOIN persona_tipo 
                     ON persona.persona_id = persona_tipo.persona_id;"""
        result = self.hacer_query(query)
        return result

    def get_clase_producto(self):
        print("trayendo la lista de clase de producto")
        query = """SELECT * FROM clase_producto"""
        result = self.hacer_query(query)
        return result

    def get_tipo_producto(self,nom_clase):
        print("trayendo la lista de tipos de producto con clase",nom_clase)
        query = query_tipos_de_clase.replace("<clase_id>",str(nom_clase))
        result = self.hacer_query(query)
        return result

    def get_personas(self):
        print("tryaendo la lista de personas sin filtros")
        query="SELECT * FROM persona"
        result = self.hacer_query(query)
        return result

    def get_instituciones(self):
        print("trayendo la lista de instituciones")
        query="SELECT * FROM instituciones"
        result = self.hacer_query(query)
        return result

    def get_paises(self):
        print("tryando lista de paises")
        query ="SELECT * FROM pais"
        result = self.hacer_query(query)
        return result

    def agregar_persona(self,persona_id,persona,tipos):
        print("Agregando personas a la DB:",persona,tipos)
        insert_per = insert_persona.replace('<p_id>',str(persona_id))
        insert_per = insert_per.replace('<p>',str(persona))
        inserts = [insert_per]
        for tipo in tipos:
            insert_t = insert_persona_tipo.replace('<p_id>',str(persona_id))
            insert_t = insert_t.replace('<t>',tipo)
            inserts.append(insert_t)
        self.ejecutar_comandos(inserts)

    def agregar_nueva_institucion(self,institucion):
        print("agregando nueva institucion",institucion)
        query = "INSERT INTO instituciones(instituciones) VALUES('<insti>')"
        q = query.replace('<insti>',institucion.upper())
        self.ejecutar_comandos([q])

    def get_lineas_y_areas_de_proyecto(self,proyecto_id):
        print("trayendo las líneas y areas de proyecto",proyecto_id)
        query = query_grupo_linea_area_de_proyecto.replace('<proyecto_id>',str(proyecto_id))
        result = self.hacer_query(query)
        return result

    def get_fechas_proyecto(self,proyecto_id):
        print("trayendo las fechas de proyecto",proyecto_id)
        query = """SELECT fecha_inicio,fecha_cierre 
                     FROM proyecto
                     WHERE proyecto_id = 2;"""

        result = self.hacer_query(query)
        fecha_inicio = result.iloc[0]['fecha_inicio']
        fecha_cierre = result.iloc[0]['fecha_cierre']
        return fecha_inicio, fecha_cierre

    def get_periodo_actual_id(self):
        print("calculando periodo actual")
        mes_actual = datetime.now().month
        periodo = 1
        if mes_actual>6:
            periodo=2
        ano_actual = datetime.now().year
        per_actual = str(ano_actual)+"-"+str(periodo)
        query = """SELECT * 
                   FROM periodo
                   WHERE periodo = '<periodo>';"""
        q = query.replace('<periodo>',per_actual)
        res = self.hacer_query(q)

        periodo_id = res.iloc[0]['periodo_id']
        return periodo_id

    def insertar_en_producto(self,nom_producto,tipo_prod_id):
        print("insertando dentro de producto",nom_producto)
        query = insert_en_producto.replace('<nom_producto>',nom_producto)
        query = query.replace('<tipo_id>',str(tipo_prod_id))
        result = self.hacer_query(query,insert=True)
        nuevo_prod_id = result.iloc[0]['producto_id']
        return nuevo_prod_id

    def insertar_convocatoria(self,convoc_id,fecha_convo):
        print("insertando convocatoria",convoc_id)
        fecha_convo = datetime.strptime(fecha_convo, "%Y-%m-%d").date()
        fecha_convo_corregida = fecha_convo.strftime('%m-%d-%Y')
        buscar_convo_query = """SELECT * FROM convocatoria WHERE convocatoria_id = '<convo_id>';"""
        query_busqueda = buscar_convo_query.replace('<convo_id>',convoc_id)
        result_busqueda = self.hacer_query(query_busqueda)
        query_convo = insert_en_convocatoria.replace('<fecha>', fecha_convo_corregida)
        query_convo = query_convo.replace('<convo_id>', convoc_id)
        if len(result_busqueda)==0:
             return query_convo
        else:
            return None

    def insertar_en_registro(self,prod_id,periodo_id,proy_id,convoc_id,fecha_reg,fecha_convo):
        print("insertando en el registro")
        query_convo = self.insertar_convocatoria(convoc_id,fecha_convo)
        comandos = []
        if query_convo is not None:
            print('agregando convocatoria',query_convo)
            comandos.append(query_convo)
        query_registro = insert_en_registro.replace('<prod_id>',str(prod_id))
        query_registro = query_registro.replace('<perio_id>',str(periodo_id))
        query_registro = query_registro.replace('<proy_id>',str(proy_id))
        query_registro = query_registro.replace('<convo_id>',convoc_id)
        #tenemos que cuadrar la fecha a mano
        fecha_corregida = fecha_reg.strftime('%m-%d-%Y')
        query_registro = query_registro.replace('<fecha>',fecha_corregida)
        comandos.append(query_registro)
        #ahora creamos el comando para asociar producto con proyecto
        query_prod_proyecto = self.asociar_producto_proyecto(prod_id,proy_id)
        comandos.append(query_prod_proyecto)
        self.ejecutar_comandos(comandos)

    def asociar_producto_proyecto(self,producto_id,proyecto_id):
        print("asociando producto y proyecto",producto_id,proyecto_id)
        query = "INSERT INTO producto_proyecto(producto_id,proyecto_id) VALUES (<prod_id>,<proy_id>);"
        query = query.replace('<prod_id>',str(producto_id))
        query = query.replace('<proy_id>',str(proyecto_id))
        return query

    def asociar_producto_personas(self,producto_id,personas_id):
        print("asociando producto y personas", producto_id, personas_id)
        query = """INSERT INTO persona_producto(persona_id,producto_id) VALUES ('<persona_id>',<producto_id>);"""
        query = query.replace('<producto_id>',str(producto_id))
        queries = []
        for p_id in personas_id:
            q = query.replace('<persona_id>',p_id)
            queries.append(q)
        self.ejecutar_comandos(queries)

    def asociar_producto_paises(self,producto_id,paises_id):
        print("asociando producto y paises", producto_id, paises_id)
        query = """INSERT INTO producto_pais(pais_id,producto_id) VALUES (<pais_id>,<producto_id>);"""
        query = query.replace('<producto_id>',str(producto_id))
        queries = []
        for p_id in paises_id:
            q = query.replace('<pais_id>',str(p_id))
            queries.append(q)
        self.ejecutar_comandos(queries)

    def asociar_producto_instituciones(self,producto_id,instituciones_id):
        print("asociando producto e instituciones", producto_id, instituciones_id)
        query = """INSERT INTO producto_instituciones(instituciones_id,producto_id) VALUES (<instituciones_id>,<producto_id>);"""
        query = query.replace('<producto_id>',str(producto_id))
        queries = []
        for p_id in instituciones_id:
            q = query.replace('<instituciones_id>',str(p_id))
            queries.append(q)
        self.ejecutar_comandos(queries)

    def asociar_producto_lineas(self,producto_id,lineas_id):
        print("asociando producto y lineas", producto_id, lineas_id)
        query = """INSERT INTO producto_linea(producto_id, linea_id) VALUES(<producto_id>, <linea_id>);"""
        query = query.replace('<producto_id>',str(producto_id))
        queries = []
        for p_id in lineas_id:
            q = query.replace('<linea_id>',str(p_id))
            queries.append(q)
        self.ejecutar_comandos(queries)

    def asociar_producto_programas(self,producto_id,programas_id):
        print("asociando producto y programas", producto_id, programas_id)
        query = """INSERT INTO producto_programa_academico(producto_id, programa_academico_id) 
                         VALUES(<producto_id>, <programa_id>);"""
        query = query.replace('<producto_id>',str(producto_id))
        queries = []
        for p_id in programas_id:
            q = query.replace('<programa_id>',str(p_id))
            queries.append(q)
        self.ejecutar_comandos(queries)





