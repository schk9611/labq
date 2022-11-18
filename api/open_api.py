import json, requests

from datetime import datetime, timedelta

from .utils import URL, KEY, TYPE


class RainfallOpenAPI:

    SERVICE = "ListRainfallService"
    START_INDEX = 1
    END_INDEX = 100

    def get_rainfall_data(GU_NAME):
        try:
            url = (
                URL
                + f"/{KEY}/{TYPE}/{RainfallOpenAPI.SERVICE}/{RainfallOpenAPI.START_INDEX}/{RainfallOpenAPI.END_INDEX}/{GU_NAME}"
            )

            res = requests.get(url)
            data = json.loads(res.content)
            return data["ListRainfallService"]["row"], None
        except KeyError:
            return None, "서울시 해당지역의 공공데이터를 찾지 못했습니다."


class DrainPipeOpenAPI:
    SERVICE = "DrainpipeMonitoringInfo"
    START_INDEX = 1
    END_INDEX = 1000

    def get_drainpipe_data(CODE):
        try:
            NOW = datetime.now()
            BEFORE_ONE_HOUR = (NOW - timedelta(hours=1)).strftime("%Y%m%d%H")

            url = (
                URL
                + f"/{KEY}/{TYPE}/{DrainPipeOpenAPI.SERVICE}/{DrainPipeOpenAPI.START_INDEX}/{DrainPipeOpenAPI.END_INDEX}/{CODE}/{BEFORE_ONE_HOUR}/{BEFORE_ONE_HOUR}"
            )

            res = requests.get(url)
            data = json.loads(res.content)
            return data["DrainpipeMonitoringInfo"]["row"], None
        except KeyError:
            return None, "서울시 해당지역의 공공데이터를 찾지 못했습니다."
