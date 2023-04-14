-- 删除统计外日期
delete from log where datetime < '2020-01-01';
delete from log where id = '177115';

-- 验证日期是否删除正确
select min(datetime) from log;

-- 获取最晚说的话
select id,user,content, datetime, DATE_FORMAT(datetime,'%H') as h from log
where DATE_FORMAT(datetime,'%H') <= 5
order by h desc, datetime;

-- 获取最长的聊天记录
select id,datetime,MAX(length(content)) as m,content,date_format(datetime,'%Y') as year from log group by id order by m
DESC,year asc limit 10;


-- 关键字
select id,user,content, datetime from log
where content like '%爱你%';

select id,content, datetime from log
where content like '%想你%';

select id,content, datetime from log
where content like '%喜欢你%';

select id,content, datetime from log
where content like '%吃什么%';

select id,content, datetime from log
where content like '%晚安%';

select id,content, datetime from log
where content like '%哈%';

select count(1) from log
where content like '%哈%';

-- 按月分组
select count(id), date_format(datetime,"%m") as m from log
group by m;

-- 按小时分组
select count(id), date_format(datetime,"%H") as m from log
group by m;

-- 根据AM PM分组
-- AM
select count(id),date_format(datetime,"%H") as dates from log where substr(datetime,21) = 'AM'  group by dates;
-- PM
select count(id),date_format(datetime,"%H") as dates from log where substr(datetime,21) = 'PM'  group by dates;