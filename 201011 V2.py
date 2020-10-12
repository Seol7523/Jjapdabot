import discord , random , time , math , asyncio , calendar , pickle , koreanbots #discord 1.3.3
from PIL import Image
developer = ("설망래 , 이기 낀 금화")
korean_one = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'] # 한글 초성
korean_two = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'] # 한글 중성
korean_three = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'] # 한글 종성
error = [] 
client = discord.Client()
prefix = "ㅉ"
for_message_playing = False
try:    
    with open('cooldown.txt', 'rb') as f:
        cooltimelist = pickle.load(f)
    error.append("쿨타임 파일 이상 없음")
except:
    error.append('쿨타임 파일 에러!!')
    cooltimelist = {"내접두사":0,"도움말":0,"상태":0,"골라":10,"반복":30,"동전던지기":5,
    "주사위던지기":5,"가위바위보":10,"계산친구들":15,"시간,요일":0,"변환친구들":20,"건의하기,건의사항삭제":20,
    "미로":300,"아스키":5,"정보":5,"소인수분해":20,"접두사설정":30,"지뢰찾기":20,"핑":20}        #명령어 추가시 반드시 여기에도 넣기
    with open('cooldown.txt', 'wb') as file:
        pickle.dump(cooltimelist, file)
try:    
    with open('prefix.txt', 'rb') as f:
        userlist = pickle.load(f)
        userprefixlist = pickle.load(f)
    error.append("접두사 파일 이상 없음")
except:
    error.append('접두사 파일 에러!!')
    userlist = []
    userprefixlist = []
    with open('prefix.txt', 'wb') as file:
        pickle.dump(userlist, file)
        pickle.dump(userprefixlist, file)
try:
    with open('iwant.txt', 'rb') as f:
        codelist = pickle.load(f)
        wantlist = pickle.load(f)
        historylist = pickle.load(f)
        error.append("건의목록 파일 이상 없음")
except:
    error.append("건의목록 파일 에러!!!")
    codelist = []
    wantlist = []
    historylist = {}
    with open('iwant.txt', 'wb') as file:
        pickle.dump(codelist, file)
        pickle.dump(wantlist, file)
        pickle.dump(historylist , file)
try:
    with open('serverlog.txt', 'rb') as f:
        serverlist = pickle.load(f)
        serverloglist = pickle.load(f)
    error.append("로그채널 파일 이상없음")
except:
    error.append("로그채널 파일 에러!!!")
    serverlist = []
    serverloglist = []
    with open('serverlog.txt', 'wb') as file:
        pickle.dump(serverlist, file)
        pickle.dump(serverloglist, file)
usercooltime = {}
usercall = {}

startmode = input("테스트용 짭다봇을 키시려면 t를, 기본 짭다봇을 키시려면 s를 입력해주세요\n그외의 문자들은 아직 작동되지 않습니다")    #봇 가동모드 설정 (test는 건의사항채널에 파일검사결과가 올라오지 않아서 깔끔함-물론 그래서 건의사항은 사용불가)
if startmode == "t":
    startmode = "test"
    BOT_TOKEN = "실험용짭다봇 토큰"
elif startmode == "s":
    startmode = "start"
    BOT_TOKEN = "짭다봇 토큰"
    Bot = koreanbots.Client(client, '코리안봇 토큰')
else:
    print("작동모드 선택 안됨!!! 다시시작하세요")

print(cooltimelist)
#쿨타임 확인함수(일일히 코드에 붙여넣기 하면 코드낭비+시간 낭비이므로 함수로 제작하여 확인)
def check_cooltime(userid , command):      #출력값으로 True , False 라고 하려고 했으나 "true"와 "쿨타임이 (숫자)초 만큼 남았어요를 출력하기로 바꿈"
    if cooltimelist[command] == "nonpossible":
        return command + "명령어는 현재 알수 없는 버그 또는 문제로 운영자가 사용을 금지한것 같아요 서둘러 고치도록 하겠습니다"
    else:
        if userid in usercooltime:            
            ti = usercooltime[userid]
            if command in ti:
                if time.time() - ti[command] > cooltimelist[command]:
                    del ti[command]
                    ti[command] = time.time()
                    usercooltime[userid] = ti
                    return True
                else:
                    return command + "의 쿨타임이 " + str(round(cooltimelist[command] - time.time() + ti[command], 1)) + "초 남았습니다"
            else:                                   
                ti[command] = time.time()
                return True
        else:                                        
            usercooltime[userid] = {str(command):time.time()}
            return True

