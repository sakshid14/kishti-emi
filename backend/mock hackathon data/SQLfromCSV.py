import pandas as pd

def sql_value(val):
    if pd.is(val):
        return &#039;NULL&#039;
    if isinstance(val, str):
        return &quot;&#039;&quot; + val.replace(&quot;&#039;&quot;, &quot;&#039;&#039;&quot;) + &quot;&#039;&quot;
    return str(val)

def df_to_insert(df, table):
    cols = &#039;, &#039;.join(df.columns)
    stmts = []
    for _, row in df.iterrows():
        vals = &#039;, &#039;.join([sql_value(row[col]) for col in df.columns])
        stmts.append(f&quot;INSERT INTO {table} ({cols}) VALUES ({vals});&quot;)
    return stmts

# Map CSV file to table name
csv_table_map = {
    &#039;mock_users.csv&#039;: &#039;users&#039;,
    &#039;mock_borrower_profiles.csv&#039;: &#039;borrowerprofile&#039;,
    &#039;mock_lender_profiles.csv&#039;: &#039;lenderprofile&#039;,
    &#039;mock_loans.csv&#039;: &#039;loan&#039;,
    &#039;mock_emi_wallets.csv&#039;: &#039;emiwallet&#039;,
    &#039;mock_transactions.csv&#039;: &#039;transaction&#039;,
    &#039;mock_emi_payments.csv&#039;: &#039;emipayment&#039;
}

all_sql = []
for csv, table in csv_table_map.items():
    df = pd.read_csv(csv, dtype=str)
    all_sql += df_to_insert(df, table)

with open(&#039;mock_data_inserts.sql&#039;, &#039;w&#039;, encoding=&#039;utf-8&#039;) as f:
    for stmt in all_sql:
        f.write(stmt + &#039;\n&#039;)

print(&#039;All INSERT statements written to mock_data_inserts.sql&#039;)