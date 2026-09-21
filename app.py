import io
import os
import zipfile
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Matrícula Colegio 25 de Mayo - 2027",
    page_icon="🎓",
    layout="wide",
)

# Directorio principal de legajos
UPLOAD_DIR = "legajos_documentacion_2027"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)

EXCEL_FILE = "inscripciones_colegio25_2027.xlsx"


def cargar_datos():
  if os.path.exists(EXCEL_FILE):
    return pd.read_excel(EXCEL_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "Fecha",
            "Nombre Alumna",
            "DNI Alumna",
            "Curso y División",
            "Nombre Tutor",
            "DNI Tutor",
            "Teléfono",
            "Email",
            "Ficha de Matrícula (Adjunto)",
            "Libre de Deuda (Adjunto)",
            "Pago Matrícula (Adjunto)",
            "ISA (Adjunto)",
            "CUS (Adjunto)",
            "Autorización Uso Imagen (Adjunto)",
            "Acta Compromiso y Constancia DJ (Adjunto)",
            "Estado Documentación",
            "Ruta Carpeta Legajo",
        ]
    )


def guardar_datos(df):
  df.to_excel(EXCEL_FILE, index=False)


# Barra lateral
st.sidebar.title("Colegio 25 de Mayo")
st.sidebar.markdown("### Ciclo Lectivo 2027")
st.sidebar.markdown("---")
menu = st.sidebar.selectbox(
    "Menú de Navegación",
    ["Formulario de Matrícula", "Panel de Control (Administrador)"],
)

df_inscripciones = cargar_datos()

if menu == "Formulario de Matrícula":
  st.title("🎓 Formulario de Matrícula - Ciclo Lectivo 2027")
  st.markdown(
      "Complete los datos correspondientes a la alumna y adjunte toda la"
      " documentación obligatoria requerida para formalizar la inscripción."
  )

  with st.form("form_matricula"):
    st.subheader("1. Datos de la Alumna")
    col1, col2 = st.columns(2)
    with col1:
      nombre_alumna = st.text_input("Apellidos y Nombres de la Alumna")
      dni_alumna = st.text_input("DNI de la Alumna")
    with col2:
      # Definición de cursos con divisiones A y B del 1° al 6° año
      curso_division = st.selectbox(
          "Curso y División",
          [
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
          ],
      )

    st.subheader("2. Datos del Tutor / Responsable")
    col3, col4 = st.columns(2)
    with col3:
      nombre_tutor = st.text_input("Apellidos y Nombres del Tutor/a")
      dni_tutor = st.text_input("DNI del Tutor/a")
    with col4:
      telefono = st.text_input("Teléfono de Contacto")
      email = st.text_input("Correo Electrónico")

    st.subheader(
        "3. Documentación Requerida (Archivos en formato PDF o Imagen)"
    )
    st.markdown(
        "Por favor, suba cada uno de los siguientes comprobantes y fichas"
        " obligatorias:"
    )

    f_ficha = st.file_uploader(
        "1. Ficha de Matrícula",
        type=["pdf", "png", "jpg", "jpeg"],
        key="ficha",
    )
    f_libre = st.file_uploader(
        "2. Libre de Deuda", type=["pdf", "png", "jpg", "jpeg"], key="libre"
    )
    f_pago = st.file_uploader(
        "3. Comprobante de Pago de Matrícula",
        type=["pdf", "png", "jpg", "jpeg"],
        key="pago",
    )
    f_isa = st.file_uploader(
        "4. ISA (Informe de Salud del Adolescente / Ficha Médica)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="isa",
    )
    f_cus = st.file_uploader(
        "5. CUS (Certificado Único de Salud)",
        type=["pdf", "png", "jpg", "jpeg"],
        key="cus",
    )
    f_img = st.file_uploader(
        "6. Autorización Uso de Imagen",
        type=["pdf", "png", "jpg", "jpeg"],
        key="img",
    )
    f_acta = st.file_uploader(
        "7. Acta Compromiso y Constancia DJ",
        type=["pdf", "png", "jpg", "jpeg"],
        key="acta",
    )

    enviar = st.form_submit_button("Enviar Matrícula")

    if enviar:
      if not nombre_alumna or not dni_alumna or not telefono:
        st.error(
            "Por favor, complete al menos los campos obligatorios: Apellidos y"
            " Nombres de la Alumna, DNI y Teléfono."
        )
      else:
        # Estructurar la carpeta por curso/división y alumna para el orden en el ZIP
        nombre_carpeta_curso = (
            curso_division.replace("° ", "_")
            .replace(" - ", "_")
            .replace(" ", "_")
        )
        subfolder_curso = os.path.join(UPLOAD_DIR, nombre_carpeta_curso)
        carpeta_alumna = os.path.join(
            subfolder_curso, f"{dni_alumna}_{nombre_alumna.replace(' ', '_')}"
        )

        if not os.path.exists(carpeta_alumna):
          os.makedirs(carpeta_alumna)

        def guardar_archivo(archivo, nombre_base):
          if archivo is not None:
            ext = archivo.name.split(".")[-1]
            path = os.path.join(carpeta_alumna, f"{nombre_base}.{ext}")
            with open(path, "wb") as f:
              f.write(archivo.getbuffer())
            return "Entregado"
          return "Pendiente"

        s_ficha = guardar_archivo(f_ficha, "Ficha_Matricula")
        s_libre = guardar_archivo(f_libre, "Libre_Deuda")
        s_pago = guardar_archivo(f_pago, "Pago_Matricula")
        s_isa = guardar_archivo(f_isa, "ISA")
        s_cus = guardar_archivo(f_cus, "CUS")
        s_img = guardar_archivo(f_img, "Autorizacion_Uso_Imagen")
        s_acta = guardar_archivo(f_acta, "Acta_Compromiso_Constancia_DJ")

        # Verificar si entregó todo
        lista_estados = [s_ficha, s_libre, s_pago, s_isa, s_cus, s_img, s_acta]
        docs_pendientes = lista_estados.count("Pendiente")
        estado_general = (
            "Completo ✅" if docs_pendientes == 0 else "Incompleto ⚠️"
        )

        nueva_fila = pd.DataFrame({
            "Fecha": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")],
            "Nombre Alumna": [nombre_alumna],
            "DNI Alumna": [dni_alumna],
            "Curso y División": [curso_division],
            "Nombre Tutor": [nombre_tutor],
            "DNI Tutor": [dni_tutor],
            "Teléfono": [telefono],
            "Email": [email],
            "Ficha de Matrícula (Adjunto)": [s_ficha],
            "Libre de Deuda (Adjunto)": [s_libre],
            "Pago Matrícula (Adjunto)": [s_pago],
            "ISA (Adjunto)": [s_isa],
            "CUS (Adjunto)": [s_cus],
            "Autorización Uso Imagen (Adjunto)": [s_img],
            "Acta Compromiso y Constancia DJ (Adjunto)": [s_acta],
            "Estado Documentación": [estado_general],
            "Ruta Carpeta Legajo": [carpeta_alumna],
        })

        df_inscripciones = pd.concat(
            [df_inscripciones, nueva_fila], ignore_index=True
        )
        guardar_datos(df_inscripciones)

        st.success(
            "¡Matrícula para el Ciclo Lectivo 2027 enviada y registrada con"
            " éxito!"
        )

