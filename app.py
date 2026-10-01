import io
import os
import shutil
import zipfile
import pandas as pd
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Matriculación 2027 - Colegio 25 de Mayo",
    page_icon="🏫",
    layout="wide",
)

# Estilos CSS personalizados
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #1b365d;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #2c4d7e;
        color: white;
    }
    h1, h2, h3 {
        color: #1b365d;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Definición de opciones por Nivel con sus respectivas divisiones A y B
SALAS_INICIAL = [
    "Sala de 3 Años - División A",
    "Sala de 3 Años - División B",
    "Sala de 4 Años - División A",
    "Sala de 4 Años - División B",
    "Sala de 5 Años - División A",
    "Sala de 5 Años - División B",
]

GRADOS_PRIMARIA = [
    "1° Grado - División A",
    "1° Grado - División B",
    "2° Grado - División A",
    "2° Grado - División B",
    "3° Grado - División A",
    "3° Grado - División B",
    "4° Grado - División A",
    "4° Grado - División B",
    "5° Grado - División A",
    "5° Grado - División B",
    "6° Grado - División A",
    "6° Grado - División B",
]

CURSOS_SECUNDARIA = [
    "1° Año - División A",
    "1° Año - División B",
    "2° Año - División A",
    "2° Año - División B",
    "3° Año - División A",
    "3° Año - División B",
    "4° Año - División A",
    "4° Año - División B",
    "5° Año - División A",
    "5° Año - División B",
    "6° Año - División A",
    "6° Año - División B",
]

DB_EXCEL = "inscripciones_colegio25_2027.xlsx"
UPLOAD_DIR = "uploads_legajos_2027"

# Contraseñas de administración por nivel
PASS_INICIAL = "inicial2027"
PASS_PRIMARIA = "primaria2027"
PASS_SECUNDARIA = "secundaria2027"


def cargar_datos():
  columnas = [
      "Nivel",
      "Estudiante",
      "Sala_Grado_Curso",
      "DNI_Tutor",
      "Partida_Nacimiento",
      "Documento_DNI",
      "Ficha_Matricula",
      "Libre_Deuda",
      "Pago_Matricula",
      "ISA",
      "CUS",
      "Autorizacion_Imagen",
      "Acta_Compromiso",
      "Constancia_DJ",
      "Estado",
  ]
  if os.path.exists(DB_EXCEL):
    try:
      df = pd.read_excel(DB_EXCEL)
      for col in columnas:
        if col not in df.columns:
          df[col] = "No"
      return df
    except Exception:
      return pd.DataFrame(columns=columnas)
  else:
    return pd.DataFrame(columns=columnas)


def guardar_datos(df):
  df.to_excel(DB_EXCEL, index=False)


df_inscripciones = cargar_datos()

# Menú lateral de navegación
st.sidebar.title("🏫 Colegio 25 de Mayo")
if os.path.exists("logo.png"):
  st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
modo = st.sidebar.selectbox(
    "Seleccionar Sección:",
    [
        "Portal de Familias (Inscripción)",
        "Panel Nivel Inicial",
        "Panel Nivel Primario",
        "Panel Nivel Secundario",
    ],
)

if modo == "Portal de Familias (Inscripción)":
  col_logo, col_titulo = st.columns([1, 4])
  with col_logo:
    if os.path.exists("logo.png"):
      st.image("logo.png", width=110)
    else:
      st.write("🏫")
  with col_titulo:
    st.title("COLEGIO 25 DE MAYO")
    st.subheader("Portal de Matriculación Unificado - Ciclo Lectivo 2027")

  st.info(
      "Estimada familia: por favor complete los datos del alumno/a, seleccione"
      " el nivel educativo, la opción correspondiente y adjunte la"
      " documentación obligatoria solicitada para el **Ciclo Lectivo 2027**."
  )

  with st.form("form_matricula"):
    st.markdown("### 1. Datos Generales")
    nombre_estudiante = st.text_input(
        "Apellidos y Nombres del Estudiante (Tal como figura en DNI)"
    )

    nivel_elegido = st.selectbox(
        "Seleccione el Nivel Educativo",
        ["Nivel Inicial", "Nivel Primario", "Nivel Secundario"],
        key="select_nivel_educativo",
    )

    # CORRECCIÓN DEFINITIVA CON KEYS ÚNICOS Y ETIQUETAS DINÁMICAS ADECUADAS
    if nivel_elegido == "Nivel Inicial":
      sala_grado_curso = st.selectbox(
          "Sala / División", SALAS_INICIAL, key="select_sala_inicial"
      )
    elif nivel_elegido == "Nivel Primario":
      sala_grado_curso = st.selectbox(
          "Grado / División", GRADOS_PRIMARIA, key="select_grado_primaria"
      )
    else:
      sala_grado_curso = st.selectbox(
          "Curso / División", CURSOS_SECUNDARIA, key="select_curso_secundaria"
      )

    dni_tutor = st.text_input(
        "DNI y Apellido del Padre / Madre / Tutor responsable"
    )

    st.markdown("---")
    st.markdown("### 2. Carga de Documentación Obligatoria")
    st.write(
        "Formatos aceptados: PDF, JPG o PNG. Asegúrese de que los archivos sean"
        " claros y legibles."
    )

    col1, col2 = st.columns(2)
    with col1:
      f_partida = st.file_uploader(
          "Partida de Nacimiento",
          type=["pdf", "png", "jpg"],
          key="up_partida",
      )
      f_dni_doc = st.file_uploader(
          "Documento (DNI)", type=["pdf", "png", "jpg"], key="up_dni"
      )
      f_matricula = st.file_uploader(
          "Ficha de Matrícula", type=["pdf", "png", "jpg"], key="up_ficha"
      )
      f_libre_deuda = st.file_uploader(
          "Libre de Deuda", type=["pdf", "png", "jpg"], key="up_libre"
      )
      f_pago = st.file_uploader(
          "Comprobante de Pago de Matrícula",
          type=["pdf", "png", "jpg"],
          key="up_pago",
      )
    with col2:
      f_isa = st.file_uploader("ISA", type=["pdf", "png", "jpg"], key="up_isa")
      f_cus = st.file_uploader(
          "CUS (Certificado Único de Salud)",
          type=["pdf", "png", "jpg"],
          key="up_cus",
      )
      f_imagen = st.file_uploader(
          "Autorización Uso de Imagen",
          type=["pdf", "png", "jpg"],
          key="up_imagen",
      )
      f_acta = st.file_uploader(
          "Acta Compromiso", type=["pdf", "png", "jpg"], key="up_acta"
      )
      f_dj = st.file_uploader(
          "Constancia Declaración Jurada (DJ)",
          type=["pdf", "png", "jpg"],
          key="up_dj",
      )

    st.markdown("---")
    submitted = st.form_submit_button("Enviar Documentación de Matrícula")

    if submitted:
      if nombre_estudiante and sala_grado_curso:
        nombre_limpio = (
            nombre_estudiante.strip().replace(" ", "_").replace(",", "")
        )
        carpeta_nivel = nivel_elegido.lower().replace(" ", "_")
        carpeta_opcion = (
            sala_grado_curso.replace("°", "")
            .replace("°", "")
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )
        ruta_carpeta = os.path.join(UPLOAD_DIR, carpeta_nivel, carpeta_opcion)
        os.makedirs(ruta_carpeta, exist_ok=True)

        archivos_dict = {
            "Partida_Nacimiento": f_partida,
            "Documento_DNI": f_dni_doc,
            "Ficha_Matricula": f_matricula,
            "Libre_Deuda": f_libre_deuda,
            "Pago_Matricula": f_pago,
            "ISA": f_isa,
            "CUS": f_cus,
            "Autorizacion_Imagen": f_imagen,
            "Acta_Compromiso": f_acta,
            "Constancia_DJ": f_dj,
        }

        registro_subidos = {}
        todos_cargados = True

        for key, archivo in archivos_dict.items():
          if archivo is not None:
            extension = archivo.name.split(".")[-1]
            nombre_archivo = f"{nombre_limpio}_{key}.{extension}"
            ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_archivo, "wb") as f:
              f.write(archivo.getbuffer())
            registro_subidos[key] = "Sí"
          else:
            registro_subidos[key] = "No"
            todos_cargados = False

        estado_actual = (
            "✅ Completo"
            if todos_cargados
            else "⚠️ Incompleto - Falta Documentación"
        )

        nuevo_registro = {
            "Nivel": nivel_elegido,
            "Estudiante": nombre_estudiante,
            "Sala_Grado_Curso": sala_grado_curso,
            "DNI_Tutor": dni_tutor,
            **registro_subidos,
            "Estado": estado_actual,
        }

        df_inscripciones = pd.concat(
            [df_inscripciones, pd.DataFrame([nuevo_registro])],
            ignore_index=True,
        )
        guardar_datos(df_inscripciones)

        if todos_cargados:
          st.success(
              "¡Inscripción registrada con ÉXITO! Toda la documentación ha sido"
              " recibida correctamente."
          )
        else:
          st.warning(
              "⚠️ Inscripción guardada parcialmente. EL ESTADO QUEDA COMO"
              " INCOMPLETO hasta adjuntar lo faltante."
          )
      else:
        st.error(
            "Por favor, complete obligatoriamente el Nombre del Estudiante y"
            " la opción correspondiente."
        )

