# house

#### 基础url: http://www.yuejuweb.com

# api

路径前缀: /wechatapi/0


### 房源列表

***

#### path: /houses/
#### method: get
#### 参数:

|参数|类型|示例|说明|
|:-------------:|:-------------:|:-------------:|:-------------:|
|page|int|1|当前页|
|page_size|int|10|每页记录数|
|keywords|str|"武昌"|搜索关键词|
|area|str|"武昌"|位置|
|start_price|int|10|开始价格范围，500， 600|
|end_price|int|10|结束价格范围，没有则不传|
|waytorent|str|"整租"|租赁方式|

#### 返回示例:
```python
{
    "data": {
        "housingresources_count": 3,
        "page_size": 5,
        "page": 1,
        "housing_resources": [
            {
                "cover": "http://oxaoo4ur4.bkt.clouddn.com/yueju/cover_1518785074.png",
                "housing_resources_id": 81,
                "community": "小区",
                "content": "ceshi1111",
                "month_rent": 1212,
                "lease": "整租"
            },
            {
                "cover": "",
                "housing_resources_id": 82,
                "community": "小区名称",
                "content": "测试2",
                "month_rent": 100,
                "lease": "整租"
            },
            {
                "cover": "",
                "housing_resources_id": 83,
                "community": "小区",
                "content": "描述111",
                "month_rent": 100,
                "lease": "整租"
            }
        ]
    },
    "error_code": 0,
    "error_msg": "请求成功"
}
```

#### 返回参数
|参数|类型|示例|说明|
|:-------------:|:-------------:|:-------------:|:-------------:|
|housingresources_count|int|1|总记录数|
|housing_resources_id|int|0|房源id|
|cover|str|0|封面图|
|community|str|""|小区名称|
|content|str|""|房屋描述|
|month_rent|int|0|租金|
|lease|str|""|租赁方式|




### 房源详情

***

#### path: /house/
#### method: get
#### 参数:

|参数|类型|示例|说明|
|:-------------:|:-------------:|:-------------:|:-------------:|
|housing_resources_id|int|1|房源id|

#### 返回示例:
```python
{
    "data": {
        "house": {
            "category": "12",
            "direction": "西",
            "buy": "",
            "layer": 12,
            "area": "武昌区",
            "bus": "",
            "total_layer": 21,
            "cover": "http://oxaoo4ur4.bkt.clouddn.com/yueju/cover_1518785074.png",
            "housing_resources_id": 81,
            "community": "小区",
            "sitting_room_area": 12,
            "content": "ceshi1111",
            "subway": "",
            "address": "街道",
            "pictures": ["http:1212.jpg", "http://122.jp"],
            "month_rent": 1212,
            "bet": 1,
            "pay": 0.5,
            "infrastructures": [{
                "infrastructure_id": 1,
                "name": "浴缸",
                "cover": "http://121212.jpg",
            },],
            "lease": "整租"
        }
    },
    "error_code": 0,
    "error_msg": "请求成功"
}
```
#### 返回参数
|参数|类型|示例|说明|
|:-------------:|:-------------:|:-------------:|:-------------:|
|housing_resources_id|int|0|房源id|
|cover|str|0|封面图|
|community|str|""|小区名称|
|content|str|""|房屋描述|
|month_rent|int|0|租金|
|lease|str|""|租赁方式|
|category|str|""|房屋类型|
|direction|str|""|房屋朝向|
|buy|str|""|附近商场|
|layer|int|0|所在楼层|
|area|str|""|所在区|
|bus|str|""|附近公交|
|total_layer|int|10|总楼层|
|sitting_room_area|float|12.3|客厅面积|
|subway|str|""|附近地铁|
|address|str|""|地址|
|pictures|list|['', '']|房源图片|
|infrastructures|list|[{}]|基础设施|
|infrastructure_id|int|0|房源基础设置id|
|bet|float|0|押|
|pay|float|0|付|




### 求租列表

***

#### path: /rent_houses/
#### method: get
#### 参数:

|参数|类型|示例|说明|
|:-------------:|:-------------:|:-------------:|:-------------:|
|page|int|1|当前页|
|page_size|int|10|每页记录数|
|keywords|str|"武昌"|搜索关键词|
|area|str|"武昌"|位置|
|start_price|int|10|开始价格范围，500， 600|
|end_price|int|10|结束价格范围，没有则不传|
|waytorent|str|"整租"|租赁方式|

#### 返回示例:
```python
{
    "data": {
        "rent_houses": [
            {
                "description": "要门面用来做生意",
                "avatar": "",
                "rent": 0,
                "infrastructures": [
                    {
                        "name": "1212a阿斯顿发",
                        "infrastructure_id": 1
                    }
                ],
                "rent_house_id": 153,
                "name": "刘道"
            }
        ],
        "rent_house_count": 2,
        "page": 1,
        "page_size": 10
    },
    "error_code": 0,
    "error_msg": "请求成功"
}
```

#### 返回参数
|参数|类型|示例|说明|
|:-------------:|:-------------:|:-------------:|:-------------:|
|rent_house_count|int|1|总记录数|
|rent_house_id|int|0|求租id|
|avatar|str|0|求租人头像|
|rent|int|0|租金|
|infrastructures|list|[{}]|基础设施|
|infrastructure_id|int|0|基础设置id|
|name|str|""|租客姓名|
|description|str|""|其他要求|