# 한글분리 함수
def detach_korean(word):
    a = ''
    for i in range(len(word)):
        if 0 < i:
            a += ', '
        askicode = ord(word[i]) - 44032
        if -1 < askicode and askicode < 11173:
            a += korean_one[askicode // 588]
            a += korean_two[(askicode // 28) % 21]
            a += korean_three[askicode % 28]
        else:
            a += word[i]
    return(a)

#소인수분해 함수
def primefactor(num):
    a = 2
    num = int(num)
    answer = []
    while num != 1:
        if num %a != 0:
            a = a+1
        else:
            num = num//a
            answer.append(a)
            a = 2
    return answer


#봇 코드 시작
@client.event
async def on_ready():
    print("------\n준비됨\n------")
    game = discord.Game("'ㅉ도움말'로 도움말 보기!!!!!!  ")
    await client.change_presence(status=discord.Status.online, activity=game)
    if startmode == "start":
        global tendinous
        tendinous = await client.get_channel(723307706223558746).send("짭다봇V2가동" + str(time.ctime()))
        await client.get_channel(723307706223558746).send("에러 검사 결과 : " + str(error) +"에러가 있으면 재시작 부탁드립니다")
    else:
        print("짭다봇V2가동" + str(time.ctime()))
        print("에러 검사 결과 : " + str(error) +"에러가 있으면 재시작 부탁드립니다")
    

@client.event
async def on_message_delete(message):
    global serverlist , serverloglist
    danger = "아직 측정 불가"
    if message.author.bot == 1:
        return None
    else:
        embed = discord.Embed(title = "삭제 감지", color = 0xFF0000)
        embed.add_field(name = "삭제된 내용", value =  message.content , inline = False)
        embed.add_field(name = "위험도", value = danger, inline = True)
        embed.add_field(name = "작성자", value = message.author , inline = True)
        if message.guild.id in serverlist:
            number = serverlist.index(message.guild.id)
            channel = serverloglist[number]
            await client.get_channel(channel).send(embed = embed)
        else:
            return None

@client.event
async def on_message_edit(before, after):
    global serverlist , serverloglist
    danger = "아직 측정불가"
    if before.author.bot == 1:
        return None
    else:
        embed = discord.Embed(title = "변경 감지", color = 0xFF0000)
        embed.add_field(name = "이전 내용", value = before.content , inline = True)
        embed.add_field(name = "변경된 내용" , value = after.content , inline = True)
        embed.add_field(name = "위험도", value = danger, inline = True)
        embed.add_field(name = "메시지의 주인", value = before.author, inline = True)
        if before.guild.id in serverlist:
            number = serverlist.index(before.guild.id)
            channel = serverloglist[number]
            await client.get_channel(channel).send(embed = embed)
        else:
            return None

@client.event
async def on_message(message):
    global prefix , userlist , userprefixlist, for_message_playing
    word = str(message.content)
    if message.channel.id == 720981860645077022:
        if word.startswith("ㅉ디버그"):
            if word.split(" ")[1] == "word":
                await message.channel.send("word는 금지어입니다")
            else:
                doword = word[5:]
                await message.channel.send(eval(doword))
        elif word.startswith("ㅉ수정"):
            doword = word[4:]
            exec(doword)
            await message.channel.send(doword + "를 실행하였습니다")
        elif word.startswith("ㅉ상태설정"):
            new = word[6:]
            if new == "기본":
                game = discord.Game("   'ㅉ도움말 ' 로 도움말 확인해주세요!!!!")
            else:
                game = discord.Game(str(new))
            await client.change_presence(status=discord.Status.online, activity=game)
            await message.channel.send("상태설정이 완료되었습니다!!!")
        elif word.startswith("ㅉ접두사설정"):
            noprefix = ["@","~","/","_","|"]
            prefixok = word.split(" ")[1]
            if len(prefixok) > 4 or len(prefixok) < 1:
                await message.channel.send("접두사는 1글자 이상 4글자 이하까지만 되요")
                return None
            else:
                pass
            for i in range(0 , len(noprefix)):
                if noprefix[i] in prefixok:
                    await message.channel.send("접두사에는 특수문자(@,/,~,_)등은 사용이 불가능합니다")
                    return None
                else:
                    pass
            prefix = prefixok
            await message.channel.send("접두사가 " + prefixok +" 로 설정되었습니다")
        elif word.startswith("ㅉ도움말"):
            embed = discord.Embed(title = "운영자 명령어 도움말", color = 0xFFE400)
            embed.add_field(name = "ㅉ디버그 (변수)", value = "(변수)값을 확인합니다 ㅉ변수목록으로 변수종류 확인가능합니다", inline = False)
            embed.add_field(name = "접두사설정", value = "전체 접두사를 변견합니다 . 기본은 'ㅉ'입니다", inline = False)
            embed.add_field(name = "ㅉ상태설정 (내용/기본)" , value = "내용 또는 기본갑으로 상태메시지를 바꿉니다" , inline = False)
            embed.add_field(name = "ㅉ명령어목록" , value = "짭다봇의 모든 명령어를 명령어 코드와 함꼐 알려줍니다" , inline = False)
            embed.add_field(name = "ㅉ변수목록" , value = "짭다봇의 변수들을 출력합니다" , inline = False)
            embed.add_field(name = "ㅉ쿨타임수정/명령어/시간" , value = "그 명령어의 쿨타임을 수정합니다" , inline = False)
            embed.set_footer(text = "본 명령어들은 운영자 명령어 사용방에서만 사용가능합니다")
            await message.channel.send(embed = embed)
        elif word.startswith("ㅉ변수목록"):
            embed = discord.Embed(title = "변수목록", color = 0xFFE400)
            embed.add_field(name = "prefix 계열", value = "userlist - 유저 id를 저장합니다\nuserprefixlist - 유저가 설정한 개인 접두사를 저장합니다", inline = False)
            embed.add_field(name = "건의사항 계열", value = "codelist - 건의를 한 유저의 id값이 저장됩니다\nwantlist - 유저가 건의한 내용을 저장합니다", inline = False)
            embed.add_field(name = "짭다봇로그 계열" , value = "serverlist - 짭다봇 로그를 사용한다고 등록한 서버들의 id를 저장합니다\nserverloglist - 짭다봇로그의 출력채널 id를 저장합니다" , inline = False)
            embed.set_footer(text = "ㅉ디버그 word 는 금지어입니다(연쇄반응)")
            await message.channel.send(embed = embed)
        elif word == "ㅉ쿨타임":
            a = list(cooltimelist.keys())
            b = list(cooltimelist.values())
            c = ""
            for i in range(0,len(a)):
                c = c + a[i] + "   :   " + str(b[i]) + " 초   \n"
            await message.channel.send(c)
        elif word.startswith("ㅉ쿨타임수정"):
            words = word.split("/")
            if word.count("/") != 2:
                await message.channel.send("쿨타임 수정 명령어의 문법은 ㅉ쿨타임수정/(명령어이름)/(수정할 시간) 입니다")
            elif words[1] not in list(cooltimelist.keys()):
                await message.channel.send("없는 명령어입니다")
            else:
                cooltimelist[str(words[1])] = int(words[2])
                with open('cooldown.txt', 'wb') as file:
                    pickle.dump(cooltimelist, file)
                await message.channel.send("수정완료")
        elif word.startswith("ㅉ쿨타임항목추가"):
            cooltimelist[word.split(" ")[1]] = 0
            with open('cooldown.txt', 'wb') as file:
                pickle.dump(cooltimelist, file)
            await message.channel.send("항목추가 완료 코드 변경은 알아서 하세요")
        elif word.startswith("ㅉ답변목록"):
            global historylist
            await message.channel.send(historylist)
        elif word.startswith("ㅉ핑"):
            embed = discord.Embed(title = "핑 측정", color = 0xFFE400)
            embed.add_field(name = "핑 측정 결과" , value = str(client.latency)[0:5] + "초입니다")
            await message.channel.send(embed = embed)

        
        else:
            return None        
    elif message.channel.id == 723307706223558746:
        if word.startswith("ㅉ답변"):    #건의 사항에 답변하는 코드
            binlist = word.split("/")
            clear = int(binlist[1]) - 1
            username = client.get_user(codelist[clear])
            channel = await username.create_dm()    
            embed = discord.Embed(title = "안녕하세요!!짭다봇 팀입니다!!!건의해주신 내용은 감사드립니다!!!", color = 0xFFE400)
            embed.add_field(name = "건의해주신내용", value = wantlist[clear], inline = False)
            historylist[wantlist[clear]] = binlist[2]
            codelist.remove(codelist[clear])
            wantlist.remove(wantlist[clear])
            with open('iwant.txt', 'wb') as file:
                pickle.dump(codelist, file)
                pickle.dump(wantlist, file)
                pickle.dump(historylist , file)
            await message.delete()
            embed.add_field(name = "답변해드리는 내용", value = binlist[2], inline = False)
            await channel.send(embed = embed)
            msg = await message.channel.send(str(username) + "님께 전달되었습니다")
            await message.channel.send("ㅉ새로고침")
            await asyncio.sleep(10)
            await msg.delete()
        elif word.startswith("ㅉ새로고침"):   #건의내용 확인하는 코드
            await message.delete()
            if len(wantlist) != 0:
                global tendinous
                await tendinous.delete()
                number = 1
                embed = discord.Embed(title = "건의사항들", color = 0xFFE400)
                while number != len(wantlist) + 1:
                    embed.add_field(name = "인식코드", value = number, inline = True)
                    embed.add_field(name = "유저이름", value = str(client.get_user(codelist[number-1])), inline = True)
                    embed.add_field(name = "건의사항", value = wantlist[number - 1], inline = False)
                    number = number + 1
                tendinous = await client.get_channel(723307706223558746).send(embed = embed)
            else:
                await tendinous.delete()
                embed = discord.Embed(title = "건의사항들", color = 0xFFE400)
                embed.add_field(name = "건의사항", value = "없음  ~~ㅅㄱㅂ~~", inline = True)
                tendinous = await client.get_channel(723307706223558746).send(embed = embed)

        
        else:
            return None
        

    else:
        if message.author.id in userlist:
            if word.startswith(prefix):
                hoprefix = prefix
            else:
                hoprefix = userprefixlist[userlist.index(message.author.id)]
        else:
            hoprefix = prefix     
        if word.startswith("ㅉ내접두사"):
            if check_cooltime(message.author.id , "내접두사") == "True":    
                try:
                    await message.channel.send(str(message.author) + "님의 접두사는 " + str(userprefixlist[userlist.index(message.author.id)]) + "입니다")
                except:
                    await message.channel.send("개인 접두사를 커스텀하시지 않으셨네요   그럼 ""ㅉ"" 입니다")
            else:
                await message.channel.send(check_cooltime(message.author.id , "내접두사"))
        elif word.startswith(hoprefix):
            word = word[len(hoprefix):]
            if message.author.bot == 1:
                return None
            elif word.startswith("도움") or word.startswith("기능") or word.startswith("게임") or word.startswith("수학") or word.startswith("잡다한") or word.startswith("채팅"):
                if check_cooltime(message.author.id , "도움말") == True:
                    if word.startswith("기능"):    
                        embed = discord.Embed(title = "잡다봇의 기능들", color = 0xFFE400)
                        embed.set_thumbnail(url = "https://media.discordapp.net/attachments/722797114647904296/735323638890233876/663bd596a48b6202.png?width=630&height=630")
                        embed.add_field(name = "명령어들", value = "여러 명령어들이 있습니다.ㅉ도움말로 확인하세요", inline = False)
                        embed.add_field(name = "즐길거리들", value = "ㅉ게임목록으로 간단한 게임들을 확인하세요", inline = False)
                        embed.add_field(name = "채팅 감시" , value = "관짝 들어갔다가 다시 살아나왔습니다\n현재 개발중인 욕설 필터링 기술과 결합하여 더욱더 강력해질 기능입니다" , inline = False)
                        await message.channel.send(embed = embed)

                    elif word.startswith("게임"):    
                        embed = discord.Embed(title = "게임목록", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "가위바위보", value = "가위바위보를 합니다.", inline = False)
                        embed.add_field(name = hoprefix + "동전던지기", value = "동전을던집니다.", inline = False)
                        embed.add_field(name = hoprefix + "주사위던지기", value = "주사위를 던집니다.", inline = False)
                        embed.add_field(name = hoprefix + "지뢰찾기", value = "랜덤한 지뢰찾기를 만듭니다.", inline = False)
                        embed.add_field(name = hoprefix + "미로/(가로)/(세로)", value = "랜덤한 미로를 만듭니다.", inline = False)
                        await message.channel.send(embed = embed)
                    
                    elif word.startswith("수학"):
                        embed = discord.Embed(title = "수학도움말", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "(더하기/곱하기) (1번 항목) (2번항목) ~~ (n번쨰 항목)", value = "항목들을 모두 더하거나 곱해 줍니다.", inline = False)
                        embed.add_field(name = hoprefix + "(빼기/나누기) (항목1) (항목2)", value = "1번 항목에서 2번 항목으로 빼거나 나누어 줍니다.", inline = False)
                        embed.add_field(name = hoprefix + "거듭제곱 (밑) (지수)" , value = "거듭제곱의 값을 알려줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "요일 (년도) (월) (일)" , value = "입력한 날의 요일을 보여줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "((단위의 종류)변환) (숫자) (입력단위) (출력단위#생략가능)" , value = "단위를 변환해 줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "소인수분해 (자연수)" , value = "소인수분해를 해줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "분석 (첫번째 값) .... (마지막 값) #숫자만 넣어주세요" , value = "평균과 분산을 구해줍니다." , inline = False)
                        await message.channel.send(embed = embed)

                    elif word.startswith("잡다한"):
                        embed = discord.Embed(title = "잡다한기능목록", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "골라 (첫번째 항목)/(두번쨰 항목)/(n번쨰 항목) (뽑을 수#없으면 자동으로 1로 설정)", value = "입력한 항목중에서 입력한 갯수를 뽑아줍니다", inline = False)
                        embed.add_field(name = hoprefix + "반복 (반복 횟수)/(반복 딜레이)/(반복 내용1)/(반복 내용2)/(반복 내용n)", value = "입력한 내용을 반복해서 보여줍니다.", inline = False)
                        embed.add_field(name = hoprefix + "건의하기 (건의할 내용)", value = "건의를 합니다", inline = False)
                        embed.add_field(name = hoprefix + "아스키해석 (아스키코드) or ㅉ아스키변환 (변환할내용)", value = "아스키코드를 해석/변환합니다", inline = False)
                        embed.add_field(name = hoprefix + "한글분리 (문장)", value = "쓴 문장을 초성, 중성, 종성으로 분리합니다.", inline = False)
                        embed.add_field(name = hoprefix + "개인접두사설정", value = "접두사를 설정합니다.", inline = False)
                        embed.add_field(name = "ㅉ내접두사", value = "접두사를 까먹으신 분은 이 명령어를 통해 접두사를 확인하세요", inline = False)
                        await message.channel.send(embed = embed)
                    
                    elif word.startswith("채팅"):
                        embed = discord.Embed(title = "채팅 관리 도움말", color = 0xFFE400)
                        embed.add_field(name = "설명" , value = "비속어,욕 등이 들어간 말이 삭제되면 짭다봇이 잡아냅니다!!!" , inline = False)
                        embed.add_field(name = "채널설정법" , value = "짭다봇이 로그를 출력할 서버를 설정하려면 채널이름을 (짭다봇로그)로 시작시키세요" , inline = False)
                        embed.add_field(name = "채널 등록법" , value = hoprefix + "로그채널등록 명령어를 사용하세요" , inline = False)
                        await message.channel.send(embed = embed)
                    else:
                        pass
                    binlist = word.split(" ")
                    binlist.append("아")
                    if binlist[1] == "수학":
                        embed = discord.Embed(title = "수학도움말", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "(더하기/곱하기) (1번 항목) (2번항목) ~~ (n번쨰 항목)", value = "항목들을 모두 더하거나 곱해 줍니다.", inline = False)
                        embed.add_field(name = hoprefix + "(빼기/나누기) (항목1) (항목2)", value = "1번 항목에서 2번 항목으로 빼거나 나누어 줍니다.", inline = False)
                        embed.add_field(name = hoprefix + "거듭제곱 (밑) (지수)" , value = "거듭제곱의 값을 알려줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "요일 (년도) (월) (일)" , value = "입력한 날의 요일을 보여줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "((단위의 종류)변환) (숫자) (입력단위) (출력단위#생략가능)" , value = "단위를 변환해 줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "분석 (첫번째 값) .... (마지막 값) #숫자만 넣어주세요" , value = "평균과 분산을 구해줍니다." , inline = False)
                        embed.add_field(name = hoprefix + "소인수분해 (자연수)" , value = "소인수분해를 해줍니다" , inline = False)
                        await message.channel.send(embed = embed)
                    elif binlist[1] == "채팅관리":
                        embed = discord.Embed(title = "채팅 관리 도움말", color = 0xFFE400)
                        embed.add_field(name = "설명" , value = "비속어,욕 등이 들어간 말이 삭제되면 짭다봇이 잡아냅니다!!!" , inline = False)
                        embed.add_field(name = "채널설정법" , value = "짭다봇이 로그를 출력할 서버를 설정하려면 채널이름을 (짭다봇로그)로 시작시키세요" , inline = False)
                        embed.add_field(name = "채널 등록법" , value = "ㅉ로그채널등록 명령어를 사용하세요" , inline = False)
                        await message.channel.send(embed = embed)
                    elif binlist[1] == "게임목록":
                        embed = discord.Embed(title = "게임목록", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "가위바위보", value = "가위바위보를 합니다.", inline = False)
                        embed.add_field(name = hoprefix + "동전던지기", value = "동전을던집니다.", inline = False)
                        embed.add_field(name = hoprefix + "주사위던지기", value = "주사위를 던집니다.", inline = False)
                        embed.add_field(name = hoprefix + "지뢰찾기", value = "랜덤한 지뢰찾기를 만듭니다.", inline = False)
                        embed.add_field(name = hoprefix + "미로/(가로)/(세로)", value = "랜덤한 미로를 만듭니다.", inline = False)
                        await message.channel.send(embed = embed)
                    elif binlist[1] == "잡다한기능들":
                        embed = discord.Embed(title = "잡다한기능목록", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "건의하기 (건의할 내용)", value = "건의를 합니다", inline = False)
                        embed.add_field(name = hoprefix + "골라 (첫번째 항목)/(두번째 항목)/(n번째 항목) (뽑을 수#없으면 자동으로 1로 설정)", value = "입력한 항목중에서 입력한 갯수를 뽑아줍니다", inline = False)
                        embed.add_field(name = hoprefix + "반복 (반복 횟수)/(반복 딜레이)/(반복 내용1)/(반복 내용2)/(반복 내용n)", value = "입력한 내용을 반복해서 보여줍니다.", inline = False)
                        embed.add_field(name = hoprefix + "아스키해석 (아스키코드) or ㅉ아스키변환 (변환할내용)", value = "아스키코드를 해석/변환합니다", inline = False)
                        embed.add_field(name = hoprefix + "한글분리 (문장)", value = "쓴 문장을 초성, 중성, 종성으로 분리합니다.", inline = False)
                        embed.add_field(name = hoprefix + "개인접두사설정", value = "접두사를 설정합니다.", inline = False)
                        embed.add_field(name = hoprefix + "시간", value = "현재시간을 알려줍니다", inline = False)
                        embed.add_field(name = "ㅉ내접두사", value = "접두사를 까먹으신 분은 이 명령어를 통해 접두사를 확인하세요", inline = False)
                        await message.channel.send(embed = embed)
                    elif binlist[1] == "단어사전":
                        embed = discord.Embed(title = "단어사전 명령어", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "단어등록 (all/local)/(단어)/(뜻)", value = "단어등록을 합니다", inline = False)
                        embed.add_field(name = "(all/local)의 차이점", value = "all로 하시면 다른 서버에서도 그 단어의 뜻을 볼수 있어요!!local은 우리서버에서만 볼수 있답니다", inline = False)
                        embed.add_field(name = hoprefix + "단어사전/(단어)", value = "그 단어를 검색해줍니다", inline = False)
                        embed.set_footer(text = "부적절한 단어는 삭제될수 있습니다")
                        await message.channel.send(embed = embed)
                    else:    
                        embed = discord.Embed(title = "도움말", color = 0xFFE400)
                        embed.add_field(name = hoprefix + "도움말 수학", value = "수학도움말을 보여줍니다.", inline = False)
                        embed.set_thumbnail(url = "https://media.discordapp.net/attachments/722797114647904296/735323638890233876/663bd596a48b6202.png?width=630&height=630")
                        embed.add_field(name = hoprefix + "도움말 채팅관리", value = "채팅관리에 관한 도움말을 보여줍니다", inline = False)
                        embed.add_field(name = hoprefix + "도움말 게임목록" , value = "게임 목록을 보여줍니다." , inline = False)
                        embed.add_field(name = hoprefix + "도움말 잡다한기능들" , value = "잡다한기능들을 보여줍니다" , inline = False)
                        embed.add_field(name = hoprefix + "도움말 단어사전" , value = "단어사전에 대한 도움말을 보여줍니다" , inline = False)
                        await message.channel.send(embed = embed)
                else:
                    await message.channel.send(check_cooltime(message.author.id , "도움말"))
            
            elif word.startswith("상태"):
                if check_cooltime(message.author.id , "상태") == True:
                    await message.channel.send("짭다봇은 현재 온라인!! 라저댓" + str(message.author) + "님")
                else:
                    await message.channel.send(check_cooltime(message.author.id , "상태"))
            elif word.startswith("골라") or word[word.find("개"):].startswith("개골라"):    
                if word.startswith("골라"):
                    count = 1
                    word = word[2:].split("/")
                else:
                    try:
                        count = int(word[0:word.find("개")])
                    except:
                        await message.channel.send("뭔가 정상적이지 못한 내용이 있어요")
                        return None
                    word = word[word.find("라") + 1:].split("/")
                choose = []
                if len(word) == 1:
                    await message.channel.send("항목은 2개이상으로 해주세요!")
                else:
                    if count <= len(word):                    
                        if check_cooltime(message.author.id , "골라") == True:    
                            try:    
                                while count != 0:
                                    choose.append(word.pop(random.randint(0 , len(word) - 1)))
                                    count = count -1
                                embed = discord.Embed(title="골라드립니다",description=str(choose) + "를 뽑았어요!!!!", color=0x00aaaa)
                                await message.channel.send(embed = embed)
                            except:
                                await message.channel.send("뭔가 정상적이지 못한 내용이 있어요.")
                        else:
                            await message.channel.send(check_cooltime(message.author.id , "골라"))
                    else:
                        await message.channel.send("뽑을 항목의 수는 당연히 항목의 수보다 작아야 겠죠???")
            elif word.startswith("반복"):    
                if for_message_playing:
                    await message.channel.send("이미 다른 반복 명령어가 실행중이에요. 좀 있다가 다시 시도해주세요.")
                    return
                word = word[3:].split('/')
                if len(word) < 3:
                    await message.channel.send("반복뒤에는 반복 횟수, 반복 딜레이가 꼭 들어가야 해요.")
                    return
                try:
                    word[0] = int(word[0])
                    word[1] = float(word[1])
                except:
                    await message.channel.send("반복 횟수와 반복 딜레이와 임베드 색깔은 16진수 숫자여야 해요.")
                    return
                if word[0] < 1 or word[1] < 0.8:
                    await message.channel.send("반복 횟수는 1이상이어야 하고, 반복 딜레이는 0.8초 이상이어야 해요.")
                    return
                if word[0] * word[1] > 60:
                    await message.channel.send("반복 횟수와 반복 딜레이를 곱한값이 60을 넘어가면 안돼요.")
                    return
                if check_cooltime(message.author.id , "반복") == True:    
                    for_message_playing = True
                    embed = discord.Embed(title = word[2], color = 0x00aaaa)
                    for_message = await message.channel.send(embed = embed)
                    for i in range(word[0] - 1):
                        await asyncio.sleep(word[1])
                        embed = discord.Embed(title = word[((i + 1) % (len(word) - 2)) + 2], color = 0x00aaaa)
                        await for_message.edit(embed = embed)
                    await asyncio.sleep(word[1])
                    for_message_playing = False
                else:
                    await message.channel.send(check_cooltime(message.author.id , "반복"))

            elif word.startswith("동전던지기"):
                if check_cooltime(message.author.id , "동전던지기") == True:    
                    embed = discord.Embed(title="동전던지기",description="던지는 중!!!", color=0x00aaaa)
                    msg1 = await message.channel.send(embed=embed)
                    await asyncio.sleep(1.0)
                    await msg1.delete()
                    a = ["앞면","뒷면","~~옆면~~"]
                    check = random.randint(0,1000)
                    if check == 1000:
                        check = 2
                    elif check <= 500:
                        check = 1
                    else:
                        check = 0
                    embed = discord.Embed(title = "동전을 던져보니 " + a[check] + "이 나왔어요" , color = 0x00aaaa )
                    await message.channel.send(embed = embed)
                else:
                    await message.channel.send(check_cooltime(message.author.id , "동전던지기"))

            elif word.startswith("주사위던지기"):
                if check_cooltime(message.author.id , "주사위던지기") == True:    
                    embed = discord.Embed(title="주사위던지기",description="던지는 중!!!", color=0x00aaaa)
                    msg1 = await message.channel.send(embed=embed)
                    await asyncio.sleep(1.0)
                    await msg1.delete()
                    check = random.randint(1,6)
                    embed = discord.Embed(title = "주사위를 던져보니 " + str(check) + "이 나왔어요" , color = 0x00aaaa )
                    await message.channel.send(embed = embed)
                else:
                    await message.channel.send(check_cooltime(message.author.id , "주사위던지기"))

            elif word.startswith('가위바위보'):
                if check_cooltime(message.author.id , "가위바위보") == True:    
                    rsp = ["가위","바위","보"]
                    embed = discord.Embed(title="가위바위보",description="가위바위보를 합니다 3초내로 (가위/바위/보)를 써주세요!", color=0x00aaaa)
                    channel = message.channel
                    msg1 = await message.channel.send(embed=embed)
                    def check(m):
                        return m.author == message.author and m.channel == channel
                    try:
                        msg2 = await client.wait_for('message', timeout=3.0, check=check)
                    except asyncio.TimeoutError:
                        await msg1.delete()
                        embed = discord.Embed(title="가위바위보",description="앗 3초가 지났네요...!", color=0x00aaaa)
                        await message.channel.send(embed=embed)
                        return
                    else:
                        await msg1.delete()
                        bot_rsp = str(random.choice(rsp))
                        user_rsp  = str(msg2.content)
                        answer = ""
                        if bot_rsp == user_rsp:
                            answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 비겼습니다."
                        elif (bot_rsp == "가위" and user_rsp == "바위") or (bot_rsp == "보" and user_rsp == "가위") or (bot_rsp == "바위" and user_rsp == "보"):
                            answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "아쉽지만 제가 졌습니다."
                        elif (bot_rsp == "바위" and user_rsp == "가위") or (bot_rsp == "가위" and user_rsp == "보") or (bot_rsp == "보" and user_rsp == "바위"):
                            answer = "저는 " + bot_rsp + "을 냈고, 당신은 " + user_rsp + "을 내셨내요.\n" + "제가 이겼습니다!"
                        else:
                            embed = discord.Embed(title="가위바위보",description="앗, 가위, 바위, 보 중에서만 내셔야죠...", color=0x00aaaa)
                            await message.channel.send(embed=embed)
                            return
                        embed = discord.Embed(title="가위바위보",description=answer, color=0x00aaaa)
                        await message.channel.send(embed=embed)
                        return
                else:
                    await message.channel.send(check_cooltime(message.author.id , "가위바위보"))

            elif word.startswith("더하기") or word.startswith("곱하기") or word.startswith("빼기") or word.startswith("나누기") or word.startswith("거듭제곱") or word.startswith("분석"):
                if check_cooltime(message.author.id , "계산친구들") == True:    
                    if word.startswith("더하기"):
                        binlist = word.split(" ")
                        if len(binlist) > 2:
                            answer = 0
                            a = int(len(binlist)) - 1
                            while a != 0:
                                answer = answer + int(binlist[a])
                                a = a - 1
                            await message.channel.send("답은 " + str(answer) + "입니다")
                        else:
                            await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

                    elif word.startswith("곱하기"):
                        binlist = word.split(" ")
                        if len(binlist) > 2:
                            answer = 1
                            a = int(len(binlist)) - 1
                            while a != 0:
                                answer = answer * int(binlist[a])
                                a = a - 1
                            await message.channel.send("답은 " + str(answer) + "입니다")
                        else:
                            await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

                    elif word.startswith("빼기"):
                        binlist = word.split(" ")
                        if len(binlist) == 3:
                            answer = 0
                            answer = int(binlist[1]) - int(binlist[2])            
                            await message.channel.send("답은 " + str(answer) + "입니다")
                        else:
                            await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

                    elif word.startswith("나누기"):
                        binlist = word.split(" ")
                        if len(binlist) == 3:
                            if binlist[2] == 0:
                                await message.channel.send("0으로 나눌수 없습니다")
                            else:
                                answer = 0
                                answer = int(binlist[1]) / int(binlist[2])            
                                await message.channel.send("답은 " + str(answer) + "입니다")
                        else:
                            await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")

                    elif word.startswith("거듭제곱"):
                        binlist = word.split(" ")
                        if len(binlist) == 3:
                            if int(binlist[2]) > 1999:
                                await message.channel.send("입력하신 숫자가 너무 ~~크고 아름다워서~~ 게산이 안되요 지수를 2000미만으로 해주세요")
                            else:    
                                try:
                                    if len(binlist) == 3:
                                        answer = pow(int(binlist[1]) , int(binlist[2]))
                                        await message.channel.send("답은 " + str(answer) + "입니다")
                                except:
                                    await message.channel.send("답이 2천자를 넘어가네요....;;죄송하지만 불가능합니다")
                        else:
                            await message.channel.send("문법오류!!ㅉ도움말 수학을 통해 문법확인하세요")
                    elif word.startswith("분석"):
                        a = word.split(" ")
                        d = len(a) - 1
                        b = []
                        while d != 0:
                            b.append(int(a[d]))
                            d = d-1
                        c = len(b)
                        qnstks = 0
                        vudrbs = int(sum(b)) / c
                        while c != 0:
                            qnstks = qnstks + pow(int(b[c-1] - vudrbs) , 2)
                            c = c - 1 
                        qnstks = qnstks / int(len(b) - 1)
                        embed = discord.Embed(title = "데이터 분석", color = 0xFFE400)
                        embed.add_field(name = "입력된 값들", value = b, inline = False)
                        embed.add_field(name = "평균", value = vudrbs , inline = False)
                        embed.add_field(name = "분산", value = qnstks, inline = False)
                        await message.channel.send(embed = embed)
                    else:
                        pass
                else:
                    await message.channel.send(check_cooltime(message.author.id , "계산친구들"))

            elif word.startswith("시간") or word.startswith("요일"):
                if check_cooltime(message.author.id , "시간,요일") == True:    
                    if word.startswith("시간"):
                        await message.channel.send(str(time.ctime()))
                    elif word.startswith("요일"):
                        binlist = word.split(" ")
                        a = calendar.weekday(int(binlist[1]) , int(binlist[2]) , int(binlist[3]))
                        days = ["월요일" , "화요일" , "수요일" , "목요일" , "금요일" , "토요일" , "일요일"]
                        await message.channel.send(str(days[a]) + "입니다")
                    else:
                        pass
                else:
                    await message.channel.send(check_cooltime(message.author.id , "시간,요일"))
            elif word.startswith("길이변환") or word.startswith("면적변환") or word.startswith("부피변환"):
                if check_cooltime(message.author.id , "변환친구들")  == True:   
                    if word.startswith("길이변환"):
                        wordlist = word.split(" ")
                        if len(wordlist) == 3 or 4:
                            if str(wordlist[2]) == "km" or "m" or "cm" or "mm" or "nm" or "in":    #길이변환 코드
                                if wordlist[2] == "km":
                                    mm = int(wordlist[1]) * 1000000
                                elif wordlist[2] == "m":
                                    mm = int(wordlist[1]) * 1000
                                elif wordlist[2] == "cm":
                                    mm = int(wordlist[1]) * 10
                                elif wordlist[2] == "nm":
                                    mm = int(wordlist[1]) * 0.000001
                                elif wordlist[2] == "in":
                                    mm = int(wordlist[1]) * 25.4
                                else:
                                    mm = int(wordlist[1])
                                if len(wordlist) == 3:
                                    embed = discord.Embed(title = "길이 단위", color = 0xFFE400)
                                    embed.add_field(name = "입력된 수", value = str(wordlist[1]) + str(wordlist[2]) , inline = False)
                                    embed.add_field(name = "km(킬로미터)", value = int(mm) / 1000000, inline = False)
                                    embed.add_field(name = "m(미터)", value = int(mm) / 1000, inline = False)
                                    embed.add_field(name = "cm(센티미터)", value = int(mm) / 10, inline = False)
                                    embed.add_field(name = "mm(밀리미터)", value = int(mm) , inline = False)
                                    embed.add_field(name = "nm(나노미터)", value = int(mm) / 0.000001 , inline = False)
                                    embed.add_field(name = "in(인치)", value = int(mm) / 25.4 , inline = False)
                                    await message.channel.send(embed = embed)
                                else:
                                    if wordlist[3] == "km":
                                        need = int(mm) / 1000000                  
                                    elif wordlist[3] == "m":
                                        need = int(mm) / 1000
                                    elif wordlist[3] == "cm":
                                        need= int(mm) / 10
                                    elif wordlist[3] == "nm":
                                        need = int(mm) / 0.000001
                                    elif wordlist[3] == "in":    
                                        need = int(mm) / 25.4
                                    else:
                                        need = int(mm)
                                    embed = discord.Embed(title = "길이 변환", color = 0xFFE400)
                                    embed.add_field(name = wordlist[1] + wordlist[2], value = str(need) + wordlist[3] , inline = False)
                                    await message.channel.send(embed = embed)
                            else:
                                await message.channel.send("없는 단위입니다")
                        else:
                            await message.channel.send("문법오류!! ㅉ도움 수학 을 통해서 문법확인하세요")
                    elif word.startswith("면적변환"):
                        wordlist = word.split(" ")
                        if len(wordlist) == 3 or 4:
                            if str(wordlist[2]) == "km2" or "m2" or "cm2" or "평" or "mm2":    #면적변환 코드
                                if wordlist[2] == "km2":
                                    cm2 = int(wordlist[1]) * 10000000000
                                elif wordlist[2] == "m2":
                                    cm2 = int(wordlist[1]) * 10000
                                elif wordlist[2] == "cm2":
                                    cm2 = int(wordlist[1]) 
                                elif wordlist[2] == "평":
                                    cm2 = int(wordlist[1]) * 33057
                                else:
                                    cm2 = int(wordlist[1]) / 100
                                if len(wordlist) == 3:
                                    embed = discord.Embed(title = "면적 단위", color = 0xFFE400)
                                    embed.add_field(name = "입력된 수", value = str(wordlist[1]) + str(wordlist[2]) , inline = False)
                                    embed.add_field(name = "km2(제곱킬로미터)", value = int(cm2) / 10000000000, inline = False)
                                    embed.add_field(name = "m2(제곱미터)", value = int(cm2) / 10000, inline = False)
                                    embed.add_field(name = "cm2(제곱센티미터)", value = int(cm2) , inline = False)
                                    embed.add_field(name = "mm2(제곱밀리미터)", value = int(cm2) / 0.01, inline = False)
                                    embed.add_field(name = "평", value = int(cm2) / 33057.85 , inline = False)
                                    await message.channel.send(embed = embed)
                                else:
                                    if wordlist[3] == "km2":
                                        need = int(cm2) / 10000000000                
                                    elif wordlist[3] == "m2":
                                        need = int(cm2) / 10000
                                    elif wordlist[3] == "cm2":
                                        need= int(cm2)
                                    elif wordlist[3] == "mm2":
                                        need = int(cm2) * 100
                                    else:
                                        need = int(cm2) / 33057
                                    embed = discord.Embed(title = "면적 변환", color = 0xFFE400)
                                    embed.add_field(name = wordlist[1] + wordlist[2], value = str(need) + wordlist[3] , inline = False)
                                    await message.channel.send(embed = embed)
                            else:
                                message.channel.send("없는 단위입니다")
                        else:
                            message.channel.send("문법 오류!! ㅉ도움 수학 을 통해 문법확인 하세요")
                    elif word.startswith("부피변환"):
                        wordlist = word.split(" ")
                        if len(wordlist) == 3 or 4:
                            if str(wordlist[2]) == "ml" or "l" or "cm3" or "m3" :    #부피변환 코드
                                if wordlist[2] == "ml":
                                    l = int(wordlist[1]) * 0.001
                                elif wordlist[2] == "cm3":
                                    l = int(wordlist[1]) * 0.001
                                elif wordlist[2] == "m3":
                                    l = int(wordlist[1]) * 1000
                                else:
                                    l = int(wordlist[1])
                                if len(wordlist) == 3:
                                    embed = discord.Embed(title = "부피 단위", color = 0xFFE400)
                                    embed.add_field(name = "입력된 수", value = str(wordlist[1]) + str(wordlist[2]) , inline = False)
                                    embed.add_field(name = "m3(세제곱미터)", value = int(l) / 1000, inline = False)
                                    embed.add_field(name = "cm3(세제곱센티미터)", value = int(cm2) * 1000 , inline = False)
                                    embed.add_field(name = "ml(밀리리터)", value = int(l) * 1000, inline = False)
                                    embed.add_field(name = "l(리터)", value = int(l)  , inline = False)
                                    await message.channel.send(embed = embed)
                                else:
                                    if wordlist[3] == "m3":
                                        need = int(l) / 1000                
                                    elif wordlist[3] == "ml":
                                        need= int(l) * 1000
                                    elif wordlist[3] == "cm3":
                                        need = int(l) * 10000
                                    else:
                                        need = int(l)
                                    embed = discord.Embed(title = "부피 변환", color = 0xFFE400)
                                    embed.add_field(name = wordlist[1] + wordlist[2], value = str(need) + wordlist[3] , inline = False)
                                    await message.channel.send(embed = embed)
                            else:
                                message.channel.send("없는 단위입니다")
                        else:
                            message.channel.send("문법 오류!! ㅉ도움 수학 을 통해 문법확인 하세요")
                    else:
                        pass
                else:
                    await message.channel.send(check_cooltime(message.author.id , "변환친구들"))
            
            elif word.startswith("건의하기") or word.startswith("건의사항삭제"):
                if word.startswith("건의하기"):    
                    code = int(message.author.id)
                    if code in codelist:
                        await message.channel.send("이미 건의를 하셨네요!!! 운영진이 답변을 해줄떄까지 기다리시거나 ㅉ건의사항삭제로 건의를 취소하세요")    
                    elif len(word[4:]) > 100:    
                        await message.channel.send("너무 길어요!!! 100자 미만으로 간결하게 적어주세요!!~~제 컴터좀 살려줘요~~")
                    else:            
                        if check_cooltime(message.author.id , "건의하기,건의사항삭제") == True:    
                            codelist.append(code)
                            wantlist.append(word[4:])
                            with open('iwant.txt', 'wb') as file:            
                                pickle.dump(codelist, file)
                                pickle.dump(wantlist, file)
                                pickle.dump(historylist , file)
                                embed = discord.Embed(title = "건의사항", description = "읽지 않은 건의사항이 있어요!", color = 0xffe400)
                                await client.get_channel(723307706223558746).send(embed = embed)
                                await message.channel.send("건의가 완료되었습니다!!! 빠르게 확인한 뒤 DM 거부가 아니시면 답변드릴게요!!!!!")
                        else:
                            await message.channel.send(check_cooltime(message.author.id , "건의하기,건의사항삭제"))                                    
                elif word.startswith("건의사항삭제"):
                    code = int(message.author.id)
                    if code in codelist:
                        if check_cooltime(message.author.id , "건의하기,건의사항삭제") == True:    
                            clear = codelist.index(code)
                            codelist.remove(codelist[clear])
                            wantlist.remove(wantlist[clear])
                            with open('iwant.txt', 'wb') as file:
                                pickle.dump(codelist, file)
                                pickle.dump(wantlist, file)
                                pickle.dump(historylist , file)
                            await message.channel.send("정상적으로 진행되었습니다...만 ~~바보같은~~운영진이 답변을 쓸수도 있으니 참고해 주세요")
                        else:
                            await message.channel.send(check_cooltime(message.author.id , "건의하기,건의사항삭제"))
                    else:
                        msg1 = await message.channel.send("음....~~건의사항을 보낸적이 없는데 지우라고???? 확 컴퓨터를 지워버릴까??~~")
                        time.sleep(5)
                        await msg1.delete()
                        await message.channel.send("건의사항을 보내신적이 없어요")
                else:
                    pass    
            elif word.startswith("아스키변환") or word.startswith("아스키해독") or word.startswith("아스키해석"):
                if check_cooltime(message.author.id , "아스키") == True:    
                    if word.startswith("아스키변환"):
                        scr = word[6:]
                        count = len(scr)
                        answer = ""
                        for i in range(0,count):
                            answer = answer + str(ord(scr[i])) + "/"
                        answer = answer[:-1]
                        await message.channel.send(scr + "의 아스키코드 변환값은 " + answer + "입니다!!!!!")
                    elif word.startswith("아스키해독") or word.startswith("아스키해석"):
                        scr = word[6:]
                        binlist = scr.split("/")
                        answer = ""
                        for i in range(0 , len(binlist)):
                            answer = answer + chr(int(binlist[i]))
                        await message.channel.send(scr + "의 해독 결과는 " + answer + "입니다!!")
                    else:
                        pass
                else:
                    await message.channel.send(check_cooltime(message.author.id , "아스키"))

            elif word.startswith("한글분리"):
                word = word[5:]
                await message.channel.send(detach_korean(word))

            elif word.startswith("로그채널등록"):
                global serverlist , serverloglist
                server = message.guild
                if server.id in serverlist:
                    await message.channel.send("이미 등록된 채널이 있어요")
                else:
                    if message.channel.name.startswith("짭다봇로그"):
                        serverlist.append(server.id)
                        serverloglist.append(message.channel.id)
                        with open('serverlog.txt', 'wb') as file:
                            pickle.dump(serverlist, file)
                            pickle.dump(serverloglist, file)
                        await message.channel.send("설정이 완료되었습니다 앞으로 삭제/변경로그는 이 채널에 나옵니다")
                    else:
                        await message.channel.send("설정하시려면 채널이름을 짭다봇로그로 시작해주셔야 합니다")
                        await message.channel.send("일반 유저의 도배를 막고 일정한 권한이 있는사람만 할수 있도록 하는 조치이니 따라주세요")

            
            elif word.startswith("서버정보") or word.startswith("채널정보") or word.startswith("짭다봇") or word.startswith("잡다봇"):
                if check_cooltime(message.author.id , "정보") == True:    
                    if word.startswith("서버정보"):
                        server = message.guild
                        embed = discord.Embed(title = "서버정보", color = 0xFFE400)
                        embed.add_field(name = "서버를 만든사람~~(대빵)~~", value = server.owner, inline = False)
                        embed.add_field(name = "니트로 가입자~~(흑우들)~~", value = server.premium_subscribers, inline = False)
                        embed.add_field(name = "멤버수 " , value = server.member_count , inline = True)
                        embed.add_field(name = "생성일" , value = server.created_at , inline = True)
                        await message.channel.send(embed = embed)
                    elif word.startswith("채널정보"):
                        channel = message.channel
                        embed = discord.Embed(title = "채널정보", color = 0xFFE400)
                        embed.add_field(name = "채널의 이름", value = channel.name, inline = False)
                        embed.add_field(name = "채널의 생성일", value = channel.created_at, inline = False)
                        embed.add_field(name = "카테고리 " , value = channel.category , inline = True)
                        embed.add_field(name = "주제" , value = channel.topic , inline = True)
                        await message.channel.send(embed = embed)
                    elif word == "짭다봇" or word == "잡다봇":
                        embed = discord.Embed(title = "잡다한 기능이 있는봇", description = "잡다한 기능을 통해 디스코드를 더욱 더\n재밌고 편리하게 만들어주는 봇입니다!", color = 0xffe400)
                        embed.add_field(name = "초대코드", value = "https://discord.com/api/oauth2/authorize?client_id=712898282979983420&permissions=3529792&scope=bot", inline = False)
                        embed.add_field(name = "공식 커뮤니티", value = "https://discord.gg/FZ4QRZ9", inline = False)
                        embed.set_thumbnail(url = "https://media.discordapp.net/attachments/722797114647904296/735323638890233876/663bd596a48b6202.png?width=630&height=630")
                        embed.set_footer(text = "개발자 - 설망래, 이끼 낀 금화")
                        await message.channel.send(embed = embed)
                    else:
                        pass
                else:
                    await message.channel.send(check_cooltime(message.author.id , "정보"))

            elif word.startswith("소인수분해"):
                word = word.split(" ")[1]
                msg = await message.channel.send(word + "를 소인수분해중입니다")
                if len(word) > 15:
                    await msg.delete()
                    await message.channel.send("너무 큰 숫자입니다 15자리 이내로 입력해주세요")
                else:
                    if word.isdigit():
                        if check_cooltime(message.author.id , "소인수분해") == True:
                            a = primefactor(word)
                            await msg.delete()
                            await message.channel.send(a)
                        else:
                            await msg.delete()
                            await message.channel.send(check_cooltime(message.author.id , "소인수분해"))
                    else:    
                        await msg.delete()
                        await message.channel.send("자연수만 넣어주세요")
                        return None
            elif word.startswith("핑"):
                if check_cooltime(message.author.id , "핑") == True:
                    embed = discord.Embed(title = "핑 측정", color = 0xFFE400)
                    embed.add_field(name = "핑 측정 결과" , value = str(client.latency)[0:5] + "초입니다")
                    await message.channel.send(embed = embed)
                else:
                    await message.channel.send(check_cooltime(message.author.id , "핑"))
                    
                    

            elif word.startswith("개인접두사설정"):
                noprefix = ["@","~","/","_","|"]
                perprefix = word.split(" ")[1]
                if len(perprefix) > 4 or len(perprefix) < 1:
                    await message.channel.send("접두사는 1글자 이상 4글자 이하까지만 되요")
                    return None
                else:
                    pass
                for i in range(0 , len(noprefix)):
                    if noprefix[i] in perprefix:
                        await message.channel.send("접두사에는 특수문자(@,/,~,_)등은 사용이 불가능합니다")
                        return None
                    else:
                        pass
                if message.author.id in userlist:
                    number = userlist.index(message.author.id)
                    del userlist[number]
                    del userprefixlist[number]
                else:
                    pass
                if check_cooltime(message.author.id , "접두사설정") == True:    
                    userlist.append(message.author.id)
                    userprefixlist.append(perprefix)
                    with open('prefix.txt', 'wb') as file:
                        pickle.dump(userlist, file)
                        pickle.dump(userprefixlist, file)
                    await message.channel.send(str(message.author) + "님의 개인 접두사가" + perprefix + "로 변경되었습니다")
                else:
                    await message.channel.send(check_cooltime(message.author.id , "접두사설정"))


            elif word.startswith('지뢰찾기'):
                number_English = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',0:'zero'}
                if word.count('/') != 2:
                    await message.channel.send("가로의 길이와 세로의 길이와 지뢰의 갯수를 '/' 으로 구분해주어야 해요!")
                else:
                    word = word[5:]
                    width = word.split('/')[0]
                    height = word.split('/')[1]
                    mine_count = word.split('/')[2]
                    if width.isdigit() and height.isdigit() and mine_count.isdigit():
                        width = int(width)
                        height = int(height)
                        mine_count = int(mine_count)
                        if width > 10 or height > 10:
                            await message.channel.send("가로와 세로의 길이는 10 이하여야 해요!")
                            return
                        if mine_count > width * height:
                            await message.channel.send("지뢰의 갯수는 칸의 갯수보다 많으면 안돼요!")
                            return
                        if check_cooltime(message.author.id , "지뢰찾기") == True:    
                            mine_map = []
                            for i in range(height):
                                mine_map.append([])
                                for j in range(width):
                                    mine_map[i].append(0)
                            check = 0
                            while check < mine_count:
                                mine_x, mine_y = random.randint(0, width - 1), random.randint(0, height - 1)
                                if mine_map[mine_y][mine_x] != 9:
                                    mine_map[mine_y][mine_x] = 9
                                    if mine_x != 0:
                                        if mine_map[mine_y][mine_x - 1] != 9:
                                            mine_map[mine_y][mine_x - 1] += 1
                                        if mine_y != 0:
                                            if mine_map[mine_y - 1][mine_x - 1] != 9:
                                                mine_map[mine_y - 1][mine_x - 1] += 1
                                        if mine_y != height - 1:
                                            if mine_map[mine_y + 1][mine_x - 1] != 9:
                                                mine_map[mine_y + 1][mine_x - 1] += 1
                                    if mine_x != width - 1:
                                        if mine_map[mine_y][mine_x + 1] != 9:
                                            mine_map[mine_y][mine_x + 1] += 1
                                        if mine_y != 0:
                                            if mine_map[mine_y - 1][mine_x + 1] != 9:
                                                mine_map[mine_y - 1][mine_x + 1] += 1
                                        if mine_y != height - 1:
                                            if mine_map[mine_y + 1][mine_x + 1] != 9:
                                                mine_map[mine_y + 1][mine_x + 1] += 1
                                    if mine_y != 0:
                                        if mine_map[mine_y - 1][mine_x] != 9:
                                            mine_map[mine_y - 1][mine_x] += 1
                                    if mine_y != height - 1:
                                        if mine_map[mine_y + 1][mine_x] != 9:
                                            mine_map[mine_y + 1][mine_x] += 1
                                    check += 1
                            word = ''
                            for i in range(height):
                                for j in range(width):
                                    if mine_map[i][j] == 9:
                                        word = word + '||:boom:||'
                                    elif mine_map[i][j] == 0:
                                        word = word + ':blue_square:'
                                    else:
                                        word = word + '||:' + number_English[mine_map[i][j]] + ':||'
                                word = word + '\n'
                            word = word + '지뢰갯수 : ' + str(mine_count)
                            await message.channel.send(word)
                        else:
                            await message.channel.send(check_cooltime(message.author.id , "지뢰찾기"))
                    else:
                        await message.channel.send("'/' 사이에는 정수만 들어가야 해요!")
                        
            elif word.startswith("미로"):
                
                # ---------- 미로를 만들수 있는 조건인지 확인 ----------
                if check_cooltime(message.author.id, "미로") != True: # 미로 쿨타임 확인
                    await message.channel.send(check_cooltime(message.author.id, "미로"))
                    return
                word = word[3:].split('/') # word[0] = 가로의 길이, word[1] = 세로의 길이
                if len(word) != 2: # 가로와 세로를 썼는지 / 가로와 세로 이외에 썼는지 확인
                    await message.channel.send("가로와 세로의 길이만 '/' 으로 구분해주어야 해요! (예 : 미로 10/10)")
                    return
                try: # 쓴 가로와 세로가 숫자인지 확인 / 쓴 숫자가 소수라면 정수로 바꾸기
                    maze_width = int(word[0]) # 미로의 가로세로길이
                    maze_height = int(word[1])
                except:
                    await message.channel.send("가로와 세로의 길이는 자연수여야 해요!")
                    return
                if maze_width < 1 or 50 < maze_width or maze_height < 1 or 50 < maze_height: # 미로의 가로와 세로의 길이가 적당한지 확인
                    await message.channel.send("가로와 세로의 길이는 1 ~ 50 이어야 해요!")
                    return
                maze_size = maze_width * maze_height
                if maze_size < 51:
                    await message.channel.send("예상시간 : 0.6초")
                elif maze_size < 251:
                    await message.channel.send("예상시간 : 0.8초")
                elif maze_size < 651:
                    await message.channel.send("예상시간 : 1.2초")
                elif maze_size < 1251:
                    await message.channel.send("예상시간 : 2.6초")
                elif maze_size < 2051:
                    await message.channel.send("예상시간 : 4.6초")
                else:
                    await message.channel.send("예상시간 : 5.2초")

                # ---------- 미로 제작 ----------
                maze_map = [] # 미로판. 0 = 길(하양), 1 = 벽(검정), 2 = 입구(초록), 3 = 출구(빨강) (미로판 ≠ 미로)
                maze_map_width, maze_map_height = maze_width * 2 + 1, maze_height * 2 + 1 # 미로판의 가로세로길이
                maze_check = [] # 만들어진 구역
                maze_map_not_check = [] # maze_check와 인접하지만 만들어지지 않은 구역
                maze_answer_pos = [] # 미로의 전의 길을 기록하는 리스트 (정답에 필요)
                for i in range(maze_map_width): # 미로 기본틀 제작
                    maze_map.append([])
                    for j in range(maze_map_height):
                        if i % 2 == 0 or j % 2 == 0:
                            maze_map[i].append(1)
                        else:
                            maze_map[i].append(0)
                maze_map[0][1] = 2 # 미로의 입구
                maze_check.append([1, 1])
                maze_answer_pos.append(0) # 미로의 시작부분의 순서를 저장함
                
                for i in range(maze_width * maze_height - 1): # 미로 길 뚫기
                    if maze_check[-1][0] < maze_map_width - 2 and not [maze_check[-1][0] + 2, maze_check[-1][1]] in maze_check and not [maze_check[-1][0] + 2, maze_check[-1][1]] in maze_map_not_check: # 새로 뚫린길 주변이 maze_check에 없다면 maze_map_not_check에 추가
                        maze_map_not_check.append([maze_check[-1][0] + 2, maze_check[-1][1]])
                    if maze_check[-1][0] > 1 and not [maze_check[-1][0] - 2, maze_check[-1][1]] in maze_check and not [maze_check[-1][0] - 2, maze_check[-1][1]] in maze_map_not_check:
                        maze_map_not_check.append([maze_check[-1][0] - 2, maze_check[-1][1]])
                    if maze_check[-1][1] < maze_map_height - 2 and not [maze_check[-1][0], maze_check[-1][1] + 2] in maze_check and not [maze_check[-1][0], maze_check[-1][1] + 2] in maze_map_not_check:
                        maze_map_not_check.append([maze_check[-1][0], maze_check[-1][1] + 2])
                    if maze_check[-1][1] > 1 and not [maze_check[-1][0], maze_check[-1][1] - 2] in maze_check and not [maze_check[-1][0], maze_check[-1][1] - 2] in maze_map_not_check:
                        maze_map_not_check.append([maze_check[-1][0], maze_check[-1][1] - 2])
                    maze_check_end = random.randint(0, len(maze_map_not_check) - 1) # maze_check_end : 뚫을 길의 끝이 리스트의 어느 항목인지 알려줌. maze_check_start와 인접해 있어야 함 / 아래부터는 end라 부르겠음
                    maze_check_start = [] # maze_check_start : 뚫을 길의 시작이 리스트의 어느 항목인지 알려줌 / 아래부터는 start라 부르겠음
                    maze_check_direction = [] # start에서 어느쪽으로 벽을 뚫어야 end로 갈수있는지 알려줌 (이름만 방향이고 [x좌표, y좌표] 임) / 아래부터는 direction이라 부르겠음
                    if [maze_map_not_check[maze_check_end][0] + 2, maze_map_not_check[maze_check_end][1]] in maze_check: # end와 근접해있는 maze_check(start) 를 찾음
                        maze_check_start.append(maze_check.index([maze_map_not_check[maze_check_end][0] + 2, maze_map_not_check[maze_check_end][1]]))
                        maze_check_direction.append([1, 0])
                    if [maze_map_not_check[maze_check_end][0] - 2, maze_map_not_check[maze_check_end][1]] in maze_check:
                        maze_check_start.append(maze_check.index([maze_map_not_check[maze_check_end][0] - 2, maze_map_not_check[maze_check_end][1]]))
                        maze_check_direction.append([-1, 0])
                    if [maze_map_not_check[maze_check_end][0], maze_map_not_check[maze_check_end][1] + 2] in maze_check:
                        maze_check_start.append(maze_check.index([maze_map_not_check[maze_check_end][0], maze_map_not_check[maze_check_end][1] + 2]))
                        maze_check_direction.append([0, 1])
                    if [maze_map_not_check[maze_check_end][0], maze_map_not_check[maze_check_end][1] - 2] in maze_check:
                        maze_check_start.append(maze_check.index([maze_map_not_check[maze_check_end][0], maze_map_not_check[maze_check_end][1] - 2]))
                        maze_check_direction.append([0, -1])
                    maze_check.append(maze_map_not_check[maze_check_end]) # 만들어지지 않은 구역(end)을 만들어진 구역으로 옴김
                    del maze_map_not_check[maze_check_end]
                    a = random.randint(0, len(maze_check_start) - 1) # 여러개의 start와 direction 중 하나를 고름
                    maze_check_start = maze_check_start[a]
                    maze_check_direction = maze_check_direction[a]
                    maze_map[maze_check[-1][0] + maze_check_direction[0]][maze_check[-1][1] + maze_check_direction[1]] = 0 # start와 end사이의 벽을 뚫음 (길로 만듬)
                    maze_answer_pos.append(maze_check[maze_check_start]) # 이 길을 어느길에서 와야하는지 저장

                maze_map[maze_map_width - 1][maze_map_height - 2] = 3 # 미로의 출구
                maze_exit = [maze_map_width - 2, maze_map_height - 2]
                maze_exit = maze_check.index(maze_exit)

                # 미로 사진으로 출력
                maze_pixel = [] # 미로 데이터를 색깔로 옴기기
                for i in range(maze_map_height):
                    for j in range(maze_map_width):
                        if maze_map[j][i] == 0:
                            maze_pixel.append((255, 255, 255))
                        elif maze_map[j][i] == 1:
                            maze_pixel.append((0, 0, 0))
                        elif maze_map[j][i] == 2:
                            maze_pixel.append((0, 255, 0))
                        elif maze_map[j][i] == 3:
                            maze_pixel.append((255, 0, 0))
                maze_image = Image.new("RGB", (maze_map_width, maze_map_height), "white") # 새로운 백지 사진 만들기
                maze_image.putdata(maze_pixel) # 사진에 미로 붙이기
                maze_image = maze_image.resize((maze_map_width * 10, maze_map_height * 10), resample = False) # 미로의 길이를 10배로 만듬
                maze_image.save("maze_image.png") # 미로사진 저장

                maze_pixel[maze_check[0][0] + maze_check[0][1] * maze_map_width] = (255, 127, 0)
                while maze_answer_pos[maze_exit] != 0: # 정답 표시하기
                    maze_check_start = [maze_check[maze_exit][0], maze_check[maze_exit][1]]
                    maze_check_end = [maze_answer_pos[maze_exit][0], maze_answer_pos[maze_exit][1]]
                    maze_pixel[maze_check_start[0] + maze_check_start[1] * maze_map_width] = (255, 127, 0)
                    if maze_check_start[0] == maze_check_end[0]:
                        if maze_check_start[1] < maze_check_end[1]:
                            maze_pixel[maze_check_start[0] + (maze_check_start[1] + 1) * maze_map_width] = (255, 127, 0)
                        else:
                            maze_pixel[maze_check_start[0] + (maze_check_start[1] - 1) * maze_map_width] = (255, 127, 0)
                    else:
                        if maze_check_start[0] < maze_check_end[0]:
                            maze_pixel[maze_check_start[0] + 1 + maze_check_start[1] * maze_map_width] = (255, 127, 0)
                        else:
                            maze_pixel[maze_check_start[0] - 1 + maze_check_start[1] * maze_map_width] = (255, 127, 0)
                    maze_exit = maze_check.index(maze_answer_pos[maze_exit])
                maze_image = Image.new("RGB", (maze_map_width, maze_map_height), "white") # 새로운 백지 사진 만들기
                maze_image.putdata(maze_pixel) # 사진에 미로 붙이기
                maze_image = maze_image.resize((maze_map_width * 10, maze_map_height * 10), resample = False) # 미로의 길이를 10배로 만듬
                maze_image.save("maze_image_answer.png") # 정답표시된 미로사진 저장

                await message.channel.send(file = discord.File("maze_image.png")) # 미로사진 올리기
                await message.channel.send(file = discord.File("maze_image_answer.png", spoiler = True)) # 정답표시된 미로사진 올리기
                    
            else:
                return None
        


        



client.run(BOT_TOKEN)
