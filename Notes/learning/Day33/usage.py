from utils.data_reader_util import read_csv_data, read_excel_data, read_json_data

# Read JSON data
json_data = read_json_data("testdata/data.json")

# Read CSV data
csv_data = read_csv_data("testdata/data.csv")

# Read Excel data
excel_data = read_excel_data("testdata/data.xlsx")

print(json_data)
print(csv_data)
print(excel_data)
