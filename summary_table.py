import psycopg2
from tabulate import tabulate
from config import load_config
from decimal import Decimal

config = load_config()
conn = psycopg2.connect(**config)

EUR_USD_RATE = Decimal("1.2")



def create_summary_table():
  sql = """
    CREATE TABLE IF NOT EXISTS summary (
        publication_year INT PRIMARY KEY,
        book_count INT NOT NULL,
        average_price NUMERIC(10, 2) NOT NULL
    );
  """

  with conn:
    with conn.cursor() as cur:
        cur.execute(sql)

  print("Summary table is ready.")

# i did not use python to do below job. I simply want to show my sql knowledge. the below sql selects from the source table and inserts it to summary table
def build_summary_table_with_sql():
  sql = """
    INSERT INTO summary (
        publication_year,
        book_count,
        average_price
    )
    SELECT
        year AS publication_year,
        COUNT(*) AS book_count,
        ROUND(
            AVG(
                CASE
                    WHEN currency = 'EUR' THEN price * %s
                    ELSE price
                END
            )::numeric,
            2
        ) AS average_price
    FROM source
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year ASC
    ;
  """

  with conn:
    with conn.cursor() as cur:
      # i had to make sure the summary table is up to date with the source one. and thus i wrote a logic to delete the data inside the summary table.
      cur.execute("DELETE FROM summary;")
      cur.execute(sql, (EUR_USD_RATE,))
      print(f"Summary rebuilt: {cur.rowcount} rows.")

def count_summary_table():
  with conn:
    with conn.cursor() as cur:
      cur.execute("SELECT COUNT(*) FROM summary;")
      rowcount = cur.fetchone()[0]
      print(
          f"Summary table contains {rowcount} "
          f"{'rows' if rowcount != 1 else 'row'}."
      )
      return rowcount


def display_summary_table():
  with conn:
    with conn.cursor() as cur:
      cur.execute("SELECT * FROM summary;")
      rows = cur.fetchall()
      headers = [desc[0] for desc in cur.description]
      
      print("Description: summary of all books' publication year")
      print(f"Total records: {cur.rowcount}")
      print()
      print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))


def match_book_counts_with_source(source_count:int):
  with conn:
    with conn.cursor() as cur:
      cur.execute("SELECT SUM(book_count) FROM summary")
      row = cur.fetchone()
      result = f"\n\nSource table:\n\t\t{source_count}\nBook count in Summary table:\n\t\t{row[0]}\nThe summary table {"IS" if row[0]==source_count else "is NOT"} consistent with the source table."

      print(result)
  pass