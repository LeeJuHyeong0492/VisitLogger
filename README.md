# VisitLogger

## 프로젝트 설명

VisitLogger는 출석 체크 버튼으로 AWS의 S3, DynamoDB, SNS, CloudWatch에 모든 기록을 자동으로 기록하는 웹 애플리케이션 입니다.

---
깃허브 링크
https://github.com/LeeJuHyeong0492/VisitLogger
---

##  사용 기술 및 인프라 구성

###  Docker
- Python Flask 앱을 Docker 이미지로 빌드
- 로컬에서 Docker 컨테이너 실행

###  AWS 서비스 (8개)
| 서비스 | 역할 |
|--------|------|
| **API Gateway** | HTTP → Lambda 연동 |
| **Lambda** | 버튼 클릭 처리 로직 |
| **S3** | 클릭 로그 저장 (JSON) |
| **DynamoDB** | 클릭 이벤트 DB 저장 |
| **SNS** | 이메일 알림 전송 |
| **CloudWatch Logs** | Lambda 실행 로그 확인 |
| **IAM** | Lambda가 리소스 접근할 수 있도록 권한 설정 |
| **Docker** | 컨테이너화 및 실행 |

---

##  실행 방법

- Docker Desktop을 설치한다 ([https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop))
- 아래 명령어로 VisitLogger 코드를 클론한다
  ```bash
  git clone https://github.com/LeeJuHyeong0492/VisitLogger.git
  cd VisitLogger
  ```
- Dockerfile을 기반으로 이미지 빌드
  ```bash
  docker build -t visitlogger .
  ```
- Flask 앱을 Docker 컨테이너로 실행
  ```bash
  docker run -p 8080:80 visitlogger
  ```
- 웹 브라우저에서 다음 주소로 접속
  ```
  http://localhost:8080
  ```
- 버튼을 클릭하면 다음 기능이 작동함:
  - API Gateway를 통해 Lambda 트리거
  - Lambda가 DynamoDB에 클릭 정보 저장
  - Lambda가 S3에 JSON 로그 업로드
  - Lambda가 SNS로 이메일 알림 전송
  - Lambda 실행 로그가 CloudWatch에 자동 기록됨

---

##  동작 구조

###  동작 흐름 요약
1. 사용자가 웹 브라우저에서 버튼 클릭
2. Flask 앱이 `API Gateway URL`로 POST 요청 전송
3. `API Gateway`가 요청을 받아 지정된 `Lambda 함수`를 실행
4. `Lambda 함수` 내부 로직 수행:
   - DynamoDB에 클릭 로그 저장 (IP, 시간 등)
   - JSON 형식으로 S3 버킷에 로그 파일 업로드
   - SNS 주제(Topic)로 이메일 알림 전송
   - 모든 실행 로그를 CloudWatch에 자동 기록


##  AWS 구성 및 설정

- **API Gateway**
  - 리소스: `/click`, 메서드: `GET`
  - Lambda 통합 방식 설정 (프록시 모드)
  - 리소스 기반 정책에 `lambda:InvokeFunction` 권한 부여

- **Lambda**
  - Python 코드 배포 및 테스트
  - 실행 역할에 다음 권한 포함:
    - CloudWatch Logs
    - S3 접근 (`PutObject`)
    - DynamoDB 접근 (`PutItem`)
    - SNS 접근 (`Publish`)

- **DynamoDB**
  - 테이블 이름: `ClickLog`
  - 파티션 키: `timestamp` (string)

- **S3**
  - 버킷 이름: `visitlogger-logs`
  - 저장 경로: `logs/yyyy-mm-dd-uuid.json`

- **SNS**
  - 주제(Topic) 생성 후 수신 이메일 구독 등록
  - Lambda에서 `boto3`로 `publish()` 호출 시 메일 수신됨

- **CloudWatch**
  - `/aws/lambda/HandleClickLambda` 로그 자동 생성됨

---
