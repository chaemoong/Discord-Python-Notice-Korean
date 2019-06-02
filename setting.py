"""
Discord-Python-Notice-Korean
Contributors Chaemoong and ttakkku 
"""

class set:
    def __init__(self):
        # 봇의 토큰을 입력하세요!
        self.token = 'TOKEN'
        # 봇의 주인의 ID를 입력하세요!
        self.owner = 'ID'
        # 공지 명령어 접두사를 설정해주세요! (기본 !)
        self.first = '!'
        # 공지 명령어 이름을 설정해주세요! (기본 '공지')
        self.second = '공지'
        # 공지 채널을 설정하는 명령어의 이름을 설정해주세요! (기본 채널설정)
        self.notice = '채널설정' 
        # 공지 채널을 삭제하는 명령어의 이름을 설정해주세요! (기본 채널삭제)
        self.remove = '채널삭제' 
        # 이 부분은 건들지 마세요!  
        self.json = 'channel.json'
        # self.first와 self.second와 self.notice, self.remove 수정하시면 소스 몇개를 수정하셔야 합니다
        # 단 접두사는 1자 이상일 경우와 second와 notice와 remove는 2글자 이상 넘어갈 경우
