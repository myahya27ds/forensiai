import sqlite3


conn = sqlite3.connect(
    "forensiai.db"
)

cursor = conn.cursor()


columns = [

    (
        "manipulation_probability",
        "REAL"
    ),

    (
        "authenticity_score",
        "REAL"
    ),

    (
        "mean_noise",
        "REAL"
    ),

    (
        "std_noise",
        "REAL"
    ),

    (
        "noise_level",
        "TEXT"
    ),

    (
        "explanation",
        "TEXT"
    )

]


for column_name, column_type in columns:

    try:

        cursor.execute(
            f"""
            ALTER TABLE image_analysis
            ADD COLUMN {column_name}
            {column_type}
            """
        )

        print(
            f"[OK] Added column: {column_name}"
        )

    except Exception:

        print(
            f"[SKIP] Column exists: {column_name}"
        )

conn.commit()
conn.close()

print(
    "\nMigration v0.9.0 completed."
)