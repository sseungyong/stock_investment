import pandas as pd
import requests
from io import BytesIO
import datetime
from datetime import datetime as dt


# 일일 거래 정보 불러오는 함수
# 정보 = [년/월/일(거래일),종가,대비,거래량(주),거래대금(원),시가,고가,저가,시가총액(백만),상장주식수(주)]
def get_daily_price(isu_code, fromdate=None, todate=None):
    assert type(isu_code) == str and len(isu_code) == 12, print('isu_code must be string of length 12')
    
    # 조회일 시작일과 끝일을 지정해주지 않으면 최근 일주일간 데이터 조회
    if fromdate == None:
        fromdate = (dt.now() - datetime.timedelta(days=7)).strftime('%Y%m%d')
    else:
        assert type(fromdate) == int or len(fromdate) == 8, print('length must be 8 as YYYYMMDD')
        fromdate = str(fromdate)
            
    if todate == None:
        todate = dt.now().strftime('%Y%m%d')
    else:
        assert type(todate) == int or len(todate) == 8, print('todate length must be 8 as YYYYMMDD')
        todate = str(todate)
    
    # marketdata.krx 에  종목 정보 조회 요청
    otp_req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    query_str_parms = {
        'name' : 'fileDown',
        'filetype' : 'csv',
        'url' : 'MKD/04/0402/04020100/mkd04020100t3_02',
        # 'isu_cdnm' : '005930',
        # 'isu_cd' : 'KR7005930003',
        # 'isu_nm' : '삼성전자',
        # 'isu_srt_cd' : 'A005930',
        'isu_cd' : isu_code,
        'fromdate' : fromdate,
        'todate' : todate
    }
    try:
        dpr = requests.get(otp_req_url, query_str_parms)
    except:
        print('failed to request OTP')
        raise

    # marketdata.krx에서 종목 data 받기
    down_req_url = 'http://file.krx.co.kr/download.jspx'
    headers = {
        'Referer' : 'http://marketdata.krx.co.kr/mdi'
    }
    form_data = {
        'code' : dpr.content
    }
    try:
        dpd = requests.post(down_req_url, form_data, headers=headers)
    except:
        print('failed to download')
        raise

    # 다운로드한 정보를 dataframe 으로 변환
    daily_price_df = pd.read_csv(BytesIO(dpd.content))
    daily_price_df = daily_price_df.sort_index(ascending=False).reset_index(drop=True)

    return daily_price_df


# 연도로 조회
def get_year_price(isu_code, fromyear=None, toyear=None):
    assert type(isu_code) == str and len(isu_code) == 12, print('isu_code must be string of length 12')
    
    # 조회일 시작년과 끝년을 지정해주지 않으면 시작과 끝을 올해. 즉, 올해 데이터만 조회
    if fromyear == None:
        fromyear = dt.now().year
    else:
        assert type(fromyear) == int and fromyear >= 2000 and fromyear < dt.now().year, print('fromyear must be int of length 4, YYYY')
        fromyear = fromyear
            
    if toyear == None:
        toyear = dt.now().year
    else:
        assert type(toyear) == int and toyear >= 2000 and toyear < dt.now().year, print('toyear length must be string of length 4, YYYY')
        toyear = toyear

    fromdate = str(fromyear) + '0101'
    todate = str(fromyear) + '1231'
    annual_df = get_daily_price(isu_code, fromdate, todate)

    for year in range(fromyear + 1, toyear + 1):
        fromdate = str(year) + '0101'
        todate = str(year) + '1231'
        df = get_daily_price(isu_code, fromdate, todate)
        annual_df = annual_df.append(df, ignore_index=True)
    
    return annual_df


code = 'KR7005930003'  # 삼성전자 code 주의 >> 6자리,7자리 코드/종목명으로는 조회가 안됨....왜죠???
# ddf = get_daily_price(code, '20110101', '20111231')
ydf = get_year_price(code, 2011, 2015)  # 2011~ 2015 년까지 삼성전자 정보
print(ydf)