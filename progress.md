## Get Stock Information

#### 1. KRX 상장기업지원 서비스
- https://kasp.krx.co.kr/index.jsp
- http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng?code='종목코드'
- 정보를 xml 파일로 받아 올 수 있다.
- 받을 수 있는 정보
    : 10일간의 전체적 정보 ['day_date', 'code', 'day_low', 'day_high', 'day_start', 'day_endprice', 'day_dungrak', 'day_getdebi', 'day_volume', 'day_getamount']
    : 최근 10건 거래내용 ['time', 'negoprice', 'Dungrak', 'Debi', 'sellprice', 'buyprice', 'amount']
- 장점 : 한 페이지에 필요한 정보가 있다.
- 단점 : 숫자 정보가 string(,가 포함된)으로 들어온다.


#### 2. KOSCOM 개발자 센터
- https://developers.koscom.co.kr/
- 시도 해보지 못함! why? 회사명/대표자/사업자등록번호 필요


#### 3. 한국예탁결제원(seibro.or.kr)_주식정보서비스
- https://www.data.go.kr/dataset/15001145/openapi.do


### issue
한국거래소 자본시장 정보데이터 종합센터 구축한다...오픈API 도입 등 정보사업 확대
발행일 : 2019.07.14
http://www.etnews.com/20190712000242