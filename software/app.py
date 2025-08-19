import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import random
import pydeck as pdk
import pandas as pd
import json
from datetime import datetime, timedelta
import pywhatkit as pwk

LIMITES = {
    "cardiaca": {
        "normal": {
            "inicio": 60,
            "fim": 120,
        },
        "anormal": {
            "inicio": 51,
            "fim": 250,
        },
        "irreal": {
            "inicio": float("-inf"),
            "fim": float("inf"),
        },
    },
    "temperatura": {
        "normal": {
            "inicio": 35.5,
            "fim": 37.8,
        },
        "anormal": {
            "inicio": 34.1,
            "fim": 42.5,
        },
        "irreal": {
            "inicio": float("-inf"),
            "fim": float("inf"),
        },
    },
    "oxigenacao": {
        "normal": {
            "inicio": 88,
            "fim": 100,
        },
        "anormal": {
            "inicio": 60,
            "fim": 87,
        },
        "irreal": {
            "inicio": float("-inf"),
            "fim": float("inf"),
        },
    },
}


def enviar_mensagem(numero, mensagem):
    pwk.sendwhatmsg(numero, mensagem, hora, minuto)
    print("Mensagem enviada com sucesso!")


def add_record(
    new_record: dict, filename: str = "dados.json"
) -> None:  # Substitua pelo JSON de destino
    """
    Adiciona um novo registro no arquivo json
    """
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    new_record["horario"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data.append(new_record)

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Funções
def get_categoria(sinal: str, valor: float) -> str:
    """
    Extrai a categoria com base no valor do sinal
    """
    categoria_correta = None
    for categoria, limites in LIMITES.get(sinal).items():
        if limites.get("inicio") <= valor <= limites.get("fim"):
            categoria_correta = categoria
            break
    return categoria_correta


# Verifica se o aplicativo Firebase já foi inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(
        "your-credentialL.json"  # Substitua pelo credencial JSON de destino
    )
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://YOUR-URL-DATABASE.com/"  # Substitua pelo URL de destino
        },
    )

st.sidebar.title("HDS")
opcao = st.sidebar.selectbox(
    "Selecione uma opção",
    ("Início", "Monitoramento em Tempo Real", "Localização", "Monitoramento Geral"),
)

# Exibição do conteúdo com base na opção selecionada
if opcao == "Início":
    st.title("Dashboard HDS")
    st.subheader("Bem-vindo ao dashboard realtime da Hazard Detection System")
    st.write(
        "Uma empresa focada em dar segurança a funcionários que se expõem a riscos à saúde em grandes indústrias."
    )

    # Exibir a imagem com o caminho especificado
    st.image(
        r"c:\Users\imagem.jpeg",  # Substitua pela imagem de destino
        width=650,
    )

elif opcao == "Monitoramento em Tempo Real":
    st.title("Monitoramento de Sinais Vitais")

    pessoa = st.sidebar.selectbox("Selecione a pessoa", ("Henrique", "Bruno"))

    def get_data():
        ref = db.reference()
        data = ref.get()
        return data

    frequencia_cardiaca_box = st.empty()
    oxigenacao_box = st.empty()
    temperatura_corporal_box = st.empty()
    alerta_box = st.empty()

    alerta_ativo = False  # Variável de controle para o alerta

    while True:
        if pessoa == "Henrique":
            data_one = get_data()
            dados = [{"nome": pessoa, **sinais} for pessoa, sinais in data_one.items()]
            add_record(
                [
                    {
                        key: dado[key]
                        for key in ["nome", "cardiaca", "oxigenacao", "temperatura"]
                    }
                    for dado in dados
                ][0]
            )

            sinais_anormais = False

            if data_one:
                # Cardiaca
                categoria = get_categoria(
                    sinal="cardiaca",
                    valor=dados[0]["cardiaca"],
                )

                if categoria == "irreal":
                    print(f"Cardiaca {dados[0]['cardiaca']} - categoria irreal.")
                    pass

                elif categoria == "anormal":
                    frequencia_cardiaca_box.metric(
                        "Frequência Cardíaca (bpm) ❤️", dados[0]["cardiaca"]
                    )
                    sinais_anormais = True

                elif categoria == "normal":
                    frequencia_cardiaca_box.metric(
                        "Frequência Cardíaca (bpm) ❤️", dados[0]["cardiaca"]
                    )
                    alerta_box.empty()

                else:
                    raise ValueError(f"Categoria desconhecida. {categoria}")

                # Oxigenação
                categoria = get_categoria(
                    sinal="oxigenacao",
                    valor=dados[0]["oxigenacao"],
                )

                if categoria == "irreal":
                    print(f"Oxigenacao {dados[0]['oxigenacao']} - categoria irreal.")
                    pass

                elif categoria == "anormal":
                    oxigenacao_box.metric("Oxigenação (%) 🩸", dados[0]["oxigenacao"])
                    sinais_anormais = True

                elif categoria == "normal":
                    oxigenacao_box.metric("Oxigenação (%) 🩸", dados[0]["oxigenacao"])
                    alerta_box.empty()

                else:
                    raise ValueError(f"Categoria desconhecida. {categoria}")

                # Temperatura
                categoria = get_categoria(
                    sinal="temperatura",
                    valor=dados[0]["temperatura"],
                )

                if categoria == "irreal":
                    print(f"Temperatura - categoria irreal.")
                    pass

                elif categoria == "anormal":
                    temperatura_corporal_box.metric(
                        "Temperatura Corporal (°C) 🌡️", dados[0]["temperatura"]
                    )
                    sinais_anormais = True

                elif categoria == "normal":
                    temperatura_corporal_box.metric(
                        "Temperatura Corporal (°C) 🌡️", dados[0]["temperatura"]
                    )
                    alerta_box.empty()

                else:
                    raise ValueError(f"Categoria desconhecida. {categoria}")

            if sinais_anormais:
                alerta_box.error("Alerta: Sinais vitais fora da normalidade!")

            # Verifica o botão de pânico
            ref_botton = db.reference("/henrique/botton")
            botton_status = ref_botton.get()

            if botton_status:
                if not alerta_ativo:  # Se o alerta ainda não foi exibido
                    st.warning(" Henrique está em uma emergência! 🚨")
                    alerta_ativo = True
                # Reseta o botão para evitar múltiplos pop-ups
                ref_botton.set(False)

                now = datetime.now()
                future_time = now + timedelta(minutes=1)
                hora = future_time.hour
                minuto = future_time.minute
                numero_destino = "+5511999999999"  # Substitua pelo número de destino
                mensagem_envio = "_*Alerta!* Henrique em situação de risco_"
                enviar_mensagem(numero_destino, mensagem_envio)
            else:
                alerta_ativo = False  # Reseta a variável de controle
        elif pessoa == "Bruno":
            frequencia_cardiaca = random.randint(60, 100)
            oxigenacao = random.uniform(95, 100)
            temperatura_corporal = random.uniform(36, 37.5)

            frequencia_cardiaca_box.metric(
                "Frequência Cardíaca (bpm) ❤️", frequencia_cardiaca
            )
            oxigenacao_box.metric("Oxigenação (%) 🩸", round(oxigenacao, 2))
            temperatura_corporal_box.metric(
                "Temperatura Corporal (°C) 🌡️", round(temperatura_corporal, 2)
            )

        time.sleep(2)

