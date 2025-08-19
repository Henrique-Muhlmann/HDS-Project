import pandas as pd
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# Função para carregar dados do arquivo JSON
def load_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return pd.DataFrame(data)


# Função para treinar o modelo
def train_model(X, y):
    # Dividir os dados em conjunto de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Criar e treinar o modelo
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Avaliar o modelo
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    return model


# Função para prever sinais vitais
def predict_vitals(models, input_data):
    return {key: model.predict(input_data) for key, model in models.items()}


# Carregar dados
data = load_data("dados.json")  # SUBSTITUA PELO SEU JSON

# Separar características e alvos
X = data[["oxigenacao", "temperatura"]]
y_cardiaca = data["cardiaca"]
y_oxigenacao = data["oxigenacao"]
y_temperatura = data["temperatura"]

# Treinar modelos
models = {
    "cardiaca": train_model(X, y_cardiaca),
    "oxigenacao": train_model(X, y_oxigenacao),
    "temperatura": train_model(X, y_temperatura),
}

# Definir o intervalo de dados para previsão
start_index = 0  # Início do intervalo
end_index = 5  # Fim do intervalo (não inclusivo)
input_data = data[["oxigenacao", "temperatura"]].iloc[start_index:end_index]

# Fazer previsões para o intervalo
predictions = predict_vitals(models, input_data)

# Calcular intervalo de previsões para cada variável
for key in predictions:
    min_prediction = predictions[key].min()
    max_prediction = predictions[key].max()
    print(
        f"\nPrevisões para {key}:\nMínimo: {min_prediction}, Máximo: {max_prediction}"
    )
