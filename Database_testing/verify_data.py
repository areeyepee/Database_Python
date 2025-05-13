import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('identifier.sqlite')
cursor = conn.cursor()

# Function to execute a query and print results
def execute_and_print(query, description):
    cursor.execute(query)
    results = cursor.fetchall()
    print(f"\n{description} ({len(results)} total records):")
    # Print at most 5 records
    for i, row in enumerate(results[:5]):
        print(f"  {row}")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more records")

# Check each table
execute_and_print("SELECT * FROM Professoren", "Professors")
execute_and_print("SELECT * FROM Studenten", "Students")
execute_and_print("SELECT * FROM Vorlesungen", "Lectures")
execute_and_print("SELECT * FROM voraussetzen", "Prerequisites")
execute_and_print("SELECT * FROM hoeren", "Student-Lecture Relationships")
execute_and_print("SELECT * FROM Assistenten", "Assistants")
execute_and_print("SELECT * FROM pruefen", "Exam Records")

# Some interesting queries
print("\nSome interesting statistics:")

# Average grade per lecture
cursor.execute("""
SELECT v.Titel, AVG(p.Note)/10.0 as AvgGrade, COUNT(*) as NumStudents
FROM pruefen p
JOIN Vorlesungen v ON p.VorlNR = v.VorlNR
GROUP BY p.VorlNR
ORDER BY AvgGrade
LIMIT 5
""")
results = cursor.fetchall()
print("\nTop 5 lectures by average grade (lower is better):")
for row in results:
    print(f"  {row[0]}: {row[1]:.1f} (from {row[2]} students)")

# Professors with most lectures
cursor.execute("""
SELECT p.Name, COUNT(*) as NumLectures
FROM Professoren p
JOIN Vorlesungen v ON p.PersNR = v.gelesenVon
GROUP BY p.PersNR
ORDER BY NumLectures DESC
LIMIT 5
""")
results = cursor.fetchall()
print("\nTop 5 professors by number of lectures:")
for row in results:
    print(f"  {row[0]}: {row[1]} lectures")

# Students with most exams
cursor.execute("""
SELECT s.Name, COUNT(*) as NumExams, AVG(p.Note)/10.0 as AvgGrade
FROM Studenten s
JOIN pruefen p ON s.MatrNR = p.MatrNR
GROUP BY s.MatrNR
ORDER BY NumExams DESC
LIMIT 5
""")
results = cursor.fetchall()
print("\nTop 5 students by number of exams taken:")
for row in results:
    print(f"  {row[0]}: {row[1]} exams, average grade: {row[2]:.1f}")

# Close the connection
conn.close()