# cuttu_bot
한글 끝말잇기 - 매너, 어인정 모드

1) 구글 로그인을 통해 크투코리아 자동접속,
2) 사용자가 임의로 방 입장,
3) 진행여부 확인 : 'N'입력시 -> (5)커밋여부 확인, 그 외 -> (4)봇 시작,
4) 봇 시작 : 자동으로 끝말잇기 진행, 게임 종료시 (3)진행여부 확인
5) 커밋여부 확인 : 'Y'입력시 commit, 그 외 rollback

DB : 크투 공식 db 사용 (https://github.com/JJoriping/KKuTu)
BeautifulSoup4, selenium, psycopg2 등 사용

## secret_data.py내부
id = 'google_id'

password = 'google_pw'

db_name = 'main'

db_user = 'postgres'

db_host = 'localhost'

db_password = 'db_pw'

## DELETE 되는 경우
1) 내차례에 틀린 답으로 나오는 경우 (label의 class="game-fail-text" 존재)

## INSERT 되는 경우 (미구현)
1) 다른유저 차례에 history의 첫 단어가 db에 없는 경우

## 제작하게 된 계기
입대 2일전 (어떤걸 하던 알차게 살고싶은 시기)
???가 크투 봇을 만들어 대결하자고 해서, 크롤링, sql, python등을 해볼겸 호다닥 제작

## TMI
2020.4.20 -> 5주간 훈련소행~ (대충 5주 지나면 업데이트한다는 뜻)
코드가 댕댕판!
