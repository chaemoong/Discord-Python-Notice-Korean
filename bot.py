"""
Discord-Python-Notice-Korean
Contributors Chaemoong
"""
import setting
import discord
from dataIO import dataIO
from discord.ext.commands import AutoShardedBot as a

set = setting.set()
bot = a(command_prefix=set.first, description='명령어 정보는 https://github.com/chaemoong/Discord-Python-Notice-Korean 에서 확인해주세요!')
owner = []

@bot.event
async def on_ready():
    print("=" * 50)
    print('{0.user} 계정에 로그인 하였습니다!'.format(bot))
    print("=" * 50)
    bot.load_extension('cogs.notice')

bot.run(set.token)
