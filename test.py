import snowflake.connector

conn = snowflake.connector.connect(
     user="chaithu59",
    password="tk.-e7NTRrv5ise",
    account="BSEXVIS-FO68852",
    warehouse="COMPUTE_WH",
    database="FRAUD_ANALYTICS_DB",
    schema="GOLD"
)

cur = conn.cursor()

cur.execute("SELECT * FROM FACT_TRANSACTIONS LIMIT 10")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()
