import os


URL = "http://openAPI.seoul.go.kr:8088"
KEY = os.environ.get("AUTHENTICATION_KEY")
TYPE = "json"


class GubnCode:
    def get_gubn_code(gubn):
        gubn_dict = {
            "종로": "01",
            "중": "02",
            "용산": "03",
            "성동": "04",
            "광진": "05",
            "동대문": "06",
            "중랑": "07",
            "성북": "08",
            "강북": "09",
            "도봉": "10",
            "노원": "11",
            "은평": "12",
            "서대문": "13",
            "마포": "14",
            "양천": "15",
            "강서": "16",
            "구로": "17",
            "금천": "18",
            "영등포": "19",
            "동작": "20",
            "관악": "21",
            "서초": "22",
            "강남": "23",
            "송파": "24",
            "강동": "25",
        }
        code = gubn_dict.get(gubn, None)
        if not code:
            return None, f"{gubn}구 지역은 존재하지 않습니다."
        return code, None
