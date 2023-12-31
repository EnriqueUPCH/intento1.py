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

st.title("Áreas Naturales Protegidas (ANP) ")

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
data = pd.read_csv("comps/ANP.csv", sep=";", encoding="utf-8").dropna(how='all')
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
st.write("----")
st.write("""
    Seleccione la ANP que desea ver por departamento
	""")
opti= st.multiselect(
    "Seleccione para ver cuantas ANP tiene cada departamento", 
    options= sinRepe["ANP_CATE"].unique()
    )
    
nombre= sinRepe[sinRepe["ANP_CATE"].isin(opti)]
st.dataframe(nombre)
contN= nombre["DEPARTAMENTO1"].value_counts().sort_values(ascending=False)
contN_sorted = pd.DataFrame({'Departamento': contN.index, 'Cantidad': contN.values}).sort_values(by='Cantidad', ascending=False)

st.subheader("Departamentos que cuentan con la ANP seleccionada")

fig = px.bar(
    contN_sorted,
    x='Departamento',
    y='Cantidad',
    title="Cantidad de ANP por Departamento",
)
fig.update_layout(xaxis_categoryorder='total ascending')
st.plotly_chart(fig)


st.write("---")

opti2 = st.multiselect(
    "Seleccione para ver el área de cada ANP", 
    options=data["ANP_NOMB"].unique()
)

are = data[data["ANP_NOMB"].isin(opti2)]

are_sorted = are.sort_values(by="ANP_SULEG", ascending=False)

fig = px.bar(are_sorted, x="ANP_NOMB", y="ANP_SULEG", title="Área de ANP", text="ANP_SULEG")
fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
fig.update_layout(xaxis_categoryorder='total ascending',xaxis_title="Nombre", yaxis_title="Area")

st.plotly_chart(fig)

st.write("---")

st.write("""
	A continuación se visualiza el area de cada ANP
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
    nuevo_mapa = nuevo_mapa.rename(columns={"latitud": "latitude", "longitud": "longitude"})
    nuevo_mapaT = nuevo_mapa.dropna(subset=["latitude", "longitude"])
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
    nuevo_mapa = mapa1[["latitud", "longitud"]].copy()
    nuevo_mapa = nuevo_mapa.rename(columns={"latitud": "latitude", "longitud": "longitude"})
    nuevo_mapa = nuevo_mapa.dropna(subset=["latitude", "longitude"])

    st.map(nuevo_mapa)

    

    st.write("---")
st.subheader("Integrantes")

st.write("Jordan Andres Nieves Sulca")
st.write("Adim Gomez Rodrigez")
st.write("Lila Zarai Huanca Ampuero")
st.write("Slim Aspur Mendoza")
st.write("Jeferson Rojas Burgos")

st.write("----")
st.write("Para ver mas el codigo de la pagina puede entrar al siguiente enlace:")
st.info("[Repositorio de Github](https://github.com/)")
