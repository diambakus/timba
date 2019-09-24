import xlwt

def output_to_excel(filename, content, sheet):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)