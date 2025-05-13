import sqlite3
import random
import datetime

# Lists for generating names
first_names = ["Anna", "Max", "Sophie", "Felix", "Emma", "Paul", "Maria", "Alexander", "Laura", "Thomas",
               "Julia", "Michael", "Sarah", "David", "Lisa", "Andreas", "Lena", "Stefan", "Hannah", "Christian",
               "Katharina", "Daniel", "Nina", "Markus", "Melanie", "Tobias", "Sabine", "Martin", "Claudia", "Peter"]
last_names = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
              "Schäfer", "Koch", "Bauer", "Richter", "Klein", "Wolf", "Schröder", "Neumann", "Schwarz", "Zimmermann",
              "Braun", "Krüger", "Hofmann", "Hartmann", "Lange", "Schmitt", "Werner", "Schmitz", "Krause", "Meier"]

def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Connect to the SQLite database
conn = sqlite3.connect('identifier.sqlite')
cursor = conn.cursor()

# Clear existing data (optional)
tables = ["Professoren", "Studenten", "Vorlesungen", "voraussetzen",
          "hoeren", "Assistenten", "pruefen"]
for table in tables:
    cursor.execute(f"DELETE FROM {table}")

# Generate data for Professoren
professoren_data = []
for i in range(1, 21):  # 20 professors
    pers_nr = i
    name = generate_name()
    rang = random.choice(["C2", "C3", "C4"])
    raum = f"{random.choice(['A', 'B', 'C', 'D'])}-{random.randint(100, 399)}"
    professoren_data.append((pers_nr, name, rang, raum))

cursor.executemany("INSERT INTO Professoren (PersNR, Name, Rang, Raum) VALUES (?, ?, ?, ?)",
                  professoren_data)

# Generate data for Studenten
studenten_data = []
for i in range(1, 201):  # 200 students
    matr_nr = i + 10000  # Start from 10001
    name = generate_name()
    semester = random.randint(1, 12)
    studenten_data.append((matr_nr, name, semester))

cursor.executemany("INSERT INTO Studenten (MatrNR, Name, Semester) VALUES (?, ?, ?)",
                  studenten_data)

# Generate data for Vorlesungen
vorlesungen_data = []
lecture_titles = [
    "Grundlagen der Informatik", "Algorithmen und Datenstrukturen",
    "Programmierung I", "Programmierung II", "Datenbanksysteme",
    "Betriebssysteme", "Rechnernetze", "Softwaretechnik",
    "Theoretische Informatik", "Künstliche Intelligenz",
    "Machine Learning", "Computer Vision", "Web Development",
    "Mobile Computing", "IT-Sicherheit", "Computergrafik",
    "Verteilte Systeme", "Cloud Computing", "Big Data Analytics",
    "Human-Computer Interaction", "Embedded Systems", "Robotik",
    "Numerische Mathematik", "Diskrete Mathematik", "Lineare Algebra",
    "Analysis", "Statistik", "Wahrscheinlichkeitstheorie",
    "Logik", "Formale Sprachen"
]
for i in range(1, 31):  # 30 lectures
    vorl_nr = i
    titel = lecture_titles[i-1] if i <= len(lecture_titles) else f"Vorlesung {i}"
    sws = random.choice([2, 3, 4, 6])
    gelesen_von = random.choice([p[0] for p in professoren_data])
    vorlesungen_data.append((vorl_nr, titel, sws, gelesen_von))

cursor.executemany("INSERT INTO Vorlesungen (VorlNR, Titel, SWS, gelesenVon) VALUES (?, ?, ?, ?)",
                  vorlesungen_data)

# Generate data for voraussetzen (prerequisites)
voraussetzen_data = []
for i in range(10):  # Some random prerequisites
    vorgaenger = random.randint(1, 15)  # Earlier lectures
    nachfolger = random.randint(16, 30)  # Later lectures
    # Avoid duplicates
    if (vorgaenger, nachfolger) not in voraussetzen_data:
        voraussetzen_data.append((vorgaenger, nachfolger))

cursor.executemany("INSERT INTO voraussetzen (Vorgaenger, Nachfolger) VALUES (?, ?)",
                  voraussetzen_data)

# Generate data for hoeren (students attending lectures)
hoeren_data = []
for student in studenten_data:
    # Each student attends 3-8 lectures
    num_lectures = random.randint(3, 8)
    lectures = random.sample([v[0] for v in vorlesungen_data], num_lectures)
    for lecture in lectures:
        hoeren_data.append((student[0], lecture))

cursor.executemany("INSERT INTO hoeren (MatrNR, VorlNR) VALUES (?, ?)",
                  hoeren_data)

# Generate data for Assistenten
assistenten_data = []
fachgebiete = ["Datenbanken", "Algorithmen", "KI", "Netzwerke", "Sicherheit",
               "Software Engineering", "Theoretische Informatik", "Computergrafik"]
for i in range(1, 41):  # 40 assistants
    pers_nr = i + 100  # Start from 101 to avoid collision with professors
    name = generate_name()
    fachgebiet = random.choice(fachgebiete)
    boss = random.choice([p[0] for p in professoren_data])
    assistenten_data.append((pers_nr, name, fachgebiet, boss))

cursor.executemany("INSERT INTO Assistenten (PersNR, Name, Fachgebiet, Boss) VALUES (?, ?, ?, ?)",
                  assistenten_data)

# Generate data for pruefen (exams)
pruefen_data = []
# Create a set to track unique student-lecture combinations
student_lecture_pairs = set()

# Try to generate around 300 exam records
attempts = 0
while len(pruefen_data) < 300 and attempts < 1000:
    attempts += 1
    matr_nr = random.choice([s[0] for s in studenten_data])
    vorl_nr = random.choice([v[0] for v in vorlesungen_data])

    # Check if this student-lecture pair already exists
    if (matr_nr, vorl_nr) in student_lecture_pairs:
        continue

    # Add to tracking set
    student_lecture_pairs.add((matr_nr, vorl_nr))

    # Exams can be conducted by professors or assistants
    if random.random() < 0.7:  # 70% by professors
        pers_nr = random.choice([p[0] for p in professoren_data])
    else:  # 30% by assistants
        pers_nr = random.choice([a[0] for a in assistenten_data])

    # German grading system: 1.0 (best) to 5.0 (fail)
    note = random.choice([10, 13, 17, 20, 23, 27, 30, 33, 37, 40, 50])

    pruefen_data.append((matr_nr, vorl_nr, pers_nr, note))

cursor.executemany("INSERT INTO pruefen (MatrNR, VorlNR, PersNR, Note) VALUES (?, ?, ?, ?)",
                  pruefen_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data generation complete!")
print(f"Inserted {len(professoren_data)} professors")
print(f"Inserted {len(studenten_data)} students")
print(f"Inserted {len(vorlesungen_data)} lectures")
print(f"Inserted {len(voraussetzen_data)} prerequisites")
print(f"Inserted {len(hoeren_data)} student-lecture relationships")
print(f"Inserted {len(assistenten_data)} assistants")
print(f"Inserted {len(pruefen_data)} exam records")
