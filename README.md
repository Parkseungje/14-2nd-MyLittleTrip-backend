# mylittletrip
---

## 마이리얼트립
-  [myrealtrip](https://www.myrealtrip.com/)  사이트

## 팀원
- Front-end: 김병준, 김현지, 이승윤
- Back-end: 박승제, 백승찬, 장규석

## 개발 기간
- 기간: 2020.11.30 ~ 2020.12.11 (11일)

## 적용 기술
- Front-end: React.js(Class), React-router, React-slick, SASS
- Back-end: Django, Python, MySQL, jwt, bcrypt

## 구현 기능

## 영상
(완성 후 등록 예정)

## 개인 역할

`박승제`
-
`백승찬`
-
`장규석`
-
## 소감 및 후기
- 박승제:
- 백승찬:
- 장규석:
## 레퍼런스
- 이 프로젝트는 [myrealtrip](https://www.myrealtrip.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.

## 초기세팅 방법

### 가상환경 생성(miniconda3)
```
conda create -n 'mylittletrip' python=3.8
conda activate mylittletrip
```
### requirment.txt로 자동 모듈 설치
```
pip install -r requirments.txt
```

### my_settings.py 형식:
```
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '데이터베이스이름',
        'USER': 'root',
        'PASSWORD': '비밀번호',
        'HOST': '아이피주소',
        'PORT': '포트번호',
    }
}

SECRET_KEY = '시크릿키 비밀번호'
```
