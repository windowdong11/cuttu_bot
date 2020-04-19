
# 모드 : 매너, 어인정
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import psycopg2
import time
import sys
import datetime
import secret_data

# 로그 저장위치
sys.stdout = open('log'+time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))+'.txt','w')

# 구글아이디, 비밀번호
#id = 'google_id'
#password = 'your_password'
#db_name = 'main'
#db_user = 'postgres'
#db_host = 'localhost'
#db_password = 'your_password'

id = secret_data.id
password = secret_data.password
db_name = secret_data.db_name
db_user = secret_data.db_user
db_host = secret_data.db_host
db_password = secret_data.db_password


# --------------------------------------------------------------------------------------------------------


driver = webdriver.Chrome('C:\SeleniumDriver\chromedriver.exe')
soup = BeautifulSoup(driver.page_source, 'html.parser')
wait = WebDriverWait(driver, 10)
conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(db_name, db_user, db_host, db_password))
cur = conn.cursor()

# driver를 이용한 soup 업데이트
def updateSoup():
	global soup
	soup = BeautifulSoup(driver.page_source, 'html.parser')

# class_name 찾을 때까지 기다리고, 클릭
def wait_find_by_class_name(class_):
	wait.until(lambda driver: driver.find_element_by_class_name(class_))
	return driver.find_element_by_class_name(class_)

# name 찾을 때까지 기다리고, 클릭
def wait_find_by_name(name):
	wait.until(lambda driver: driver.find_element_by_name(name))
	return driver.find_element_by_name(name)
		
# id 찾을 때까지 기다리고, 클릭
def wait_find_by_id(id):
	wait.until(lambda driver: driver.find_element_by_id(id))
	return driver.find_element_by_id(id)

# 로그인
def login():
	# 구글아이디 로그인
	driver.get('https://kkutu.co.kr/')
	wait_find_by_id('account').click()
	time.sleep(1.2)
	wait_find_by_class_name('login-google').click()

	wait_find_by_name('identifier').send_keys(id)
	wait_find_by_id('identifierNext').click()
	wait_find_by_name('password').send_keys(password)
	wait_find_by_id('passwordNext').click()

# 서버 입장
def enter_server():
	# 서버 이름을 받고, 출력
	wait_find_by_class_name('server-name')
	driver.implicitly_wait(10)
	updateSoup()
	server_list = soup.find_all('div', class_='server-name')
	# 미완성, 가장 적은 서버 인원수 자동 접속
	#server_status_players = 400
	idx = 1
	for server in server_list:
		print(idx, server.string)
		idx = idx + 1

	# 아래 주석은 서버 선택을 위한 입력
	#selected_server = int(input("서버선택 : ")) - 1
	selected_server = 2
	print("서버선택 : ", selected_server)
	driver.find_element_by_id('server-' + str(selected_server)).click()

	time.sleep(0.5)
	# 모든 안내문 확인클릭
	for element in driver.find_elements_by_id('oppo-ok'):
		element.click()
	for element in driver.find_elements_by_id('notice-nolook'):
		element.click()
	for element in driver.find_elements_by_id('notice-ok'):
		element.click()

def make_room():
	# 방 만들기
	driver.find_element_by_id('NewRoomBtn').click()
	# 제목 설정
	room_title = input("방 제목 : ")
	driver.find_element_by_id('room-title').send_keys(room_title)
	# 비밀번호 설정
	while True:
		is_pw_avail = input("비밀번호 생성 여부 (Y/N): ")
		if is_pw_avail == 'Y' or is_pw_avail == 'y':
			room_pw = input("비밀번호 : ")
			driver.find_element_by_id('room-pw').send_keys(room_pw)
			break;
		elif is_pw_avail == 'N' or is_pw_avail == 'n':
			break
	# 플레이어 수 설정
	while True:
		room_limit = int(input("플레이어 수 1~8 : "))
		if 1 <= room_limit and room_limit <= 8:
			driver.find_element_by_id('room-limit').send_keys(room_limit)
	# 라운드 수 설정
	while True:
		room_round = int(input("라운드 수 1~10 : "))
		if 1 <= room_round and room_round <= 8:
			driver.find_element_by_id('room-round').send_keys(room_round)
	# TODO : 게임 유형 설정, 

def send_message(word): # 채팅창으로 메세지 보내기
	driver.find_element_by_xpath("//input[@autocomplete='off']").send_keys(word)
	driver.find_element_by_id("ChatBtn").click()

def isGameEnded(): # 종료시 나타나는 다이얼로그의 style이 block을 가지는 경우, 게임종료로 판단
	return soup.find('div', class_='dialog-front')['style'][38] == 'b'

def readCenterMessageTag():	# 게임 상태, 첫 글자, 완성/미완성 단어 중 하나의 정보를 포함하는 메세지 태그 반환
	# 미완성 단어? : 완성 단어가 "지금은맞고그때는틀리다"일때, "지금은맞고"까지만 작성된 경우 미완성 단어라 함
	return soup.find('div', class_='jjo-display')

def isGameStartPhase(): # 게임이 시작하는 단계의 경우 True
	return readCenterMessageTag().string == "잠시 후 게임이 시작됩니다!"

def readTurn():	# chain 읽기
	return soup.find('div', class_='chain')

def isMyTurn():
	# "당신의 차례! 아래의 채팅 창에서 입력하세요"라고 적힌 창이 block속성으로 보여지는 경우 내 턴
	return soup.find('div', class_='game-input')['style'][9] == 'b'

