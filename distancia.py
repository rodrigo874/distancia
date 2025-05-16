import streamlit as st
import pandas as pd

def calcular_tamanio_silueta_poligono(distancia_simulada, distancia_observacion,
                                     ancho_real=50, alto_real=50,
                                     max_ancho_a4=21, max_alto_a4=29.7):
    """
    Calcula el tamaño de una silueta de polígono de tiro para imprimir en A4.
    (Misma función del código original, sin cambios)
    """
    escala = distancia_observacion / distancia_simulada
    ancho_impresa = ancho_real * escala
    alto_impresa = alto_real * escala
    if alto_impresa > max_alto_a4 or ancho_impresa > max_ancho_a4:
        factor = min(max_alto_a4 / alto_impresa, max_ancho_a4 / ancho_impresa)
        alto_impresa *= factor
        ancho_impresa *= factor
    return ancho_impresa, alto_impresa

# Configuración de la página
st.title("Calculadora de Tamaño de Silueta para A4")
st.write("Calcula el tamaño de una silueta de polígono de tiro para imprimir en A4, simulando distancias mayores.")

# Entrada de datos
distancia_observacion = st.number_input("Distancia desde la hoja A4 (metros, ej. 1):",
                                       min_value=0.01, value=1.0, step=0.1)
distancias_input = st.text_input("Distancias simuladas (metros, separadas por comas, ej. 5,10,15,20,25):",
                                 value="5,10,15,20,25")

# Botón para calcular
if st.button("Calcular"):
    try:
        # Validar distancia de observación
        if distancia_observacion <= 0:
            raise ValueError("La distancia de observación debe ser mayor a 0.")

        # Validar distancias simuladas
        distancias_simuladas = [float(dist.strip()) for dist in distancias_input.split(",")]
        if not distancias_simuladas or any(dist <= 0 for dist in distancias_simuladas):
            raise ValueError("Las distancias simuladas deben ser números mayores a 0.")

        # Calcular resultados
        resultados = []
        for dist in distancias_simuladas:
            ancho, alto = calcular_tamanio_silueta_poligono(dist, distancia_observacion)
            resultados.append({
                "Distancia simulada (m)": dist,
                "Ancho (cm)": round(ancho, 2),
                "Alto (cm)": round(alto, 2)
            })

        # Mostrar resultados en una tabla
        df = pd.DataFrame(resultados)
        st.write("**Tamaños de la silueta para imprimir en A4:**")
        st.dataframe(df, use_container_width=True)

    except ValueError as e:
        st.error(f"Error: {e}. Por favor, ingresa valores válidos.")
