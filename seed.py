from app.models.mountain import Mountain

def seed_data():
    mountains = [
        {
            "name": "玉山主峰",
            "altitude": 3952,
            "location": "南投縣信義鄉、高雄市桃源區、嘉義縣阿里山鄉交界",
            "description": "台灣第一高峰，百岳之首。主峰四面皆是陡壁危崖，南北兩側是千仞峭壁，西側絕壑深溝，東側則是碎石陡坡。玉山不僅是台灣的最高峰，也是東北亞第一高峰。",
            "safety_warning": "近期午後常有雷陣雨，請注意保暖與防雨。排雲山莊目前供水正常，但仍建議攜帶足夠飲水。",
            "equipment_list": "- 頭燈及備用電池\n- 兩截式雨衣褲\n- 登山杖\n- 保暖衣物\n- 行動糧與水\n- 個人急救包",
            "trail_timeline": "D1:\n08:00 塔塔加登山口起登\n10:00 孟祿亭\n14:00 排雲山莊 (宿)\n\nD2:\n02:30 排雲山莊出發\n04:30 碎石坡\n05:30 玉山主峰 (看日出)\n07:30 排雲山莊\n12:00 塔塔加登山口"
        },
        {
            "name": "雪山主峰",
            "altitude": 3886,
            "location": "台中市和平區與苗栗縣泰安鄉交界",
            "description": "台灣第二高峰。以著名的雪山圈谷聞名，是台灣冰河遺跡的代表之一。冬季時常有積雪，是台灣熱門的雪季攀登路線。",
            "safety_warning": "黑森林路段容易迷路，請務必結伴同行並攜帶離線地圖。目前無積雪，但夜間氣溫仍低。",
            "equipment_list": "- 基本登山裝備\n- 離線地圖設備\n- 足夠的保暖衣物\n- 岩盔 (經過黑森林及圈谷時建議配戴)",
            "trail_timeline": "D1:\n09:00 雪山登山口\n11:00 七卡山莊\n15:00 三六九山莊 (宿)\n\nD2:\n03:00 三六九山莊出發\n04:30 黑森林營地\n06:00 圈谷底部\n07:30 雪山主峰\n09:30 三六九山莊\n14:00 雪山登山口"
        },
        {
            "name": "合歡山主峰",
            "altitude": 3417,
            "location": "南投縣仁愛鄉",
            "description": "最平易近人的百岳之一，步道平緩好走，適合新手與家庭健行。山頂視野遼闊，可遠眺奇萊連峰、南湖大山等著名山岳。",
            "safety_warning": "雖為大眾路線，但仍處於高海拔，請注意防範高山症。午後容易起霧，建議早上前往。",
            "equipment_list": "- 輕裝背包\n- 防風保暖外套\n- 飲用水及行動糧\n- 遮陽帽及防曬用品",
            "trail_timeline": "09:00 登山口出發\n09:30 觀景台\n10:30 合歡主峰三角點\n11:30 回到登山口"
        }
    ]

    for m in mountains:
        Mountain.create(m)
    print("Seed data inserted successfully.")

if __name__ == '__main__':
    seed_data()
