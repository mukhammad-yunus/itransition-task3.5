import json
import re
import sys
from source_table import create_source_table_if_not_exists, insert_source_table, count_source_table, delete_source_data
from summary_table import create_summary_table, build_summary_table_with_sql, count_summary_table, display_summary_table, match_book_counts_with_source

# Here it opens and reads the json file. Since the provided json file is not clean, having malformed structure, i had to clean the string first and then turn this into pure json.
try:
    with open("data/task1_d.json", encoding="utf-8") as file:
        data_string = file.read()

    pattern = r':([A-Za-z_]\w*)\s*=>'
    cleaned_string = re.sub(pattern, r'"\1":', data_string)

    data = tuple(json.loads(cleaned_string))

except FileNotFoundError:
    print("Error: The input file was not found.")
    sys.exit(1)

except json.JSONDecodeError as error:
    print(f"Error: Invalid JSON: {error}")
    sys.exit(1)

except OSError as error:
    print(f"Error reading the file: {error}")
    sys.exit(1)

# after cleaning the json I made sure that the source table is created. I did not quite understand the requirements well, so i improvised by using python for rdbms queries, aka sql queries
create_source_table_if_not_exists()
#if the source table exists AND it has data, that would ruin our ingestion. so i wrote a script to delete all information in the source table
delete_source_data()

# now it is time to map the json and ingest it to the database. count is just a variable for visualization in terminal.
count = 1
for element in data:
  currency_price = element["price"]
  currency = ""
  price = currency_price[1::]
  if currency_price.startswith("$"):
    currency = "USD"
  elif currency_price.startswith("€"):
    currency = "EUR"
  """pass tuple with exact same order: id, title, author, genre, publisher, year, price, currency"""
  arg_tuple = (element["id"], element["title"], element["author"], element["genre"], element["publisher"], element["year"], price, currency)
  insert_source_table(arg_tuple)
  print(f"\r{count}", end="", flush=True)
  count +=1
print("\rJSON is ingested to Database successfully!", flush=True)

create_summary_table()
build_summary_table_with_sql()

source_count = count_source_table()

count_summary_table()

display_summary_table()

match_book_counts_with_source(source_count=source_count)