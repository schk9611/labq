import re, statistics, datetime

from itertools import groupby
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import GubnCode
from .open_api import DrainPipeOpenAPI, RainfallOpenAPI
from .serializers import SeoulOpenDataSerializer


class SeoulOpenDataVeiw(APIView):
    """
    query param: gubn
    return: json
    detail: 구(지역) 이름을 입력받으면 서울시 하수관, 강우량 데이터를 수집/가공하여 결합된 데이터를 반환합니다.
    """

    def get(self, request):
        try:
            gubn = request.GET.get("gubn", None)
            if not gubn:
                return Response({"detail": "구이름을 입력하세요."}, status=400)

            """
            구(지역)의 이름을 확인하고 매칭되는 구분코드를 가져옵니다.
            """
            code, err = GubnCode.get_gubn_code(gubn)
            if err:
                return Response({"detail": err}, status=400)

            """
            서울시 해당 구(지역)의 하수관로 수위 데이터를 가져옵니다.
            """
            drain_pipe_data, err = DrainPipeOpenAPI.get_drainpipe_data(code)
            if err:
                return Response({"detail": err}, status=400)

            """
            하수관로 수위 데이터에서 구(지역)의 이름을 가져옵니다.
            """
            gu_name = drain_pipe_data[0].get("GUBN_NAM", None)
            if not gu_name:
                return Response({"detail": f"서울시 {gu_name}구의 공공데이터가 존재하지 않습니다."}, status=400)

            """
            서울시 해당 구(지역)의 강우량 데이터를 가져옵니다.
            """
            rainfall_data, err = RainfallOpenAPI.get_rainfall_data(gu_name)
            if err:
                return Response({"detail": err}, status=400)

            """
            최근 1시간을 기준으로 서울시 해당 구(지역)의 하수관로 수위 데이터의 평균값을 구합니다.
            """
            latest_one_hour_drainpipe_level = round(
                statistics.mean([i["MEA_WAL"] for i in drain_pipe_data]), 2
            )

            """
            최근 1시간을 기준으로 서울시 해당 구(지역)의 강우량 데이터를 RAINGAUGE_NAME 단위로 가공하고,
            RAINGAUGE별로 강우량의 총 합계를 구합니다.
            """
            rainfall_groupby_raingauge = groupby(
                sorted(rainfall_data, key=lambda x: x["RAINGAUGE_CODE"]),
                lambda x: x["RAINGAUGE_NAME"],
            )
            rainfall_by_raingauge_dict = {
                i: round(
                    sum(
                        map(
                            lambda x: float(x["RAINFALL10"])
                            if re.sub("[-:\s]", "", x["RECEIVE_TIME"])[:10]
                            == (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime(
                                "%Y%m%d%H"
                            )
                            else 0,
                            j,
                        )
                    ),
                    2,
                )
                for i, j in rainfall_groupby_raingauge
            }
            rainfall_by_raingauge = []

            for i, j in rainfall_by_raingauge_dict.items():
                rainfall_by_raingauge.append({"raingauge_name": i, "sum_rain_fall": j})

            """
            서울시 Open API의 데이터를 수집/가공하여 만든 새로운 공공데이터입니다.
            """
            data = {
                "gu_name": gu_name,
                "avg_water_level": latest_one_hour_drainpipe_level,
                "raingauge_info": rainfall_by_raingauge,
            }

            """
            Serializer를 활용하여 데이터의 Validation 여부를 체크합니다.
            """
            serializer = SeoulOpenDataSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data, status=200)

            return Response(serializer.errors, status=400)

        except KeyError:
            return Response({"detail": f"서울시 {gubn}구의 공공데이터 조회를 실패했습니다."}, status=400)
