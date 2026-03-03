import pandas as pd
import sqlite3

conn = sqlite3.connect('FinalDB.db')

files = {
    'ChicagoCensusData.csv':    'CHICAGO_CENSUS',
    'ChicagoCrimeData.csv':     'CHICAGO_CRIME_DATA',
    'ChicagoPublicSchools.csv': 'CHICAGO_SCHOOLS',
}

for fname, tablename in files.items():
    df = pd.read_csv(fname)
    df.to_sql(tablename, conn, if_exists='replace', index=False)
    print(f'loaded {len(df)} rows into {tablename}')

# preview one of the tables
preview = pd.read_sql("SELECT * FROM CHICAGO_CRIME_DATA LIMIT 5", conn)
print(preview)

# Problem 1: Total number of crimes
result1 = pd.read_sql("SELECT COUNT(*) as total_crimes FROM CHICAGO_CRIME_DATA", conn)
print("Problem 1 - Total crimes:")
print(result1)
# Problem 2: Community areas with per capita income < 11000
result2 = pd.read_sql("""
    SELECT "Community_Area_Name", "Community_Area_Number" 
    FROM CHICAGO_CENSUS 
    WHERE "PER_CAPITA_INCOME" < 11000
""", conn)
print("\nProblem 2 - Communities with per capita income < 11000:")
print(result2)

# Problem 3: Case numbers for crimes involving minors
result3 = pd.read_sql("""
    SELECT "Case_Number" 
    FROM CHICAGO_CRIME_DATA 
    WHERE "Arrest" = TRUE AND "Domestic" = FALSE
""", conn)
print("\nProblem 3 - Crimes involving minors:")
print(result3)

# Problem 4: Kidnapping crimes involving a child
result4 = pd.read_sql("""
    SELECT * 
    FROM CHICAGO_CRIME_DATA 
    WHERE "Primary_Type" = 'KIDNAPPING'
""", conn)
print("\nProblem 4 - Kidnapping crimes involving a child:")
print(result4)

# Problem 5: Crimes recorded at schools (no repetitions)
result5 = pd.read_sql("""
    SELECT DISTINCT "Primary_Type" 
    FROM CHICAGO_CRIME_DATA 
    WHERE "Location_Description" LIKE '%SCHOOL%'
""", conn)
print("\nProblem 5 - Crimes at schools:")
print(result5)

# Problem 6: School types with average safety score
result6 = pd.read_sql("""
    SELECT "School_Type", AVG("Safety_Score") as avg_safety_score 
    FROM CHICAGO_SCHOOLS 
    GROUP BY "School_Type"
""", conn)
print("\nProblem 6 - School types and average safety score:")
print(result6)

# Problem 7: 5 communities with highest % below poverty line
result7 = pd.read_sql("""
    SELECT "Community_Area_Name", "PERCENT_HOUSEHOLDS_BELOW_POVERTY" 
    FROM CHICAGO_CENSUS 
    ORDER BY "PERCENT_HOUSEHOLDS_BELOW_POVERTY" DESC 
    LIMIT 5
""", conn)
print("\nProblem 7 - Top 5 communities by poverty rate:")
print(result7)

# Problem 8: Most crime prone community area
result8 = pd.read_sql("""
    SELECT "Community_Area_Number", COUNT(*) as crime_count 
    FROM CHICAGO_CRIME_DATA 
    GROUP BY "Community_Area_Number" 
    ORDER BY crime_count DESC 
    LIMIT 1
""", conn)
print("\nProblem 8 - Most crime prone community area:")
print(result8)

# Problem 9: Community area with highest hardship index
result9 = pd.read_sql("""
    SELECT "Community_Area_Name" 
    FROM CHICAGO_CENSUS 
    WHERE "HARDSHIP_INDEX" = (SELECT MAX("HARDSHIP_INDEX") FROM CHICAGO_CENSUS)
""", conn)
print("\nProblem 9 - Community with highest hardship index:")
print(result9)

# Problem 10: Community area with most crimes
result10 = pd.read_sql("""
    SELECT c."Community_Area_Name", COUNT(cr."Case_Number") as crime_count 
    FROM CHICAGO_CENSUS c 
    LEFT JOIN CHICAGO_CRIME_DATA cr ON c."Community_Area_Number" = cr."Community_Area_Number" 
    GROUP BY c."Community_Area_Name" 
    ORDER BY crime_count DESC 
    LIMIT 1
""", conn)
print("\nProblem 10 - Community with most crimes:")
print(result10)

conn.close()