# Lab-Q

## 프로젝트 소개

Open API 방식의 공공데이터를 수집, 가공하여 전달하는 REST API와 이를 요청하는 클라이언트 개발

<br>

## 요구사항 및 해결방안

- 서울 열린데이터 광장에서 하수관로 수위 현황과 강우량 정보 데이터를 수집

- 출력값 중 GUBN_NAM과 GU_NAME 기준으로 데이터를 결합

- 데이터는 JSON으로 전달

<br>

## API 명세서

#### 지역에 해당하는 하수구 수위와 강우량 데이터

- METHOD: GET
- URL: /api/seoul/drainpipe-rainfall/?gubn=지역명
- Request
  ```
  {}
  ```
- Response
  ```
  {
      "gu_name": "종로",
      "avg_water_level": 0.11,
      "raingauge_info": [
          {
              "raingauge_name": "종로구청",
              "sum_rain_fall": 0.0
          },
          {
              "raingauge_name": "부암동",
              "sum_rain_fall": 0.0
          }
      ]
  }
  ```
