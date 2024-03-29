# -*- coding:utf-8 -*-
# Author: MoncozGC
# Date  : 2023/4/13
# Desc  : 豆瓣电影信息爬取
import requests


def rep_movie():
    """
    通过接口信息获取
    """
    url = 'https://movie.douban.com/j/chart/top_list?type=13&interval_id=100:90&action=&start=40&limit=20'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"
    }
    param = {
        "type": 13,
        "interval_id": '100:90',
        'action': '',
        'start': 0,
        'limit': 20
    }

    requests_get = requests.get(url=url, headers=header, params=param)
    # 获取到json数据
    get_text = requests_get.json()

    return get_text


def data_parse(text):
    """
    数据解析
    """
    for mov in text:
        print("电影名称: " + mov['title'])
        print("演员名称: %s" % mov['actors'])
        print("制片国家: " + ', '.join(mov['regions']))
        print("影片类型: " + ', '.join(mov['types']))
        print("上映日期: " + mov['release_date'])
        print("豆瓣评分: " + mov['score'])
        print("短评数量: %d" % mov['vote_count'])
        print("#####################################################")


def test_data():
    """
    测试数据
    """
    return [
        {"rating": ["8.8", "45"], "rank": 41, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2555762374.jpg", "is_playable": 'true', "id": "1296339",
         "types": ["剧情", "爱情"], "regions": ["美国", "奥地利", "瑞士"], "title": "爱在黎明破晓前", "url": "https:\/\/movie.douban.com\/subject\/1296339\/", "release_date": "1995-01-27",
         "actor_count": 18, "vote_count": 664704, "score": "8.8",
         "actors": ["伊桑·霍克", "朱莉·德尔佩", "安德莉亚·埃克特", "汉诺·波西尔", "卡尔·布拉克施魏格尔", "特克斯·鲁比诺威茨", "埃尔尼·曼戈尔德", "多米尼克·卡斯特尔", "海蒙·玛丽亚·巴汀格", "哈拉尔德·魏格莱因", "汉斯·魏因加特纳", "彼得·艾利·休默", "休伯特·法比安·库尔特勒",
                    "约翰·斯洛斯", "克里斯蒂安·安科维奇", "亚当·戈德堡", "保罗·波伊特", "金·克里桑"], "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 42, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2070153774.jpg", "is_playable": 'true', "id": "10577869",
         "types": ["喜剧", "爱情", "奇幻"], "regions": ["英国"], "title": "时空恋旅人", "url": "https:\/\/movie.douban.com\/subject\/10577869\/", "release_date": "2013-09-04", "actor_count": 44,
         "vote_count": 648358, "score": "8.8",
         "actors": ["多姆纳尔·格里森", "瑞秋·麦克亚当斯", "比尔·奈伊", "莉迪亚·威尔逊", "琳赛·邓肯", "理查德·科德里", "约书亚·麦圭尔", "汤姆·霍兰德尔", "玛格特·罗比", "维尔·梅里克", "凡妮莎·柯比", "汤姆·休斯", "哈利·海顿-佩顿", "米切尔·马伦", "丽莎·艾科恩",
                    "珍妮·莱恩斯福德", "菲利普-沃斯", "凯瑟琳·斯戴曼", "汤姆·斯托顿", "安部春香", "李·阿斯奎斯-柯", "理查德·班克斯", "保罗·布莱克维尔", "贝恩·科拉科", "格拉姆·柯里", "罗薇娜·戴蒙德", "约翰·达根", "迪诺·法赞尼", "内芙·加切夫", "理查德·E·格兰特",
                    "理查德·格雷弗斯", "李·尼古拉斯·哈里斯", "理查德·赫德曼", "李仙湖", "马修·C·马蒂诺", "马汀·麦格", "艾莉克丝·摩尔", "艾薇·维", "艾莎·哈特", "黛博拉·罗桑", "弗朗西斯卡·祖琪妮", "朱莉·沃洛诺", "阿曼达·伦贝里", "尼可拉·芬恩"],
         "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 43, "cover_url": "https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p854757687.jpg", "is_playable": 'true', "id": "1292274",
         "types": ["喜剧", "剧情", "爱情"], "regions": ["美国"], "title": "幸福终点站", "url": "https:\/\/movie.douban.com\/subject\/1292274\/", "release_date": "2005-01-14", "actor_count": 53,
         "vote_count": 557435, "score": "8.8",
         "actors": ["汤姆·汉克斯", "凯瑟琳·泽塔-琼斯", "斯坦利·图齐", "齐·麦克布赖德", "迭戈·卢纳", "巴里·沙巴卡·亨利", "库玛·帕拉纳", "佐伊·索尔达娜", "埃迪·琼斯", "祖德·塞克利拉", "科瑞·雷诺兹", "古列雷莫·迪亚兹", "里尼·贝尔", "瓦列里·尼古拉耶夫", "迈克尔·诺里",
                    "鲍勃·莫里西", "萨沙·斯皮尔伯格", "苏珊·索洛米", "卡尔利斯·布克", "斯蒂芬·富勒", "丹·芬纳蒂", "Lydia Blanco", "肯尼斯·崔", "卡斯·安瓦尔", "康拉德·皮拉", "杜桑恩·杜基齐", "马克·伊瓦涅", "Benny Golson", "斯科特·安第斯",
                    "罗伯特·科瓦吕比亚", "Dilva Henry", "卡尔艾拉切", "哈亚提·阿克巴斯", "艾力克斯·伯恩斯", "埃莱娜·卡多纳", "Dan Chase", "查得·R·戴维斯", "安东内拉·埃莉亚", "Michael Eliopoulos", "Marston Fobbs", "Riad Galayini",
                    "杰拉德·加纳", "贾斯汀·罗杰斯豪尔", "Mohammed Hassan", "Amber Havens", "Ksenia Jarova", "巴里·朱利安", "Svilena Kidess", "Zuzana Monroe", "艾丽西亚·奥奇瑟", "本杰明·奥切恩格", "梅尔·罗德里格斯", "阿尼·萨瓦"],
         "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 44, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p792502535.jpg", "is_playable": 'true', "id": "3726072",
         "types": ["剧情", "动作", "爱情"], "regions": ["中国香港", "中国大陆", "中国台湾"], "title": "东邪西毒：终极版", "url": "https:\/\/movie.douban.com\/subject\/3726072\/", "release_date": "2009-03-26",
         "actor_count": 11, "vote_count": 193020, "score": "8.8", "actors": ["张国荣", "林青霞", "梁朝伟", "张学友", "张曼玉", "刘嘉玲", "梁家辉", "杨采妮", "白丽", "廖静妮", "王家卫"], "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 45, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2797313535.jpg", "is_playable": 'true', "id": "1295865",
         "types": ["剧情", "爱情", "战争", "西部"], "regions": ["美国"], "title": "燃情岁月", "url": "https:\/\/movie.douban.com\/subject\/1295865\/", "release_date": "1994-12-16", "actor_count": 27,
         "vote_count": 281157, "score": "8.8",
         "actors": ["布拉德·皮特", "安东尼·霍普金斯", "艾丹·奎因", "朱莉娅·奥蒙德", "亨利·托马斯", "卡琳娜·隆巴德", "坦图·卡丁诺", "高登·图托西斯", "克里斯蒂娜·皮克勒斯", "约翰·诺瓦克", "肯尼斯·威尔什", "尼格尔·本内特", "基根·麦金托什", "埃里克·约翰逊", "兰德尔·斯莱文",
                    "大卫·卡耶", "查尔斯·安德烈", "肯·科齐格", "温妮·孔", "巴特熊", "格雷格·福西特", "加里·A·赫克", "马修·罗伯特·凯利", "Sekwan Auger", "道格·休斯", "比尔·道", "罗克珊·王"], "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 46, "cover_url": "https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2351134499.jpg", "is_playable": 'true', "id": "1293964",
         "types": ["剧情", "爱情", "战争"], "regions": ["美国"], "title": "魂断蓝桥", "url": "https:\/\/movie.douban.com\/subject\/1293964\/", "release_date": "1940-05-17", "actor_count": 61,
         "vote_count": 272364, "score": "8.8",
         "actors": ["费雯·丽", "罗伯特·泰勒", "露塞尔·沃特森", "弗吉尼亚·菲尔德", "玛丽亚·彭斯卡娅", "C.奥布雷·史密斯", "Janet Shaw", "Janet Waldo", "Steffi Duna", "Virginia Carroll", "Eleanor Stewart", "Lowden Adams",
                    "Harry Allen", "Jimmy Aubrey", "Phyllis Barry", "Colin Campbell", "丽塔·卡莱尔", "里奥.G.卡罗尔", "戴维·卡文迪什", "大卫·克莱德", "汤姆·康威", "Frank Dawson", "Connie Emerald",
                    "Gilbert Emery", "赫伯特·埃文斯", "迪克·戈登", "Denis Green", "艾塞尔·格里菲斯", "Bobby Hale", "Winifred Harris", "哈利韦尔·霍布斯", "Harold Howard", "Charles Irwin", "George Kirby",
                    "Walter Lawrence", "威尔弗雷德·卢卡斯", "Dan Maxwell", "James May", "Florine McKinney", "Charles McNaughton", "Frank Mitchell", "埃德蒙·莫蒂默", "伦纳德米迪", "坦普·皮戈特", "John Power",
                    "Clara Reid", "Paul Scardon", "约翰·格雷厄姆·斯佩西", "Wyndham Standing", "哈里·斯塔布斯", "Cyril Thornton", "戴维·瑟斯比", "诺玛·威登", "帕特·威尔士", "玛莎·温特沃思", "Frank Whitbeck", "Eric Wilton",
                    "罗伯特·温克勒", "道格拉斯·伍德", "丁建华", "乔榛"], "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 47, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2357915564.jpg", "is_playable": 'true', "id": "1306249",
         "types": ["喜剧", "爱情", "古装"], "regions": ["中国香港"], "title": "唐伯虎点秋香", "url": "https:\/\/movie.douban.com\/subject\/1306249\/", "release_date": "1993-07-01", "actor_count": 33,
         "vote_count": 1055387, "score": "8.7",
         "actors": ["周星驰", "巩俐", "陈百祥", "郑佩佩", "朱咪咪", "梁家仁", "苑琼丹", "梁荣忠", "黄一山", "黄霑", "吴镇宇", "刘家辉", "蓝洁瑛", "谷德昭", "陈辉虹", "李健仁", "宣萱", "温翠苹", "朱铁和", "平田广明", "刘小芸", "李绮霞", "何英伟", "曾健明",
                    "黎彼得", "黄凤琼", "王伟梁", "贾天怡", "姜皓文", "陈家碧", "林威", "李家声", "刘锡贤"], "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 48, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2215102596.jpg", "is_playable": 'true', "id": "1307394",
         "types": ["动画", "剧情", "爱情"], "regions": ["日本"], "title": "千年女优", "url": "https:\/\/movie.douban.com\/subject\/1307394\/", "release_date": "2001-07-28", "actor_count": 25,
         "vote_count": 259013, "score": "8.8",
         "actors": ["庄司美代子", "小山茉美", "折笠富美子", "饭塚昭三", "小野坂昌也", "津田匠子", "铃置洋孝", "京田尚子", "德丸完", "片冈富枝", "石森达幸", "佐藤政道", "小形满", "麻生智久", "游佐浩二", "肥后诚", "坂口候一", "志村知幸", "木村亚希子", "佐伯志",
                    "野岛裕史", "浅野琉璃", "园部好德", "山寺宏一", "津嘉山正种"], "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 49, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1910828286.jpg", "is_playable": 'true', "id": "1291557",
         "types": ["剧情", "爱情"], "regions": ["中国香港"], "title": "花样年华", "url": "https:\/\/movie.douban.com\/subject\/1291557\/", "release_date": "2000-05-20", "actor_count": 13,
         "vote_count": 592523, "score": "8.7", "actors": ["梁朝伟", "张曼玉", "潘迪华", "萧炳林", "张耀扬", "孙佳君", "钱似莺", "顾锦华", "叶清", "陈万雷", "张同祖", "雷震", "朱连·卡邦"], "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 50, "cover_url": "https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p480956937.jpg", "is_playable": 'true', "id": "1292370",
         "types": ["剧情", "奇幻", "爱情"], "regions": ["美国"], "title": "剪刀手爱德华", "url": "https:\/\/movie.douban.com\/subject\/1292370\/", "release_date": "1990-12-06", "actor_count": 29,
         "vote_count": 1019154, "score": "8.7",
         "actors": ["约翰尼·德普", "薇诺娜·瑞德", "黛安·韦斯特", "安东尼·迈克尔·豪尔", "凯西·贝克", "罗伯特·奥利维里", "康查塔·费雷尔", "卡罗琳·阿隆", "迪克·安东尼·威廉姆斯", "澳澜·琼斯", "文森特·普莱斯", "艾伦·阿金", "苏珊·布洛马特", "约翰·戴维森", "布莱恩·拉肯",
                    "Victoria Price", "Stuart Lancaster", "Gina Gallagher", "阿隆·鲁斯汀", "阿兰·弗吉", "史蒂文·布里尔", "Peter Palmer", "马克·麦考利", "唐娜·派洛尼", "Ken DeVaul", "Kathy Dombo",
                    "Tabetha Thomas", "尼克·卡特", "布雷特·赖斯"], "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 51, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2447590313.jpg", "is_playable": 'true', "id": "1292215",
         "types": ["剧情", "喜剧", "爱情"], "regions": ["法国", "德国"], "title": "天使爱美丽", "url": "https:\/\/movie.douban.com\/subject\/1292215\/", "release_date": "2001-04-25", "actor_count": 28,
         "vote_count": 944672, "score": "8.7",
         "actors": ["奥黛丽·塔图", "马修·卡索维茨", "吕菲斯", "洛莱拉·克拉沃塔", "塞尔·梅林", "贾梅尔·杜布兹", "克洛蒂尔德·莫莱特", "克莱尔·莫里耶", "伊莎贝尔·南蒂", "多米尼克·皮侬", "阿尔蒂斯·德·彭居埃恩", "友兰达·梦露", "于尔班·康塞利埃", "莫里斯·贝尼舒", "米歇尔·罗班",
                    "安德烈·达芒", "克洛德·佩隆", "阿尔梅尔", "迪基·奥尔加多", "凯文·迪亚士", "弗洛拉·吉耶", "阿莫里·巴博尔", "欧仁·贝蒂埃", "让·达里", "马克·阿米约", "安德烈·杜索里埃", "林原惠美", "姜广涛"], "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 52, "cover_url": "https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1421018669.jpg", "is_playable": 'true', "id": "1292287",
         "types": ["动作", "爱情", "武侠", "古装"], "regions": ["中国香港", "中国大陆"], "title": "新龙门客栈", "url": "https:\/\/movie.douban.com\/subject\/1292287\/", "release_date": "2012-02-24",
         "actor_count": 21, "vote_count": 433519, "score": "8.7",
         "actors": ["张曼玉", "林青霞", "梁家辉", "甄子丹", "熊欣欣", "刘洵", "任世官", "吴启华", "袁祥仁", "徐锦江", "郑希怡", "王彤川", "王伟顺", "蔡浩", "元彬", "陈志辉", "邢金沙", "施懿", "冯雪瑞", "廖静妮", "魏晶琦"],
         "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 53, "cover_url": "https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2016401659.jpg", "is_playable": 'true', "id": "1418200",
         "types": ["剧情", "爱情"], "regions": ["法国", "英国", "美国"], "title": "傲慢与偏见", "url": "https:\/\/movie.douban.com\/subject\/1418200\/", "release_date": "2005-09-16", "actor_count": 25,
         "vote_count": 779471, "score": "8.7",
         "actors": ["凯拉·奈特莉", "马修·麦克费登", "唐纳德·萨瑟兰", "布兰达·布莱斯", "凯瑞·穆里根", "裴淳华", "吉娜·马隆", "妲露拉·莱莉", "朱迪·丹奇", "西蒙·伍兹", "克劳迪·布莱克利", "汤姆·霍兰德尔", "鲁伯特·弗兰德", "凯利·蕾莉", "皮普·托伦斯", "西妮德·马修斯",
                    "佩内洛普·威尔顿", "塔姆金·莫钦特", "利亚姆·托马斯", "Samantha Bloom", "汤姆·霍兰德", "莫亚布雷迪", "梅格·韦恩·欧文", "彼得·怀特", "Roy Holder"], "is_watched": 'false'},
        {"rating": ["9.2", "50"], "rank": 54, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1581774481.jpg", "is_playable": 'true', "id": "1298817",
         "types": ["喜剧", "爱情", "西部", "冒险"], "regions": ["美国"], "title": "淘金记", "url": "https:\/\/movie.douban.com\/subject\/1298817\/", "release_date": "1925-06-26", "actor_count": 47,
         "vote_count": 56207, "score": "9.2",
         "actors": ["查理·卓别林", "马克·斯旺", "汤姆·默里", "亨利·伯格曼", "Malcolm Waite", "乔治亚·黑尔", "Jack Adams", "Sam Allen", "Harry Arras", "艾伯特·奥斯汀", "Marta Belfort", "George Brock", "海尼·康克林",
                    "凯·德利斯", "James Dime", "Leon Farey", "Charles Force", "J.C. Fowler", "阿尔·欧内斯特·加西亚", "Inez Gomez", "希德·格鲁曼", "丽塔·格雷", "雷·格雷", "F.F. Guenste", "Jack Herrick",
                    "George Holt", "Jean Huntley", "Gladys Johnston", "Fred Karno Jr.", "Elias Lazaroff", "Joan Lowell", "Chris-Pin Martin", "Clyde McAtee", "John Millerta", "贝蒂莫里西",
                    "Florence Murth", "约翰兰德", "蒂尼·桑福德", "Frank Stockdale", "Frank Rice", "Lillian Rosine", "C.F. Roark", "Armand Triller", "John Wallace", "Tom Wood", "Ed Wilson",
                    "Bess Wade"], "is_watched": 'false'},
        {"rating": ["9.3", "50"], "rank": 55, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1339915772.jpg", "is_playable": 'true', "id": "1303418",
         "types": ["喜剧", "爱情", "战争"], "regions": ["美国"], "title": "你逃我也逃", "url": "https:\/\/movie.douban.com\/subject\/1303418\/", "release_date": "1942-03-06", "actor_count": 49,
         "vote_count": 45816, "score": "9.3",
         "actors": ["卡洛·朗白", "杰克·本尼", "罗伯特·斯塔克", "菲利克斯·布雷萨特", "莱昂内尔·阿特威尔", "斯坦利·里吉斯", "西戈·鲁曼", "查尔斯·霍尔顿", "George Lynn", "Henry Victor", "Maude Eburne", "哈利韦尔·霍布斯", "迈尔斯·曼德", "鲁道夫·安德斯",
                    "Sven Hugo Borg", "丹尼·鲍沙其", "巴斯特·布罗迪", "Alec Craig", "赫尔穆特·丹丁", "Jack Deery", "Leslie Denison", "詹姆斯·芬利森", "贝丝·弗劳尔斯", "Stuart Hall", "莱兰·霍奇森", "Shep Houghton",
                    "奥拉夫·许滕", "Charles Irwin", "Tiny Jones", "约翰·凯洛格", "Adolf E. Licho", "Wilbur Mack", "John Meredith", "Maurice Murphy", "Richard Neill", "拉斯·鲍威尔", "弗兰克·雷歇尔",
                    "Otto Reichow", "Gene Rizzi", "John Roy", "Hans Schumm", "Stephen Soldi", "Count Stefenelli", "罗兰德·瓦尔诺", "Ernö Verebes", "Dorothy Vernon", "Armand 'Curly' Wright",
                    "Wolfgang Zilzer", "汤姆·杜根"], "is_watched": 'false'},
        {"rating": ["8.7", "45"], "rank": 56, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1900812761.jpg", "is_playable": 'true', "id": "6860160",
         "types": ["剧情", "爱情", "歌舞"], "regions": ["英国", "美国"], "title": "悲惨世界", "url": "https:\/\/movie.douban.com\/subject\/6860160\/", "release_date": "2013-02-28", "actor_count": 58,
         "vote_count": 332263, "score": "8.7",
         "actors": ["休·杰克曼", "罗素·克劳", "安妮·海瑟薇", "阿曼达·塞弗里德", "萨莎·拜伦·科恩", "海伦娜·伯翰·卡特", "埃迪·雷德梅恩", "艾伦·特维特", "萨曼莎·巴克斯", "丹尼尔·赫特斯通", "约瑟夫·阿尔京", "理查德·迪克森", "安迪·比克维奇", "康姆·威尔金森", "希瑟·切森",
                    "保罗·索恩利", "迈克尔·吉普森", "凯特·弗利特伍德", "汉娜·沃丁厄姆", "博迪·卡维尔", "蒂姆·唐尼", "安德鲁·哈维尔", "丹尼尔·伊万斯", "杰甘·艾伊", "阿德里安·斯卡伯勒", "弗兰西斯·拉菲勒", "夏洛特·斯宾塞", "阿什莉·阿尔图斯", "戴维·坎恩", "波丽·坎普",
                    "伊恩·皮里", "朱利安·布里奇", "马克·皮克林", "伊莎贝尔·艾伦", "娜塔莉亚·安吉尔·华莱士", "洛蒂·斯蒂尔", "马克·多诺万", "黛安·皮尔金顿", "诺尔玛·阿塔拉", "帕特里克·戈弗雷", "理查德·科德里", "基利安·唐纳利", "乔治·布莱顿", "休·斯金纳", "阿利斯泰尔·布拉默",
                    "哈德利·弗雷泽", "林兹·黑特利", "杰玛·瓦德尔", "吉娜·贝克", "凯蒂·霍尔", "夏洛特·霍普", "艾拉·亨特", "安东尼娅·克拉克", "莎拉·弗林德", "朱莉·沃洛诺", "贝西·卡特", "乔尔·菲利莫尔", "Freya Parks"], "is_watched": 'false'},
        {"rating": ["8.8", "45"], "rank": 57, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2021127692.jpg", "is_playable": 'true', "id": "10484041",
         "types": ["剧情", "爱情"], "regions": ["日本"], "title": "横道世之介", "url": "https:\/\/movie.douban.com\/subject\/10484041\/", "release_date": "2013-02-23", "actor_count": 18,
         "vote_count": 158156, "score": "8.8",
         "actors": ["高良健吾", "吉高由里子", "池松壮亮", "伊藤步", "绫野刚", "井浦新", "国村隼", "堀内敬子", "古关安广", "余贵美子", "朝仓亚纪", "柄本佑", "江口德子", "佐津川爱美", "真岛秀和", "黑川芽以", "涩川清彦", "中岛步"], "is_watched": 'false'},
        {"rating": ["8.6", "45"], "rank": 58, "cover_url": "https://img9.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p453716305.jpg", "is_playable": 'false', "id": "1828115",
         "types": ["剧情", "爱情", "情色"], "regions": ["中国台湾", "中国大陆", "美国", "中国香港"], "title": "色，戒", "url": "https:\/\/movie.douban.com\/subject\/1828115\/", "release_date": "2007-11-01",
         "actor_count": 23, "vote_count": 779596, "score": "8.6",
         "actors": ["梁朝伟", "汤唯", "陈冲", "王力宏", "庹宗华", "朱芷莹", "高英轩", "柯宇纶", "阮德锵", "钱嘉乐", "苏岩", "何赛飞", "宋茹惠", "樊光耀", "卢燕", "刘洁", "余娅", "王琳", "王侃", "竹下明子", "阿努潘·凯尔", "唐亚俊", "韦奕波"],
         "is_watched": 'false'},
        {"rating": ["8.6", "45"], "rank": 59, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p1982176012.jpg", "is_playable": 'true', "id": "1292328",
         "types": ["剧情", "动作", "爱情", "武侠", "古装"], "regions": ["中国香港", "中国台湾"], "title": "东邪西毒", "url": "https:\/\/movie.douban.com\/subject\/1292328\/", "release_date": "1994-09-17",
         "actor_count": 14, "vote_count": 566573, "score": "8.6", "actors": ["张国荣", "林青霞", "梁朝伟", "张学友", "张曼玉", "刘嘉玲", "梁家辉", "杨采妮", "邹兆龙", "萧德虎", "廖静妮", "王祖贤", "白丽", "刘洵"],
         "is_watched": 'false'},
        {"rating": ["8.6", "45"], "rank": 60, "cover_url": "https://img2.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2570901292.jpg", "is_playable": 'true', "id": "1303394",
         "types": ["剧情", "爱情", "奇幻", "古装"], "regions": ["中国香港", "中国大陆"], "title": "青蛇", "url": "https:\/\/movie.douban.com\/subject\/1303394\/", "release_date": "1993-11-04",
         "actor_count": 11, "vote_count": 512622, "score": "8.6", "actors": ["张曼玉", "王祖贤", "赵文卓", "吴兴国", "马精武", "田丰", "刘洵", "邢金沙", "黄德仁", "冯雪瑞", "陈冬梅"], "is_watched": 'false'}]


if __name__ == '__main__':
    data = test_data()
    json_text = rep_movie()
    data_parse(json_text)
