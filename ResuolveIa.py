
from pymongo import MongoClient
from bson.json_util import dumps

import pandas as pd
import numpy as np
from time import sleep

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split

# Definindo Target e Feature
pmt_mtrc = [
    'disk_free_bytes',
    'hikaricp_connections_acquire_seconds_count',
    'hikaricp_connections_creation_seconds_count',
    'hikaricp_connections_pending',
    'hikaricp_connections_timeout_total',
    'hikaricp_connections_usage_seconds_count',
    'http_server_requests_seconds_count',
    'http_server_requests_seconds_max',
    'http_server_requests_seconds_sum',
    'jdbc_connections_active',
    'jvm_memory_max_bytes',
    'jvm_memory_usage_after_gc_percent',
    'jvm_memory_used_bytes',
    'logback_events_total',
    'process_cpu_usage',
]
target = 'system_cpu_usage'

# conectando ao mongoDB
cluster = MongoClient(
    "mongodb+srv://resuolve:123@cluster0.ogtku.mongodb.net/resuolve?retryWrites=true&w=majority")
db = cluster['resuolve']
collection = db['metrics']

# Valor Minimo do bd para gerar o df
listaCount = []
datacounttg = collection.find({"name":  target})
listaCountTg = list(datacounttg)
listaCount.append(len(listaCountTg))
for i in range(len(pmt_mtrc)):
    dataCountFt = collection.find({"name": pmt_mtrc[i]})
    listaCountFt = list(dataCountFt)
    listaCount.append(len(listaCountFt))

minValue = min(listaCount)


# Gerando o target de treino
dicdf = {}
datatg = collection.find({"name":  target})

listdata = list(datatg)
listTarget = []
for i in range(minValue):
    valortg = listdata[i].get('value')
    valortg = float(valortg)
    if valortg > 0.6:
        listTarget.append(1)
    else:
        listTarget.append(0)

dicTarget = {'Target': listTarget}

dicdf.update(dicTarget)

# Gerando as features de Treino

for i in range(len(pmt_mtrc)):
    data = collection.find({"name": pmt_mtrc[i]})
    listadt = list(data)
    listadt = listadt[0]
    listavalor = []
    for j in range(minValue):
        valor = listadt.get('value')
        listavalor.append(valor)
    dic1 = {pmt_mtrc[i]: listavalor}
    dicdf.update(dic1)


# Gerando DataFrame
dfFinal = pd.DataFrame(dicdf)

# Separando Features e Target dentro do DataFrame
x = dfFinal[['disk_free_bytes',
            'hikaricp_connections_acquire_seconds_count',
             'hikaricp_connections_creation_seconds_count',
             'hikaricp_connections_pending',
             'hikaricp_connections_timeout_total',
             'hikaricp_connections_usage_seconds_count',
             'http_server_requests_seconds_count',
             'http_server_requests_seconds_max',
             'http_server_requests_seconds_sum',
             'jdbc_connections_active',
             'jvm_memory_max_bytes',
             'jvm_memory_usage_after_gc_percent',
             'jvm_memory_used_bytes',
             'logback_events_total',
             'process_cpu_usage']]

y = dfFinal['Target']

# Definindo Modelo

modelo = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,  # 3, 5, 10 --> influencia bastante no resultado final
    min_samples_split=2,
    min_samples_leaf=1,
    min_weight_fraction_leaf=0,
    max_features="auto",
    max_leaf_nodes=None,
    min_impurity_decrease=0,
    bootstrap=True,
    oob_score=False,
    n_jobs=None,
    random_state=None,
    verbose=0,
    warm_start=False,
    class_weight='balanced',
    ccp_alpha=0,
    max_samples=None
)

# Separando treino e teste e treinando modelo
tts = train_test_split
SEED = 5
treino_x, teste_x, treino_y, teste_y = tts(x, y,
                                           random_state=SEED,
                                           train_size=0.7,
                                           stratify=y)
rf1 = modelo.fit(treino_x, treino_y)
#print(rf1.score(teste_x, teste_y))


# criando loop de verificação com o modelo treinado
while True == True:
    reset = False
    dicRt = {}
    for i in range(len(pmt_mtrc)):
        uri = 'https://prometheus.herokuapp.com/api/v1/query?query=' + \
            pmt_mtrc[i]
        dfRt = pd.read_json(uri)
        valorRt = dfRt.data[0]
        if valorRt == []:
            print('servidor caiu')
            reset = True
            break
        else:
            valorRt = valorRt[0]
            valorRt = valorRt.get('value')
            valorRt = valorRt[1]
            dicRt1 = {pmt_mtrc[i]: valorRt}
            dicRt.update(dicRt1)
    if reset == True:
        break
    else:
        dfTest = pd.DataFrame(dicRt, index=[0])
        print('resultado', rf1.predict(dfTest))
        print(f'probabilidade de ser [0 e 1]', rf1.predict_proba(dfTest))
        sleep(5)
