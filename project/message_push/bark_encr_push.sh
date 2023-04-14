#!/usr/bin/env bash
# bark 加密推送

set -e

message=$1
group_name=$2
sound=$3
icon_name=$4
icon_url="https://gitee.com/Jadeqi/python-learn/raw/master/project/message_push/datas/${icon_name}"


# bark key
deviceKey=$5
# push payload
# 将message引起来, 让curl解析
json='{
    "title":"加密消息",
    "body": "'${message//,/\\,}'",
    "group": "'${group_name//,/\\,}'",
    "sound": "'${sound//,/\\,}'",
    "icon": "'${icon_url//,/\\,}'"
    }'

# 必须16位
# 从配置文件中获取key和iv
key=$(grep -A1 "[message_push]" ../../config.ini | grep -E "key=" | awk -F= '{print $2}')
# IV可以是随机生成的，但如果是随机的就需要放在 iv 参数里传递。
iv=$(grep -A1 "[message_push]" ../../config.ini | grep -E "iv=" | awk -F= '{print $2}')

# OpenSSL 要求输入的 Key 和 IV 需使用十六进制编码。
key=$(printf $key | xxd -ps -c 200)
iv=$(printf $iv | xxd -ps -c 200)

ciphertext=$(echo -n $json | openssl enc -aes-128-cbc -K $key -iv $iv | base64 | tr -d '\n')

# 控制台将打印 "voWZZZaTLNVOHwLC1JOyEdF55fOrIHAkuueEKYLqvI5Pn6MRywXd+3U1ocIomGNt"
#echo $ciphertext

# 密文可能有特殊字符，所以记得 URL 编码一下。
curl --data-urlencode "ciphertext=$ciphertext" --data-urlencode "iv=$(grep -A1 "[message_push]" ../../config.ini | grep -E "iv=" | awk -F= '{print $2}')" https://api.day.app/$deviceKey