else:
  # CONFIGURACIÓN DE PANELES DE CONTROL ADMINISTRATIVOS INDIVIDUALIZADOS
  if modo == "Panel Nivel Inicial":
    titulo_panel = "🔒 Panel de Control - Nivel Inicial"
    sub_titulo = "Gestión de Matrículas (Salas de 3, 4 y 5 años)"
    password_correcto = PASS_INICIAL
    filtro_nivel = "Nivel Inicial"
    prefijo_archivo = "nivel_inicial"
    sub_opciones = SALAS_INICIAL

  elif modo == "Panel Nivel Primario":
    titulo_panel = "🔒 Panel de Control - Nivel Primario"
    sub_titulo = "Gestión de Matrículas (1° a 6° Grado)"
    password_correcto = PASS_PRIMARIA
    filtro_nivel = "Nivel Primario"
    prefijo_archivo = "nivel_primario"
    sub_opciones = GRADOS_PRIMARIA

  else:
    titulo_panel = "🔒 Panel de Control - Nivel Secundario"
    sub_titulo = "Gestión de Matrículas (1° a 6° Año)"
    password_correcto = PASS_SECUNDARIA
    filtro_nivel = "Nivel Secundario"
    prefijo_archivo = "nivel_secundario"
    sub_opciones = CURSOS_SECUNDARIA

  st.title(titulo_panel)
  st.write(sub_titulo)

  password = st.text_input(
      f"Ingrese la contraseña de administración ({filtro_nivel}):",
      type="password",
      key=f"pass_{prefijo_archivo}",
  )

  if password == password_correcto:
    st.success(f"Acceso concedido al {filtro_nivel}.")
    st.markdown("---")

    # Filtrar estrictamente los datos correspondientes al nivel del administrador
    df_nivel = df_inscripciones[
        df_inscripciones["Nivel"] == filtro_nivel
    ].copy()

    if not df_nivel.empty:
      total_inscriptas = len(df_nivel)
      completos = len(df_nivel[df_nivel["Estado"].str.contains("Completo")])
      incompletos = total_inscriptas - completos

      col1, col2, col3 = st.columns(3)
      col1.metric("Total Registrados", total_inscriptas)
      col2.metric("Legajos Completos", completos)
      col3.metric("Legajos Incompletos", incompletos)

      st.markdown("---")

      # Filtro interno por sección
      selector_seccion = st.selectbox(
          "Filtrar por sección específica:",
          ["Todas"] + sub_opciones,
          key=f"filtro_seccion_{prefijo_archivo}",
      )
      if selector_seccion != "Todas":
        df_nivel = df_nivel[df_nivel["Sala_Grado_Curso"] == selector_seccion]

      st.dataframe(df_nivel, use_container_width=True)

      st.markdown("---")
      st.markdown("### ⚙️ Gestión y Eliminación de Registros")
      nombres_alumnos = df_nivel["Estudiante"].tolist()
      alumna_a_borrar = st.selectbox(
          "Seleccione un estudiante para eliminar su registro si es necesario:",
          ["Seleccione..."] + nombres_alumnos,
          key=f"del_{prefijo_archivo}",
      )

      if alumna_a_borrar != "Seleccione...":
        if st.button(
            "Eliminar Registro Seleccionado",
            key=f"btn_del_{prefijo_archivo}",
        ):
          indice_real = df_nivel[
              df_nivel["Estudiante"] == alumna_a_borrar
          ].index[0]
          nombre_limpio = (
              alumna_a_borrar.strip().replace(" ", "_").replace(",", "")
          )

          for foldername, subfolders, filenames in os.walk(UPLOAD_DIR):
            for filename in filenames:
              if filename.startswith(nombre_limpio):
                try:
                  os.remove(os.path.join(foldername, filename))
                except Exception as e:
                  st.warning(f"No se pudo borrar el archivo físico: {e}")

          df_inscripciones = df_inscripciones.drop(indice_real).reset_index(
              drop=True
          )
          guardar_datos(df_inscripciones)
          st.success(
              f"Se ha eliminado a {alumna_a_borrar} y sus legajos"
              " correctamente."
          )
          st.rerun()

      st.markdown("---")
      st.markdown(f"### 📥 Descargar Reportes ({filtro_nivel})")
      col_d1, col_d2 = st.columns(2)

      with col_d1:
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer:
          df_nivel.to_excel(writer, index=False, sheet_name=filtro_nivel)
        buffer_excel.seek(0)

        st.download_button(
            label=f"📊 Descargar Planilla Excel ({filtro_nivel})",
            data=buffer_excel,
            file_name=f"inscripciones_{prefijo_archivo}_2027.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
            key=f"dl_excel_{prefijo_archivo}",
        )

      with col_d2:
        path_nivel_dir = os.path.join(
            UPLOAD_DIR, filtro_nivel.lower().replace(" ", "_")
        )
        if os.path.exists(path_nivel_dir) and os.listdir(path_nivel_dir):
          zip_buffer = io.BytesIO()
          with zipfile.ZipFile(
              zip_buffer, "w", zipfile.ZIP_DEFLATED
          ) as zip_file:
            for foldername, subfolders, filenames in os.walk(path_nivel_dir):
              for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_file.write(
                    file_path,
                    arcname=os.path.relpath(file_path, start=path_nivel_dir),
                )
          zip_buffer.seek(0)

          st.download_button(
              label=(
                  f"📁 Descargar Legajos de {filtro_nivel} Ordenados (ZIP)"
              ),
              data=zip_buffer,
              file_name=f"legajos_{prefijo_archivo}_2027.zip",
              mime="application/zip",
              key=f"dl_zip_{prefijo_archivo}",
          )
        else:
          st.info(
              "Aún no hay archivos de documentación subidos en este nivel para"
              " descargar."
          )

    else:
      st.info(f"Aún no hay registros de inscripción para el {filtro_nivel}.")

  elif password != "":
    st.error(
        f"Contraseña incorrecta. La clave de administración para {filtro_nivel}"
        f" es: {password_correcto}"
    )
