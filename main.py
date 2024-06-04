from parser import parse_xlsx, get_element_by_enum
from enums import KostilType
from nicknames import makeQuestion
def main():
    file_path = './src/kostili.xlsx'
    all_sheets_data, sheets = parse_xlsx(file_path)
    # for _ in all_sheets_data[KostilType.NICKNAMES.value]:
        # print(_)
    makeQuestion(get_element_by_enum(all_sheets_data, KostilType.NICKNAMES))

if __name__ == "__main__":
    main()