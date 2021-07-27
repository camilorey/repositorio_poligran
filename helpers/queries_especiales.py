query_grps_esc_facs_proy_id = """SELECT grupo.grupo_id,
                                        grupo.grupo,
                                        escuela.escuela_id,
                                        escuela.escuela,
                                        facultad.facultad_id,
                                        facultad.facultad
                                FROM proyecto_grupo JOIN grupo_escuela ON proyecto_grupo.grupo_id = grupo_escuela.grupo_id
                                                    JOIN escuela ON grupo_escuela.escuela_id = escuela.escuela_id
                                                    JOIN facultad ON escuela.facultad_id = facultad.facultad_id
                                                    JOIN grupo ON proyecto_grupo.grupo_id = grupo.grupo_id
                                WHERE proyecto_grupo.proyecto_id=<proy_id>"""

query_tipos_de_clase = """SELECT tipo_producto.tipo_producto_id,
                                 tipo_producto.tipo_producto 
FROM clase_tipo_producto JOIN tipo_producto ON clase_tipo_producto.tipo_producto_id = tipo_producto.tipo_producto_id
WHERE clase_tipo_producto.clase_producto_id = <clase_id>;"""

insert_persona = """INSERT INTO persona(persona_id,persona) VALUES('<p_id>','<p>');"""
insert_persona_tipo = """INSERT INTO persona_tipo(persona_id,tipo) VALUES('<p_id>','<t>');"""

query_grupo_linea_area_de_proyecto = """SELECT grupo_linea_area.grupo_linea_area_id,
                                               area.area_id,
                                               area.area,
                                               linea.linea_id,
                                               linea.linea 
                                        FROM proyecto_grupo JOIN grupo_linea_area ON proyecto_grupo.grupo_id = grupo_linea_area.grupo_id
                                                            JOIN area ON grupo_linea_area.area_id = area.area_id
                                                            JOIN linea ON grupo_linea_area.linea_id = linea.linea_id
                                        WHERE proyecto_id = <proyecto_id>;"""

query_linea_area_todos = """SELECT grupo_linea_area.grupo_linea_area_id,
                                   area.area_id,
                                   area.area,
                                   linea.linea_id,
                                   linea.linea 
                            FROM proyecto_grupo JOIN grupo_linea_area ON proyecto_grupo.grupo_id = grupo_linea_area.grupo_id
                                                JOIN area ON grupo_linea_area.area_id = area.area_id
                                                JOIN linea ON grupo_linea_area.linea_id = linea.linea_id;"""

insert_en_producto = """INSERT INTO producto(producto,clase_tipo_producto_id) 
                        VALUES ('<nom_producto>',<tipo_id>) 
                        RETURNING producto_id;"""


#recordar pasar la fecha a MM-DD-YYYY
insert_en_convocatoria = """INSERT INTO convocatoria(convocatoria_id,tipo_convocatoria_id,fecha_convocatoria) 
                            VALUES ('<convo_id>',1,'<fecha>');"""

insert_en_registro = """INSERT INTO registro_producto(producto_id,periodo_id,proyecto_id,convocatoria_id,fecha_registro) 
                        VALUES (<prod_id>,<perio_id>,<proy_id>,'<convo_id>','<fecha>');"""
