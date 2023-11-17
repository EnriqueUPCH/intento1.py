import streamlit as st
import pandas as pd
import gdown
import plotly.express as px

st.set_page_config(page_title="Trabajo", page_icon=":bar_chart:")

@st.experimental_memo
def download_img():
    url = "https://drive.google.com/uc?id=103SAhh3PcJQpdyhJN6cCExZ1ydObhMcZ"
    output = 'imagen.png'
    gdown.download(url, output, quiet=False)

@st.experimental_memo
def download_data1():
    url = "https://drive.google.com/uc?id=1zL1z4QvIrNbyyzA6tVQPFjNw4A199p3k"
    output = 'comps/ANP.csv'
    gdown.download(url, output, quiet=False)

@st.experimental_memo
def download_dataInei():
    url = "https://drive.google.com/uc?id=1qpFTkksCq6ZiyJLODBmWxLaS8EM0RihP"
    output = 'TB_UBIGEOS.csv'
    gdown.download(url, output, quiet=False)

download_img()
download_data1()
download_dataInei()

st.title("Áreas Naturales Protegidas (ANP)")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Objetivo")
        st.write(
            """
            Crear una página web para difundir 
            información clave sobre Áreas Naturales Protegidas, fomentando 
            la conciencia ambiental y la conservación de la biodiversidad.
            """
        )
    with right_column:
        imagen_url = 'imagen.png'  
        st.image(imagen_url, use_column_width=True)

st.write("----")
st.write("*- A continuación se muestra la tabla general de las ANP con sus datos respectivos*")
st.subheader("Tabla General")
data = pd.read_csv("comps/ANP.csv", sep=";", encoding="utf-8")
inei=pd.read_csv("comps/Inei.csv", sep=",", encoding="utf-8")
x = data.set_index("ANP_NOMB")
sinRepe = x.dropna(how='all')

st.dataframe(sinRepe)
st.info("[Información de la tabla](https://www.datosabiertos.gob.pe/dataset/%C3%A1reas-naturales-protegidas-anp-de-administraci%C3%B3n-nacional-definitiva)")

cont_ANP = x["ANP_CATE"].value_counts()
repe = (cont_ANP / len(x)) * 100

fig = px.pie(
    names=repe.index,
    values=repe.values,
    title="Porcentaje de las ANP",
)
st.plotly_chart(fig)

st.write("---")

st.write("""
	A continuación se visualiza la cantidad de ANP organizadas por departamento
	""")
depa = data["DEPARTAMENTO1"].dropna().unique()
depaT = depa.tolist()
depaT.append("TODOS")

estado = st.selectbox("Selecciona un departamento:", depaT)

if estado == "TODOS":
    st.dataframe(sinRepe)
    todosSel = sinRepe["UBIGEO1"]
    mapa1 = inei[inei["ubigeo_inei"].isin(todosSel)]
    st.dataframe(mapa1)
    nuevo_mapa = mapa1[["latitud", "longitud"]].copy()
    nuevo_mapa = nuevo_mapa.rename(columns={"latitud": "LAT", "longitud": "LON"})
    nuevo_mapaT = nuevo_mapa.dropna(subset=["LAT", "LON"])

    st.map(nuevo_mapaT)
else:
    tablaDep = sinRepe[sinRepe["DEPARTAMENTO1"] == estado] 
    st.dataframe(tablaDep)
    cont = tablaDep["ANP_CATE"].value_counts()
    repi = (cont / len(x)) * 100

    fig_dep = px.pie(
        names=repi.index,
        values=repi.values,
        title="ANP por departamento",
    )
    st.plotly_chart(fig_dep)

    mapa1 = inei[inei["ubigeo_inei"].isin(sinRepe[sinRepe["DEPARTAMENTO1"]== estado]["UBIGEO1"])]
    st.dataframe(mapa1)
    nuevo_mapa = mapa1[["latitud", "longitud"]].copy()
    nuevo_mapa = nuevo_mapa.rename(columns={"latitud": "LAT", "longitud": "LON"})

    st.map(nuevo_mapa)

    st.write("---")
st.subheader("Integrantes")


st.write("----")
st.write("Para ver mas el codigo de la pagina puede entrar al siguiente enlace:")
st.info("[Repositorio de Github](https://github.com/)")