import xlwt


def output_to_excel(filename, content, sheet):
    book = xlwt.Workbook(encoding="utf-8")
    write_sheet = book.add_sheet(sheet)
    style0 = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on',
                         num_format_str='#,##0.00')
    style1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off')

    write_sheet.write(4, 2, 'NOME', style0)
    write_sheet.write(4, 3, 'E-MAIL', style0)
    write_sheet.write(4, 4, 'JANEIRO', style0)
    write_sheet.write(4, 5, 'FEVEREIRO', style0)
    write_sheet.write(4, 6, 'MARÇO', style0)
    write_sheet.write(4, 7, 'ABRIL', style0)
    write_sheet.write(4, 8, 'MAIO', style0)
    write_sheet.write(4, 9, 'JUNHO', style0)
    write_sheet.write(4, 10, 'JULHO', style0)
    write_sheet.write(4, 11, 'AGOSTO', style0)
    write_sheet.write(4, 12, 'SETEMBRO', style0)
    write_sheet.write(4, 13, 'OUTUBRO', style0)
    write_sheet.write(4, 14, 'NOVEMBRO', style0)
    write_sheet.write(4, 15, 'DEZEMBRO', style0)

    row = 5
    for mapeador in content:
        column = 2
        write_sheet.write(row, column, mapeador.get_nome(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_email(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_jan(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_fev(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_mar(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_abr(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_mai(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_jun(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_jul(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_ago(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_sep(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_out(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_nov(), style1)
        column += 1
        write_sheet.write(row, column, mapeador.get_dez(), style1)
        row += 1
    book.save(filename)

