# -*- coding:utf-8 -*-
# Author: pengqi
# Date  : 2023/3/23
# Desc  : 批量重命名字段
# 场景: 对一个dataframe处理合并是, 因为会有相同的字段名, 所以会自动给字段名加上后缀. _x, _y
# 而又要将 字段名_x, 这样的字段的后缀去掉. 如果一个个去重命名列会很难维护. 所以使用下面的方式进行处理

if __name__ == '__main__':
    df_column = ['oid_x', 'aid_x', 'diszn', 'disen_x', 'disals_x', 'dison_x',
                 'relatedsymptom_x', 'diseasesite_x', 'medicaldept_x', 'relateddrug_x',
                 'dspn_x', 'discau_x', 'resource_id_x', 'dis_oid_x', 'null_num_x',
                 'upt_x', 'row_num_x', 'oid_y', 'aid_y', 'disen_y', 'disals_y',
                 'dison_y', 'relatedsymptom_y', 'diseasesite_y', 'medicaldept_y',
                 'relateddrug_y', 'dspn_y', 'discau_y', 'resource_id_y', 'dis_oid_y',
                 'null_num_y', 'upt_y', 'row_num_y']

    new_column = {col: col.rstrip('_x') for col in df_column if col.endswith('_x')}
    print(new_column)

    # 使用一下代码就可以对sec_df的列明重命名
    # sec_df = sec_df.rename(columns=columns_to_rename)


def chb_renamer(df, fst_df):
    sec_df = (df(fst_df, how="left", left_on="diszn", right_on="diszn")  # 关联表
              .query('resource_id_y.isnull()')  # 空值判断
              .pipe(lambda x: x.rename(columns={col: col.rstrip('_x') for col in x.columns if col.endswith('_x')})))  # 删除后缀_x, 重命名列
