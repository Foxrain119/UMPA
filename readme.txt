readme

메인기능 4가지

예금 & 적금 금리 비교
신혼 여행을 위한 환율 계산기
내 집 주변 은행 검색
나에게 맞는 상품 추천 (가장 중요)

1차 개인 분담

	성준 CSS
성 1. 메인 페이지(프론트 구성)
	준 2. 회원 커스터마이징
		회원관리 (회원가입, 로그인, 로그아웃)
		필수 필드: 유저이름, 이메일, 가입한 상품 목록(blank=true, null=true 옵션 활용)
		상품 목록 필드는 쉼표로 구분된 텍스트, 리스트등 관리하기 편한 데이터 타입과 규칙으로 구성
성 3. 예적금 금리 비교
성 4. 환율 계산기
	준 5. 근처 은행 검색
		카카오 API를 이용
		위치와 은행을 선택(입력)할 수 있도록 구성
		선택 시, 해당 위치 근처의 은행 정보를 적절하게 출력
	준 6. 커뮤니티(게시판)
		소통 공간 구성
		권한 설정(본인이 작성한 게시글 및 댓글만 삭제, 수정 가능하도록 구성)
		방식 예시: 금융 상품 리뷰 게시판, 내가 가입한 상품 자랑 게시판 등
	준 7. 프로필 페이지
		회원의 기본 정보 출력
		가입 상품 리스트 출력
		차트 라이브러리를 활용해 상품 금리 정보를 그래프로 출력
		예시 구성: 프로필 페이지(기본 정보 수정 탭) -> 기본 정보 수정(기본 정보, 가입 상품 목록, 가입 상품 금리 그래프), 포트폴리오 수정, 상품 추천 받기
		작성글 목록, 작성 댓글 목록, 좋아요 한 글 목록, 스크랩 한 글 목록
	성준 8. 금융 상품 추천 알고리즘
		AI를 활용한 데이터 분류(선택사항)
		예시1. 상품 추천 챗봇 (프롬프트 엔지니어링)
		예시2. 나와 비슷한 사람들이 가입한 상품 10개 추천 (나이, 자산, 연봉 필드 추가)

9. 생성형 AI
10. README
11. 기타

추가 기능
1. 뉴스 피드 (api)
2. 환율 그래프 (api)
3. 날씨 (api)
4. 추천 챗봇
5. 나만의 금융 플래너



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
	- 역참조: N:1 관계에서 1에서 N을 참조하거나 조회하는 것 (1->N)
		- N은 외래 키를 가지고 있어 물리적 참조가 가능하지만, 1은 N에 대한 참조 방법이 존재하지않아 별도의 역참조 키워드 필요(related_name=; 기본값은 역참조 할 모델 이름_set)
    	- comment는 article을 참조하고 article은 comment에 참조된다(역참조)
	- comment가 참조하는 대상 = article
	- article에 참조되는 대상 = comment
	- 모델 관계상 관계가 중첩되는 경우(Nested relationships)는 serializers를 필드로 사용하여 표현 가능(역참조 매니저 활용 comment_set을 override)
	- 외래키 작성
    - 로그인 사양 변경 후 username NOT NULL 에러
    - 댓글 작성 시 user 필드 오버라이딩 에러



D3 진행예정
	- 커스텀 유저 모델의 필드 추가
		기존: username, email, / phone, age
		추가: property(자산), marital_status(결혼 여부), financial_products(가입 상품 목록), profile_img(프사 blank=True) 
		     custom_page(화면 커스텀 상태, list), is_staff, gender, contracted_deposit(가입 예금 목록), contracted_savings(가입 적금 목록)
		     salary(연봉, 급여), tendency(투자 성향)


	- 근처 은행 찾기

D3 진행사항
	- 커뮤니티 페이지의 permission 속성을 IsAuthenticated 에서 IsAuthenticatedOrReadOnly로 변경
	    (권한 없는 유저는 커뮤니티 접근 불가 상태에서 GET 메서드 요청만 가능하도록 변경)
	- 게시글 및 정보의 수정은 해당 작성 유저만 요청이 가능하도록 권한 설정
		- 각 기능의 view 함수마다 권한을 확인하는 방식 대신 DRF의 permission 클래스를 커스텀후 적용하여 코드의 재사용성을 높힘
	- 게시글 추천(MtoM)
	- 게시글 북마크(MtoM)

D3 challenge
	- django의 superuser, staff 차이
	- DRF의 permission 클래스 커스텀
	- MtoM 관계에서는 중개모델을 활용한다
		- django에서는 ManyToManyField()를 이용해 자동으로 중개모델 생성
		- 참조/역참조 관계만 잘 기억해두면 어느쪽에 작성해도 상관없음. (종속 관계가 아닌 양방향 관계)
		- ManyToManyField()를 가진 쪽에서 -> 없는 쪽으로 "참조"
		- 필드명은 1:N 모델 관계와 구분하기 위해 복수형으로 작성
		- 'through' argument: 중개 테이블에 추가데이터를 사용해 관계 형성하기 위해 사용


참고자료
이미지 처리 예시
https://wayhome25.github.io/django/2017/05/11/image-thumbnail/
전화번호 필드
https://hunstory.tistory.com/48
https://velog.io/@mmy789/Django-User-%EB%AA%A8%EB%8D%B8%EC%97%90-%ED%95%B8%EB%93%9C%ED%8F%B0-%EB%B2%88%ED%98%B8-%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0


참고키워드
autogpt

프롬프트 고정
모든 답변의 세부 과정마다 어떤 로직으로, 왜 그렇게 작성했는지 이유를 상세하게 설명해줘

1ea6b46be14c59d5b1b2e52378d985d8d7c53bbc
4e7815e311bb0b28a4a828776f66a3c028254314
73e53131881d8ada5b86e38543b880869fb2cfc1