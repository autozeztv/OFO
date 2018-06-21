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
    helpMessage = "╔═══════════════" + "\n" + \
                  "║" + "\n" + \
                  "║✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡" + "\n" + \
                  "║" + "\n" + \
                  "╠══✪〘เมนูคำสั่ง〙✪══" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘คำสั่งต่างๆ〙✪════════" + "\n" + \
                  "╠➥ คำสั่ง" + "\n" + \
                  "╠➥ แปลภาษา" + "\n" + \
                  "╠➥ คำสั่งสิริ" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘 สเตตัส 〙✪════════" + "\n" + \
                  "╠➥ รีบอท" + "\n" + \
                  "╠➥ ออน" + "\n" + \
                  "╠➥ Speed" + "\n" + \
                  "╠➥ เชคค่า" + "\n" + \
                  "╠➥ ข้อมูล" + "\n" + \
                  "╠➥ ลบรัน" + "\n" + \
                  "╠➥ เทส" + "\n" + \
                  "╠➥ ยกเลิก" + "\n" + \
                  "╠➥ พูด [สั่งสิริพูดตาม]" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘เรา〙✪═════════" + "\n" + \
                  "╠➥ คท" + "\n" + \
                  "╠➥ ไอดี" + "\n" + \
                  "╠➥ เนม" + "\n" + \
                  "╠➥ สถานะ" + "\n" + \
                  "╠➥ รูป" + "\n" + \
                  "╠➥ รูปวีดีโอ" + "\n" + \
                  "╠➥ รูปปก" + "\n" + \
                  "╠➥ รายชื่อกลุ่ม" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘คนอื่น〙✪═════════" + "\n" + \
                  "╠➥ คท「@คนอื่น」" + "\n" + \
                  "╠➥ มิด「@คนอื่น」" + "\n" + \
                  "╠➥ ชื่อ「@คนอื่น」" + "\n" + \
                  "╠➥ ตัส「@คนอื่น」" + "\n" + \
                  "╠➥ ดิส「@คนอื่น」" + "\n" + \
                  "╠➥ ดิสวีดีโอ「@คนอื่น」" + "\n" + \
                  "╠➥ ดิสปก「@คนอื่น」" + "\n" + \
                  "╠➥ ก็อปปี้「@คนอื่น」" + "\n" + \
                  "╠➥ กลับร่าง" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘กลุ่ม〙✪════════" + "\n" + \
                  "╠➥ เชคแอด" + "\n" + \
                  "╠➥ ไอดีกลุ่ม" + "\n" + \
                  "╠➥ ชื่อกลุ่ม" + "\n" + \
                  "╠➥ รูปกลุ่ม" + "\n" + \
                  "╠➥ ลิ้งกลุ่ม" + "\n" + \
                  "╠➥ ลิ้งกลุ่ม「On/Off」" + "\n" + \
                  "╠➥ รายชื่อสมาชิกกลุ่ม" + "\n" + \
                  "╠➥ ข้อมูลกลุ่ม" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘คำสั่งอื่นๆ〙✪═══════" + "\n" + \
                  "╠➥ พิมตาม「On/Off」" + "\n" + \
                  "╠➥ รายชื่อคนพิมตาม" + "\n" + \
                  "╠➥ เพิ่มพิมตาม「@คนอื่น」" + "\n" + \
                  "╠➥ ลบพิมตาม「@คนอื่น」" + "\n" + \
                  "╠➥ แทค" + "\n" + \
                  "╠➥ หาคนอ่าน「Oɴ/Off/Reset」" + "\n" + \
                  "╠➥ อ่าน" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘 สื่อ 〙✪════════" + "\n" + \
                  "╠➥ ปฏิทิน" + "\n" + \
                  "╠➥ ตรวจสอบวันที่「วันที่」" + "\n" + \
                  "╠➥ ข้อมูลIG「ชื่อผู้ใช้」" + "\n" + \
                  "╠➥ โพสIG「ชื่อผู้」" + "\n" + \
                  "╠➥ ยูทูป「ชื่อ」" + "\n" + \
                  "╠➥ ขอเพลง「ชื่อเพลง」" + "\n" + \
                  "╠➥ เนื้อเพลง「ชื่อเพลง」" + "\n" + \
                  "╠➥ รูปภาพ「ค้นหา」" + "\n" + \
                  "╠➥ เว็บไซต์ภาพหน้าจอ「ลิ้งเว็บ」" + "\n" + \
                  "║" + "\n" + \
                  "╠✪〘การตั้งค่า〙✪═══════" + "\n" + \
                  "╠➥ AutoBlock「On/Off」" + "\n" + \
                  "╠➥ AutoJoin「On/Off」" + "\n" + \
                  "╠➥ AutoLeave「On/Off」" + "\n" + \
                  "╠➥ AutoRead「On/Off」" + "\n" + \
                  "╠➥ CheckSticker「On/Off」" + "\n" + \
                  "╠➥ DetectMention「On/Off」" + " \n" + \
                  "║" + "\n" + \
                  "╚═〘Ｈ̶̵̷͓͓͓̽̽̽  ҉Ｉ ̶̵̷͓͓͓̽̽̽ ҉Ｅ̶̵̷͓͓͓̽̽̽ ҉Ｔ̶̵̷͓͓͓̽̽̽ ҉Ｏ̶̵̷͓͓͓̽̽̽ ҉ Ｃ̶̵̷͓͓͓̽̽̽ ҉Ｉ ̶̵̷͓͓͓̽̽̽ ҉Ｈ̶̵̷͓͓͓̽̽̽ ҉〙"
    return helpMessage
    
 def help2():
    help2 =        "✪〘คำสั่งตั้งค่าต่างๆ〙✪" + "\n" + \
                         "👑AutoJoin 「On/Off」" + "\n" + \
                         "👑AutoRead「On/Off」" + "\n" + \
                         "👑AutoBlock 「On/Off」" + "\n" + \
                         "👑CheckSticker「On/Off」" + "\n" + \
                         "👑AutoLeave 「On/Off」" + "\n" + \
                         "👑Tag 「On/Off」" + "\n" + \
                         "👑Tag2 「On/Off」" + "\n" + \
                         "👑Join 「On/Off」" + "\n" + \
                         "👑Leave 「On/Off」" + "\n" + \
                         " " + "\n" + \
                         "✪〘คำสั่งตั้งต่างๆ〙✪" + "\n" + \
                         "🔥ตั้งแทค:" + "\n" + \
                         "🔥ตั้งออก:" + "\n" + \
                         "🔥ตั้งเข้า:" + "\n" + \
                         "🔥เชคแทค" + "\n" + \
                         "🔥เชคออก" + "\n" + \
                         "🔥เชคเข้า" + "\n" + \
                         " " + "\n " \
                         "✍️  ᴛ⃢​ᴇ⃢​ᴀ⃢​ᴍ⃢   🔝ͲᎻᎬᖴ͙͛Ꮮ͙͛ᗩ͙͛ᔑ͙͛Ꮋ͙  ̾⚡"
    return help2

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
                    help2 = help2()
                    nadya.sendMessage(to, str(help2))
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
                        ret_ = "╔══[ Status ]"
                        if settings["autoAdd"] == True: ret_ += "\n╠ Auto Add ✅"
                        else: ret_ += "\n╠ Auto Add ❌"
                        if settings["autoJoin"] == True: ret_ += "\n╠ Auto Join ✅"
                        else: ret_ += "\n╠ Auto Join ❌"
                        if settings["autoLeave"] == True: ret_ += "\n╠ Auto Leave ✅"
                        else: ret_ += "\n╠ Auto Leave ❌"
                        if settings["autoRead"] == True: ret_ += "\n╠ Auto Read ✅"
                        else: ret_ += "\n╠ Auto Read ❌"
                        if settings["checkSticker"] == True: ret_ += "\n╠ Check Sticker ✅"
                        else: ret_ += "\n╠ Check Sticker ❌"
                        if settings["detectMention"] == True: ret_ += "\n╠ Detect Mention ✅"
                        else: ret_ += "\n╠ Detect Mention ❌"
                        ret_ += "\n╚══[ Status ]"
                        nadya.sendMessage(to, str(ret_))
                    except Exception as e:
                        nadya.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoblock on':
                    settings["autoAdd"] = True
                    nadya.sendMessage(to, "┏───༺ ͜͡👑 ͜͡ ༻───┓\n 👍〘เปิดระบบออโต้บล็อค〙✔️\n┗───༺ ͜͡👑 ͜͡ ༻───┛")
                elif text.lower() == 'autoblock off':
                    settings["autoAdd"] = False
                    nadya.sendMessage(to, "┏───༺ ͜͡👑 ͜͡ ༻───┓ \n   👍〘ปิดระบบออโต้บล็อค〙🚫\n┗───༺ ͜͡👑 ͜͡ ༻───┛")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    nadya.sendMessage(to, "┏────༺ ͜͡🔥 ͜͡ ༻────┓\n    👍〘เปิดระบบเข้ากลุ่มออโต้〙✔️\n┗────༺ ͜͡🔥 ͜͡ ༻────┛")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    nadya.sendMessage(to, "┏────༺ ͜͡🔥 ͜͡ ༻────┓\n     👍〘ปิดระบบเข้ากลุ่มออโต้〙🚫\n┗────༺ ͜͡🔥 ͜͡ ༻────┛")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    nadya.sendMessage(to, "┏────༺ ͜͡🇹🇭 ͜͡ ༻────┓\n    👍〘เปิดระบบออกกลุ่มออโต้〙✔️\n┗────༺ ͜͡🇹🇭 ͜͡ ༻────┛")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    nadya.sendMessage(to, "┏────༺ ͜͡🇹🇭 ͜͡ ༻────┓\n     👍〘ปิดระบบออกกลุ่มออโต้〙🚫\n┗────༺ ͜͡🇹🇭 ͜͡ ༻────┛")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    nadya.sendMessage(to, "┏────༺ ͜͡❇️ ͜͡ ༻────┓\n       👍〘เปิดระบบอ่านออโต้〙✔️\n┗────༺ ͜͡❇️ ͜͡ ༻────┛")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    nadya.sendMessage(to, "┏────༺ ͜͡❇️ ͜͡ ༻────┓\n        👍〘ปิดระบบอ่านออโต้〙🚫\n┗────༺ ͜͡❇️ ͜͡ ༻────┛")
                elif text.lower() == 'checksticker on':
                    settings["checkSticker"] = True
                    nadya.sendMessage(to, "┏────༺ ͜͡🌟 ͜͡ ༻────┓\n    👍〘เปิดระบบเช็คสติ้กเกอร์〙✔️\n┗────༺ ͜͡🌟 ͜͡ ༻────┛")
                elif text.lower() == 'checksticker off':
                    settings["checkSticker"] = False
                    nadya.sendMessage(to, "┏────༺ ͜͡🌟 ͜͡ ༻────┓\n     👍〘ปิดระบบเช็คสติ้กเกอร์〙🚫\n┗────༺ ͜͡🌟 ͜͡ ༻────┛")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    nadya.sendMessage(to, "┏────༺ ͜͡⚡ ͜͡ ༻────┓\n      👍〘เปิดระบบการกล่าวถึง〙✔️\n┗────༺ ͜͡⚡ ͜͡ ༻────┛")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    nadya.sendMessage(to, "┏────༺ ͜͡⚡ ͜͡ ༻────┓\n       👍〘ปิดระบบการกล่าวถึง〙🚫\n┗────༺ ͜͡⚡ ͜͡ ༻────┛")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    nadya.sendMessage(to, "┏────༺ ͜͡🎃 ͜͡ ༻────┓\n👍〘เปิดระบบก็อปปี้ด้วยคอนแทค〙✔️\n┗────༺ ͜͡🎃 ͜͡ ༻────┛")
