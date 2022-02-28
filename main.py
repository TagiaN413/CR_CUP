import json
import os
import requests
import sys
import traceback

import discord 
from discord.ext import commands



import settings

API_KEY = settings.API_KEY
URL = settings.URL
invitationURL = settings.invitationURL
client = discord.Client()
client = commands.Bot(
    command_prefix="!" 
)
client.remove_command('help')
leader_list = ['vodka','chigusa','wokka','francisco','kuzuha','ratna','kinako','ru','stylishnoob','shaka','kawase','ras','virtualgorilla','bobsappaim','shibuyahal','darumaisgod','chihiro','amatsuki','kun','admin'] #20チームのリスト
del_list = []
remain_team = 20
game_num = 1

@client.event
async def on_ready():
    print('接続しました')
    await client.change_presence(
            activity=discord.Streaming(
                name="CR CUP",
                url=URL
            )
        )

@client.event
async def on_command_error(ctx, error):
    # 存在しないコマンド打たれた時に出るエラーの判定
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("存在しないコマンドです　!helpで確認してください")
    else:
        raise error

@client.command()
async def leadercheck(ctx):
    await ctx.send(leader_list)
 
@client.command()
async def report(ctx, arg2, arg3, arg4):
    global remain_team
    leader = arg2
    ranking = int(arg3)
    kill = int(arg4)

    if leader in del_list:
        await ctx.send('報告済みのリーダーです。修正する場合は!revisionを使ってください')
    elif (leader in leader_list) == False:
        await ctx.send('リーダー名を正しく入力してください')
    elif ranking>20 or ranking<=0 :
        await ctx.send('順位を正しく入力してください')
    else:
        remain_team -= 1
        leader_list.remove(leader)
        del_list.append(leader)
        await ctx.send('ありがとうございます。残り' + str(remain_team) + 'チームです。')
        params = {"ranking":ranking, "kill": kill}
        response = requests.post(  #json投げるとこ
                    url='https://olkcs5v2e0.execute-api.ap-northeast-1.amazonaws.com/test/result/'+str(game_num)+'/'+leader,
                    data=json.dumps(params).encode('utf-8'), headers={'Content-Type': 'application/json'})
        print(response)
        print('送信しました')
@report.error #これは42行目のreportcommandのエラーなのでここにいれてください
async def report_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #エラーの内容を判別
        await ctx.send('!helpで確認してください。')
    else:
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.command()
@commands.has_role('管理者')
async def ranking(ctx):
    global remain_team
    global game_num
    requests.post(url='https://olkcs5v2e0.execute-api.ap-northeast-1.amazonaws.com/test/ranking/'+str(game_num))
    await ctx.send(f'{game_num}試合目のランキングを作成します。')
    remain_team = 20
    game_num += 1
    leader_list.extend(del_list)
    del_list.clear()
@ranking.error
async def report_error(ctx,error):
    if isinstance(error, commands.MissingRole): #エラーの内容を判別
        await ctx.send('権限がないです。')
    else:
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.command()
@commands.has_role('管理者')
async def reset(ctx):
    global game_num
    global remain_team
    remain_team = 20
    game_num = 1
    await ctx.send('試合数をリセットします。')
    leader_list.extend(del_list)
    del_list.clear()
@ranking.error
async def report_error(ctx,error):
    if isinstance(error, commands.MissingRole): #エラーの内容を判別
        await ctx.send('権限がないです。')
    else:
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@client.command()
@commands.has_role('管理者')
async def gamenum(ctx,arg1):
    global game_num
    game_num = arg1
    await ctx.send('game_numを'+arg1+'にしました')
@ranking.error
async def report_error(ctx,error):
    if isinstance(error, commands.MissingRole): #エラーの内容を判別
        await ctx.send('権限がないです。')
    else:
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@client.command(pass_context = True)
@commands.has_role('管理者')
async def clear(ctx, number):
    mgs = [] 
    number = int(number) 
    async for x in channel.history(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)
@ranking.error
async def report_error(ctx,error):
    if isinstance(error, commands.MissingRole): #エラーの内容を判別
        await ctx.send('権限がないです。')
    else:
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@client.command()
async def revise(ctx, arg2, arg3, arg4):
    leader = arg2
    ranking = int(arg3)
    kill = int(arg4)
    if leader in leader_list:
        await ctx.send('まだ報告されていないリーダー名です。')
    elif (leader in del_list) == False:
        await ctx.send('リーダー名を間違えている可能性があります。')
    elif ranking>20 or ranking<=0 :
        await ctx.send('順位を正しく入力してください。')

    else:
        await ctx.send('ありがとうございます。残り' + str(remain_team) + 'チームです。')
        params = {"ranking":ranking, "kill": kill}
        response = requests.post(  #json投げるとこ
                    url='https://olkcs5v2e0.execute-api.ap-northeast-1.amazonaws.com/test/result/'+game_num+'/'+leader,
                    data=json.dumps(params).encode('utf-8'), headers={'Content-Type': 'application/json'})
@revise.error #これは42行目のreportcommandのエラーなのでここにいれてください
async def report_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): #エラーの内容を判別
        await ctx.send('!helpで確認してください。')
    else:
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@client.command()
async def help(ctx):
    embed = discord.Embed(title="CR bot", description="コマンド一覧:", color=0xeee657)
    embed.add_field(name="!help", value="このメッセージを送ります。", inline=False)
    embed.add_field(name="!report", value="[リーダー名] [ランキング] [キル数]を入力してください。", inline=False)
    embed.add_field(name="!revise",value="報告に誤りがある場合はこのコマンドで修正してください。", inline=False)
    embed.add_field(name="!info", value="このbotに関する情報を知りたければ！", inline=False)
    embed.add_field(name="!leadercheck",value="リーダー一覧を送ります。", inline=False)
    await ctx.send(embed=embed)
    
@client.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<PEKE>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(client.guilds)}")

    # give users a link to invite this bot to their server
    embed.add_field(name="Invite", value=invitationURL)

    await ctx.send(embed=embed)


            
client.run(API_KEY)
print('hello')