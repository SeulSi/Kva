import discord
import asyncio
import random 
import sys
import os
import PW 
import aiomysql 
import pickle
from send import Command
import TOKEN

prefix = TOKEN.prefix

"""
봇 주인만 사용 가능한 비밀 명령어를 수록합니다.
"""


""" Function """
def restart_bot():
    python = sys.executable
    os.execl(python, python, * sys.argv)


""" Main """ 
class owner(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)

        self.noticelist = ["봇-공지","봇_공지", "봇공지", "공지", "bot-notice", "bot_notice", "botnotice",  "notice", "bot-announcement", "botannouncment", "bot_announcement", "공지사항", "공지", "공지-사항", "공지입니다"]
        #self.noticelist = "botdevleopertestchannel"

    def search_notice_channel(self):

        allserver = []
        self.noticechannels = []
        for i in self.client.guilds:
            allserver.append(i)
        for b in allserver:
            for i in b.channels:
                if "bot-announcement" in i.name or "bot_announcement" in i.name or "봇-공지" in i.name or "봇_공지" in i.name:
                    self.noticechannels.append(i)
      
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        for b in allserver:
            for i in b.channels:
                if "bot-notice" in i.name or "bot_notice" in i.name:
                    self.noticechannels.append(i)
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        for b in allserver:
            for i in b.channels:
                if "notice" in i.name or "공지" in i.name:
                    self.noticechannels.append(i)
        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass

        self.noserver = []
        for b in allserver:
            for i in b.channels:
                if "announcement" in i.name or "annoucement" in i.name:
                    self.noticechannels.append(i)

        for c in self.noticechannels:
            try:
                allserver.remove(c.guild)
            except:
                pass
        for a in allserver:
            self.noserver.append(a.name)

                    



    async def on_message(self,message):


        if message.content.startswith(prefix+"봇경고보기"):
            if not message.mentions == []:
                user = message.mentions[0]
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                        row = await cur.fetchone()
                        
                        if row is None:
                            warns = 0
                            embed=discord.Embed(title="✅ 봇경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="경고 수", value=str(warns) + "회" )
                            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

                        else:
                            warns = row[1]
                            embed=discord.Embed(title="✅ 봇경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="경고 수", value=str(warns) + "회" )
                            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

                await message.channel.send(embed=embed)

            else:
                user = message.author
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                        row = await cur.fetchone()
                        
                        if row is None:
                            warns = 0
                            embed=discord.Embed(title="✅ 봇경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="경고 수", value=str(warns) + "회" )
                            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

                        else:
                            warns = row[1]
                            embed=discord.Embed(title="✅ 봇경고 조회", description="%s 님의 경고를 불러옵니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="경고 수", value=str(warns) + "회" )
                            embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")

                await message.channel.send(embed=embed)

        if message.author.id == 294146247512555521 or message.author.id == 371639335046348802 or message.author.id == 271639823859580939:


            if message.content == prefix+"재시작":
                restart_bot()


            if message.content == prefix+"종료":
                await message.channel.send("봇을 종료합니다...")
                exit()

            if message.content.startswith(prefix+"강제초대"):
                a = message.content
                serverid = message.content.split(' ')[1]
                invite = self.client.get_channel(int(serverid))
            
                link = await invite.create_invite(max_uses=1, reason="자동 초대")
                
                await message.channel.send(link)



            if message.content.startswith(prefix+"봇경고추가"):
                if not message.mentions == []:
                    user = message.mentions[0]
                    async with self.conn_pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                            row = await cur.fetchone()
                            
                            if row is None:
                                warns = 1
                                await cur.execute("""INSERT INTO warn (id, times) VALUES (%s, %s)""", (str(user.id), 1 ))
                            else:
                                warns = int(row[1]) + 1
                                await cur.execute("""UPDATE warn SET times=%s WHERE id = %s""", (warns, str(user.id)))

                    embed=discord.Embed(title="✅ 봇경고 추가", description="%s 님의 경고를 성공했습니다." %(user.mention) ,color=0x1dc73a )
                    embed.add_field(name="봇경고 수", value=str(warns) + "회" )
                    embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")
                    await message.channel.send(embed=embed)

                else:
                    embed=discord.Embed(title="⚠ 주의", description="선택되지 않은 사용자.",color=0xd8ef56)
                    await message.channel.send(embed=embed)

            if message.content.startswith(prefix+"경고차감"):
                if not message.mentions == []:
                    user = message.mentions[0]
                    async with self.conn_pool.acquire() as conn:
                        async with conn.cursor() as cur:
                            await cur.execute("""SELECT * FROM warn WHERE id = %s""", (str(user.id) ))
                            row = await cur.fetchone()
                            
                            if row is None:
                                warns = 1
                                await cur.execute("""INSERT INTO warn (id, times) VALUES (%s, %s)""", (str(user.id), 1 ))
                            else:
                                warns = int(row[1]) - 1
                                await cur.execute("""UPDATE warn SET times=%s WHERE id = %s""", (warns, str(user.id)))

                    embed=discord.Embed(title="✅ 봇경고 차감", description="%s 님의 경고 차감을 성공하였습니다." %(user.mention) ,color=0x1dc73a )
                    embed.add_field(name="봇경고 수", value=str(warns) + "회" )
                    embed.set_footer(text="5회 이상 경고 발생시 제제 처리됩니다.")
                    await message.channel.send(embed=embed)

                else:
                    embed=discord.Embed(title="⚠ 주의", description="선택되지 않은 사용자.",color=0xd8ef56)
                    await message.channel.send(embed=embed)
                    


            if message.content.startswith(prefix+"공지"):
                contents = message.content[4:].lstrip()
                if contents == "" or contents is None:
                    await message.channel.send("내용을 입력하세요. 전송에 실패하였습니다.")
                else:
                    await message.channel.send("정말 전송합니까? (y/n)")
                    def usercheck(a):
                        return a.author == message.author

                    answer = await self.client.wait_for("message", check=usercheck, timeout=30)
                    answer = answer.content

                    if answer == "y":
                        self.search_notice_channel()
                        for i in self.noticechannels:
                            try:
                                await i.send(contents)
                            except:
                                pass
                        
                        await message.channel.send("전송 완료! 전송 하지 못한 서버들 : %s" %(self.noserver))
                    else:
                        await message.channel.send("전송을 취소합니다.")

            if message.content.startswith(prefix+'서버퇴장'):
                if message.content == prefix+'서버퇴장':
                    await message.channel.send('사용법: '+prefix+'서버퇴장 <서버아이디>')
                else:
                    a = message.content.split(' ')[1]
                    b = self.client.get_guild(int(a))
                    try:
                        await b.leave()
                        await message.channel.send('해당 서버에서 봇을 나가게 하였습니다.')
                    except Exception as error:
                        await message.channel.send('해당 서버에서 나가지 못했어요.```py\n{}\n```'.format(str(error)))
                


