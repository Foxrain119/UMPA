readme


D1 회원 커스터마이징
	- 유저 모델 커스텀
	- 회원 가입 후 DB에 회원 정보 저장

    환경 설정
	- dj-rest-auth에서 registration기능의 추가 설정을 위한 dj-rest-auth의 optional 패키지 설치
	  'dj-rest-auth[with-social]'  # allauth 라이브러리가 포함된 dj-rest-auth 추가기능

	- 파이썬 이미지 처리(프로필, 썸네일 등) 라이브러리 설치 및 세팅
	pillow, PILKit, django-imagekit



D2 회원 커스터마이징
	- 로그인 사양 변경
		- 로컬 인증 시 이메일과 패스워드만으로 인증
	- 회원 정보 조회 사양 변경
		- AbstractUser의 기본 필드인 first_name, last_name 반환하지 않도록 수정(기존엔 빈 문자열 출력됨)
		  애초에 dj-rest-auth 의 registration 기능에서 사용하지 않는 필드
		- db단계에서 필드를 제거하고 싶다면 AbstractBaseUser 상속으로 변경해야함
		- pk, username, email, phone(임시), age(임시)

	- 프로필 페이지
		- 로그인 유저만 페이지 접근 가능
		- 회원 정보 조회, 수정, 탈퇴 .....
    커뮤니티(게시판)
	- 로그인 사용자만 article_list 접근 가능 (게시판 최상위 url) (수정 예정, GET은 전체, 수정 및 생성만 로그인 사용자)
	- 게시글
		- 게시글 리스트 조회, 단일 게시글 조회
		- CRUD
		- 단일 게시글 조회 시 해당 게시글에 달린 댓글(comment_set)과 댓글 개수(comment_count)제공
	- 댓글
		- 댓글 리스트 조회, 단일 댓글 조회
		- CRUD
		- 댓글 조회 시 해당 댓글이 달린 게시글의 id, title 제공
D2 challenge
    API 문서화
	- OpenAPI Specification(OAS): RESTful API를 설명하고 시각화하는 표준화된 방법(API에 대한 세부사항을 기술할 수 있는 공식 표준)
	- OAS기반 API에 대한 문서 생성(API 명세서 작성)에 도움을 주는 프레임워크 -> Swagger, Redoc
	- 문서화를 위해 drf-spectacular 라이브러리 패키지 설치 (pip freeze 및 settings 수정 완료)

    - serializer의 역할
    - 참조, 역참조 개념
    	- comment는 article을 참조하고 article은 comment에 참조된다(역참조)
	- comment가 참조하는 대상 = article
	- article에 참조되는 대상 = comment
	- 모델 관계상 관계가 중첩되는 경우(Nested relationships)는 serializers를 필드로 사용하여 표현 가능(역참조 매니저 활용 comment_set을 override)
	- 외래키 작성
    - 로그인 사양 변경 후 username NOT NULL 에러
    - 댓글 작성 시 user 필드 오버라이딩 에러



참고자료
이미지 처리 예시
https://wayhome25.github.io/django/2017/05/11/image-thumbnail/
전화번호 필드
https://hunstory.tistory.com/48
https://velog.io/@mmy789/Django-User-%EB%AA%A8%EB%8D%B8%EC%97%90-%ED%95%B8%EB%93%9C%ED%8F%B0-%EB%B2%88%ED%98%B8-%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0


참고키워드
autogpt

1ea6b46be14c59d5b1b2e52378d985d8d7c53bbc
4e7815e311bb0b28a4a828776f66a3c028254314
73e53131881d8ada5b86e38543b880869fb2cfc1