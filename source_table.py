import psycopg2
from config import load_config
config = load_config()
conn = psycopg2.connect(**config)
def create_source_table_if_not_exists():
  command = """
    CREATE TABLE IF NOT EXISTS source (
      id VARCHAR(20) PRIMARY KEY,
      title VARCHAR(255) NOT NULL,
      author VARCHAR(255) NOT NULL,
      genre VARCHAR(255) NOT NULL,
      publisher VARCHAR(255) NOT NULL,
      year INT NOT NULL,
      price NUMERIC(10, 2) NOT NULL,
      currency VARCHAR(3) NOT NULL
    );
  """
  with conn:
    with conn.cursor() as cur:
      cur.execute(command)
      print("source table: CREATED")

def insert_source_table(data:tuple):
  sql = """
    INSERT INTO source (
    id,
    title,
    author,
    genre,
    publisher,
    year,
    price,
    currency
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    );
  """
  with conn:
    with conn.cursor() as cur:
      cur.execute(sql, data)


def count_source_table():
  with conn:
    with conn.cursor() as cur:
      cur.execute("SELECT COUNT(*) FROM source;")
      row = cur.fetchone()
      rowcount = row[0]
      print(
          f"Source table contains {rowcount} "
          f"{'rows' if rowcount != 1 else 'row'}."
      )
      return rowcount


def delete_source_data():
  with conn:
    with conn.cursor() as cur:
      cur.execute("DELETE FROM source;")
