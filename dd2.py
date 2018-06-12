# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator
#==============================================================================#
botStart = time.time()

nadya = LINE()
#nadya = LINE("TOKEN KAMU")
#nadya = LINE("Email","Password")
nadya.log("Auth Token : " + str(nadya.authToken))
channelToken = nadya.getChannelResult()
nadya.log("Channel Token : " + str(channelToken))

nadyaMID = nadya.profile.mid
nadyaProfile = nadya.getProfile()
lineSettings = nadya.getSettings()
oepoll = OEPoll(nadya)
#==============================================================================#
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")

read = json.load(readOpen)
settings = json.load(settingsOpen)

wait = {
   'acommentOn':False,
   'bcommentOn':False,
   'Tag':"ตั้งแทคด้วยครับ\n✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨",
   'message':"ระบบป้องกันรันจะทำการบล็อคคุณไว้\nหากต้องการให้ปลดกรุณาแท็กในกลุ่มบอกก่อนʕ•ᴥ•ʔ\n\n✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨"
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}

myProfile["displayName"] = nadyaProfile.displayName
myProfile["statusMessage"] = nadyaProfile.statusMessage
myProfile["pictureStatus"] = nadyaProfile.pictureStatus
#==============================================================================#
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
#    time.sleep(3)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    nadya.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        nadya.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
        
def helpmessage():
    helpMessage = "✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨" + "\n" + \
                  " " + "\n" + \
                  "✪〘เมนูคำสั่ง〙✪" + "\n" + \
                  "🌠คำสั่ง" + "\n" + \
                  "🌠คำสั่ง2" + "\n" + \
         	     " " + "\n" + \
                  "✪〘สเตตัส〙✪" + "\n" + \
                  "🌠สปีด" + "\n" + \
                  "🌠เช็คค่า" + "\n" + \
                  "🌠ข้อมูล" + "\n" + \
                  "🌠เทส" + "\n" + \
                  "🌠รีบอท" + "\n" + \
                  "🌠ออน" + "\n" + \
                  "🌠พูด(ข้อความ)" + "\n" + \
                  "🌠ชื่อ: (ชื่อ)" + "\n" + \
                  "🌠ข้อมูล" + "\n" + \
                  "🌠โทร" + "\n" + \
                  "🌠เชคแอด" + "\n" + \
                  "🌠สแปม「On/Off」(ข้อความ)(เลข)" + "\n" + \
                  " " + "\n" + \
                  "✪〘เรา〙✪" + "\n" + \
                  "🌠คท" + "\n" + \
                  "🌠มิด" + "\n" + \
                  "🌠ชื่อ" + "\n" + \
                  "🌠ตัส" + "\n" + \
                  "🌠รูป" + "\n" + \
                  "🌠ปก" + "\n" + \
		          " " + "\n" + \
                  "✪〘คนอื่น〙✪" + "\n" + \
                  "🌠คท @" + "\n" + \
                  "🌠มิด @" + "\n" + \
                  "🌠ชื่อ @" + "\n" + \
                  "🌠ตัส @" + "\n" + \
                  "🌠ดิส @" + "\n" + \
                  "🌠เตะ @" + "\n" + \
                  "🌠เด้ง @" + "\n" + \
                  "🌠!แทค" + "\n" + \
                  "🌠!มิด" "\n" + \
                  "🌠!คท" + "\n" + \
                  " " + "\n" + \
                  "✪〘กลุ่ม〙✪" + "\n" + \
                  "🌠แทค" + "\n" + \
                  "🌠ชื่อกลุ่ม" + "\n" + \
                  "🌠ไอดีกลุ่ม" + "\n" + \
                  "🌠รูปกลุ่ม" + "\n" + \
                  "🌠กลุ่มทั้งหมด" + "\n" + \
                  "🌠ข้อมูลกลุ่ม" + "\n" + \
                  "🌠สมาชิก" + "\n" + \
                  "🌠ลิ้งกลุ่ม" + "\n" + \
	              "🌠ลิ้ง 「On/Off」" + "\n" + \
                  " " + "\n" + \
                  "✪〘คำสั่งอื่นๆ〙✪" + "\n" + \
                  "🌠พิมตาม 「On/Off」" + "\n" + \
                  "🌠เพิ่มพิมตาม" + "\n" + \
                  "🌠ลบพิมตาม" + "\n" + \
                  "🌠เปิดอ่าน" + "\n" + \
                  "🌠ปิดอ่าน" + "\n" + \
                  "🌠อ่าน" + "\n" + \
                  "🌠ลบเวลา" + "\n" + \
                  "🌠ยกเลิก" + "\n" + \
                  "🌠!!ประกาศ:" + "\n" + \
                  " " + "\n" + \
                  "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡"
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   "✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨" + "\n" + \
                         " " + "\n " \
                         "✪〘คำสั่งตั้งค่าต่างๆ〙✪" + "\n" + \
                         "👑AutoJoin 「On/Off」" + "\n" + \
                         "👑AutoRead「On/Off」" + "\n" + \
                         "👑AutoBlock 「On/Off」" + "\n" + \
                         "👑CheckSticker「On/Off」" + "\n" + \
                         "👑AutoLeave 「On/Off」" + "\n" + \
                         "👑Tag 「On/Off」" + "\n" + \
                         "👑Tag2 「On/Off」" + "\n" + \
                         "👑Join 「On/Off」" + "\n" + \
                         "👑Leave 「On/Off」" + "\n" + \
                         "👑Tag:" + "\n" + \
                         "👑Join:" + "\n" + \
                         "👑Leave:" + "\n" + \
                         " " + "\n " \
                         "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡"
    return helpTextToSpeech

