import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('mock_database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient_scores (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    scores TEXT,
    date TEXT
)
''')


data = [
    (1, 1323, "{'satisfaction': 9, 'pain': 2, 'fatigue': 2}", '2020-06-25'),
    (2, 9032, "{'satisfaction': 2, 'pain': 7, 'fatigue': 5}", '2020-06-30'),
    (3, 2331, "{'satisfaction': 7, 'pain': 1, 'fatigue': 1}", '2020-07-05'),
    (4, 2303, "{'satisfaction': 8, 'pain': 9, 'fatigue': 0}", '2020-07-12'),
    (5, 1323, "{'satisfaction': 10, 'pain': 0, 'fatigue': 0}", '2020-07-09'),
    (6, 2331, "{'satisfaction': 8, 'pain': 9, 'fatigue': 5}", '2020-07-20')
]


def generate_additional_records(base_id, num_records):
    additional_data = []
    start_date = datetime.strptime('2020-06-25', '%Y-%m-%d')
    for i in range(num_records):
        base_id += 1
        patient_id = random.choice([1323, 9032, 2331, 2303])
        scores = {
            'satisfaction': random.randint(0, 10),
            'pain': random.randint(0, 10),
            'fatigue': random.randint(0, 10)
        }
        date = start_date + timedelta(days=random.randint(1, 30))
        additional_data.append((base_id, patient_id, str(scores), date.strftime('%Y-%m-%d')))
    return additional_data


additional_data = generate_additional_records(6, 20)


cursor.executemany('''
INSERT INTO patient_scores (id, patient_id, scores, date)
VALUES (?, ?, ?, ?)
''', data + additional_data)

conn.commit()
conn.close()