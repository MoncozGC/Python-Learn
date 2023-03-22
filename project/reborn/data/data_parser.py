import json


def parse():
    with open('raw_data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    ans = {}
    for i in data:
        ans[i["short"]] = {}
        ans[i["short"]]['name_en'] = i['en']
        ans[i["short"]]['name_cn'] = i['name']
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(ans, ensure_ascii=False, indent=4))


def add_population():
    with open('raw_population.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('data.json', encoding='utf-8') as json_file:
        data2 = json.load(json_file)

    for i in data.keys():
        for j in data2.keys():
            if i == data2[j]['name_en']:
                data2[j]['population'] = data[i]

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data2, ensure_ascii=False, indent=4))


def add_birth_rate():
    with open('raw_birth_data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('data.json', encoding='utf-8') as json_file:
        data2 = json.load(json_file)

    for i in data.keys():
        for j in data2.keys():
            if i == data2[j]['name_en']:
                data2[j]['birth_rate'] = data[i]

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data2, ensure_ascii=False, indent=4))


def add_position():
    with open('raw_position.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('data.json', encoding='utf-8') as json_file:
        data2 = json.load(json_file)

    for i in data.keys():
        for j in data2.keys():
            if i == data2[j]['name_cn']:
                data2[j]['position'] = data[i]

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data2, ensure_ascii=False, indent=4))
        # json_file.write(json.dumps(data2, ensure_ascii=False, indent=4).replace('    ', '').replace('\n', '').replace('\n\r', ''))

def add_continent():
    with open('raw_continent.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    with open('data.json', encoding='utf-8') as json_file:
        data2 = json.load(json_file)

    for i in data:
        for j in data2.keys():
            if j == i['country_code']:
                data2[j]['continent'] = i['continent_name']

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data2, ensure_ascii=False, indent=4))


def test():
    with open('data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for i in data.keys():
        if 'position' not in data[i].keys():
            print(i)
        if 'population' not in data[i].keys():
            print(i)
        if 'birth_rate' not in data[i].keys():
            print(i)
        if 'continent' not in data[i].keys():
            print(i)


def get_country_proportion():
    with open('data.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    result = []
    total_birth = 0
    for key in data.keys():
        birth_of_year = data[key]['population'] * data[key]['birth_rate']
        total_birth += birth_of_year
        # if key == 'CN':
        #     a = 0
    result.append({
        'total_birth': total_birth
    })
    for key in data.keys():
        temp = {}
        birth_of_year = data[key]['population'] * data[key]['birth_rate']
        temp['cn'] = data[key]['name_cn']
        temp['en'] = data[key]['name_en']
        temp['continent'] = data[key]['continent']
        temp['position'] = data[key]['position']
        temp['birth_rate'] = round(birth_of_year / total_birth * 100, 4)
        result.append(temp)
        with open('result.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(result, ensure_ascii=False, indent=4))
            # json_file.write(json.dumps(result, ensure_ascii=False, indent=4).replace('    ', '').replace('\n', '').replace('\n\r', ''))
    # a = 0
    # for i in result[1:]:
    #     a += i['birth_rate']
    # print(a)


if __name__ == '__main__':
    parse()
    add_population()
    add_birth_rate()
    add_position()
    add_continent()
    test()
    get_country_proportion()