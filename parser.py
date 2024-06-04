import openpyxl
from enums import KostilType

def parse_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path)

    all_sheets_data = []
    sheets = []

    for sheet in workbook.worksheets:
        sheet_data = []
        for row in sheet.iter_rows(values_only=True):
            filtered_row = [cell for cell in row if cell is not None]
            if len(list(filtered_row)) >0:
                sheet_data.append(list(filtered_row))
        all_sheets_data.append(sheet_data)
        sheets.append(sheet)

    return all_sheets_data, sheets

def get_element_by_enum(data_list, enum):
    return data_list[enum.value]