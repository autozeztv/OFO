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
    helpMessage ="✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨" + "\n" + \
                  " " + "\n" + \
                  "🌠คำสั่ง" + "\n" + \
                  "🌠คำสั่ง2" + "\n" + \
         	     " " + "\n" + \
                  "🌠Speed" + "\n" + \
                  "🌠เช็คค่า" + "\n" + \
                  "🌠ข้อมูล" + "\n" + \
                  "🌠เทส" + "\n" + \
                  "🌠คท" + "\n" + \
                  "🌠มิด" + "\n" + \
                  "🌠ชื่อ" + "\n" + \
                  "🌠ตัส" + "\n" + \
                  "🌠รูป" + "\n" + \
                  "🌠ปก" + "\n" + \
		          " " + "\n" + \
                  "🌠คท @" + "\n" + \
                  "🌠มิด @" + "\n" + \
                  "🌠ชื่อ @" + "\n" + \
                  "🌠ตัส @" + "\n" + \
                  "🌠ดิส @" + "\n" + \
                  "🌠เด้ง @" + "\n" + \
                  "🌠!แทค" + "\n" + \
                  "🌠!มิด" "\n" + \
                  "🌠!คท" + "\n" + \
                  "🌠ก็อปปี้ @" + "\n" +\
	              " " + "\n" + \
                  "🌠พิมตาม on/off" + "\n" + \
                  "🌠เพิ่มพิมตาม" + "\n" + \
                  "🌠ลบพิมตาม" + "\n" + \
                  "🌠รีบอท" + "\n" + \
                  "🌠ออน" + "\n" + \
                  "🌠พูด(ข้อความ)" + "\n" + \
                  "🌠name (ชื่อ)" + "\n" + \
                  "🌠เตะ" + "\n" + \
                  "🌠ข้อมูล" + "\n" + \
                  "🌠โทร" + "\n" + \
                  "🌠เชคแอด" + "\n" + \
		          " " + "\n" + \
                  "🌠แทค" + "\n" + \
                  "🌠ชื่อกลุ่ม" + "\n" + \
                  "🌠ไอดีกลุ่ม" + "\n" + \
                  "🌠รูปกลุ่ม" + "\n" + \
                  "🌠กลุ่มทั้งหมด" + "\n" + \
                  "🌠ข้อมูลกลุ่ม" + "\n" + \
                  "🌠สมาชิก" + "\n" + \
                  "🌠เปิดอ่าน" + "\n" + \
                  "🌠ปิดอ่าน" + "\n" + \
                  "🌠อ่าน" + "\n" + \
                  "🌠ลบเวลา" + "\n" + \
                  "🌠ยกเลิก" + "\n" + \
                  "🌠ลิ้งกลุ่ม" + "\n" + \
	              "🌠ลิ้ง 「On/Off」" + "\n" + \
	              " " + "\n" + \
                  "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡"
    return helpMessage
    
def helptexttospeech():
    helpTextToSpeech =   "✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨" + "\n" + \
                         "👑Tag 「On/Off」" + "\n" + \
                         "👑Tag2 「On/Off」" + "\n" + \
                         "👑AutoJoin 「On/Off」" + "\n" + \
                         "👑AutoRead「On/Off」" + "\n" + \
                         "👑AutoBlock 「On/Off」" + "\n" + \
                         "👑CheckSticker「On/Off」" + "\n" + \
                         "👑AutoLeave 「On/Off」" + "\n" + \
                         " " + "\n" + \
                         "🌟ตั้งแทค: " + "\n" + \
                         "🌟ตั้งเข้า: " + "\n" + \
                         "🌟ตั้งออก: " + "\n" + \
                         "🌟เชคแทค" + "\n" + \
                         "🌟เชคเข้า" + "\n" + \
                         "🌟เชคออก" + "\n" + \
                         "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡"
    return helpTextToSpeech
    
