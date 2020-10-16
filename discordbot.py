#from discord.ext import commands
#import os
#import traceback
import discord
import random
import re

import os

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

'''
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
'''
client = discord.Client()
#
pattern = '\d{1,2}d\d{1,3}|\d{1,2}D\d{1,3}'
split_pattern = 'd|D'
def judge_nDn(src):
    repatter = re.compile(pattern)
    result = repatter.fullmatch(src)
    if result is not None:
        return True
    elif src == '1d114514' or src == '1D114514':
        return True
    return False
def split_nDn(src):
    return re.split(split_pattern,src)
def role_nDn(src):
    result = []
    sum_dice = 0
    role_index = split_nDn(src)
    role_count = int(role_index[0])
    nDice = int(role_index[1])
    for i in range(role_count):
        tmp = random.randint(1,nDice)
        result.append(tmp)
        sum_dice = sum_dice + tmp
    is1dice = True if role_count == 1 else False
    return result,sum_dice,is1dice
def nDn(text):
    if judge_nDn(text):
        result,sum_dice,is1dice = role_nDn(text)
        if is1dice:
            return 'いくらです(⑅•ᴗ•⑅)\n' + text + 'と入力されました( ´艸` )\n出目は' + str(sum_dice) + 'です!(≧∇≦)ﾉ彡'
        else:
            return 'いくらです(⑅•ᴗ•⑅)\n' + text + 'と入力されました( ´艸` )\n出目は' + str(result) + 'となりましたので、\n合計は' + str(sum_dice) +'です!(≧∇≦)ﾉ彡'
    else:
        return None


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "案内所": 
            ruru = '<#597806952621408259>'
           # syokai = '<#597436185337659433>'
            num = member.guild.member_count
            await channel.send(f"""{member.mention}様！撃 エンジョイ組へようこそ！いくらです！(≧▽≦)ﾉｼ\n\
{member.name}様の参加により本サーバーは{num}人となりました！\n\
ご案内いたしますので指示に従って自己紹介まで終えてください٩(ˊᗜˋ)و\n\
まず初めての方は%sを全て目を通してください！( ´艸` )\n\
ウェブページも作成してあります！(o^^o)\n\
こちらも同様に目を通してください！( ⑉¯ ꇴ ¯⑉ )\n\
※招待した方から音声による説明がある場合はミュートでも構わないので\
「説明部屋」にてVCをお繋げください(≧∇≦)ﾉ彡\n\n""" % (ruru));


@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "脱退メンバー": 
            mes = str(f"""{member}様が脱退しました""")
            await channel.send(mes)


@client.event
async def on_message_delete(message):
        if str(message.channel) != "消去状況":
            meg_del = str('消去内容: {0.author}さん:「{0.content}」(チャンネル:{0.channel})'.format(message))
            channel = client.get_channel(701526609508958279)
            await channel.send(meg_del)