def helptranslate():
    helpTranslate =    "╔══[ T R A N S L A T E ]" + "\n" + \
                       "╠ af : afrikaans" + "\n" + \
                       "╠ sq : albanian" + "\n" + \
                       "╠ am : amharic" + "\n" + \
                       "╠ ar : arabic" + "\n" + \
                       "╠ hy : armenian" + "\n" + \
                       "╠ az : azerbaijani" + "\n" + \
                       "╠ eu : basque" + "\n" + \
                       "╠ be : belarusian" + "\n" + \
                       "╠ bn : bengali" + "\n" + \
                       "╠ bs : bosnian" + "\n" + \
                       "╠ bg : bulgarian" + "\n" + \
                       "╠ ca : catalan" + "\n" + \
                       "╠ ceb : cebuano" + "\n" + \
                       "╠ ny : chichewa" + "\n" + \
                       "╠ zh-cn : chinese (simplified)" + "\n" + \
                       "╠ zh-tw : chinese (traditional)" + "\n" + \
                       "╠ co : corsican" + "\n" + \
                       "╠ hr : croatian" + "\n" + \
                       "╠ cs : czech" + "\n" + \
                       "╠ da : danish" + "\n" + \
                       "╠ nl : dutch" + "\n" + \
                       "╠ en : english" + "\n" + \
                       "╠ eo : esperanto" + "\n" + \
                       "╠ et : estonian" + "\n" + \
                       "╠ tl : filipino" + "\n" + \
                       "╠ fi : finnish" + "\n" + \
                       "╠ fr : french" + "\n" + \
                       "╠ fy : frisian" + "\n" + \
                       "╠ gl : galician" + "\n" + \
                       "╠ ka : georgian" + "\n" + \
                       "╠ de : german" + "\n" + \
                       "╠ el : greek" + "\n" + \
                       "╠ gu : gujarati" + "\n" + \
                       "╠ ht : haitian creole" + "\n" + \
                       "╠ ha : hausa" + "\n" + \
                       "╠ haw : hawaiian" + "\n" + \
                       "╠ iw : hebrew" + "\n" + \
                       "╠ hi : hindi" + "\n" + \
                       "╠ hmn : hmong" + "\n" + \
                       "╠ hu : hungarian" + "\n" + \
                       "╠ is : icelandic" + "\n" + \
                       "╠ ig : igbo" + "\n" + \
                       "╠ id : indonesian" + "\n" + \
                       "╠ ga : irish" + "\n" + \
                       "╠ it : italian" + "\n" + \
                       "╠ ja : japanese" + "\n" + \
                       "╠ jw : javanese" + "\n" + \
                       "╠ kn : kannada" + "\n" + \
                       "╠ kk : kazakh" + "\n" + \
                       "╠ km : khmer" + "\n" + \
                       "╠ ko : korean" + "\n" + \
                       "╠ ku : kurdish (kurmanji)" + "\n" + \
                       "╠ ky : kyrgyz" + "\n" + \
                       "╠ lo : lao" + "\n" + \
                       "╠ la : latin" + "\n" + \
                       "╠ lv : latvian" + "\n" + \
                       "╠ lt : lithuanian" + "\n" + \
                       "╠ lb : luxembourgish" + "\n" + \
                       "╠ mk : macedonian" + "\n" + \
                       "╠ mg : malagasy" + "\n" + \
                       "╠ ms : malay" + "\n" + \
                       "╠ ml : malayalam" + "\n" + \
                       "╠ mt : maltese" + "\n" + \
                       "╠ mi : maori" + "\n" + \
                       "╠ mr : marathi" + "\n" + \
                       "╠ mn : mongolian" + "\n" + \
                       "╠ my : myanmar (burmese)" + "\n" + \
                       "╠ ne : nepali" + "\n" + \
                       "╠ no : norwegian" + "\n" + \
                       "╠ ps : pashto" + "\n" + \
                       "╠ fa : persian" + "\n" + \
                       "╠ pl : polish" + "\n" + \
                       "╠ pt : portuguese" + "\n" + \
                       "╠ pa : punjabi" + "\n" + \
                       "╠ ro : romanian" + "\n" + \
                       "╠ ru : russian" + "\n" + \
                       "╠ sm : samoan" + "\n" + \
                       "╠ gd : scots gaelic" + "\n" + \
                       "╠ sr : serbian" + "\n" + \
                       "╠ st : sesotho" + "\n" + \
                       "╠ sn : shona" + "\n" + \
                       "╠ sd : sindhi" + "\n" + \
                       "╠ si : sinhala" + "\n" + \
                       "╠ sk : slovak" + "\n" + \
                       "╠ sl : slovenian" + "\n" + \
                       "╠ so : somali" + "\n" + \
                       "╠ es : spanish" + "\n" + \
                       "╠ su : sundanese" + "\n" + \
                       "╠ sw : swahili" + "\n" + \
                       "╠ sv : swedish" + "\n" + \
                       "╠ tg : tajik" + "\n" + \
                       "╠ ta : tamil" + "\n" + \
                       "╠ te : telugu" + "\n" + \
                       "╠ th : thai" + "\n" + \
                       "╠ tr : turkish" + "\n" + \
                       "╠ uk : ukrainian" + "\n" + \
                       "╠ ur : urdu" + "\n" + \
                       "╠ uz : uzbek" + "\n" + \
                       "╠ vi : vietnamese" + "\n" + \
                       "╠ cy : welsh" + "\n" + \
                       "╠ xh : xhosa" + "\n" + \
                       "╠ yi : yiddish" + "\n" + \
                       "╠ yo : yoruba" + "\n" + \
                       "╠ zu : zulu" + "\n" + \
                       "╠ fil : Filipino" + "\n" + \
                       "╠ he : Hebrew" + "\n" + \
                       "╚══[ Jangan Typo ]" + "\n" + "\n\n" + \
                         "Contoh : tr"
    return helpTranslate
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return
        if op.type == 5:
            print ("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                nadya.blockContact(op.param1)
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = nadya.getGroup(op.param1)
            if settings["autoJoin"] == True:
                nadya.acceptGroupInvitation(op.param1)

        if op.type == 15:
            if wait["bcommentOn"] and "bcomment" in wait:
                nadya.sendMessage(op.param1,nadya.getContact(op.param2).displayName + "\n\n" + str(wait["bcomment"]))

        if op.type == 17:
            if wait["acommentOn"] and "acomment" in wait:
                cnt = nadya. getContact(op.param2)
                nadya.sendMessage(op.param1,cnt.displayName + "\n\n" + str(wait["acomment"]))

       if op.type == 24:
            print ("[ 24 ] NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                nadya.leaveRoom(op.param1)
        if op.type == 25:
            print ("[ 25 ] SEND MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != nadya.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
#==============================================================================#
                if text.lower() == 'คำสั่ง':
                    helpMessage = helpmessage()
                    nadya.sendMessage(to, str(helpMessage))
                elif text.lower() == 'คำสั่ง2':
                    helpTextToSpeech = helptexttospeech()
                    nadya.sendMessage(to, str(helpTextToSpeech))
                elif text.lower() == 'translate':
                    helpTranslate = helptranslate()
                    nadya.sendMessage(to, str(helpTranslate))
 #==============================================================================#
                 elif "สแปม " in msg.text:
                    txt = msg.text.split(" ")
                    jmlh = int(txt[2])
                    teks = msg.text.replace("สแปม "+str(txt[1])+" "+str(jmlh)+" ","")
                    tulisan = jmlh * (teks+"\n")
                    if txt[1] == "on":
                        if jmlh <= 100000:
                           for x in range(jmlh):
                               nadya.sendMessage(msg.to, teks)
                        else:
                           nadya.sendMessage(msg.to, "Out of Range!")
                    elif txt[1] == "off":
                        if jmlh <= 100000:
                            nadya.sendMessage(msg.to, tulisan)
                        else:
                            nadya.sendMessage(msg.to, "Out Of Range!")
                 elif "!!ประกาศ:" in msg.text:
                    bctxt = text.replace("!!ประกาศ:","")
                    n = nadya.getGroupIdsJoined()
                    for manusia in n:
                        nadya.sendMessage(manusia,(bctxt))
                elif "โทร" in msg.text.lower():
                     if msg.toType == 2:
                            sep = text.split(" ")
                            strnum = text.replace(sep[0] + " ","")
                            num = int(strnum)
                            nadya.sendMessage(to, "👍เชิญเข้าร่วมการโทรʕ•ᴥ•ʔ")
                            for var in range(0,num):
                                group = nadya.getGroup(to)
                                members = [mem.mid for mem in group.members]
                                nadya.acquireGroupCallRoute(to)
                                nadya.inviteIntoGroupCall(to, contactIds=members)
                elif "ทีมงาน" == msg.text.lower():
                    msg.contentType = 13
                    nadya.sendMessage(to, "✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨")
                    nadya.sendContact(to, "u07fb5496b409998a4f1f0af307d2c6e9")
                    nadya.sendContact(to, "ua11927d673a2ae7bab9c737e4bd206d2")
                    nadya.sendContact(to, "ua9ff83cd324d68d68952753f556c07c2")
                    nadya.sendContact(to, "ud4a3a6e0cea235eb8316c13637f82a7d")
                    nadya.sendContact(to, "u9ed31efc986199adedb27386c9b1f458")
                    nadya.sendContact(to, "u3f7b84b0f05591dd3bd459a23f238f1d")
                elif "เทส" == msg.text.lower():
                    nadya.sendMessage(to,"LOADING:▒...0%")
                    nadya.sendMessage(to,"█▒... 10.0%")
                    nadya.sendMessage(to,"██▒... 20.0%")
                    nadya.sendMessage(to,"███▒... 30.0%")
                    nadya.sendMessage(to,"████▒... 40.0%")
                    nadya.sendMessage(to,"█████▒... 50.0%")
                    nadya.sendMessage(to,"██████▒... 60.0%")
                    nadya.sendMessage(to,"███████▒... 70.0%")
                    nadya.sendMessage(to,"████████▒... 80.0%")
                    nadya.sendMessage(to,"█████████▒... 90.0%")
                    nadya.sendMessage(to,"███████████..100.0%")
                    nadya.sendMessage(to,"👍บอทปกติดีʕ•ᴥ•ʔ")
                elif "ชื่อ: " in msg.text.lower():
                    spl = re.split("ชื่อ: ",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                       prof = nadya.getProfile()
                       prof.displayName = spl[1]
                       nadya.updateProfile(prof)
                       nadya.sendMessage(to, "👍เปลี่ยนชื่อสำเร็จแล้วʕ•ᴥ•ʔ")
                elif "ยกเลิก" == msg.text.lower():
                    if msg.toType == 2:
                        group = nadya.getGroup(msg.to)
                        gMembMids = [contact.mid for contact in group.invitee]
                        for _mid in gMembMids:
                            nadya.cancelGroupInvitation(msg.to,[_mid])
                        nadya.sendMessage(to,"👍ยกเลิกค้างเชิญเสร็จสิ้นʕ•ᴥ•ʔ")
                elif text.lower() == 'ลบรัน':
                    gid = nadya.getGroupIdsInvited()
                    start = time.time()
                    for i in gid:
                        nadya.rejectGroupInvitation(i)
                    elapsed_time = time.time() - start
                    nadya.sendMessage(to, "👍กำลังดำเนินการʕ•ᴥ•ʔ")
                    nadya.sendMessage(to, "👍เวลาที่ใช้: %sวินาทีʕ•ᴥ•ʔ" % (elapsed_time))
                elif msg.text in ["spedd","Speed","Sp","sp"]:
                    start = time.time()
                    nadya.sendMessage(to, "👍การตอบสนองของบอทʕ•ᴥ•ʔ")
                    elapsed_time = time.time() - start
                    nadya.sendMessage(msg.to, "[ %s Seconds ]\n[ " % (elapsed_time) + str(int(round((time.time() - start) * 1000)))+" ms ]")
                elif text.lower() == 'รีบอท':
                    nadya.sendMessage(to, "กำลังรีบอท กรุณารอสักครู่.....")
                    time.sleep(5)
                    nadya.sendMessage(to, "รีบอทสำเร็จแล้ว\n✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨\n乂\n✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡")
                    restartBot()
                elif text.lower() == 'ออน':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    nadya.sendMessage(to, "ʕ•ᴥ•ʔระยะเวลาการทำงานของบอทʕ•ᴥ•ʔ\n{}".format(str(runtime)))
                elif text.lower() == 'ข้อมูล':
                    try:
                        arr = []
                        owner = "ude3230559bf63a55b9c28aa20ea194e3"
                        creator = nadya.getContact(owner)
                        contact = nadya.getContact(nadyaMID)
                        grouplist = nadya.getGroupIdsJoined()
                        contactlist = nadya.getAllContactIds()
                        blockedlist = nadya.getBlockedContactIds()
                        ret_ = "╔══[ ข้อมูลไอดีคุณ ]"
                        ret_ += "\n╠ ชื่อ : {}".format(contact.displayName)
                        ret_ += "\n╠ กลุ่ม : {}".format(str(len(grouplist)))
                        ret_ += "\n╠ เพื่อน : {}".format(str(len(contactlist)))
                        ret_ += "\n╠ บล็อค : {}".format(str(len(blockedlist)))
                        ret_ += "\n╚══[ ข้อมูลไอดีคุณ ]"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))
#==============================================================================#
                elif text.lower() == 'เชคค่า':
                    try:
                        ret_ = "╔════════════"
                        if settings["autoAdd"] == True: ret_ += "\n║ ระบบออโต้บล็อค ✔"
                        else: ret_ += "\n║ ระบบออโต้บล็อค ✘"
                        if settings["autoJoin"] == True: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✔"
                        else: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✘"
                        if settings["autoLeave"] == True: ret_ += "\n║ ระบบออกกลุ่มออโต้  ✔"
                        else: ret_ += "\n║ ระบบออกกลุ่มออโต้ ✘"
                        if settings["autoRead"] == True: ret_ += "\n║ ระบบอ่านข้อความออโต้  ✔"
                        else: ret_ += "\n║ ระบบอ่านข้อความออโต้ ✘"
                        if settings["checkSticker"] == True: ret_ += "\n║ ระบบเช็คสติ้กเกอร์ ✔"
                        else: ret_ += "\n║ ระบบเช็คสติ้กเกอร์ ✘"
                        if settings["detectMention"] == True: ret_ += "\n║ ระบบข้อความแทค ✔"
                        else: ret_ += "\n║ ระบบข้อความแทค ✘"
                        if settings["detectMention"] == True: ret_ += "\n║ ระบบแทคส่งรูป ✔"
                        else: ret_ += "\n║ ระบบแทคส่งรูป ✘"
                        if wait["acommentOn"] == True: ret_ += "\n║ ระบบตอนรับคนเข้ากลุ่ม ✔"
                        else: ret_ += "\n║ ระบบตอนรับคนเข้ากลุ่ม ✘"
                        if wait["bcommentOn"] == True: ret_ += "\n║ ระบบตอนรับคนออกกลุ่ม ✔"
                        else: ret_ += "\n║ ระบบตอนรับคนออกกลุ่ม ✘"
                        ret_ += "\n╚════════════"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoblock on':
                    settings["autoAdd"] = True
                    nadya.sendMessage(to, "👍เปิดระบบออโต้บล็อคแล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'autoblock off':
                    settings["autoAdd"] = False
                    nadya.sendMessage(to, "👎ปิดออโต้บล็อคแล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'autojoin on':
                    settings["AutoJoin"] = True
                    nadya.sendMessage(to, "👍เปิดระบบออโต้เข้ากลุ่มแล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'autojoin off':
                    settings["AutoJoin"] = False
                    nadya.sendMessage(to, "👎ปิดระบบเข้ากลุ่มออโต้แล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    nadya.sendMessage(to, "👍เปิดระบบออกกลุ่มออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    nadya.sendMessage(to, "👎ปิดระบบออกกลุ่มออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autoread on':
                    settings["AutoRead"] = True
                    nadya.sendMessage(to, "👍เปิดระบบอ่านออโต้แล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'autoread off':
                    settings["AutoRead"] = False
                    nadya.sendMessage(to, "👎ปิดระบบอ่านออโต้แล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'checkSticker on':
                    settings["checkSticker"] = True
                    nadya.sendMessage(to, "👍เปิดระบบแชร์ลิ้งสต๊กเกอร์แล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'checkSticker off':
                    settings["checkSticker"] = False
                    nadya.sendMessage(to, "👎ปิดระบบแชร์ลิ้งสติกเกอร์แล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'tag on':
                    settings["detectMention"] = True
                    nadya.sendMessage(to, "👍เปิดแทคเรียบร้อยʕ•ᴥ•ʔ")
                elif text.lower() == 'tag off':
                    settings["detectMention"] = False
                    nadya.sendMessage(to, "👎ปิดแทคเรียบร้อยแล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'tag2 on':
                    settings['potoMention'] = True
                    nadya.sendMessage(msg.to,"👍เปิดแทครูปภาพแล้วʕ•ᴥ•ʔ")
                elif text.lower() == 'tag2 off':
                    settings['potoMention'] = False
                elif msg.text.lower() ==  'join on':
                    wait['acommentOn'] = True
                    nadya.sendMessage(msg.to,"👍เปิดระบบข้อความตอนรับเข้าʕ•ᴥ•ʔ")
                elif msg.text.lower() ==  'join off':
                    wait['acommentOn'] = False
                    nadya.sendMessage(msg.to,"👎ปิดระบบข้อความตอนรับเข้าʕ•ᴥ•ʔ")
                elif msg.text.lower() == 'leave on':
                    wait["bcommentOn"] = True
                    nadya.sendMessage(msg.to,"👍เปิดระบบข้อความตอนรับออกʕ•ᴥ•ʔ")
                elif msg.text.lower() == 'leave off':
                    wait['leavemessage'] = False
                    nadya.sendMessage(msg.to,"👎ปิดระบบข้อความตอนรับออกʕ•ᴥ•ʔ")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    nadya.sendMessage(to, "👍ก็อปปี้ด้วยคอนแทคʕ•ᴥ•ʔ")

                elif "Tag: " in msg.text:
                    settings["Tag"] = msg.text.replace("Tag: ","")
                    nadya.sendMessage(msg.to,"👍ตั้งข้อความกล่าวถึงคนแทคสำเร็จʕ•ᴥ•ʔ\n\n" + "➤" + str(settings["Tag"]))

                elif "Join:" in msg.text.lower():
                    c = msg.text.replace("Join:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"👎เกิดข้อผิดพลาดʕ•ᴥ•ʔ")
                    else:
                        wait["acomment"] = c
                        nadya.sendMessage(msg.to,"👍ตั้งข้อความคนเข้าเสร็จสิ้นʕ•ᴥ•ʔ" + "\n\n➤" + str(wait["acomment"]))

                elif "Leave:" in msg.text.lower():
                    c = msg.text.replace("Leave:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"👎เกิดข้อผิดพลาดʕ•ᴥ•ʔ")
                    else:
                        wait["bcomment"] = c
                        nadya.sendMessage(msg.to,"👍ตั้งข้อความคนออกเสร็จสิ้นʕ•ᴥ•ʔ" + "\n\n➤" + str(wait["bcomment"]))
#==============================================================================#
                elif text.lower() == '!แทค':
                    gs = nadya.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        nadya.sendMessage(to, "👍ไม่มีคนใส่ชื่อร่องหนʕ•ᴥ•ʔ")
                    else:
                        mc = ""
                        for target in targets:
                            mc += sendMessageWithMention(to,target) + "\n"
                        nadya.sendMessage(to, mc)
                elif text.lower() == '!มิด':
                    gs = nadya.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        nadya.sendMessage(to, "👍ไม่มีคนใส่ชื่อร่องหนʕ•ᴥ•ʔ")
                    else:
                        mc = ""
                        for mi_d in lists:
                            mc += "->" + mi_d + "\n"
                        nadya.sendMessage(to,mc)
                elif text.lower() == '!คท':
                    gs = nadya.getGroup(to)
                    lists = []
                    for g in gs.members:
                        if g.displayName in "":
                            lists.append(g.mid)
                    if lists == []:
                        nadya.sendMessage(to, "👍ไม่มีคนใส่ชื่อร่องหนʕ•ᴥ•ʔ")
                    else:
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(to, mi_d)
                elif msg.text in ["Me","me","คท"]:
                    nadya.sendContact(to, nadyaMID)
                elif msg.text in ["มิด","MID","mid"]:
                    nadya.sendMessage(msg.to,nadyaMID)
                elif msg.text in ["ชื่อ","เนม","name","Name"]:
                    me = nadya.getContact(nadyaMID)
                    nadya.sendMessage(msg.to,me.displayName)
                elif msg.text in ["ตัส","สถานะ"]:
                    me = nadya.getContact(nadyaMID)
                    nadya.sendMessage(msg.to,me.statusMessage)
                elif msg.text in ["ดิส","รูป"]:
                    me = nadya.getContact(nadyaMID)
                    nadya.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif msg.text in ["ดิสวีดีโอ","รูปวีดีโอ","วีดีโอ"]:
                    me = nadya.getContact(nadyaMID)
                    nadya.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif msg.text in ["ปก","ดิสปก","รูปปก"]:
                    me = nadya.getContact(nadyaMID)
                    cover = nadya.getProfileCoverURL(nadyaMID)    
                    nadya.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("คท "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("มิด "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = " "
                        for ls in lists:
                            ret_ += "\n" + ls
                        nadya.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("ชื่อ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to,contact.displayName)
                elif msg.text.lower().startswith("ตัส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to,contact.statusMessage)
                elif msg.text.lower().startswith("ดิส "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus
                            nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("ข้อมูล "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to, contact.displayName)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                            contact = nadya.getContact(ls)
                            nadya.sendMessage(msg.to, contact.statusMessage)
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "\n"
                        for ls in lists:
                            ret_ += ls
                        nadya.sendMessage(msg.to, str(ret_))
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus
                            nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith(".cover "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = nadya.getProfileCoverURL(ls)
                                nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("copy "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            nadya.cloneContactProfile(contact)
                            nadya.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                        except:
                            nadya.sendMessage(msg.to, "Gagal clone member")
                            
                elif text.lower() == 'load':
                    try:
                        nadyaProfile.displayName = str(myProfile["displayName"])
                        nadyaProfile.statusMessage = str(myProfile["statusMessage"])
                        nadyaProfile.pictureStatus = str(myProfile["pictureStatus"])
                        nadya.updateProfileAttribute(8, nadyaProfile.pictureStatus)
                        nadya.updateProfile(nadyaProfile)
                        nadya.sendMessage(msg.to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                    except:
                        nadya.sendMessage(msg.to, "Gagal restore profile")
                        
#==============================================================================#
                elif "เด้ง:" in text:
                    midd = msg.text.replace("เด้ง:","")
                    nadya. kickoutFromGroup(msg.to,[midd])
                    nadya. findAndAddContactsByMid(midd)
                    nadya.inviteIntoGroup(msg.to,[midd])
                    nadya.cancelGroupInvitation(msg.to,[midd])
                elif "เด้ง " in msg.text:
                        vkick0 = msg.text.replace("เด้ง ","")
                        vkick1 = vkick0.rstrip()
                        vkick2 = vkick1.replace("@","")
                        vkick3 = vkick2.rstrip()
                        _name = vkick3
                        gs = nadya.getGroup(msg.to)
                        targets = []
                        for s in gs.members:
                            if _name in s.displayName:
                                targets.append(s.mid)
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    nadya.kickoutFromGroup(msg.to,[target])
                                    nadya.findAndAddContactsByMid(target)
                                    nadya. inviteIntoGroup(msg.to,[target])
                                except:
                                    pass
                elif msg.text.lower().startswith("เตะ "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            nadya.kickoutFromGroup(msg.to,[target])
                        except:
                            nadya.sendText(msg.to,"Error")
                elif msg.text.lower().startswith("เพิ่มพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            nadya.sendMessage(msg.to,"👍เพิ่มคนพิมตามแล้วʕ•ᴥ•ʔ")
                            break
                        except:
                            nadya.sendMessage(msg.to,"Added Target Fail !")
                            break
                elif msg.text.lower().startswith("ลบคนพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            nadya.sendMessage(msg.to,"👍ลบการเลียนแบบแล้วʕ•ᴥ•ʔ")
                            break
                        except:
                            nadya.sendMessage(msg.to,"Deleted Target Fail !")
                            break
                elif text.lower() == 'รายชื่อคนพิมตาม':
                    if settings["mimic"]["target"] == {}:
                        nadya.sendMessage(msg.to,"Tidak Ada Target")
                    else:
                        mc = "╔══[ Mimic List ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+nadya.getContact(mi_d).displayName
                        nadya.sendMessage(msg.to,mc + "\n╚══[ Finish ]")
                    
                elif "love" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            nadya.sendMessage(msg.to,"Reply Message on")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            nadya.sendMessage(msg.to,"Reply Message off")
#==============================================================================#
                elif text.lower() == 'เชคแอด':
                    group = nadya.getGroup(to)
                    GS = group.creator.mid
                    nadya.sendContact(to, GS)
                elif text.lower() == 'ไอดีกลุ่ม':
                    gid = nadya.getGroup(to)
                    nadya.sendMessage(to, "\n" + gid.id)
                elif text.lower() == 'รูปกลุ่ม':
                    group = nadya.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    nadya.sendImageWithURL(to, path)
                elif text.lower() == 'ชื่อกลุ่ม':
                    gid = nadya.getGroup(to)
                    nadya.sendMessage(to, "\n" + gid.name)
                elif text.lower() == 'ลิ้งกลุ่ม':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            ticket = nadya.reissueGroupTicket(to)
                            nadya.sendMessage(to, "https://line.me/R/ti/g/{}".format(str(ticket)))
                        else:
                            nadya.sendMessage(to, "Grup qr tidak terbuka silahkan buka terlebih dahulu dengan perintah {}openqr".format(str(settings["keyCommand"])))
                elif text.lower() == 'เปิดลิ้ง':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            nadya.sendMessage(to, "👍เปิดลิ้งสำเร็จʕ•ᴥ•ʔ")
                        else:
                            group.preventedJoinByTicket = False
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "👍ลิ้งเปิดอยู่ครับʕ•ᴥ•ʔ")
                elif text.lower() == 'ปิดลิ้ง':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            nadya.sendMessage(to, "👍ปิดอยู่ʕ•ᴥ•ʔ")
                        else:
                            group.preventedJoinByTicket = True
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "👍ปิดลิ้งสำเร็จʕ•ᴥ•ʔ")
                elif text.lower() == 'ข้อมูลกลุ่ม':
                    group = nadya.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "Tidak ditemukan"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "Tertutup"
                        gTicket = "Tidak ada"
                    else:
                        gQr = "เชคกลุ่ม"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(nadya.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ ข้อมูลกลุ่ม ]"
                    ret_ += "\n╠ ชื่อกลุ่ม : {}".format(str(group.name))
                    ret_ += "\n╠ ไอดีกลุ่ม : {}".format(group.id)
                    ret_ += "\n╠ ผู้สร้าง : {}".format(str(gCreator))
                    ret_ += "\n╠ สมาชิกในกลุ่ม : {}".format(str(len(group.members)))
                    ret_ += "\n╠ จำนวนค้างเชิญ : {}".format(gPending)
                    ret_ += "\n╠ กลุ่ม Qr : {}".format(gQr)
                    ret_ += "\n╠ https://line.me/R/ti/g/{}".format(str(ticket))
                    ret_ += "\n╚══[ ข้อมูลกลุ่ม ]"
                    nadya.sendMessage(to, str(ret_))
                    nadya.sendImageWithURL(to, path)
                elif text.lower() == 'สมาชิก':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        ret_ = "╔══[ จำนวน List ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ จำนวน {} ]".format(str(len(group.members)))
                        nadya.sendMessage(to, str(ret_))
                elif text.lower() == 'กลุ่มทั้งหมด':
                        groups = nadya.groups
                        ret_ = "╔══[ กลุ่ม List ]"
                        no = 0 + 1
                        for gid in groups:
                            group = nadya.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ จำนวน {} กลุ่ม ]".format(str(len(groups)))
                        nadya.sendMessage(to, str(ret_))
#==============================================================================#          
                elif text.lower() == 'แทค':
                    group = nadya.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        nadya.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        nadya.sendMessage(to, "👍จำนวนสมาชิก {} คนʕ•ᴥ•ʔ".format(str(len(nama))))          
                elif text.lower() == 'เปิดอ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read['readPoint']:
                            try:
                                del read['readPoint'][msg.to]
                                del read['readMember'][msg.to]
                                del read['readTime'][msg.to]
                            except:
                                pass
                            read['readPoint'][msg.to] = msg.id
                            read['readMember'][msg.to] = ""
                            read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                            read['ROM'][msg.to] = {}
                            with open('read.json', 'w') as fp:
                                json.dump(read, fp, sort_keys=True, indent=4)
                                nadya.sendMessage(msg.to,"Lurking already on")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                            pass
                        read['readPoint'][msg.to] = msg.id
                        read['readMember'][msg.to] = ""
                        read['readTime'][msg.to] = datetime.now().strftime('%H:%M:%S')
                        read['ROM'][msg.to] = {}
                        with open('read.json', 'w') as fp:
                            json.dump(read, fp, sort_keys=True, indent=4)
                            nadya.sendMessage(msg.to, "Set reading point:\n" + readTime)
                            
                elif text.lower() == 'ปิดอ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to not in read['readPoint']:
                        nadya.sendMessage(msg.to,"Lurking already off")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        nadya.sendMessage(msg.to, "Delete reading point:\n" + readTime)
    
                elif text.lower() == 'ลบเวลา':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if msg.to in read["readPoint"]:
                        try:
                            del read["readPoint"][msg.to]
                            del read["readMember"][msg.to]
                            del read["readTime"][msg.to]
                        except:
                            pass
                        nadya.sendMessage(msg.to, "\n" + readTime)
                    else:
                        nadya.sendMessage(msg.to, "Lurking belum diaktifkan ngapain di reset?")
                        
                elif text.lower() == 'อ่าน':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    if receiver in read['readPoint']:
                        if read["ROM"][receiver].items() == []:
                            nadya.sendMessage(receiver,"[ Reader ]:\nNone")
                        else:
                            chiya = []
                            for rom in read["ROM"][receiver].items():
                                chiya.append(rom[1])
                            cmem = nadya.getContacts(chiya) 
                            zx = ""
                            zxc = ""
                            zx2 = []
                            xpesan = 'ผู้ที่แอบอ่าน\n\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\nออกมาเร็วจะแอบทำไม\n" + readTime
                        try:
                            nadya.sendMessage(receiver, text, contentMetadata={'MENTION':str('{"MENTIONEES":'+json.dumps(zx2).replace(' ','')+'}')}, contentType=0)
                        except Exception as error:
                            print (error)
                        pass
                    else:
                        nadya.sendMessage(receiver,"Lurking has not been set.")
#==============================================================================#
                elif msg.text.lower().startswith("พูด "):
                    sep = text.split(" ")
                    say = text.replace(sep[0] + " ","")
                    lang = 'th'
                    tts = gTTS(text=say, lang=lang)
                    tts.save("hasil.mp3")
                    nadya.sendAudio(msg.to,"hasil.mp3")
#==============================================================================#
            elif msg.contentType == 7:
                if settings["checkSticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "╔══( ข้อมูลสติกเกอร์ )"
                    ret_ += "\n╠ สติกเกอร์ id : {}".format(stk_id)
                    ret_ += "\n╠ แพคเกจสติกเกอร์ : {}".format(pkg_id)
                    ret_ += "\n╠ เวอร์ชั่นสติกเกอร: {}".format(stk_ver)
                    ret_ += "\n╠ ลิ้งสติกเกอร์ : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n╚══( ข้อมูลสติกเกอร์ )"
                    nadya.sendMessage(to, str(ret_))
                    
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = nadya.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break                             
                        else:
                            targets.append(copy)
                    if targets == []:
                        nadya.sendText(msg.to, "Not Found...")
                        pass
                    else:
                        for target in targets:
                            try:
                                nadya.cloneContactProfile(target)
                                nadya.sendMessage(msg.to, "Berhasil clone member tunggu beberapa saat sampai profile berubah")
                                settings['copy'] = False
                                break
                            except:
                                     msg.contentMetadata = {'mid': target}
                                     settings["copy"] = False
                                     break                     
                    
                    
#==============================================================================#
        if op.type == 26:
            print ("[ 26 ] RECEIVE MESSAGE")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != nadya.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    nadya.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        nadya.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in nadyaMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys())!= None:
                        if settings['potoMention'] == True:
                             contact = nadya.getContact(msg._from)
                             cName = contact.pictureStatus
                             balas = ["http://dl.profile.line-cdn.net/" + cName]
                             ret_ = random.choice(balas)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention["MENTIONEES"]
                             for mention in mentionees:
                                   if mention["M"] in nadyaMID:
                                          nadya.sendImageWithURL(to,ret_)
                                          break
                if msg.contentType == 0 and sender not in nadyaMID and msg.toType == 2:
                    if "MENTION" in list(msg.contentMetadata.keys()) != None:
                         if settings['detectMention'] == True:
                             contact = nadya.getContact(msg._from)
                             cName = contact.displayName
                             balas = ["『ᴅᴏᴀᴍᴍᴇᴇ』" + "\n\n" + str(settings["Tag"])]
                             ret_ = "" + random.choice(balas)
                             name = re.findall(r'@(\w+)', msg.text)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention['MENTIONEES']
                             for mention in mentionees:
                                   if mention['M'] in nadyaMID:
                                          nadya.sendMessage(to,ret_)
                                          sendMessageWithMention(to, contact.mid)
                                          break
                if msg.text in ["Speed","speed","Sp","sp",".Sp",".sp",".Speed",".speed","!sp","!Sp","!Speed","!speed","\Sp","\sp","\speed","\Speed"]:
                	nadya.sendMessage(to, "👍แรงแล้วครับพี่ʕ•ᴥ•ʔ")
                if msg.text in ["Me","me","คท","!me","!Me",".me",".Me"]:
            	    nadya.sendMessage(to, "👍เช็คจังหนังกระโปกʕ•ᴥ•ʔ")
                if msg.text in ["ออน",".ออน","!ออน","\ออน",".uptime",".Uptime","!uptime","!Uptime","\Uptime","\uptime"]:
                	nadya.sendMessage(to, "👍ออนนานเกิ๊นʕ•ᴥ•ʔ")
                if msg.text in [".มอง","มอง"]:
                	nadya.sendMessage(to, "👍มองจังไอสัสʕ•ᴥ•ʔ")
                if msg.text in ["5","55","555","5555","55555","555555","5555555"]:
                	nadya.sendMessage(to, "👍ขำเหี้ยไรสัสʕ•ᴥ•ʔ")
                if msg.text in ["--","-.-","-..-","-,,-","-,-","+.+","*-*","-*-","=-=","=.=","=_=","._.",".__.","=="]:
                	nadya.sendMessage(to, "👍หน้าหีมากสัสʕ•ᴥ•ʔ")
                if msg.text in [".","..","...","....",".....","......",".......","........",".........","............","..................."]:
                	nadya.sendMessage(to, "👍จุดจบมึง?ʕ•ᴥ•ʔ")
                if msg.text in ["Tag","tagall","แทค","แทก","Tagall","tag"]:
                	nadya.sendMessage(to,"👍แทคทำควยไรʕ•ᴥ•ʔ")
                if msg.text in ["กำ",".กำ"]:
                	nadya.sendMessage(to,"👍กำไรดีควยหรือหีʕ•ᴥ•ʔ")
                if msg.text in [".ขำ",".ขรรม","ขำ","ขรรม","ขำๆ"]:
                	nadya.sendMessage(to,"👍ขำทำเหี้ยไรʕ•ᴥ•ʔ")
                
#==============================================================================#
        if op.type == 5:
            if RfuProtect["autoAdd"] == True:
                if (settings["message"] in [""," ","\n",None]):
                    pass
                else:
                    now2 = datetime.datetime.now()
                    nowT = datetime.datetime.strftime(now2,"%H")
                    nowM = datetime.datetime.strftime(now2,"%M")
                    nowS = datetime.datetime.strftime(now2,"%S")
                    tm = "\n\n"+nowT+":"+nowM+":"+nowS
                    nadya.sendMessage(op.param1,str(settings["message"]) + "\n" + tm)
        if op.type == 55:
            print ("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
