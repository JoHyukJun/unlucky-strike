# web
### Author: Jo Hyuk Jun
#
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/JoHyukJun/web)
#


## Introduction
This project is being developed using Python and is aimed at creating web apps.
#
## Information
- Current website address: www.unluckystrike.com
#
## Knowledge
### JWT(Json Web Token)

> Structure: xxx.yyy.zzz (header.payloader.signature)
>> header
>>> - alg: 해싱 알고리즘 
>>> - typ: 토큰 타입 -> jwt 

```
{
  "alg": "HS512",
  "typ": "JWT"
}
```

>> payload
>>> - 클레임(OPTIONAL)
>>> - sub: 제목
>>> - aud: 대상자
>>> - iss: 발급자
>>> - exp: 만료시간
>>> - iat: 발급시간
```
{
  "sub": "1234567890",
  "name": "Jo Hyuk Jun",
  "admin": true,
  "iat": 1516239022
}
```

>> signature
```
HMACSHA512(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  your-512-bit-secret
)
```

> 장점
>> - 정보를 payloader 에 전달하기 때문에 서버상의 저장공간을 차지 하지 않음.
>> - 쿠키를 사용하는 취약점 보완.

> 단점
>> - 정보가 많아지면 네트워크 트레픽 부화됨.
>> - payloader가 base64 로 인코딩됨.(탈취후 디코딩 가능성) -> exp 설정

### ORM(Object Relation Mapping)

> - Object와 관계형 DB 데이터 매핑하는 매게체 역할
> - Object 와 DB
> - 장점
>> - 비즈니스 로직에 집중에 도움됨.(클래스와 메소드를 통한 DB 컨트롤 + 코드라인 감소 + 코드 가독성 상승 + 객체지향적)
>> - 유지보수성(DBMS에 독립적 + 마이그레이션)
> - 단점
>> - 설계 오류시 서비스에 치명적(속도 저하 등)

### REST(Representational State Transfer) API

> - HTTP URI(Uniform Resource Identifier)를 통해 자원(Resource) 명시 -> HTTP Method(POST, GET, UPDATE, DELETE) -> 해당 URI에 대한 CRUD(CREATE, READ, UPDATE, DELETE) OP 수행.
> - Structure
>> - Resource: HTTP URI
>> - Verb: HTTP Method(GET, POST, UPDATE, DELETE)
>> - Representations: HTTP Message pay load
> - Features
>> - Server-Client
>> - Stateless
>> - Cacheable
>> - Layered system
>> - Uniform interface
> - 장점
>> - HTTP 프로토콜 인프라 사용하여 별도의 인프라 구축 필요 없음.
>> - 플랫폼 독립적
>> - 서버, 클라이트 역할 분리(빠른 배포와 개발)
>- 단점
>> - HTTP Method 자체의 한계
>> - 표준의 부재

### HTTP(Hyper Text Transfer Protocol)

> - 서버, 클라이언트 모델을 따라 데이터를 주고 받기 위한 프로토콜
> - PORT: 80
> - TCP/IP(애플리케이션 레벨)
> - Method, Path, Headers, Body
> - 평문 전송

<img src="https://mdn.mozillademos.org/files/13673/HTTP%20&%20layers.png" title="http layers" alt="http layers" width="50%">

### HTTPS(Hyper Text Transfer Protocol Secure)

> - HTTP + Secure Layer
> - PORT: 443
> - 대칭키 암호화
>> - 클라이언트와 서버 동일한 키를 이용해 암,복호화 수행.
>> - 속도가 빠르지만 키가 노출될 위험 존재.
> - 비대칭키 암호화
>> - 공개키와 개인키가 존재하여 암,복호화 수행.
> - HTTPS 에서 첫 세션키 생성시에는 비대칭키 암호화 수행하며 이 후에는 만들어진 세션키를 대칭키로 사용해 암,복호화 수행.