from rest_framework import serializers


class RainfallDataSerializer(serializers.Serializer):
    """
    계량기별 강우량 데이터 시리얼라이저
    """

    raingauge_name = serializers.CharField(max_length=50)
    sum_rain_fall = serializers.FloatField()


class SeoulOpenDataSerializer(serializers.Serializer):
    """
    서울시 공공데이터(평균 하수관로 수위 및 계량기별 총 강우량) 시리얼라이저
    """

    gu_name = serializers.CharField(max_length=20)
    avg_water_level = serializers.FloatField()
    raingauge_info = RainfallDataSerializer(many=True)