def getWord(word):	# word로 시작하는 단어 반환
	# word의 형태 : "극" or "릇(늣)"
	front_query_command = "select _id from kkutu_ko where _id like '"
	mid_query_command = "%' and isused=false order by length(_id) "
	order = "DESC"
	end_query_command = " limit 1;"

	if float(soup.find('div', class_='jjo-turn-time').string[:-1]) < 2.0:
		jjo_round_time = float(soup.find('div', class_='jjo-round-time').string[:-1])
		if  1.0 < jjo_round_time and jjo_round_time < 3.0:
			time.sleep(0.1)	# 시간이 촉박하면, 상대의 시간을 줄이기 위해 딜레이, 미완성
		mid_query_command = "%' and isused=false "
		order = ""
	if len(word) > 1:
		words = []
		cur.execute(front_query_command + word[0] + mid_query_command + order + end_query_command)
		query_result = cur.fetchall()
		if len(query_result) > 0 and len(query_result[0]) > 0:
			words.append(query_result[0][0])

		cur.execute(front_query_command + word[2] + mid_query_command + order + end_query_command)
		query_result = cur.fetchall()
		if len(query_result) > 0 and len(query_result[0]) > 0:
			words.append(query_result[0][0])
		if len(words) == 2:
			if len(words[0]) >= len(words[1]):
				word = words[0]
			else:
				word = words[1]
		elif len(words) == 1:
			word = words[0]
		else:
			time.sleep(max(float(soup.find('div', class_='jjo-turn-time').string[:-1]) - 0.1, 0.0))
			word = ""
	else:
		cur.execute(front_query_command + word + mid_query_command + order + end_query_command)
		query_result = cur.fetchall()
		if len(query_result) > 0 and len(query_result[0]) > 0:
			word = query_result[0][0]
		else:
			time.sleep(max(float(soup.find('div', class_='jjo-turn-time').string[:-1]) - 0.1, 0.0))
			word = ""
	# 찾은 단어 isused = true
	if not(word == ""):
		cur.execute("update public.kkutu_ko set isused=true where _id ='" + word + "'")
		print("SELF USE : ", word)
	return word

def insertWord(word):	# db에 word추가
	cur.execute("insert into kkutu_ko values ('" + word + "', false)")
	print("insert : ", word)

def deleteWord(word):	# db에 word삭제
	cur.execute("delete from kkutu_ko where _id='" + word + "'")
	print("delete : ", word)

def isWordExist(word):	# db에 word존재여부 확인
	cur.execute("select exists(select 1 from kkutu_ko where _id='"+ word + "')")
	return cur.fetchall()[0][0]


def InitializeDB(): # db의 모든 isused 초기화
	cur.execute("update kkutu_ko set isused=false where isused=true;")

def makeBotRoom(): # 미완성, 봇전 방 생성
	driver.find_element_by_id("NewRoomBtn").click()
	driver.find_element_by_id("room-manner").click()
	driver.find_element_by_id("room-injeong").click()
	driver.find_element_by_id("room-pw").send_message('1234ne') # send_message(password)
	driver.find_element_by_id("room-ok").click()
	driver.find_element_by_id("PracticeBtn").click()
	#driver.find_element_by_xpath('//option[@value="3"]').click()
	driver.find_element_by_id("practice-ok").click()


login()
enter_server()
#make_room()
updateSoup()
while not soup.find('div', id="Intro").has_attr("style"):
	updateSoup()
#time.sleep(2)
#makeBotRoom()
cur.execute("begin")
while True:
	#아래는 봇과 대결하기 위한 줄
	#driver.find_element_by_id('PracticeBtn').click()
	#driver.find_element_by_id('practice-ok').click()
	check_continue = input("종료하려면 N입력 :  ")
	if check_continue == 'N':
		break
	prev_turn = -1
	cur_turn = 0
	print_status = False
	last_word = ""
	while True:
		updateSoup()
		center_message = readCenterMessageTag().text
		if center_message == "잠시 후 게임이 시작됩니다!":
			break

	while True:
		updateSoup()
		center_message = readCenterMessageTag()
		if not (center_message == "잠시 후 게임이 시작됩니다!"):
			break
	
	while True:
		#아래 주석을 해제하면, 수동
		#input()
		updateSoup()
		center_message_tag = readCenterMessageTag()
		center_message = center_message_tag.text

		print("turn changed : ", center_message_tag)

		if center_message == "게임 끝!":
			prev_turn = -1
			InitializeDB()
			break
		# 메세지 확인
		
		elif isMyTurn():
			# 첫 글자 주어짐
			# 내 턴 확인, 단어 전송
			while True:
				updateSoup()
				# 단어 보냄
				word = getWord(center_message)
				send_message(word)
				
				#print(center_message.find('label', {'style':'color:rgb(170,170,170);'}))
				time.sleep(0.1)
				# 틀렸는지 확인
				updateSoup()
				center_message_tag = readCenterMessageTag()

				if center_message_tag.find('label', class_='game-fail-text') == None:
					print("RIGHT : ", center_message_tag)
					break
				else: # 틀린경우 단어 삭제
					if len(center_message_tag.text) > 7 and center_message_tag.text[6] == ':':
						continue
					print("WRONG : ", center_message_tag)
					deleteWord(center_message_tag.text)
		else:
			print("ELSE : ", center_message_tag)
			if not(len(center_message) == 1) and center_message_tag.find('label', class_='game-fail-text') == None:
				cur.execute("update public.kkutu_ko set isused=true where _id = '" 
				   + center_message + "'")
				print("ELSE IF : ", center_message_tag)
				#print("USED : ", center_message)

InitializeDB()
if input("db롤백? (Y):") == 'Y':
	cur.execute("commit")
	print("commited")
else:
	cur.execute("rollback")
	print("rollbacked")