#==============================================================================#
                elif text.lower() == 'คท':
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
                                path = nadya.getProfileCoverURL(ls)
                                nadya.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("ก็อปปี้ "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            nadya.cloneContactProfile(contact)
                            nadya.sendMessage(msg.to, "ก็อปปี้เสร็จสิ้นกรุณารอโปรไฟล์เปลี่ยนสักครู่..♨️")
                        except:
                            nadya.sendMessage(msg.to, "ก็อปปี้ล้มเหลวกรุณาลองใหม่อีกครั้ง..♨️")
                            
                elif text.lower() == 'กลับร่าง':
                    try:
                        nadyaProfile.displayName = str(myProfile["displayName"])
                        nadyaProfile.statusMessage = str(myProfile["statusMessage"])
                        nadyaProfile.pictureStatus = str(myProfile["pictureStatus"])
                        nadya.updateProfileAttribute(8, nadyaProfile.pictureStatus)
                        nadya.updateProfile(nadyaProfile)
                        nadya.sendMessage(msg.to, "กู้คืนโปรไฟล์สำเร็จกรุณารอจนกว่าโปรไฟล์จะเปลี่ยน..🌙️")
                    except:
                        nadya.sendMessage(msg.to, "กู้คืนโปรไฟล์ล้มเหลว..🌙️")
                        
#==============================================================================#
                elif msg.text.lower().startswith("เพิ่มพิมตาม "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            settings["mimic"]["target"][target] = True
                            nadya.sendMessage(msg.to,"เพิ่มพิมตามเรียบร้อย..😛")
                            break
                        except:
                            nadya.sendMessage(msg.to,"เพิ่มพิมตามล้มเหลว..😛")
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
                            nadya.sendMessage(msg.to,"ลบพิมตามเรียบร้อย..😝")
                            break
                        except:
                            nadya.sendMessage(msg.to,"ลบพิมตามล้มเหลว..😝")
                            break
                elif text.lower() == 'รายชื่อคนพิมตาม':
                    if settings["mimic"]["target"] == {}:
                        nadya.sendMessage(msg.to,"ไม่มีการเพิ่มก่อนหน้านี้")
                    else:
                        mc = "╔══[ รายชื่อคนพิมตาม ]"
                        for mi_d in settings["mimic"]["target"]:
                            mc += "\n╠ "+nadya.getContact(mi_d).displayName
                        nadya.sendMessage(msg.to,mc + "\n╚══[ 🔝ƬΣΛM✍️ŦЂềƒÎάŠħ⚡]")
                    
                elif "พิมตาม" in msg.text.lower():
                    sep = text.split(" ")
                    mic = text.replace(sep[0] + " ","")
                    if mic == "on":
                        if settings["mimic"]["status"] == False:
                            settings["mimic"]["status"] = True
                            nadya.sendMessage(msg.to,"เปิดระบบพิมตามเรียบร้อย..😊")
                    elif mic == "off":
                        if settings["mimic"]["status"] == True:
                            settings["mimic"]["status"] = False
                            nadya.sendMessage(msg.to,"ปิดระบบพิมตามเรียบร้อย..😊")
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
                            nadya.sendMessage(to, "กรุณาเปิดลิ้งกลุ่มก่อน\nลงคำสั่งนี้ด้วยครับ😊".format(str(settings["keyCommand"])))
                elif text.lower() == 'ลิ้งกลุ่ม on':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            nadya.sendMessage(to, "ลิ้งกลุ่มเปิดอยู่แล้ว..😶")
                        else:
                            group.preventedJoinByTicket = False
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "เปิดลิ้งกลุ่มเรียบร้อย..😶")
                elif text.lower() == 'ลิ้งกลุ่ม off':
                    if msg.toType == 2:
                        group = nadya.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            nadya.sendMessage(to, "ลิ้งกลุ่มปิดอยู่แล้ว..😌")
                        else:
                            group.preventedJoinByTicket = True
                            nadya.updateGroup(group)
                            nadya.sendMessage(to, "ลิ้งกลุ่มปิดเรียบร้อย..😌")
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
                        ret_ += "\n╚══[ จำนวนสมาชิก👉 {} คน👑 ]".format(str(len(group.members)))
                        nadya.sendMessage(to, str(ret_))
                elif text.lower() == 'รายชื่อกลุ่ม':
                        groups = nadya.groups
                        ret_ = "╔══[ รายชื่อกลุ่ม ]"
                        no = 0 + 1
                        for gid in groups:
                            group = nadya.getGroup(gid)
                            ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n╚══[ จำนวนกลุ่ม👉 {} กลุ่ม👑 ]".format(str(len(groups)))
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
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if nadyaMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = nadya.getContact(sender)
                                    nadya.sendMessage(to, "sundala nu")
                                    sendMessageWithMention(to, contact.mid)
                                break
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
