# 读取文件
import re

if __name__ == '__main__':
    # fo = open("hydee.INI", "r+")
    # print("文件名为: ", fo.name)
    key = ['ServerName=', 'hostname=', 'port=']

    with open("hydee.INI") as f:
        content = " ".join([l.rstrip() for l in f])
    print(content)
    #
    # pattern = r"ServerName="
    # m = re.search(pattern, content)
    # print(m)

    # 关闭文件
    # fo.close()

    str = 'ServerName="xxxx" mac="5405DB7CD282" dock_mac="5405DB7CD283" UUID="79AB03CEF59F4CBBB99A5405DB7CD282" model="G46ZD_A" partno="45M1TUM7A04"'
    regx = '(?<=ServerName=").[a-zA-z0-9_.]*'
    findall = re.findall(regx, str)
    print(findall)
