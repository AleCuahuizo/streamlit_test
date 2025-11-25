import streamlit as st
import pandas as pd
import scipy.stats
import time

# Variables de estado que se conservan cuando Streamlit vuelve a ejecutar este script

if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

# ----- Interfaz de encabezado ------
st.header("Lanzar una moneda")

# Crear un gráfico de la línea inicial
chart = st.line_chart([0.5])

# ----- Función principal -----
# Lanza una moneda n veces
# Ve actualizando la media acumulada y agregando puntos al gráfico
# Devuelve la media final (proporción de 1's)


def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0  # Contador de intentos
    outcome_1_count = 0  # Contador de 1's (caras)

    # Recorremos cada resultado y actualizamos la media
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count/outcome_no
        chart.add_rows([mean])  # Agrega la media al nuevo gráfico
        time.sleep(0.05)  # Pausa para que la animación sea visible
    return mean

# ------ Widges -----


# Slider para elegir el número de intentos (1,...,100), valor por defecto = 10
number_of_trials = st.slider('¿Número de intentos?', 1, 100, 10)

# Botón que devuelve TRUE solo en la ejecución en que el usuario lo presionó
start_button = st.button('Ejecutar')

# ----- Lógica activada por el botón -----

if start_button:
    # Mensaje informativo
    st.write(f'Experimento con {number_of_trials} intentos en curso')

    # Incrementamos el contador de experimentos (variable de estado)
    st.session_state['experiment_no'] += 1

    # Ejecutamos la simulación (actualizar la gráfica)
    mean = toss_coin(number_of_trials)

    # Construimos un DataFrame con los resultados del experimento actual
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
    ],
        axis=0)

    # Reindexamos
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(
        drop=True)

    # ----- Mostrar resultados acumulados -----
    st.write(st.session_state['df_experiment_results'])
