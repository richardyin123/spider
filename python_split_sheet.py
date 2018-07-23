# -*- coding: utf-8 -*-
#author:dbuging


import xlrd

input_name = 'E:/workplaces/python/work/tables_test.xlsx'
df = xlrd.open_workbook(input_name)
table = df.sheets()[0]


merged_sheet1 = {}

def get_merged_cells(sheet):
    if sheet.merged_cells:
        n = 0
        while n < len(sheet.merged_cells):
            yield sheet.merged_cells[n]
            n += 1
###获取合并单元格
for merge in get_merged_cells(table):
    for rows in  range(merge[0],merge[1]):
        for cols in range(merge[2],merge[3]):
            if (rows,cols) != (merge[0],merge[2]):
                merged_sheet1.update({(rows,cols):(merge[0],merge[2])})
print(merged_sheet1)


def get_null_cols(table_list):
    for x, y in enumerate(table_list):
        if sum(table_list[:x + 1]) != 0:
            return x
    return x


def get_fisrt_cell(table,fisrt_cell,end_cell,ty=0):
    for i in range(end_cell -fisrt_cell+1):
        if ty == 1:
            n_liste =  table.col_types(i, start_rowx=fisrt_cell, end_rowx=end_cell)
            if set(n_liste) != {0} and i <end_cell:
                return i
        n_liste = table.row_types(i, start_colx=fisrt_cell, end_colx=end_cell)
        if set(n_liste) != {0} and i <end_cell:
            return i
    return

def get_end_cell(table,fisrt_cell,end_cell,x,ty=0):
    for i in range(end_cell -fisrt_cell+1):
        if ty == 1:
            n_liste =  table.col_types(i, start_rowx=fisrt_cell, end_rowx=x)
            if set(n_liste) == {0} and i <= end_cell:
                return i
        n_liste = table.row_types(i, start_colx=fisrt_cell, end_colx=x)
        if set(n_liste) == {0} and  i == end_cell:
            return i
    return end_cell



def table_split(sheet):
    rows_start = 0
    rows_end = sheet.nrows
    cols_start = 0
    cols_end  = sheet.ncols

    first_row_types= sheet.col_types(rows_start, start_rowx=rows_start, end_rowx=rows_end)
    null_rows_list = [x for x, y in enumerate(first_row_types) if y == 0]

    print(null_rows_list)

    if  len(null_rows_list):
        for x in null_rows_list:
            row_types_list = sheet.row_types(x, start_colx=cols_start, end_colx=cols_end)
            null_col = get_null_cols(row_types_list)
            if merged_sheet1.get((x,null_col)):
                print(sheet.cell_value(*merged_sheet1.get((x,null_col))))
                continue
            col_ends = get_end_cell(sheet,cols_start,null_col,x,1)
            if col_ends > null_col:
                continue
            elif col_ends <= null_col:
                print(x,col_ends,cols_start,cols_end)


#

   # print(table_firt_types)


table_split(table)











# if __name__ == '__main__':
#     input_name = 'E:/workplaces/python/work/tables_test.xlsx'
#     df = xlrd.open_workbook(input_name)
#     table = df.sheets()[0]
#     table_split(table)

