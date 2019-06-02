"""
Discord-Python-Notice-Korean
Contributors Chaemoong and ttakkku 
"""

# setting.json를 가지고 온다
import setting
# disocrd를 가지고 온다
import discord
# dataIO를 가지고 온다
from dataIO import dataIO

# 디스코드 클라이언트를 봇으로 번경
bot = discord.Client()
# 세팅을 세팅으로 변경
set = setting.set()
# 오너 ID 저장 공간
owner = []


# 봇 이벤트
@bot.event
#레디 이벤트
async def on_ready():
    # 레디 확인용
    print('{0.user}에 로그인 되었습니다!'.format(bot))
    owner.append(set.owner)

# 봇 이벤트
@bot.event
# 메세지 이벤트
async def on_message(message):
    # 메세지 채널을 메세지 채널로 변수 설정
    messageauthorchannel = message.channel
    # 메세지 유저를 유저로 변수 설정
    user = message.author
    # s는 설정 프리픽스 와 설정 명령어
    s = set.first + set.second
    if s in message.content:
        # 만약 유저가 따노슈(봇 소유주)가 될 경우
        if message.author.id in owner:
            # dataIO를 이용해서 channel.json 파일 로드 
            #  메세지 유저를 author로 변경 
            author = message.author
            # 메세지 보내는 서버를 보낸 서버로 지정
            authorserver=message.author.server
            # 보낼 채널 channel id 가져오기 
            channels_to_send = dataIO.load_json('channel.json')['channel']
            for channels_to_send in channels_to_send:
                if message is None:
                    pass
                else:
                    channel = bot.get_channel(channels_to_send)
                    em = discord.Embed(colour=0x80ff80)
                    em.add_field(name='공지', value=message.content[3:])
                    em.set_footer(text='공지 작성자: ' + author.name + ' - 인증됨',icon_url=author.avatar_url)
                    await bot.send_message(channel, embed=em)
        # 아닐 경우
        else:
            # 관리자 아니라고 보냄
            await bot.send_message(messageauthorchannel, '{}, 당신은 관리자가 아닙니다!'.format(user.mention))
         #만약 설정 프리픽스랑 설정 공지가 메세지 이면   
    elif set.first + set.notice in message.content:
        # 디스코드 채널 맨션을 채널로 변수 설정
        channel = message.content[8:26]
        # setting.json에 로드 하는 데 변수 설정
        notice = dataIO.load_json('channel.json')
        # setting.json에 채널 id를 등록
        notice['channel'].append(channel)
        # setting.json 저장
        dataIO.save_json('channel.json', notice)            
    elif set.first + set.remove in message.content:
        # 디스코드 채널 맨션을 채널로 변수 설정
        channel = message.content[8:26]
        # setting.json에 로드 하는 데 변수 설정
        notice = dataIO.load_json('channel.json')
        # setting.json에 채널 id를 삭제
        notice['channel'].remove(channel)
        # setting.json 저장
        dataIO.save_json('channel.json', notice)            
    elif set.first + 'shutdown' in message.content:
        await bot.logout()         

        


# 봇이 setting.py 에서 토큰 가지고 와서 봇 돌림
bot.run(set.token)