elif opcao == "Localização":
    # Função para obter latitude e longitude do Firebase e converter para float
    def get_location():
        lat_ref = db.reference("/henrique/lat")
        lng_ref = db.reference("/henrique/lng")

        latitude_str = lat_ref.get()
        longitude_str = lng_ref.get()

        try:
            latitude = float(latitude_str)
            longitude = float(longitude_str)
        except (ValueError, TypeError):
            latitude = None
            longitude = None

        return latitude, longitude

    # Obter a localização do Firebase
    latitude, longitude = get_location()

    # Verificar se a localização foi obtida corretamente
    if latitude is None or longitude is None:
        st.error("Não foi possível obter os dados de localização do Firebase.")
    else:
        st.title("Localização Precisa do Usuário")

        # Criar um DataFrame com as coordenadas
        data = pd.DataFrame({"lat": [latitude], "lon": [longitude]})

        # Exibir o mapa com o menor ponto possível
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v10",
                initial_view_state=pdk.ViewState(
                    latitude=latitude,
                    longitude=longitude,
                    zoom=18,  # Zoom elevado para maior precisão
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=data,
                        get_position="[lon, lat]",
                        get_color="[0, 0, 255, 160]",  # Cor azul
                        get_radius=1,  # Menor tamanho possível
                    ),
                ],
            )
        )

elif opcao == "Monitoramento Geral":
    st.title("Monitoramento Geral")

    # Função para obter dados do Firebase
    def get_data():
        ref = db.reference()
        data = ref.get()
        return data

    def exibir_dados(pessoa):
        frequencia_cardiaca_box = st.empty()
        oxigenacao_box = st.empty()
        temperatura_corporal_box = st.empty()
        alerta_box = st.empty()

        if pessoa == "Henrique":
            data_one = get_data()
            dados = [{"nome": pessoa, **sinais} for pessoa, sinais in data_one.items()]

            sinais_anormais = False

            if data_one:
                categoria = get_categoria("cardiaca", dados[0]["cardiaca"])
                frequencia_cardiaca_box.metric(
                    f"Frequência Cardíaca ({pessoa}) ❤️", dados[0]["cardiaca"]
                )

                categoria = get_categoria("oxigenacao", dados[0]["oxigenacao"])
                oxigenacao_box.metric(
                    f"Oxigenação ({pessoa}) 🩸", dados[0]["oxigenacao"]
                )

                categoria = get_categoria("temperatura", dados[0]["temperatura"])
                temperatura_corporal_box.metric(
                    f"Temperatura Corporal ({pessoa}) 🌡️", dados[0]["temperatura"]
                )

                if sinais_anormais:
                    alerta_box.error(
                        f"Alerta: {pessoa} com sinais vitais fora da normalidade!"
                    )

        elif pessoa == "Bruno":
            frequencia_cardiaca = random.randint(60, 100)
            oxigenacao = random.uniform(95, 100)
            temperatura_corporal = random.uniform(36, 37.5)

            frequencia_cardiaca_box.metric(
                f"Frequência Cardíaca ({pessoa}) ❤️", frequencia_cardiaca
            )
            oxigenacao_box.metric(f"Oxigenação ({pessoa}) 🩸", round(oxigenacao, 2))
            temperatura_corporal_box.metric(
                f"Temperatura Corporal ({pessoa}) 🌡️", round(temperatura_corporal, 2)
            )

    # Exibir os dados de Henrique e Bruno lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Henrique")
        exibir_dados("Henrique")

    with col2:
        st.subheader("Bruno")
        exibir_dados("Bruno")
