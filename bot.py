# -*- coding: utf-8 -*-
import asyncio
import functools
import itertools
import math
import json
import random
import os
import discord
from async_timeout import timeout
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Эту команду нельзя использовать в личке.')

        return True

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Произошла ошибка: {}'.format(str(error)))

    @commands.command(name='привет', aliases=['хай'])
    async def _hello(self, ctx: commands.Context):
        await ctx.send(f"Привет, {ctx.author.mention}! Я бот-клоун, и я ничего не умею делать :disappointed:")
    @commands.command(name='клоуны')
    async def _clowns_number(self, ctx: commands.Context):
        await ctx.send(f"Количество клоунов: {ctx.guild.member_count}\n А ты клоун, {ctx.author.mention}?") 
    @commands.command(name='играй')
    async def _play(self, ctx: commands.Context):
        for member in ctx.guild.members:
            if member.name == 'Groovy':
                groovy = member
                break
        await ctx.send(f"Я больше этого не умею :disappointed:, но c этим тебе может помочь {groovy.mention}.") 
    @commands.command(name='помоги', aliases=['помощь'])
    async def _help(self, ctx: commands.Context):
        embed = discord.Embed(title="Помощь от бота-клоуна", description="Мои очень полезные команды")
        embed.add_field(name="!привет", value="Поприветствую тебя")
        embed.add_field(name="!клоуны", value="Скажу сколько клоунов на сервере")
        embed.add_field(name="!ктоя", value='Поиграем в "Кто я?"')
        await ctx.send(content=None, embed=embed)
   
class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Эту команду нельзя использовать в личке.')
        return True
    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Произошла ошибка: {}'.format(str(error)))

    @commands.command(name='ктоя')
    async def _WhoAmI(self, ctx: commands.Context):
        members = ctx.author.voice.channel.members
        members = [member for member in members if member.bot==False]
        if (len(members)>1):
            members_mentions = [member.mention for member in members]
            members_str = ', '.join(members_mentions)
            await ctx.send(f'Будет сделано, {ctx.author.mention}! Провожу игру "Кто я?" в канале {ctx.author.voice.channel}. \n Участники: {members_str}.')
            with open('words.json','r', encoding = 'utf-8') as words_file:
                words_dict = json.load(words_file)
            words = list(itertools.chain.from_iterable(words_dict.values()))
            del words_dict
            selected_words = random.sample(words, len(members)) 
            del words
            couples = [(members[i],selected_words[i]) for i in range(len(members))]
            for member in members:
                msg = ''
                for chosen in couples:
                    if chosen[0] != member:
                        msg += f'{chosen[0].nick} - {chosen[1]}\n'
                await member.send(msg)
        else:
            await ctx.send(f'Извини, {ctx.author.mention}, но эта игра для двух и более человек.')

        
    

bot = commands.Bot('!', description='Клоун-бот')
bot.add_cog(Fun(bot))
bot.add_cog(Game(bot))

@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="!ктоя"))

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send_message(f"""Добро пожаловать на сервер клоун! {member.mention}""")

bot.run(os.environ.get("BOT_TOKEN"))