import pymssql


class MsSql():
    def __init__(self):
        self.server='127.0.0.1'
        self.user='sa'
        self.password='lhm@922357'
        self.db='Check_work_attendance'
    def __connect(self):
        self.conn = pymssql.connect(self.server, self.user, self.password, self.db)
        cursor = self.conn.cursor()        # 将数据库连接信息，赋值给cursor。
        if not cursor:
            raise (NameError, "连接数据库失败")
        else:
            return cursor


    def execquery(self,sql):
        cursor=self.__connect()
        cursor.execute(sql)  # 执行查询语句
        result = cursor.fetchall()  # fetchall()获取查询结果
        # 查询完毕关闭数据库连接
        #cursor = conn.cursor(as_dict=True)
        self.conn.close()
        return result

    def exec_insert(self,sql,values):
        cursor=self.__connect()

        try:
            cursor.execute(sql,values)
            self.conn.commit()
            print("Successful!")
        except:
            self.conn.rollback()
            print('Failed')
        #插入多条记录
        # cursor.executemany(
        #     "INSERT INTO persons VALUES (%d, %s, %s)",
        #     [(1, 'John Smith', 'John Doe'),
        #      (2, 'Jane Doe', 'Joe Dog'),
        #      (3, 'Mike T.', 'Sarah H.')])

        self.conn.close()

if __name__ == '__main__':
    rsp=MsSql()
    uid=input("请输入uid：")
    name=input("请输入name：")
    face_encoding='''
[-0.06231602  0.09483757  0.06800126 -0.00957789 -0.03037139 -0.06792561
 -0.05069385 -0.12880635  0.12245566 -0.04446673  0.26189667 -0.11769579
 -0.23479551 -0.08676491 -0.04032281  0.141238   -0.18688831 -0.11508614
  0.03983352  0.02498471  0.13251652 -0.02655542 -0.00434379  0.06215578
 -0.06122598 -0.30002561 -0.10860527 -0.08308491  0.08019172 -0.0445453
 -0.05514668  0.04998603 -0.1553507  -0.08247115  0.05493213  0.05256106
  0.01872887 -0.04577283  0.21488175 -0.05317416 -0.23605461  0.02372845
  0.04318678  0.22843672  0.15034758  0.12273102 -0.01895807 -0.17193678
  0.10046072 -0.15322225  0.07972376  0.18380709  0.08405419  0.03959332
 -0.01314422 -0.21015206  0.02009756  0.05692921 -0.16001512  0.02738299
  0.09241804 -0.09743489  0.05864884 -0.0606539   0.16799897  0.01073734
 -0.10194744 -0.1507871   0.11388136 -0.12037496 -0.06700303  0.10976218
 -0.1514454  -0.16475391 -0.34131688  0.00462583  0.44648212  0.07911418
 -0.17073743  0.05639031 -0.05017262 -0.02869224  0.15995516  0.14161304
 -0.01946001 -0.02320711 -0.13209635 -0.01530544  0.18763605 -0.06778876
 -0.05709177  0.1556243  -0.04378904  0.12840292 -0.00047833  0.07601841
 -0.06291768  0.05485945 -0.12760209 -0.03581638  0.0407353   0.01399226
  0.00138128  0.15824759 -0.17671378  0.073399    0.04265197  0.01086004
  0.00209904  0.00924559 -0.08378707 -0.03268468  0.12023329 -0.24315061
  0.21254091  0.1605342   0.08856452  0.09821687  0.10965643  0.0635113
  0.00125186 -0.08643655 -0.21849181 -0.02921811  0.0867001   0.01947043
  0.11805956  0.01005479]'''
    # rsp.exec_values_query("insert into code_user(uid,name) values(%s,%s)",(uid,name))
    date ={
        'uid': uid,
        'name':name,
        'face_encoding':face_encoding
    }
    keys=','.join(date.keys())
    values=','.join(['%s']*len(date))
    table='code_user'
    condition="name='lhc'"

    # rsp.execquery("delete {table} where {condition}".format(table=table,condition=condition)) #删
    # rsp.execquery("update {table} set name='lhc' where {condition}".format(table=table,condition=condition))  #改
    # rsp.execquery("select * from {table} where {condition}".format(table=table,condition=condition))   #查
    rsp.exec_insert("insert into {table}({keys}) values ({values})".format(table=table,keys=keys,values=values),tuple(date.values()))  #增
    # rsp.execquery("insert into {table}({keys}) values ({values})".format(table=table,keys=keys,values=values),tuple(date.values()))