elif menu == "Panel de Control (Administrador)":
  st.title("🔒 Panel de Control - Administración Colegio 25 de Mayo")
  password = st.text_input("Ingrese la clave de administrador", type="password")

  if password == "secundaria2027":
    st.success("Acceso autorizado")

    st.subheader("📋 Listado General de Alumnas Inscriptas (Ciclo 2027)")
    if not df_inscripciones.empty:
      total_inscriptas = len(df_inscripciones)
      completas = len(
          df_inscripciones[
              df_inscripciones["Estado Documentación"] == "Completo ✅"
          ]
      )
      incompletas = total_inscriptas - completas

      col_m1, col_m2, col_m3 = st.columns(3)
      col_m1.metric("Total Inscriptas", total_inscriptas)
      col_m2.metric("Documentación Completa ✅", completas)
      col_m3.metric("Documentación Incompleta ⚠️", incompletas)

      st.markdown("---")
      st.dataframe(
          df_inscripciones.drop(columns=["Ruta Carpeta Legajo"], errors="ignore")
      )

      st.markdown("---")
      st.subheader("🗑️ Gestión de Bajas (Eliminar Inscripción)")
      st.markdown(
          "Seleccione una alumna si cambió de institución para borrar todos"
          " sus registros y archivos asociados."
      )

      opciones_alumnas = [
          f"{row['Nombre Alumna']} (DNI: {row['DNI Alumna']}) - {row['Curso y División']}"
          for index, row in df_inscripciones.iterrows()
      ]

      alumna_a_eliminar = st.selectbox(
          "Seleccionar Alumna para Eliminar", options=opciones_alumnas
      )

      if st.button("Eliminar Registro de Alumna Seleccionada", type="primary"):
        indice_seleccionado = opciones_alumnas.index(alumna_a_eliminar)
        ruta_carpeta = df_inscripciones.loc[
            indice_seleccionado, "Ruta Carpeta Legajo"
        ]

        if pd.notna(ruta_carpeta) and os.path.exists(ruta_carpeta):
          try:
            for root, dirs, files in os.walk(ruta_carpeta, topdown=False):
              for file in files:
                os.remove(os.path.join(root, file))
              os.rmdir(root)
          except Exception as e:
            st.warning(f"No se pudo borrar completamente la carpeta: {e}")

        df_inscripciones = df_inscripciones.drop(indice_seleccionado).reset_index(
            drop=True
        )
        guardar_datos(df_inscripciones)
        st.success("Se ha eliminado la alumna y sus legajos correctamente.")
        st.rerun()

      st.markdown("---")
      st.markdown("### 📥 Descargar Reportes y Documentación")
      col_d1, col_d2 = st.columns(2)

      with col_d1:
        if os.path.exists(EXCEL_FILE):
          with open(EXCEL_FILE, "rb") as f:
            st.download_button(
                label="📊 Descargar Planilla Excel (Ciclo 2027)",
                data=f,
                file_name="inscripciones_colegio25_2027.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
            )

      with col_d2:
        if os.path.exists(UPLOAD_DIR) and os.listdir(UPLOAD_DIR):
          zip_buffer = io.BytesIO()
          with zipfile.ZipFile(
              zip_buffer, "w", zipfile.ZIP_DEFLATED
          ) as zip_file:
            for foldername, subfolders, filenames in os.walk(UPLOAD_DIR):
              for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_file.write(
                    file_path,
                    arcname=os.path.relpath(file_path, start=UPLOAD_DIR),
                )
          zip_buffer.seek(0)

          st.download_button(
              label=(
                  "📁 Descargar Todos los Legajos Ordenados por Curso y"
                  " División (ZIP)"
              ),
              data=zip_buffer,
              file_name="legajos_por_cursos_ciclo_2027.zip",
              mime="application/zip",
          )
        else:
          st.info(
              "Aún no hay archivos de documentación subidos para descargar."
          )

    else:
      st.info("Aún no hay registros de inscripción para el ciclo 2027.")

  elif password != "":
    st.error(
        "Contraseña incorrecta. La clave de administrador es: secundaria2027"
    )
