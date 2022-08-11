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

## TODO LIST
- [x] App 구조
- [x] 시스템 셋업
- [x] 프로젝트 셋업
- [x] Git Actions 
- [ ] TDD with Django
- [ ] Configure Database
- [ ] Create User Model
- [ ] Setup Django Admin
- [ ] API DOCS
- [ ] Build User API
- [ ] Build Recipe API
- [ ] Build Tags API
- [ ] Build Inggredients API
- [ ] Recuoe Image API
- [ ] Implement Fitering
- [ ] Deploy


