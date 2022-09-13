'''
Handles functionality for writing to excel
'''

import xlsxwriter
from logo import Logo


def exportToExcel(logos: list[Logo]) -> None:
    #There must be at least one logo
    assert(len(logos) > 0)
    
    workbook = xlsxwriter.Workbook('LogoDataNew.xlsx')
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})

    #Create Header Row
    worksheet.write(0, 0, "Company Name", bold)
    worksheet.write(0, 1, "Start Year", bold)
    worksheet.write(0, 2, "End Year", bold)

    col = 3
    for key in logos[0].attributes:
        worksheet.write(0, col, key, bold)
        col += 1

    #Increase width of columns
    worksheet.set_column(0, col, 20)
    
    #Fill in the data for all other logos
    row = 1
    for logo in logos:
        try:
            logoDescriptors = logo.name.split(".")[0].split("_")

            worksheet.write(row, 0, logoDescriptors[0]) #Company Name
            worksheet.write(row, 1, logoDescriptors[1]) #Logo Start Year
            worksheet.write(row, 2, logoDescriptors[2]) #Logo End Year

            col = 3
            for key in logos[0].attributes:
                worksheet.write(row, col, str(logo.attributes[key]))
                col += 1
            row += 1
        except:
            print("\nWriting to excel failed for " + logo.name + ".")
            print("Check and see if the name is formatted correctly.\n")

    workbook.close()