def helptranslate():
    helpTranslate =    " เสียงสิริ " + "\n" + \
                       " af : afrikaans" + "\n" + \
                       " sq : albanian" + "\n" + \
                       " am : amharic" + "\n" + \
                       " ar : arabic" + "\n" + \
                       " hy : armenian" + "\n" + \
                       " az : azerbaijani" + "\n" + \
                       " eu : basque" + "\n" + \
                       " be : belarusian" + "\n" + \
                       " bn : bengali" + "\n" + \
                       " bs : bosnian" + "\n" + \
                       " bg : bulgarian" + "\n" + \
                       " ca : catalan" + "\n" + \
                       " ceb : cebuano" + "\n" + \
                       " ny : chichewa" + "\n" + \
                       " zh-cn : chinese (simplified)" + "\n" + \
                       " zh-tw : chinese (traditional)" + "\n" + \
                       " co : corsican" + "\n" + \
                       " hr : croatian" + "\n" + \
                       " cs : czech" + "\n" + \
                       " da : danish" + "\n" + \
                       " nl : dutch" + "\n" + \
                       " en : english" + "\n" + \
                       " eo : esperanto" + "\n" + \
                       " et : estonian" + "\n" + \
                       " tl : filipino" + "\n" + \
                       " fi : finnish" + "\n" + \
                       " fr : french" + "\n" + \
                       " fy : frisian" + "\n" + \
                       " gl : galician" + "\n" + \
                       " ka : georgian" + "\n" + \
                       " de : german" + "\n" + \
                       " el : greek" + "\n" + \
                       " gu : gujarati" + "\n" + \
                       " ht : haitian creole" + "\n" + \
                       " ha : hausa" + "\n" + \
                       " haw : hawaiian" + "\n" + \
                       " iw : hebrew" + "\n" + \
                       " hi : hindi" + "\n" + \
                       " hmn : hmong" + "\n" + \
                       " hu : hungarian" + "\n" + \
                       " is : icelandic" + "\n" + \
                       " ig : igbo" + "\n" + \
                       " id : indonesian" + "\n" + \
                       " ga : irish" + "\n" + \
                       " it : italian" + "\n" + \
                       " ja : japanese" + "\n" + \
                       " jw : javanese" + "\n" + \
                       " kn : kannada" + "\n" + \
                       " kk : kazakh" + "\n" + \
                       " km : khmer" + "\n" + \
                       " ko : korean" + "\n" + \
                       " ku : kurdish (kurmanji)" + "\n" + \
                       " ky : kyrgyz" + "\n" + \
                       " lo : lao" + "\n" + \
                       " la : latin" + "\n" + \
                       " lv : latvian" + "\n" + \
                       " lt : lithuanian" + "\n" + \
                       " lb : luxembourgish" + "\n" + \
                       " mk : macedonian" + "\n" + \
                       " mg : malagasy" + "\n" + \
                       " ms : malay" + "\n" + \
                       " ml : malayalam" + "\n" + \
                       " mt : maltese" + "\n" + \
                       " mi : maori" + "\n" + \
                       " mr : marathi" + "\n" + \
                       " mn : mongolian" + "\n" + \
                       " my : myanmar (burmese)" + "\n" + \
                       " ne : nepali" + "\n" + \
                       " no : norwegian" + "\n" + \
                       " ps : pashto" + "\n" + \
                       " fa : persian" + "\n" + \
                       " pl : polish" + "\n" + \
                       " pt : portuguese" + "\n" + \
                       " pa : punjabi" + "\n" + \
                       " ro : romanian" + "\n" + \
                       " ru : russian" + "\n" + \
                       " sm : samoan" + "\n" + \
                       " gd : scots gaelic" + "\n" + \
                       " sr : serbian" + "\n" + \
                       " st : sesotho" + "\n" + \
                       " sn : shona" + "\n" + \
                       " sd : sindhi" + "\n" + \
                       " si : sinhala" + "\n" + \
                       " sk : slovak" + "\n" + \
                       " sl : slovenian" + "\n" + \
                       " so : somali" + "\n" + \
                       " es : spanish" + "\n" + \
                       " su : sundanese" + "\n" + \
                       " sw : swahili" + "\n" + \
                       " sv : swedish" + "\n" + \
                       " tg : tajik" + "\n" + \
                       " ta : tamil" + "\n" + \
                       " te : telugu" + "\n" + \
                       " th : thai" + "\n" + \
                       " tr : turkish" + "\n" + \
                       " uk : ukrainian" + "\n" + \
                       " ur : urdu" + "\n" + \
                       " uz : uzbek" + "\n" + \
                       " vi : vietnamese" + "\n" + \
                       " cy : welsh" + "\n" + \
                       " xh : xhosa" + "\n" + \
                       " yi : yiddish" + "\n" + \
                       " yo : yoruba" + "\n" + \
                       " zu : zulu" + "\n" + \
                       " fil : Filipino" + "\n" + \
                       " he : Hebrew" + "\n" + \
                       "✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨" + "\n" + "\n\n" + \
                         "วิธีใช้ tr-ตามด้วยตัวย่อประเทศ\nเช่น tr-th สวัสดี เป็นต้น"
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
                #nadya.sendMessage(op.param1, "Halo {} terimakasih telah menambahkan saya sebagai teman :D".format(str(nadya.getContact(op.param1).displayName)))
        if op.type == 13:
            print ("[ 13 ] NOTIFIED INVITE GROUP")
            group = nadya.getGroup(op.param1)
            if settings["autoJoin"] == True:
                nadya.acceptGroupInvitation(op.param1)

        if op.type == 15:
            if wait["bcommentOn"] and "bcomment" in wait:
                nadya.sendMessage(op.param1,nadya.getContact(op.param2).displayName + "\n\n" + str(settings["bcomment"]))

        if op.type == 17:
            if wait["acommentOn"] and "acomment" in wait:
                cnt = nadya. getContact(op.param2)
                nadya.sendMessage(op.param1,cnt.displayName + "\n\n" + str(settings["acomment"]))

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
                elif text.lower() == 'คำสั่งสิริ':
                    helpTranslate = helptranslate()
                    nadya.sendMessage(to, str(helpTranslate))
