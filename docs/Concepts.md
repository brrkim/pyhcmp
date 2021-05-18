# Concepts of Plugin Architecture
```
-------------
|           |
|           | 
|   CORE    | ------------- [plugin 1]
|           | |  Plug-in  | [plugin 2]
|           | | Standards |    ...
------------- ------------- [plugin n]

* CORE: 어떻게 동작하는지와 기본 비즈니스 로직을 정의. 워크플로우.
* Plug-in modules: stand-alone. 독립적인 컴포넌트. 코어 기능 확장을 위한 커스텀 코드
* 중복 최소화, 표준화된 방식으로 커뮤니케이션. 하나의 단일 구조를 가져야함
* 모든 기능이 플러그인화 될 수는 없음. 공통 기능 검토 및 플러그인 대상인지 검토 필요

```

- ${Provider}의 ${Service}를 ${Driver}로 ${Action}한다
- ${Provider+Zone}의 ${Service}를 ${Action}한다
- ${Provider}의 ${Zone}의 ${Service}를 ${Action}한다

# 연동방식

- API
  - REST
  - RESTFUL
  - SOAP
  - JSONRPC
  - gRPC
- SDK
- CDK

# 연동규격

1. KT Cloud
   1. DX존 --> API|CDK|SDK 중에 상속
      1. 컴퓨팅 ---> 인터페이스 (하위는 알아서 구현이지만 강제)
         1. 서버
            1. 생성
            2. 조회
            3. 수정
            4. 삭제
         2. 네트워킹
      2. 네트워크
         1. 서브넷
   2. G1존
      1. 컴퓨팅
         1. 서버
         2. 네트워킹
      2. 네트워크
         1. 서브넷
   3. G2존
      1. 컴퓨팅
         1. 서버
         2. 네트워킹
      2. 네트워크
         1. 서브넷
   4. 공공존
      1. 컴퓨팅
         1. 서버
         2. 네트워킹
      2. 네트워크
         1. 서브넷
   5. 엔터시큐
   6. ...



# AWS

1. AWS
   1. 리전&존
      1. 컴퓨트
         1. EC2
      2. 네트워크
         1. VPC
         2. 서브넷
      3. ...
   2. 