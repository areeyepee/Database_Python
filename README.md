# SQLite Database Data Generator

This project provides scripts to generate and verify test data for a university database system in SQLite.

## Database Schema

The database models a university system with the following tables:

1. **Professoren** (Professors): PersNR, Name, Rang (Rank), Raum (Room)
2. **Studenten** (Students): MatrNR (Student ID), Name, Semester
3. **Vorlesungen** (Lectures): VorlNR (Lecture ID), Titel (Title), SWS (Weekly hours), gelesenVon (Taught by)
4. **voraussetzen** (Prerequisites): Vorgaenger (Predecessor), Nachfolger (Successor)
5. **hoeren** (Attending): MatrNR, VorlNR
6. **Assistenten** (Assistants): PersNR, Name, Fachgebiet (Field), Boss
7. **pruefen** (Exams): MatrNR, VorlNR, PersNR, Note (Grade)

## Scripts

### 1. inspect_db.py

This script inspects the database schema and displays the structure of all tables.

```bash
python inspect_db.py
```

### 2. generate_data.py

This script generates realistic test data for all tables in the database:

- 20 professors with names, ranks, and room numbers
- 200 students with names and semester information
- 30 lectures with titles, weekly hours, and assigned professors
- 10 prerequisite relationships between lectures
- Student-lecture attendance relationships (each student attends 3-8 lectures)
- 40 assistants with names, specialties, and assigned professors
- 300 exam records with grades

```bash
python generate_data.py
```

### 3. verify_data.py

This script verifies the generated data by displaying sample records from each table and some interesting statistics:

- Top 5 lectures by average grade
- Top 5 professors by number of lectures
- Top 5 students by number of exams taken

```bash
python verify_data.py
```

## Data Generation Details

- Names are generated using a combination of common German first and last names
- Professors are assigned random ranks (C2, C3, C4) and room numbers
- Students are assigned random semester numbers (1-12)
- Lectures are assigned realistic titles and weekly hours
- Prerequisites are established between earlier and later lectures
- Each student attends 3-8 random lectures
- Assistants are assigned to professors and given specific fields of expertise
- Exam grades follow the German grading system (1.0 best to 5.0 fail)

## Usage

1. Run `inspect_db.py` to understand the database structure
2. Run `generate_data.py` to populate the database with test data
3. Run `verify_data.py` to check the generated data and see some statistics