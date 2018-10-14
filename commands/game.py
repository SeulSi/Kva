import discord
import datetime
import os
import random
from bs4 import BeautifulSoup
import sys 
import aiohttp
import asyncio
import requests 
import json 
import time
import TOKEN
from send import Command
import aiomysql

prefix = TOKEN.prefix

class game(Command):
    
    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, **kwargs)
        
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.guild:
            return
        else:
            exps = random.randint(0,3)
            #exps = random.randint(3,7)
            user = message.author
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""SELECT * FROM money WHERE id = %s""", (str(user.id) ))
                    row = await cur.fetchone()
                    if row is None:
                        moneys = 0
                        await cur.execute("""INSERT INTO money (id, moneys) VALUES (%s, %s)""", (str(user.id), moneys ))
                    else:
                        moneys = int(row[1]) + exps
                        await cur.execute("""UPDATE money SET moneys=%s WHERE id = %s""", (moneys, str(user.id)))

        if message.content.startswith(prefix+"랭크") or message.content.startswith(prefix+"랭킹") or message.content.startswith(prefix+"머니순위") or message.content.startswith(prefix+"머니랭크") or message.content.startswith(prefix+"머니랭킹") or message.content.startswith(prefix+"돈순위") or message.content.startswith(prefix+"돈 순위") or message.content.startswith(prefix+"돈 랭킹") or message.content.startswith(prefix+"돈 랭크"):
            async with self.conn_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM money ORDER BY moneys DESC LIMIT 10;")
                    row = await cur.fetchall()
                    n = 0
                    if not row is None:
                        embed=discord.Embed(title='돈 순위', color=0x1DDB16)
                        for i in row:
                            # 임베디드 add_filed
                            n = n + 1
                            embed.add_field(name='{} 위'.format(n), value='<@{id}> / {money} 원'.format(id=i[0],money=i[1]), inline=False)
                    #메시지 보내기 코드
                    await message.channel.send(embed=embed)

        if message.content.startswith(prefix+"돈"):
            if not message.mentions == []:
                user = message.mentions[0]
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT * FROM money WHERE id = %s""", (str(user.id) ))
                        row = await cur.fetchone()
                        
                        if row is None:
                            moneys = 0
                            embed=discord.Embed(title="✅ 잔액 조회", description="%s 님의 잔액을 확인합니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="현재 잔액", value=str(moneys) + "원" )
                            embed.set_footer(text="화이팅하세요!")

                        else:
                            moneys = row[1]
                            embed=discord.Embed(title="✅ 잔액 조회", description="%s 님의 잔액을 확인합니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="현재 잔액", value=str(moneys) + "원" )
                            embed.set_footer(text="화이팅하세요!")

                await message.channel.send(embed=embed)

            else:
                user = message.author
                async with self.conn_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("""SELECT * FROM money WHERE id = %s""", (str(user.id) ))
                        row = await cur.fetchone()
                        
                        if row is None:
                            moneys = 0
                            embed=discord.Embed(title="✅ 잔액 조회", description="%s 님의 잔액을 확인합니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="현재 잔액", value=str(moneys) + "원" )
                            embed.set_footer(text="화이팅하세요!")

                        else:
                            moneys = row[1]
                            embed=discord.Embed(title="✅ 잔액 조회", description="%s 님의 잔액을 확인합니다." %(user.mention) ,color=0x1dc73a )
                            embed.add_field(name="현재 잔액", value=str(moneys) + "원" )
                            embed.set_footer(text="화이팅하세요!")

                await message.channel.send(embed=embed)


