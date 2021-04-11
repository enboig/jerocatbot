from jerocat import Jerocat
from pyexcel_ods import get_data
import json
# import pandas as pd
# from pandas_ods_reader import read_ods
import pyexcel as pe


if __name__ == '__main__':
    print("Actualitzant")
    j = Jerocat()
    u1 = j.user_get(id=0)

    book = pe.get_book(file_name="insert.ods")
    # print(book)
    for sheet in book:
        if (sheet.name!="Helper"):
            print(sheet.name)
            g = j.game_get(name=sheet.name)
            if g == None:
                g = j.game_add(name=sheet.name, user=u1, status=j.STATUS_PUBLIC)
            for row in sheet:
                q = None
                first = True
                for cell in row:
                    if first:
                        q = j.question_get(g, text=str(cell).strip())
                        if q == None:
                            q = j.question_add(game=g, question=str(cell).strip())
                        first = False
                    else:
                        if str(cell).strip()!="":
                            a = j.answer_get(q, text=str(cell).strip())
                            if a == None:
                                a = j.answer_add(question=q, answer=str(cell).strip())
