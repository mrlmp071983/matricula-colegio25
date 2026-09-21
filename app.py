import os
import zipfile
import io
import pandas as pd
import streamlit as st

# Configuración de la página y diseño estético inicial
st.set_page_config(
    page_title="Matrícula Colegio 25 de Mayo", page_icon="🎓", layout="wide"
)

# Directorio donde se guardarán los archivos subidos por los padres
UPLOAD_DIR = "legajos_documentacion"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

EXCEL_FILE = "inscripciones_colegio25.xlsx"


def cargar_datos():
  if os.path.exists(EXCEL_FILE):
    return pd.read_excel(EXCEL_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "Fecha",
            "Nombre Alumna",
            "DNI Alumna",
            "Año a Cursar",
            "Nombre Tutor",
            "DNI Tutor",
            "Teléfono",
            "Email",
            "Documentación Entregada",
            "Ruta Archivo",
        ]
    )


def guardar_datos(df):
  df.to_excel(EXCEL_FILE, index=False)


# Barra lateral de navegación
st.sidebar.image("logo.png", width=120, use_column_width=False)
st.sidebar.title("Colegio 25 de Mayo")
menu = st.sidebar.selectbox(
    "Menú de Navegación",
    ["Formulario de Matrícula", "Panel de Control (Administrador)"],
)

df_inscripciones = cargar_datos()

if menu == "Formulario de Matrícula":
  st.title("🎓 Formulario de Matrícula - Ciclo Lectivo")
  st.markdown(
      "Complete los datos correspondientes a la alumna y adjunte la"
      " documentación requerida."
  )

  with st.form("form_matricula"):
    st.subheader("1. Datos de la Alumna")
    col1, col2 = st.columns(2)
    with col1:
      nombre_alumna = st.text_input("Apellidos y Nombres de la Alumna")
      dni_alumna = st.text_input("DNI de la Alumna")
    with col2:
      anio_cursar = st.selectbox(
          "Año a Cursar",
          [
              "1° Año",
              "2° Año",
              "3° Año",
              "4° Año",
              "5° Año",
              "6° Año (Orientado)",
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

    st.subheader("3. Documentación Requerida")
    st.markdown(
        "Por favor, adjunte la documentación en formato digital (PDF, Foto de"
        " DNI, Partida de Nacimiento, Ficha Médica, etc.)."
    )
    archivo_subido = st.file_uploader(
        "Subir Archivo de Documentación", type=["pdf", "png", "jpg", "jpeg"]
    )

    enviar = st.form_submit_button("Enviar Matrícula")

    if enviar:
      if not nombre_alumna or not dni_alumna or not telefono:
        st.error(
            "Por favor, complete al menos los campos obligatorios de la"
            " alumna y teléfono."
        )
      else:
        ruta_guardado = ""
        if archivo_subido is not None:
          extension = archivo_subido.name.split(".")[-1]
          nombre_archivo_limpio = (
              f"{dni_alumna}_{nombre_alumna.replace(' ', '_')}.{extension}"
          )
          ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo_limpio)

          with open(ruta_guardado, "wb") as f:
            f.write(archivo_subido.getbuffer())

        # Registrar inscripción
        nueva_fila = pd.DataFrame({
            "Fecha": [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")],
            "Nombre Alumna": [nombre_alumna],
            "DNI Alumna": [dni_alumna],
            "Año a Cursar": [anio_cursar],
            "Nombre Tutor": [nombre_tutor],
            "DNI Tutor": [dni_tutor],
            "Teléfono": [telefono],
            "Email": [email],
            "Documentación Entregada": [
                "Sí (Adjunta)" if archivo_subido else "Pendiente"
            ],
            "Ruta Archivo": [ruta_guardado],
        })

        df_inscripciones = pd.concat(
            [df_inscripciones, nueva_fila], ignore_index=True
        )
        guardar_datos(df_inscripciones)

        st.success(
            "¡Matrícula enviada y registrada correctamente con su"
            " documentación!"
        )

elif menu == "Panel de Control (Administrador)":
  st.title("🔒 Panel de Control - Administración Colegio 25 de Mayo")

  password = st.text_input("Ingrese la clave de administrador", type="password")

  if password == "colegio25":
    st.success("Acceso autorizado")

    st.subheader("Listado de Alumnas Inscriptas")
    if not df_inscripciones.empty:
      st.dataframe(
          df_inscripciones.drop(columns=["Ruta Archivo"], errors="ignore")
      )

      # Sección de Gestión / Eliminación de Inscripciones
      st.markdown("---")
      st.subheader("🗑️ Gestión de Bajas (Eliminar Inscripción)")
      st.markdown(
          "Seleccione una alumna de la lista si desea darla de baja y borrar"
          " todos sus registros y documentos asociados."
      )

      # Creamos opciones legibles para el selector (Nombre + DNI)
      opciones_alumnas = [
          f"{row['Nombre Alumna']} (DNI: {row['DNI Alumna']})"
          for index, row in df_inscripciones.iterrows()
      ]

      alumna_a_eliminar = st.selectbox(
          "Seleccionar Alumna para Eliminar", options=opciones_alumnas
      )

      if st.button("Eliminar Registro de Alumna Seleccionada", type="primary"):
        # Encontrar el índice correspondiente
        indice_seleccionado = opciones_alumnas.index(alumna_a_eliminar)

        # Verificar si tiene un archivo asociado y borrarlo del disco
        ruta_archivo = df_inscripciones.loc[
            indice_seleccionado, "Ruta Archivo"
        ]
        if (
            pd.notna(ruta_archivo)
            and ruta_archivo != ""
            and os.path.exists(ruta_archivo)
        ):
          try:
            os.remove(ruta_archivo)
          except Exception as e:
            st.warning(f"No se pudo eliminar el archivo físico: {e}")

        # Eliminar la fila del DataFrame
        df_inscripciones = df_inscripciones.drop(indice_seleccionado).reset_index(
            drop=True
        )
        guardar_datos(df_inscripciones)

        st.success(
            f"Se ha eliminado correctamente a la alumna y su documentación del"
            f" sistema."
        )
        st.experimental_rerun()  # Actualiza la vista

      # Descargar planilla Excel y Legajos
      st.markdown("---")
      st.markdown("### Descargar Reportes y Documentación")
      col_d1, col_d2 = st.columns(2)

      with col_d1:
        if os.path.exists(EXCEL_FILE):
          with open(EXCEL_FILE, "rb") as f:
            st.download_button(
                label="📊 Descargar Planilla Excel de Inscriptos",
                data=f,
                file_name="inscripciones_colegio_25.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
            )

      with col_d2:
        if os.path.exists(UPLOAD_DIR) and os.listdir(UPLOAD_DIR):
          zip_buffer = io.BytesIO()
          with zipfile.ZipFile(
              zip_buffer, "zip", zipfile.ZIP_DEFLATED
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
              label="📁 Descargar Todos los Legajos (ZIP)",
              data=zip_buffer,
              file_name="legajos_digitales_alumnas.zip",
              mime="application/zip",
          )
        else:
          st.info(
              "Aún no hay archivos de documentación subidos para descargar."
          )

    else:
      st.info("Aún no hay registros de inscripción.")

  elif password != "":
    st.error("Contraseña incorrecta. La clave por defecto es: colegio25")
