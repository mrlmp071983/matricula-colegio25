import os
import pandas as pd
import streamlit as st

# Configuración de la página y diseño estético inicial
st.set_page_config(
    page_title="Matriculación 2027 - Colegio 25 de Mayo",
    page_icon="🏫",
    layout="wide",
)

# Estilos CSS personalizados para mejorar la estética visual y la paleta de colores
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
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Definición exacta de los cursos
CURSOS = [
    "1° Año A",
    "1° Año B",
    "2° Año A",
    "2° Año B",
    "3° Año A",
    "3° Año B",
    "4° Año A (Naturales)",
    "4° Año B (Sociales)",
    "5° Año A (Naturales)",
    "5° Año B (Sociales)",
    "6° Año A (Naturales)",
    "6° Año B (Sociales)",
]

DB_FILE = "datos_matricula.csv"
PASSWORD_SECRETARIA = "secundaria2027"


def cargar_datos():
  columnas = [
      "Alumna",
      "Curso",
      "DNI_Tutor",
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
  if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    for col in columnas:
      if col not in df.columns:
        df[col] = "No"
    return df
  else:
    return pd.DataFrame(columns=columnas)


df = cargar_datos()

# Menú lateral de navegación con toque institucional
st.sidebar.title("🏫 Colegio 25 de Mayo")
st.sidebar.markdown("---")
modo = st.sidebar.selectbox(
    "Seleccionar Sección:",
    ["Portal de Padres (Inscripción)", "Panel de Control (Secretaría)"],
)

if modo == "Portal de Padres (Inscripción)":
  # Encabezado visual con Logo y Título Institucional actualizado a 2027
  col_logo, col_titulo = st.columns([1, 4])
  with col_logo:
    if os.path.exists("logo.png"):
      st.image("logo.png", width=110)
    else:
      st.write("🏫")  # Ícono de respaldo si falta la imagen
  with col_titulo:
    st.title("COLEGIO 25 DE MAYO")
    st.subheader("Portal de Matriculación - Ciclo Lectivo 2027")

  st.info(
      "Estimada familia: por favor complete los datos de la alumna y cargue"
      " toda la documentación requerida para finalizar la inscripción al"
      " **Ciclo Lectivo 2027**. Ante cualquier duda o consulta, comuníquese con"
      " secretaría a través de:"
      " **secretaria.secundario@colegio25demayo.edu.ar**"
  )

  with st.form("form_matricula"):
    st.markdown("### 1. Datos Generales de la Alumna")
    nombre_alumna = st.text_input(
        "Apellidos y Nombres de la Alumna (Tal como figura en DNI)"
    )
    curso_elegido = st.selectbox(
        "Curso al que ingresa para el Ciclo Lectivo 2027", CURSOS
    )
    dni_tutor = st.text_input(
        "DNI y Apellido del Padre / Madre / Tutor responsable"
    )

    st.markdown("---")
    st.markdown("### 2. Carga de Documentación Obligatoria")
    st.write(
        "Formatos aceptados: PDF, JPG o PNG. Asegúrese de que los archivos sean"
        " legibles."
    )

    col1, col2 = st.columns(2)
    with col1:
      f_matricula = st.file_uploader(
          "Ficha de Matrícula", type=["pdf", "png", "jpg"]
      )
      f_libre_deuda = st.file_uploader(
          "Libre de Deuda", type=["pdf", "png", "jpg"]
      )
      f_pago = st.file_uploader(
          "Comprobante de Pago de Matrícula", type=["pdf", "png", "jpg"]
      )
      f_isa = st.file_uploader("ISA", type=["pdf", "png", "jpg"])
    with col2:
      f_cus = st.file_uploader(
          "CUS (Certificado Único de Salud)", type=["pdf", "png", "jpg"]
      )
      f_imagen = st.file_uploader(
          "Autorización Uso de Imagen", type=["pdf", "png", "jpg"]
      )
      f_acta = st.file_uploader("Acta Compromiso", type=["pdf", "png", "jpg"])
      f_dj = st.file_uploader(
          "Constancia Declaración Jurada (DJ)", type=["pdf", "png", "jpg"]
      )

    st.markdown("---")
    submitted = st.form_submit_button("Enviar Documentación de Matrícula")

    if submitted:
      if nombre_alumna and curso_elegido:
        nombre_limpio = (
            nombre_alumna.strip().replace(" ", "_").replace(",", "")
        )
        curso_carpeta = (
            curso_elegido.replace("°", "")
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )
        ruta_curso = os.path.join("uploads", curso_carpeta)
        os.makedirs(ruta_curso, exist_ok=True)

        archivos_dict = {
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
            ruta_archivo = os.path.join(ruta_curso, nombre_archivo)
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
            "Alumna": nombre_alumna,
            "Curso": curso_elegido,
            "DNI_Tutor": dni_tutor,
            **registro_subidos,
            "Estado": estado_actual,
        }

        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)

        if todos_cargados:
          st.success(
              "¡Inscripción registrada con ÉXITO! Toda la documentación ha sido"
              " recibida y guardada en la carpeta del curso."
          )
        else:
          st.warning(
              "⚠️ Inscripción guardada parcialmente. EL ESTADO QUEDA COMO"
              " INCOMPLETO hasta que se adjunten los documentos faltantes."
          )
      else:
        st.error(
            "Por favor, complete obligatoriamente el Nombre de la Alumna y el"
            " Curso."
        )

