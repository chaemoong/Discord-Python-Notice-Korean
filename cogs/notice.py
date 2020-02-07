import discord
from discord.ext import commands
import setting
from cogs.utils.chat_formatting import pagify
from dataIO import dataIO
import traceback
import datetime

class notice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def owner(ctx):
        if ctx.author.id == int(setting.set().owner):
            return True

    async def admin(ctx):
        if ctx.author.guild_permissions.administrator == True:
            return True 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            log = "".join(traceback.format_exception(type(error), error, error.__traceback__))
            for page in pagify(log):
                asdf = f'```py\n{log}\n```'
            embed = discord.Embed(title=f'{ctx.command.qualified_name} 명령어에 에러가 발생하였습니다!', colour=discord.Colour.green())
            await ctx.send('에러 내용을 봇 관리진에게 보냈습니다! 빠른 시일내에 고치도록 하겠습니다!')
            await self.bot.get_user(int(setting.set().owner)).send(embed=embed, content=asdf)
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(f'{ctx.author.mention}, 관리진 명령어를 사용하지 마세욧!')
        elif isinstance(error, commands.CommandNotFound):
            pass

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(owner)
    async def reload(self, ctx):
        self.bot.reload_extension('cogs.notice')
        return await ctx.send(f'{ctx.author.mention}, 모듈 리로드에 성공하였습니다!')

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(owner) #봇 전용 명령어가 아닌 서버 관리진 전용 명령어로 만드실 경우에는 owner를 admin으로 바꾸시면됩니다.
    async def notice(self, ctx, *, message=None):
        author = ctx.author
        if message == None:
            return await ctx.send(f'{author.mention}, 메시지를 적어주세요!')
        data = dataIO.load_json('channel.json')
        if data.get('channel') == None:
            return await ctx.send(f'{author.mention}, 공지 데이터가 없습니다!')
        em = discord.Embed(colour=0xFFC0CB) #색깔은 HEX코드입니다!
        em.add_field(name=f'{ctx.bot.user.name} 공지', value=message)
        em.set_footer(text=f'공지 작성자: {author} - 인증됨', icon_url=author.avatar_url)
        a = data.get('channel')
        if a == None:
            return await ctx.send('공지 채널이 설정되지 않아 취소되었습니다!')
        for id in a:
            await self.bot.get_channel(int(id)).send(embed=em)
        return await ctx.send('모든 채널에 전송을 완료했습니다!')
        

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    async def 공지등록(self, ctx, channel:discord.TextChannel=None):
        author = ctx.author
        if not channel:
            return await ctx.send(f'{author.mention}, 채널을 멘션 해주세요!')
        data = dataIO.load_json('channel.json')
        em = discord.Embed(colour=0x42FF33, title='채널 설정', timestamp=datetime.datetime.utcnow())
        em.add_field(name='정말 진행하시겠습니까?', value=f'정말 {channel.mention} 채널을 공지 채널로 하시겠습니까?')
        asdf = ['⭕', '❌']
        msg = await ctx.send(embed=em)
        for a in asdf:
            await msg.add_reaction(a)
        def check(reaction, user):
            if user == ctx.author and str(reaction.emoji) in asdf: 
                return True 
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await msg.edit(content='> 정상적으로 취소되었습니다!')
        if True:
            em2 = discord.Embed(colour=0x42FF33, title='채널 설정', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                if data.get('channel') == None:
                    data['channel'] = []
                if data.get('server') == None:
                    data['server'] = []
                if ctx.guild.id in data.get('server'):
                    await msg.delete()
                    return await ctx.send(f'{author.mention}, 이 서버는 이미 공지 채널이 등록 되있습니다! `{ctx.prefix}공지삭제` 명령어로 채널을 삭제하세요!')
                data['channel'].append(int(channel.id))
                data['server'].append(int(ctx.guild.id))
                dataIO.save_json('channel.json', data)
                em2.add_field(name='성공!', value=f'공지 채널을 {channel.mention}으로 설정하였습니다!')
                return await msg.edit(content=author.mention, embed=em2)
            if reaction.emoji == '❌':
                em2.add_field(name='실패!', value='취소되었습니다.')
                return await msg.edit(content=author.mention, embed=em2)
            else:
                em2.add_field(name='실패!', value='다른 이모지를 추가하셔서 취소되었습니다.')
                return await msg.edit(content=author.mention, embed=em2)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    async def 공지삭제(self, ctx, channel:discord.TextChannel=None):
        author = ctx.author
        if not channel:
            return await ctx.send(f'{author.mention}, 채널을 멘션 해주세요!')
        data = dataIO.load_json('channel.json')
        em = discord.Embed(colour=0x42FF33, title='채널 설정', timestamp=datetime.datetime.utcnow())
        em.add_field(name='정말 진행하시겠습니까?', value=f'정말 {channel.mention} 채널을 공지 채널에서 삭제 하시겠습니까?')
        asdf = ['⭕', '❌']
        msg = await ctx.send(embed=em)
        for a in asdf:
            await msg.add_reaction(a)
        def check(reaction, user):
            if user == ctx.author and str(reaction.emoji) in asdf: 
                return True 
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await msg.edit(content='> 정상적으로 취소되었습니다!')
        if True:
            em2 = discord.Embed(colour=0x42FF33, title='채널 설정', timestamp=datetime.datetime.utcnow())
            if reaction.emoji == '⭕':
                if data.get('channel') == None:
                    data['channel'] = []
                if data.get('server') == None:
                    data['server'] = []
                if not ctx.guild.id in data.get('server'):
                    return await ctx.send(f'{author.mention}, 이 서버는 이미 공지 채널이 등록 되있지 않습니다! `{ctx.prefix}공지등록` 명령어 공지채널을 등록하세요!')
                data['channel'].remove(int(channel.id))
                data['server'].remove(int(ctx.guild.id))
                dataIO.save_json('channel.json', data)
                em2.add_field(name='성공!', value='공지 채널을 삭제하였습니다!')
                return await msg.edit(content=author.mention, embed=em2)
            if reaction.emoji == '❌':
                em2.add_field(name='실패!', value='취소되었습니다.')
                return await msg.edit(content=author.mention, embed=em2)
            else:
                em2.add_field(name='실패!', value='다른 이모지를 추가하셔서 취소되었습니다.')
                return await msg.edit(content=author.mention, embed=em2)

        


def setup(bot):
    bot.add_cog(notice(bot))