@client.event
async def on_message(message):
    print('{0.author}さん:「{0.content}」(チャンネル:{0.channel})'.format(message))
    if message.author == client.user:
        return
    elif str(message.channel) == "案内所":
        if message.content == 'num':
            num = message.guild.member_count - 5
            str1 = "現在このサーバーには{}人のプレイヤーがいます!"
            await message.channel.send(str1.format(num))
    elif str(message.channel) == "雑談部屋":# or str(message.channel) == "ミュージック用雑談♡" or str(message.channel) == "テキスト✍"
        if message.content.startswith('こんにち'):
            msg = message.author.mention + "様 こんにちは！"
            await message.channel.send(msg)
        if message.content.startswith('おはよ'):
            msg = message.author.mention + "様 おはようございます！"
            await message.channel.send(msg)
        if message.content.startswith('こんばん'):
            msg = message.author.mention + "様 こんばんは！"
            await message.channel.send(msg)
        if message.content.startswith('おやす'):
            msg = message.author.mention + "様 おやすみなさい！"
            await message.channel.send(msg)
        if message.content.startswith('いくらちゃんありが'):
            await message.channel.send('おやすいごようです！(｀-ω-´)✧')
        if message.content.startswith('いくらちゃんかわ'):
            await message.channel.send('(((o(♡´▽`♡)o)))えへへ')
        if message.content.startswith('ひま'):
            await message.channel.send('私とおはなししよ？(´∇ˋ)ﾉ')
        if message.content.startswith('タロット'):
            await message.channel.send('「サイコロ部屋」で「タロット」って打ってみると･･･？')
        if message.content.startswith('めんさん'):
            await message.channel.send('⎝･･⎠⍦　～♪')
    elif str(message.channel) == "サイコロ部屋":
        msg = message.content
        result = nDn(msg)
        if result is not None:
            await message.channel.send(result)
        elif message.content == 'coin':
            dice = random.randint(1,2)
            if dice == 1:
               await message.channel.send('表')
            else:
               await message.channel.send('裏')
        elif message.content.startswith('説明'):
            await message.channel.send('ようこそサイコロ部屋へ！\n「1d6」と打って\
みてください！\n6面のサイコロを振ることができます！٩(*´︶`*)۶\nいくらは少しお勉強をしてきたので、ちょっと難しいダイスも触れるようになりました！(｀-ω-´)✧\n\
「#d#」と打ってみてください！٩(ˊᗜˋ)و（#は数字で、最大99d999までです！)\nコイントスもやります！「coin」と打ってください(*´∇`*)\n\
タロット機能も増えました！「タロット」と打って今日の運勢を占ってみましょう(o^^o)')
        elif message.content.startswith('タロット'):
            dice_tarot = random.randint(1,44)
            if dice_tarot == 1:
                await message.channel.send('マジシャン【I: 魔術師】の正位置：独創性・自信・想像力・柔軟性・決断力・策略')
            elif dice_tarot == 2:
                await message.channel.send('マジシャン【I: 魔術師】の逆位置：悪い影響・創造性の欠如・意志薄弱')
            elif dice_tarot == 3:
                await message.channel.send('調香師【II: 女教皇】の正位置：良識・聡明さ・学究的要素・理解力・精神的な愛')
            elif dice_tarot == 4:
                await message.channel.send('調香師【II: 女教皇】の逆位置：無理解・わがまま・裏切り・ヒステリー')
            elif dice_tarot == 5:
                await message.channel.send('血の女王【III: 女帝】の正位置：理解力・優雅さ・豊かさ・思いやり・進歩')
            elif dice_tarot == 6:
                await message.channel.send('血の女王【III: 女帝】の逆位置：気迷い・怠惰・軽率さ・偏愛・注意力散漫')
            elif dice_tarot == 7:
                await message.channel.send('復讐者【IV: 皇帝】の正位置：意志力・行動力・支配力・達成への心構え')
            elif dice_tarot == 8:
                await message.channel.send('復讐者【IV: 皇帝】の逆位置：論争・傲慢・脆弱な性格・未熟者')
            elif dice_tarot == 9:
                await message.channel.send('写真家【V: 法皇】の正位置：慈（いつく）しみ・信仰心・深い愛・良い忠告・美徳')
            elif dice_tarot == 10:
                await message.channel.send('写真家【V: 法皇】の逆位置：親切心が仇になる・孤立無援・狭い心')
            elif dice_tarot == 11:
                await message.channel.send('庭師【VI: 恋人たち】の正位置：愛の可能性・魅力・直感力・結合・選択・決着')
            elif dice_tarot == 12:
                await message.channel.send('庭師【VI: 恋人たち】の逆位置：不信・離別・失敗・矛盾')
            elif dice_tarot == 13:
                await message.channel.send('ガードNo.26【VII: 戦車】の正位置：勝利・適応性・能動性・確信・旅立ち')
            elif dice_tarot == 14:
                await message.channel.send('ガードNo.26【VII: 戦車】の逆位置：不成功・停止・敗北・挫折')
            elif dice_tarot == 15:
                await message.channel.send('オフェンス【VIII: 力】の正位置：勇気・独立・決断・実行・和解する心')
            elif dice_tarot == 16:
                await message.channel.send('オフェンス【VIII: 力】の逆位置：力の乱用・無能力・弱点・意志の弱さ')
            elif dice_tarot == 17:
                await message.channel.send('冒険家【IX: 隠者】の正位置：秘められた英知・真実の愛・自制心')
            elif dice_tarot == 18:
                await message.channel.send('冒険家【IX: 隠者】の逆位置：孤独な人・疑い深い人・悪い旅行')
            elif dice_tarot == 19:
                await message.channel.send('幸運児【X: 運命の輪】の正位置：幸運・思いがけない収入・計画の好転・転換期')
            elif dice_tarot == 20:
                await message.channel.send('幸運児【X: 運命の輪】の逆位置：誤算・とりとめない変化・放棄・激しい打撃')
            elif dice_tarot == 21:
                await message.channel.send('祭司【XI: 裁判の女神】の正位置：公明正大さ・寛容な心・均衡の良さ・正義・誠実')
            elif dice_tarot == 22:
                await message.channel.send('祭司【XI: 裁判の女神】の逆位置：倫理観の欠如・偏見・損失・無実の罪')
            elif dice_tarot == 23:
                await message.channel.send('傭兵【XII: 釣られた男】の正位置：試練に耐える・自己犠牲・服従・忍耐・苦難')
            elif dice_tarot == 24:
                await message.channel.send('傭兵【XII: 釣られた男】の逆位置：無意味な犠牲・不本意な仕事・悪あがき')
            elif dice_tarot == 25:
                await message.channel.send('納棺師【XIII: 死】の正位置：突発的な事故・思いがけない変化・失敗・損失')
            elif dice_tarot == 26:
                await message.channel.send('納棺師【XIII: 死】の逆位置：好転する運命・再生・立ち直り')
            elif dice_tarot == 27:
                await message.channel.send('機械技師【XIV: 節制】の正位置：受容性・安定感・自制心・忍耐・倹約')
            elif dice_tarot == 28:
                await message.channel.send('機械技師【XIV: 節制】の逆位置：利害の衝突・健康管理の悪さ')
            elif dice_tarot == 29:
                await message.channel.send('黄衣の王【XV: 悪魔】の正位置：心の弱さ・誘惑への傾斜・病魔・未練')
            elif dice_tarot == 30:
                await message.channel.send('黄衣の王【XV: 悪魔】の逆位置：束縛からの解放・弱者・屈従')
            elif dice_tarot == 31:
                await message.channel.send('狂眼【XVI: 塔】の正位置：予期せぬ出来事・信念の崩壊')
            elif dice_tarot == 32:
                await message.channel.send('狂眼【XVI: 塔】の逆位置：不幸な状態・窮地に追い込まれること・投獄されるような出来事')
            elif dice_tarot == 33:
                await message.channel.send('心眼【XVII: 星】の正位置：明るい前途・洞察力・充足感・奇蹟的な救い')
            elif dice_tarot == 34:
                await message.channel.send('心眼【XVII: 星】の逆位置：充たされない願望・失望・不信')
            elif dice_tarot == 35:
                await message.channel.send('リッパー【XVIII: 月】の正位置：曖昧な精神状況・危険な関係・自己欺瞞（ぎまん）')
            elif dice_tarot == 36:
                await message.channel.send('リッパー【XVIII: 月】の逆位置：誤解が解ける・過去の物事の好影響・夜明け')
            elif dice_tarot == 37:
                await message.channel.send('囚人【XIX: 太陽】の正位置：進歩的な考え方・生きる喜び・勝利・幸福')
            elif dice_tarot == 38:
                await message.channel.send('囚人【XIX: 太陽】の逆位置：生活不安・仕事の取り消し')
            elif dice_tarot == 39:
                await message.channel.send('弁護士【XX: 審判】の正位置：復活・地位の好転・償いの気持ち・決断・更新')
            elif dice_tarot == 40:
                await message.channel.send('弁護士【XX: 審判】の逆位置：真実を見失う・罪の意識・閉ざされた心情')
            elif dice_tarot == 41:
                await message.channel.send('占い師【XXI: 世界】の正位置：ものごとの完成・最高潮の機運・超能力')
            elif dice_tarot == 42:
                await message.channel.send('占い師【XXI: 世界】の逆位置：沈滞ムード・エネルギーの欠如・挫折')
            elif dice_tarot == 43:
                await message.channel.send('泥棒【愚者】の正位置：発展へ向かう歩み・冒険への出発・夢想家')
            elif dice_tarot == 44:
                await message.channel.send('泥棒【愚者】の逆位置：愚かな行為・間違った方向・中断・空虚')
        #elif message.content.startswith('#d#'):
            #await message.channel.send('#の中は数字です！\n「2d3」「10d2」「3d10」など、打ってみてください！٩(ˊᗜˋ)و')
    else:
        return
#bot.run(token)
client.run(token)