else:
  # PANEL DE CONTROL (SECRETARÍA - PROTEGIDO CON CONTRASEÑA)
  st.title("Panel de Control - Secretaría Docente")
  st.write(
      "COLEGIO 25 DE MAYO | Gestión de Matriculación Ciclo Lectivo 2027"
  )

  password_ingresado = st.text_input(
      "Ingrese la contraseña de Secretaría:", type="password"
  )

  if password_ingresado == PASSWORD_SECRETARIA:
    st.success("Acceso concedido.")
    st.markdown("---")
    st.subheader("Seguimiento de Matrículas por Curso")

    if not df.empty:
      total_inscriptas = len(df)
      completos = len(df[df["Estado"].str.contains("Completo")])
      incompletos = len(df[df["Estado"].str.contains("Incompleto")])

      col1, col2, col3 = st.columns(3)
      col1.metric("Total Registradas", total_inscriptas)
      col2.metric("Legajos Completos", completos)
      col3.metric("Legajos Incompletos (Pendientes)", incompletos)

      st.markdown("---")

      curso_filtro = st.selectbox(
          "Filtrar listado por Curso:", ["Todos los cursos"] + CURSOS
      )
      solo_incompletos = st.checkbox(
          "Mostrar únicamente alumnas con DOCUMENTACIÓN INCOMPLETA"
      )

      df_filtrado = df.copy()
      if curso_filtro != "Todos los cursos":
        df_filtrado = df_filtrado[df_filtrado["Curso"] == curso_filtro]

      if solo_incompletos:
        df_filtrado = df_filtrado[
            df_filtrado["Estado"].str.contains("Incompleto")
        ]

      st.dataframe(df_filtrado, use_container_width=True)

      if not df_filtrado.empty:
        st.markdown("### Detalle de Faltantes por Alumna")
        columnas_docs = [
            "Ficha_Matricula",
            "Libre_Deuda",
            "Pago_Matricula",
            "ISA",
            "CUS",
            "Autorizacion_Imagen",
            "Acta_Compromiso",
            "Constancia_DJ",
        ]

        for index, row in df_filtrado.iterrows():
          if "Incompleto" in row["Estado"]:
            faltantes = [
                doc.replace("_", " ")
                for doc in columnas_docs
                if row[doc] == "No"
            ]
            st.error(
                f"**{row['Alumna']}** ({row['Curso']}) - ❌ **Falta subir:**"
                f" {', '.join(faltantes)}"
            )
          else:
            st.success(
                f"**{row['Alumna']}** ({row['Curso']}) - ✅ **Legajo Completo**"
            )

    else:
      st.info("Aún no hay registros de matriculación cargados en el sistema.")

  elif password_ingresado != "":
    st.error("Contraseña incorrecta. Acceso denegado.")
  else:
    st.info("Por favor, ingrese la contraseña para visualizar el panel.")