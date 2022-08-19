# 유대미 DRF 스터디


## Commit Message

| 용어 | 내용 |
| --- | --- |
| feat | 새로운 기능에 대한 커밋 |
| fix | build 빌드 관련 파일 수정에 대한 커밋 |
| build | 빌드 관련 파일 수정에 대한 커밋 |
| chore | 그 외 자잘한 수정에 대한 커밋(rlxk qusrud) |
| ci | CI 관련 설정 수정에 대한 커밋 |
| docs | 문서 수정에 대한 커밋 |
| style | 코드 스타일 혹은 포맷 등에 관한 커밋 |
| refactor | 코드 리팩토링에 대한 커밋 |
| test |  테스트 코드 수정에 대한 커밋 |

## Appp 구조
![Technologies](https://user-images.githubusercontent.com/22442843/184072194-0ca43bbc-a06b-4261-8db5-6385a334c7b8.JPG)

![app 구성](https://user-images.githubusercontent.com/22442843/184072236-004cd416-1278-4722-afec-cd17e9c8b754.JPG)


## Self Q & A
1. docker-compose 파일을 작성할 때 왜 Named Volumes을 사용하는가.
    A : 그냥 각각의 컨테이너에다 volums: - Host Path:컨테이너 Path를 사용 하면 되는데  
        궂이 왜? 따로 설정?

    Q : 그냥 컨테이너 Level에 volums해서 바인딩 하면 docker는 해당 폴더/파일을 관리 하지 않습니다.  
        그리고 Host Path의 폴더가 없거나 하면 Error가 뜨게 됩니다.

        하지만 Named Volumes을 쓴다면 Docker Volumes에서 관리해 주며 Volumes Command를 사용 할 수 있다. 

2. User을 커스터마이징 하는데 왜 AbstractBaseUser, PermissionsMixin를 상속을 받는가?
    AbstractBaseUser는 password, last_login, is_active같은 col이 존재하고
    PermissionsMixin는 is_supperuser, group과 같은 권한 관련 col이 존재한다.
    일반적으로 무지성으로 AbstractUser를 상속을 받는데 여기에는 first_name, last_name, username과 같은 기본적으로
    Djnago에서 구현해 놓은 col이 정의 되어 있다.

    AbstractUser는 무개가 조금 있는 User모델 이다보니 조금더 가볍게 쓰기 위해 AbstractBaseUser, PermissionsMixin를 같은 class를 
    필요에 따라 상속을 받아 사용한다.

3. settings.py에 AUTH_USER_MODEL은 왜 해줘야 하는가?
    보통 user Object를 가져올 때는 get_user_model()이라는 함수를 사용한다 
    
    모든 소스 코드에 from django.contrib.auth.models import User나 from {accounts.models} immport User을 사용하게 된다면 User 정보가 
    바뀔 경우 모든 소슼코드를 손봐야 하는 불상사를 막기 위해 get_user_model()이라는 함수를 from django.contrib.auth import get_user_model에서
    가져와서 사용한다.

    get_user_model 함수의 내부를 보면 settings.AUTH_USER_MODEL를 가져오는 부분이 있어서 우리가 settings.py 에 AUTH_USER_MODEL를 입력 하는 것이다.

4. save(using=self._db)를 위하는가?
    이 문장을 발견한 문장은 BaseUserManager에서 Custom Manager를 만들기 위해 내부를 살펴 보는 과정에서 발견 되었다.
    using을 하는 이유는 간단하다 어떤 DB에 저장할지 명시하는 것이다. 이에 대한 설명은 [여기](https://docs.djangoproject.com/en/4.1/topics/db/multi-db/)에
    설명 되어 있다.

    self._db를 print해본 결과 None이 나왔다 즉 DB Dafault 값이 기본 값으로 세팅이 된다.
    DB default 값은 setiings.py에 DB 설정 하는 부분에서 한다.


## TODO LIST
- [x] App 구조
- [x] 시스템 셋업
- [x] 프로젝트 셋업
- [x] Git Actions 
- [x] TDD with Django
- [x] Configure Database
- [x] Create User Model
- [ ] Setup Django Admin
- [ ] API DOCS
- [ ] Build User API
- [ ] Build Recipe API
- [ ] Build Tags API
- [ ] Build Inggredients API
- [ ] Recuoe Image API
- [ ] Implement Fitering
- [ ] Deploy