#==============================================================================#
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
                    spl = re.split("ชื่อ ",msg.text,flags=re.IGNORECASE)
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
                elif "ลบรัน" == msg.text.lower():
                    nadya.sendText(to,"👍กำลังลบรัน..ʕ•ᴥ•ʔ")
                    gid = nadya.getGroupIdsInvited()
                    for i in gid:
                        nadya.rejectGroupInvitation(i)
                    if wait["lang"] == "JP":
                        nadya.sendText(msg.to,"👍ลบรันเสร็จแล้วʕ•ᴥ•ʔ")
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
                        if settings["autoAdd"] == True: ret_ += "\n║ ระบบออโต้บล็อค ✔️"
                        else: ret_ += "\n║ ระบบออโต้บล็อค ✘"
                        if settings["autoJoin"] == True: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✔️"
                        else: ret_ += "\n║ ระบบเข้ากลุ่มออโต้ ✘"
                        if settings["autoLeave"] == True: ret_ += "\n║ ระบบออกกลุ่มออโต้ ✔️"
                        else: ret_ += "\n║ ระบบออกกลุ่มออโต้ ✘"
                        if settings["autoRead"] == True: ret_ += "\n║ ระบบอ่านออโต้ ✔️"
                        else: ret_ += "\n║ ระบบอ่านออโต้ ✘"
                        if settings["checkSticker"] == True: ret_ += "\n║ ระบบเช็คสติ้กเกอร์ ✔️"
                        else: ret_ += "\n║ ระบบเช็คสติ้กเกอร์ ✘"
                        if settings["detectMention"] == True: ret_ += "\n║ ระบบข้อความแทค ✔️"
                        else: ret_ += "\n║ ระบบข้อความแทค ✘"
                        if settings["potoMention"] == True: ret_ += "\n║ ระบบข้อความแทคส่งรูป ✔️"
                        else: ret_ += "\n║ ระบบข้อความแทคส่งรูป ✘"
                        ret_ += "\n╚════════════"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoblock on':
                    settings["autoAdd"] = True
                    nadya.sendMessage(to, "👍เปิดระบบออโต้บล็อคʕ•ᴥ•ʔ")
                elif text.lower() == 'autoblock off':
                    settings["autoAdd"] = False
                    nadya.sendMessage(to, "👎ปิดระบบออโต้บล็อคʕ•ᴥ•ʔ")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    nadya.sendMessage(to, "👍เปิดระบบเข้ากลุ่มออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    nadya.sendMessage(to, "👎ปิดระบบเข้ากลุ่มออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    nadya.sendMessage(to, "👍เปิดระบบออกกลุ่มออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    nadya.sendMessage(to, "👎ปิดระบบออกกลุ่มออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    nadya.sendMessage(to, "👍เปิดระบบอ่านออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    nadya.sendMessage(to, "👎ปิดระบบอ่านออโต้ʕ•ᴥ•ʔ")
                elif text.lower() == 'checksticker on':
                    settings["checkSticker"] = True
                    nadya.sendMessage(to, "👍เปิดระบบเช็คสติ้กเกอร์ʕ•ᴥ•ʔ")
                elif text.lower() == 'checksticker off':
                    settings["checkSticker"] = False
                    nadya.sendMessage(to, "👎ปิดระบบเช็คสติ้กเกอร์ʕ•ᴥ•ʔ")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    nadya.sendMessage(to, "👍เปิดระบบก็อปปี้ด้วยคอนแทคʕ•ᴥ•ʔ")
                elif text.lower() == 'tag on':
                    settings["detectMention"] = True
                    nadya.sendMessage(to, "👍เปิดระบบข้อความแทคʕ•ᴥ•ʔ")
                elif text.lower() == 'tag off':
                    settings["detectMention"] = False
                    nadya.sendMessage(to, "👎ปิดระบบข้อความแทคʕ•ᴥ•ʔ")
                elif text.lower() == 'tag2 on':
                	settings['potoMention'] = True
                    nadya.sendMessage(to,"👍เปิดระบบข้อความแทคส่งรูปʕ•ᴥ•ʔ")
                elif text.lower() == 'tag2 off':
                	settings['potoMention'] = False
                    nadya.sendMessage(to,"👎ปิดระบบข้อความแทคส่งรูปʕ•ᴥ•ʔ")
                elif "ตั้งแทค: " in msg.text:
                    settings["Tag"] = msg.text.replace("ตั้งแทค: ","")
                    nadya.sendMessage(msg.to,"👍ตั้งข้อความกล่าวถึงคนแทคสำเร็จʕ•ᴥ•ʔ")
                elif msg.text in ["เชคแทค","เช็คแทค"]:
                    nadya.sendMessage(msg.to,"👍ข้อความตั้งแทคล่าสุดคือʕ•ᴥ•ʔ\n\n" + str(settings["Tag"]) + "\n\n✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨")
                elif msg.text in ["เชคเข้า","เช็คเข้า"]:
                    nadya.sendMessage(msg.to,"👍ข้อความตอนรับเข้าล่าสุดคือʕ•ᴥ•ʔ\n\n" + str(settings["acomment"]) + "\n\n✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨")
                elif msg.text in ["เชคออก","เช็คออก"]:
                    nadya.sendMessage(msg.to,"👍ข้อความตอนรับออกล่าสุดคือʕ•ᴥ•ʔ\n\n" + str(settings["bcomment"]) + "\n\n✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨")
                elif "ตั้งเข้า:" in msg.text.lower():
                    c = msg.text.replace("ตั้งเข้า:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"👎เกิดข้อผิดพลาดʕ•ᴥ•ʔ")
                    else:
                        wait["acomment"] = c
                        nadya.sendMessage(msg.to,"👍เสร็จสิ้นʕ•ᴥ•ʔ")
                elif "ตั้งออก:" in msg.text.lower():
                    c = msg.text.replace("ตั้งออก:","")
                    if c in [""," ","\n",None]:
                        nadya.sendMessage(msg.to,"👎เกิดข้อผิดพลาดʕ•ᴥ•ʔ")
                    else:
                        settings["bcomment"] = c
                        nadya.sendMessage(msg.to,"👍เสร็จสิ้นʕ•ᴥ•ʔ")
#==============================================================================#
                elif msg.text in ["me","Me","คท"]:
                    sendMessageWithMention(to, nadyaMID)
                    nadya.sendContact(to, nadyaMID)
                elif text.lower() == 'ไอดี':
                    nadya.sendMessage(msg.to, nadyaMID)
                elif text.lower() == 'เนม':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendMessage(msg.to, me.displayName)
                elif text.lower() == 'สถานะ':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendMessage(msg.to, me.statusMessage)
                elif text.lower() == 'รูป':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'รูปวีดีโอ':
                    me = nadya.getContact(nadyaMID)
                    nadya.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'รูปปก':
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
                        ret_ = "\n"
                        for ls in lists:
                            ret_ += ls
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
                            nadya.sendMessage(msg.to, contact.displayName)
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
                            nadya.sendMessage(msg.to, contact.statusMessage)
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
                elif msg.text.lower().startswith("ดิสวีดีโอ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line-cdn.net/" + nadya.getContact(ls).pictureStatus + "/vp"
                            nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("ดิสปก "):
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
                                path = "http://dl.profile.line-cdn.net/" + nadya.getProfileCoverURL(ls)
                                nadya.sendImageWithURL(msg.to, str(path))
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
                                    nadya.cancelGroupInvitation(msg.to,[target])
                                except:
                                    pass
                elif msg.text.lower().startswith("ท้าไม้ตาย "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            nadya.sendMessage(msg.to,"โอมายวะ")
                            nadya.sendMessage(msg.to,"โมชินเดรุ")
                            nadya.sendMessage(msg.to,"หน่านี้!!")
                            nadya.kickoutFromGroup(msg.to,[target])
                        except:
                            nadya.sendMessage(msg.to,"Error")
                elif msg.text.lower().startswith("ท้าไม้ตาย2 "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            nadya.sendMessage(msg.to,"2นาฬิกาฟาเรนไฮต์อุณหภูมิ155เซลเซียสแรงปืน32อุณหภูมิความชื้น22นาฬิกาปาดขวายิงเพื่อหวังผล..")
                            nadya.kickoutFromGroup(msg.to,[target])
                            nadya.sendMessage(msg.to,"!!แตกก")
                        except:
                            nadya.sendText(msg.to,"Error")
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
#==============================================================================#
                elif text.lower() == '!แทค':
                    gs = nadya.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        nadya.sendMessage(to, "👍ไม่มีคนใส่ร่องหนʕ•ᴥ•ʔ")
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
                        nadya.sendMessage(to, "👍ไม่มีคนใส่ร่องหนʕ•ᴥ•ʔ")
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
                        nadya.sendMessage(to, "👍ไม่มีคนใส่ร่องหนʕ•ᴥ•ʔ")
                    else:
                        for ls in lists:
                            contact = nadya.getContact(ls)
                            mi_d = contact.mid
                            nadya.sendContact(to, mi_d)
                elif "Mc " in msg.text:
                    mmid = msg.text.replace("Mc ","")
                    nadya.sendContact(to, mmid)
                elif msg.text.lower().startswith("เพิ่มพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            nadya.sendMessage(msg.to,"👍เพิ่มพิมตามเรียบร้อยʕ•ᴥ•ʔ")
                            break
                        except:
                            nadya.sendMessage(msg.to,"👍เพิ่มพิมตามล้มเหลวʕ•ᴥ•ʔ")
                            break
                elif msg.text.lower().startswith("ลบพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del settings["mimic"]["target"][target]
                            nadya.sendMessage(msg.to,"👍ลบพิมตามเรียบร้อยʕ•ᴥ•ʔ")
                            break
                        except:
                            nadya.sendMessage(msg.to,"👍ลบพิมตามล้มเหลวʕ•ᴥ•ʔ")
                            break
                elif text.lower() == 'รายชื่อคนพิมตาม':
                    if settings["mimic"]["target"] == {}:
                        nadya.sendMessage(msg.to,"👍ไม่มีการเพิ่มก่อนหน้านี้ʕ•ᴥ•ʔ")
                    else:
                        mc = "╔══[ รายชื่อคนพิมตาม ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+nadya.getContact(mi_d).displayName
                        nadya.sendMessage(msg.to,mc + "\n╚══[✍️ͲɆᎪᎷ🔝ʕ•̫͡•ʔஞ௮Ҩஆี✨]")
                elif "พิมตาม" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            nadya.sendMessage(msg.to,"👍เปิดระบบพิมตามเรียบร้อยʕ•ᴥ•ʔ")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            nadya.sendMessage(msg.to,"👍ปิดระบบพิมตามเรียบร้อยʕ•ᴥ•ʔ")
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
                            nadya.sendMessage(to, "กรุณาเปิดลิ้งกลุ่มก่อน\nลงคำสั่งนี้ด้วยครับʕ•ᴥ•ʔ".format(str(settings["keyCommand"])))
                elif text.lower() == 'ลิ้งกลุ่ม on':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            nadya.sendMessage(to, "👍ลิ้งกลุ่มเปิดอยู่แล้วʕ•ᴥ•ʔ")
                        else:
                            group.preventedJoinByTicket = False
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "👍เปิดลิ้งกลุ่มเรียบร้อยʕ•ᴥ•ʔ")
                elif text.lower() == 'ลิ้งกลุ่ม off':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            nadya.sendMessage(to, "👍ลิ้งกลุ่มปิดอยู่แล้วʕ•ᴥ•ʔ")
                        else:
                            group.preventedJoinByTicket = True
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "👍ลิ้งกลุ่มปิดเรียบร้อยʕ•ᴥ•ʔ")
                elif text.lower() == 'ข้อมูลกลุ่ม':
                    group = nadya.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "ไม่พบผู้สร้าง"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "ปิด"
                        gTicket = "ลิ้งถูกปิดอยู่.."
                    else:
                        gQr = "เปิด"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(nadya.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "╔══[ ข้อมูลกลุ่ม ]"
                    ret_ += "\n╠ ชื่อกลุ่ม : {}".format(str(group.name))
                    ret_ += "\n╠ ไอดีกลุ่ม:{}".format(group.id)
                    ret_ += "\n╠ ผู้สร้างกลุ่ม : {}".format(str(gCreator))
                    ret_ += "\n╠ สมาชิกกลุ่ม : {}".format(str(len(group.members)))
                    ret_ += "\n╠ ค้างเชิญ : {}".format(gPending)
                    ret_ += "\n╠ กลุ่มตั๋ว:{}".format(gQr)
                    ret_ += "\n╠ ลิ้งกลุ่ม : {}".format(gTicket)
                    ret_ += "\n╚══[ Finish ]"
                    nadya.sendMessage(to, str(ret_))
                    nadya.sendImageWithURL(to, path)
                elif text.lower() == 'รายชื่อสมาชิกกลุ่ม':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        ret_ = "╔══[ รายชื่อสมชิกกลุ่ม ]"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n╠ {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n╚══[ 👍จำนวนสมาชิก {} คนʕ•ᴥ•ʔ ]".format(str(len(group.members)))
                        nadya.sendMessage(to, str(ret_))
                elif text.lower() == 'รายชื่อกลุ่ม':
                        groups = nadya.groups
                        ret_ = "╔══[ รายชื่อกลุ่ม ]"
                        no = 0 + 1
                        for gid in groups:
                            group = nadya.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ 👍จำนวนกลุ่ม {} กลุ่มʕ•ᴥ•ʔ ]".format(str(len(groups)))
                        nadya.sendMessage(to, str(ret_))
#==============================================================================#          
                elif "ยูทูป " == msg.text.lower():
                    try:
                        textToSearch = (msg.text).replace('ยูทูป ', "").strip()
                        query = urllib.quote(textToSearch)
                        url = "https://www.youtube.com/results?search_query=" + query
                        response = urllib2.urlopen(url)
                        html = response.read()
                        soup = BeautifulSoup(html, "html.parser")
                        results = soup.find(attrs={'class':'yt-uix-tile-link'})
                        nadya.sendMassage(msg.to,'https://www.youtube.com' + results['href'])
                    except:
                        nadya.sendMassage(msg.to,"ไม่พบ")
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
                        nadya.sendMessage(to, "จำนวนสมาชิก👉 {} คน👑 ".format(str(len(nama))))          
                elif text.lower() == 'หาคนอ่าน on':
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
                                nadya.sendMessage(msg.to,"เปิดหาคนซุ่ม..🎃")
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
                            
                elif text.lower() == 'หาคนอ่าน off':
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
                        nadya.sendMessage(msg.to,"ปิดหาคนซุ่ม..🎃")
                    else:
                        try:
                            del read['readPoint'][msg.to]
                            del read['readMember'][msg.to]
                            del read['readTime'][msg.to]
                        except:
                              pass
                        nadya.sendMessage(msg.to, "Delete reading point:\n" + readTime)
    
                elif text.lower() == 'หาคนซุ่ม reset':
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
                        nadya.sendMessage(msg.to, "Reset reading point:\n" + readTime)
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
                            xpesan = '[ Reader ]:\n'
                        for x in range(len(cmem)):
                            xname = str(cmem[x].displayName)
                            pesan = ''
                            pesan2 = pesan+"@c\n"
                            xlen = str(len(zxc)+len(xpesan))
                            xlen2 = str(len(zxc)+len(pesan2)+len(xpesan)-1)
                            zx = {'S':xlen, 'E':xlen2, 'M':cmem[x].mid}
                            zx2.append(zx)
                            zxc += pesan2
                        text = xpesan+ zxc + "\n[ Lurking time ]: \n" + readTime
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
                    ret_ = "╔══[ Sticker Info ]"
                    ret_ += "\n╠ STICKER ID : {}".format(stk_id)
                    ret_ += "\n╠ STICKER PACKAGES ID : {}".format(pkg_id)
                    ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
                    ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\n╚══[ Finish ]"
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
                             balas = balas = ["『 ระบบข้อความออโต้』\n" + cName + "\n\n" + str(settings["Tag"])]
                             ret_ = "" + random.choice(balas)
                             name = re.findall(r'@(\w+)', msg.text)
                             mention = ast.literal_eval(msg.contentMetadata["MENTION"])
                             mentionees = mention['MENTIONEES']
                             for mention in mentionees:
                                   if mention['M'] in nadyaMID:
                                          nadya.sendMessage(to,ret_)
                                          sendMessageWithMention(to, contact.mid)
                                          break
                if msg.text in ["Speed","speed","Sp","sp",".Sp",".sp",".Speed",".speed","!sp","!Sp","!Speed","!speed"]:
                	nadya.sendMessage(to, "👍แรงแล้วครับพี่ʕ•ᴥ•ʔ")
                if msg.text in ["Me","me","คท","!me","!Me",".me",".Me"]:
            	    nadya.sendMessage(to, "👍เช็คจังหนังกระโปกʕ•ᴥ•ʔ")
                if msg.text in ["ออน",".ออน","!ออน",".uptime",".Uptime","!uptime","!Uptime"]:
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
