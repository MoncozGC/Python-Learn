# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/4 15:28
# Desc  : 大数据集的处理
# 方法一: 分块处理, 效果不明显, 待优化.
# 方法二: 使用dask库进行并行数据处理
import numpy as np
import pandas as pd
import dask.dataframe as dd

from utils.comm_util import print_ts

if __name__ == '__main__':
    # 创建示例数据
    data_barc = {'cmnzn': np.random.randint(1, 1000000, 1000000),
                 'gdsn': np.random.randint(1, 1000000, 1000000),
                 'adn': np.random.randint(1, 1000000, 1000000),
                 'spec': np.random.randint(1, 1000000, 1000000),
                 'mftzn': np.random.randint(1, 1000000, 1000000),
                 'barc': np.random.randint(1, 1000000, 1000000)}

    data_bs = {'cmnzn': np.random.randint(1, 1000000, 500000),
               'gdsn': np.random.randint(1, 1000000, 500000),
               'adn': np.random.randint(1, 1000000, 500000),
               'spec': np.random.randint(1, 1000000, 500000),
               'mftzn': np.random.randint(1, 1000000, 500000),
               'mft_oid': np.random.randint(1, 1000000, 500000)}
    print_ts('jinru')
    barc_df = pd.DataFrame(data_barc)
    bs_df = pd.DataFrame(data_bs)

    # 方式一: 数据分块, 处理时间 - 34s
    # block_size = 10000
    # barc_chunks = [barc_df[i:i + block_size] for i in range(0, barc_df.shape[0], block_size)]
    #
    # result_df = []
    #
    # for i in barc_chunks:
    #     merged_chunk = barc_df.merge(bs_df, how='left', on='cmnzn', suffixes=('_barc', '_bs'))
    #     result_df.append(merged_chunk)
    #
    # pd_data_frame = pd.concat(result_df)
    # print(pd_data_frame)

    # 方式二: Dask并行计算库, 处理时间 - 1s
    """
    具有和DataFrame类似的API, 可以使用内核或多计算节点并行计算数据.
    将 Pandas DataFrame 转换为 Dask DataFrame，然后执行合并操作。
    npartitions 参数决定了 Dask 如何将数据划分为多个分区，以便进行并行处理。
    可以根据可用内核和内存调整该参数。在完成合并后，
    使用 compute() 函数将结果计算出来，并将其转换回 Pandas DataFrame。
    """
    barc_dd = dd.from_pandas(barc_df, npartitions=10)
    bs_dd = dd.from_pandas(bs_df, npartitions=10)

    merge_dd = barc_dd.merge(bs_dd, how='left', on='cmnzn', suffixes=('_barc', 'bs'))

    merge_df = merge_dd.compute()

    # merged_chunk = barc_df.merge(bs_df, how='left', on='cmnzn', suffixes=('_barc', '_bs'))
    print_ts('jieshu')

