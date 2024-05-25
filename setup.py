import json
import random
from datetime import datetime, timedelta

# Dados base fornecidos
data = [
    {"id": 1, "patient_id": 1323, "scores": {"satisfaction": 9, "pain": 2, "fatigue": 2}, "date": "2020-06-25"},
    {"id": 2, "patient_id": 9032, "scores": {"satisfaction": 2, "pain": 7, "fatigue": 5}, "date": "2020-06-30"},
    {"id": 3, "patient_id": 2331, "scores": {"satisfaction": 7, "pain": 1, "fatigue": 1}, "date": "2020-07-05"},
    {"id": 4, "patient_id": 2303, "scores": {"satisfaction": 8, "pain": 9, "fatigue": 0}, "date": "2020-07-12"},
    {"id": 5, "patient_id": 1323, "scores": {"satisfaction": 10, "pain": 0, "fatigue": 0}, "date": "2020-07-09"},
    {"id": 6, "patient_id": 2331, "scores": {"satisfaction": 8, "pain": 9, "fatigue": 5}, "date": "2020-07-20"}
]

# Função para gerar registros adicionais
def generate_additional_records(base_id, num_records):
    additional_data = []
    start_date = datetime.strptime('2020-06-25', '%Y-%m-%d')
    patient_ids = [1323, 9032, 2331, 2303, 1001, 1002, 1003, 1004]
    for i in range(num_records):
        base_id += 1
        patient_id = random.choice(patient_ids)
        scores = {
            'satisfaction': random.randint(0, 10),
            'pain': random.randint(0, 10),
            'fatigue': random.randint(0, 10)
        }
        date = start_date + timedelta(days=random.randint(1, 30))
        additional_data.append({
            "id": base_id,
            "patient_id": patient_id,
            "scores": scores,
            "date": date.strftime('%Y-%m-%d')
        })
    return additional_data

# Gerar 20 registros adicionais
additional_data = generate_additional_records(6, 20)

# Combinar dados base com dados adicionais
all_data = data + additional_data

# Salvar dados em um arquivo JSON
with open('database/patient_scores.json', 'w') as json_file:
    json.dump(all_data, json_file, indent=4)

print("Dados salvos em patient_scores.json")
