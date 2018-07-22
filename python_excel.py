# -*- coding: utf-8 -*-
#author:dbuging

import  os
import xlrd
import time

input_name = 'E:/workplaces/python/work/tables_test.xlsx'
print(input_name)


###
df = xlrd.open_workbook(input_name)
table = df.sheets()[0]

#
# start=time.clock()
# merged_cells = table.merged_cells
# merged_sheet = {}
#
# for cells in merged_cells:
#     for x in range(cells[0],cells[1]):
#         for y in range(cells[2],cells[3]):
#             if (x,y) != (cells[0],cells[2]):
#                 merged_sheet.update({(x, y): (cells[0], cells[2])})
# print(merged_sheet)
# ##################
# end=time.clock()
# print("final is in ",(end-start)*100000)
#
#


start1 = time.clock()
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

end1 = time.clock()
print("final is in ",(end1-start1)*100000)



# #输出
# for x in range(table.nrows):
#     row_sheet = table.row_values(x, start_colx=0, end_colx=None)
#     rowlen = table.row_len(x)
#     for y in range(table.ncols):
#         if merged_sheet1.get((x,y)):
#             row_sheet[y] = table.cell_value(*merged_sheet1.get((x,y)))
#
#     print(row_sheet,"\t",rowlen,"\n")
#


def get_null_cols(null_cols):
    for x, y in enumerate(table_rows_list):
        if sum(b[:x + 1]) != 0:
            return x
    return x

def table_split(sheet):
    table_firt_types = sheet.col_types(0, start_rowx=0, end_rowx=None)
    null_rows_list = [x for x, y in enumerate(table_firt_types) if y == 0]
    print(null_rows_list)
    split_list = []
    
    row_start,row_end,col_start,col_end = 0,0,0,0
    
    for x in null_rows_list:
        table_rows_list = sheet.row_types(x, start_colx=0, end_colx=None)
        null_cols = get_null_cols(table_rows_list)
        if sheet.cell_value(*merged_sheet1.get((x,null_cols))):
            continue
        if null_cols == sheet.ncols:
            split_list,append((row_start,x,col_start,null_cols))
            row_start = get_null_cols(null_rows_list[row_start:]
            
        
        null_end = get_null_cols(sheet.col_types(null_cols,start_rowx=0,end_rowx=None))
        if null_end == x:
            if len(set(sheet.row_types(x+1, start_colx=0, end_colx=None))) <=2 or :
             
            








    print(map(index(0),table_firt_types))
    print(table_firt_types[0])

table_split(table)










