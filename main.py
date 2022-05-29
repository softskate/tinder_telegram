import telebot
import sqlite3
import time
from telebot import types

bot=telebot.TeleBot(token='2066902261:AAEO3ktvWMcVPsjRvVLHvDJEY24qgXAefns')
con=sqlite3.connect('date.db')
curs=con.cursor()
#api.telegram.org/bot2026612503:AAHalelnV_FePFUlYrdmOgO_nDCUAztx9B8/getUpdates
curs.execute("""CREATE TABLE IF NOT EXISTS users(
id TEXT,
sts TEXT,
gen TEXT,
last TEXT,
auth TEXT,
log TEXT,
pass TEXT

)""")
con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS auth(
log TEXT,
pass TEXT,
gen TEXT,
photo TEXT,
like TEXT,
got TEXT

)""")

con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS done(
log TEXT,
got TEXT

)""")

con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS data(
log TEXT,
photo TEXT,
got TEXT,
want TEXT

)""")
con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS msgs(
user TEXT,
msg TEXT

)""")
con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS message(
user TEXT,
msg TEXT

)""")
con.commit()

curs.execute("""CREATE TABLE IF NOT EXISTS com(
taskid TEXT

)""")
con.commit()



@bot.message_handler(commands=['start'])
def start(message):
    con=sqlite3.connect('date.db')
    curs=con.cursor()
    chat_id=message.chat.id
    curs.execute("SELECT id,auth FROM users WHERE id=?",(chat_id,))
    data=curs.fetchone()

    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row_width=4
    kb1=types.KeyboardButton('\u2764\ufe0f\u200d\ud83d\udd25')
    kb2=types.KeyboardButton('\u2728')
    kb3=types.KeyboardButton('\ud83d\udc8c')
    kb4=types.KeyboardButton('\u2716\ufe0f')
    kb.add(kb1, kb2, kb3, kb4)

    ms=bot.send_message(chat_id, '*LAMPOO*' ,parse_mode='Markdown', reply_markup=kb)
##    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
##    kb.row_width=2
##    kb1=types.KeyboardButton('Р РµРіРёСЃС‚СЂР°С†РёСЏ')
##    kb2=types.KeyboardButton('Р’РѕР№С‚Рё')
##    kb.add(kb1, kb2)

    kb = types.InlineKeyboardMarkup(row_width=4)
    kb1=types.InlineKeyboardButton(text="Р РµРіРёСЃС‚СЂР°С†РёСЏ", callback_data="reg")
    kb4=types.InlineKeyboardButton(text="Р’РѕР№С‚Рё", callback_data="side")
    kb.add(kb1, kb4)

    if data is None:
        curs.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", (chat_id, 'log', 'boy',int(time.time()) , 'no', 'no', 'no'))
        con.commit()
        ms=bot.send_message(chat_id, 'Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ' ,parse_mode='Markdown', reply_markup=kb)
#types.ReplyKeyboardRemove()
    elif data[1]=='no':
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('log', chat_id))
        con.commit()
        ms=bot.send_message(chat_id, 'Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊРІ' ,parse_mode='Markdown', reply_markup=kb)
    else:
        try:
            curs.execute("""UPDATE users SET sts=?,auth=? WHERE id=?""", ('log', 'no', chat_id))
            con.commit()
            ms=bot.send_message(chat_id, 'Р’С‹ РІС‹С€Р»Рё РёР· *LAMPOO*' ,parse_mode='Markdown', reply_markup=kb)
        except:
            curs.execute("DELETE FROM users WHERE id=?", (chat_id,))
            con.commit()
            print('err2')
    curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,ms.id))
    con.commit()
    try:
        bot.delete_message(chat_id=chat_id,message_id=message.message_id)
    except:
        pass


@bot.message_handler(content_types=['text'])
def txt(message):
    chat_id=message.chat.id
    con=sqlite3.connect('date.db')
    curs=con.cursor()
    ms=0
    sts='fk'
    auth='no'
    log='no'
    curs.execute("SELECT sts,auth,log FROM users WHERE id=?",(chat_id,))
    stss=curs.fetchone()
    if stss is not None:
        sts=stss[0]
        auth=stss[1]
        log=stss[2]
    else:
        start(message)
    if not sts.startswith('msg '):
        try:
            bot.delete_message(chat_id=chat_id,message_id=message.message_id)
        except:
            pass
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()

    if sts is None:
        start(message)

    elif sts=='rlog':
        alpha=message.text.strip().replace('_','')
        curs.execute("SELECT log FROM auth WHERE log=?",(message.text,))
        got=curs.fetchone()
        if alpha.isalpha() and got is None and len(message.text)>3 and alpha.isascii():
            ms=bot.send_message(chat_id, "Р’РІРµРґРёС‚Рµ РїР°СЂРѕР»СЊ")
            curs.execute("""UPDATE users SET sts=?, log=? WHERE id=?""", ('rpass', message.text.strip().lower(), chat_id))
            con.commit()
        elif got is not None:
            ms=bot.send_message(chat_id, "Р­С‚РѕС‚ Р»РѕРіРёРЅ СѓР¶Рµ Р·Р°РЅСЏС‚")
        else:
            ms=bot.send_message(chat_id, "Р›РѕРіРёРЅ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ Р±РѕР»СЊС€Рµ 4 СЃРёРјРІРѕР»Р° Рё РјРѕР¶РЅРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ С‚РѕР»СЊРєРѕ Р»Р°С‚РёРЅСЃРєРёРµ Р±СѓРєРІС‹ Рё РїРѕРґС‡С‘СЂРєРёРІР°РЅРёРµ (_)")

    elif sts=='rpass':
        if len(message.text)>5:
            ms=bot.send_message(chat_id, "РћС‚РїСЂР°РІСЊС‚Рµ РґРѕ 5 С„РѕС‚РѕРіСЂР°С„РёРё")
            curs.execute("""UPDATE users SET sts=?, pass=? WHERE id=?""", ('rph', message.text, chat_id))
            con.commit()
        else:
            ms=bot.send_message(chat_id, "РџР°СЂРѕР»СЊ РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ Р±РѕР»СЊС€Рµ 4 СЃРёРјРІРѕР»Р°")

    elif sts=='log':
        ms=bot.send_message(chat_id, "Р’РІРµРґРёС‚Рµ РїР°СЂРѕР»СЊ")
        curs.execute("""UPDATE users SET sts=?, log=? WHERE id=?""", ('pass', message.text.strip().lower(), chat_id))
        con.commit()

    elif sts=='pass':
        curs.execute("SELECT log FROM users WHERE id=?",(chat_id,))
        log=curs.fetchone()[0]
        print(log)
        curs.execute("SELECT gen FROM auth WHERE log=? and pass=?",(log,message.text))
        pas=curs.fetchone()
        if pas is None:
            kb = types.InlineKeyboardMarkup(row_width=4)
            kb1=types.InlineKeyboardButton(text="Р РµРіРёСЃС‚СЂР°С†РёСЏ", callback_data="reg")
            kb4=types.InlineKeyboardButton(text="Р’РѕР№С‚Рё", callback_data="side")
            kb.add(kb1, kb4)
            ms=bot.send_message(chat_id, "РќРµ РїСЂР°РІРёР»СЊРЅС‹Р№ Р»РѕРіРёРЅ РёР»Рё РїР°СЂРѕР»СЊ.", reply_markup=kb)
            curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('log', chat_id))
            con.commit()
        else:
            curs.execute("""UPDATE users SET sts=?,auth=?,pass=?,gen=? WHERE id=?""", ('main','yes', message.text,pas[0], chat_id))
            con.commit()
            for i in msg:
                try:
                    bot.delete_message(chat_id,message_id=int(i[0]))
                except Exception as e:
                    print(e)
##            kbs = types.InlineKeyboardMarkup(row_width=4)
##            kbs1=types.InlineKeyboardButton(text="РџСЂРѕРґРѕР»Р¶РёС‚СЊ", callback_data="get")
##            kbs.add(kbs1)

            curs.execute("SELECT got,gen FROM auth WHERE log=?",(log,))
            gt=curs.fetchone()
            got=gt[0]
            ge='boy'
            if gt[1]=='boy':
                ge='girl'
            curs.execute("SELECT log FROM users WHERE gen=? and sts=?",(ge,'main'))
            io=curs.fetchone()
            if io is not None:
##                iy='"'+io[0]+'"'
##                if got is not None:
##                    iy =got+ ', "'+io[0]+'"'
##                curs.execute("""UPDATE auth SET got=? WHERE log=?""", (iy,log))
##                con.commit()
                curs.execute("SELECT photo FROM auth WHERE log=?",(io[0],))
                i=curs.fetchone()
                cot=len(i[0].split())
                kb = types.InlineKeyboardMarkup(row_width=4)
                kb1=types.InlineKeyboardButton(text="\u274c", callback_data="sget dislike "+io[0])
                kb4=types.InlineKeyboardButton(text="\u2764\ufe0f", callback_data="sget like "+io[0])
                if cot>1:
                    kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data="next "+'0 '+io[0])
                    kb.add(kb1, kb2, kb4)
                else:
                    kb.add(kb1, kb4)
                kb.row_width=4
                cap='\u25aa\ufe0f'+'\u25ab\ufe0f'*(cot-1)
                ms=bot.send_photo(chat_id=chat_id, photo=i[0].split()[0], caption=cap, reply_markup=kb)

            curs.execute("DELETE FROM users WHERE log=? and id!=?", (log,chat_id))
            con.commit()
##            curs.execute("SELECT id,name,number,loc,stat FROM tasks WHERE sts=? and tou=?",('active',data[0]))
##            data=curs.fetchall()

#auth
    elif auth=='no':
        kb = types.InlineKeyboardMarkup(row_width=4)
        kb1=types.InlineKeyboardButton(text="Р РµРіРёСЃС‚СЂР°С†РёСЏ", callback_data="reg")
        kb4=types.InlineKeyboardButton(text="Р’РѕР№С‚Рё", callback_data="side")
        kb.add(kb1, kb4)
        ms=bot.send_message(chat_id, "РђРІС‚РѕСЂРёР·СѓР№С‚РµСЃСЊ РїРѕР¶Р°Р»СѓР№СЃС‚Р°", reply_markup=kb)

    elif message.text=='\u2764\ufe0f\u200d\ud83d\udd25' or message.text=='вќ¤пёЏвЂЌрџ”Ґ':
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('main',chat_id))
        con.commit()
        #del msg
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()

        curs.execute("SELECT log FROM users WHERE id=?",(chat_id,))
        log=curs.fetchone()[0]
        curs.execute("SELECT got,gen FROM auth WHERE log=?",(log,))
        gt=curs.fetchone()
        got=gt[0]
        ge='boy'
        if gt[1]=='boy':
            ge='girl'
            
        gt='"m","m"'
        if got is not None:
            gt=got
        tx='main'
        
        curs.execute(f"SELECT log FROM users WHERE gen=? and sts=? and log not in ({gt})",(ge,tx))
        io=curs.fetchone()
        
        if io is not None:
##            iy='"'+io[0]+'"'
##            if got is not None:
##                iy =got+ ', "'+io[0]+'"'
##            curs.execute("""UPDATE auth SET got=? WHERE log=?""", (iy,log))
##            con.commit()
            curs.execute("SELECT photo FROM auth WHERE log=?",(io[0],))
            i=curs.fetchone()
            cot=len(i[0].split())
            kb = types.InlineKeyboardMarkup(row_width=4)
            kb1=types.InlineKeyboardButton(text="\u274c", callback_data="sget dislike "+io[0])
            kb4=types.InlineKeyboardButton(text="\u2764\ufe0f", callback_data="sget like "+io[0])
            if cot>1:
                kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data="next "+'0 '+io[0])
                kb.add(kb1, kb2, kb4)
            else:
                kb.add(kb1, kb4)
            kb.row_width=4
            cap='\u25aa\ufe0f'+'\u25ab\ufe0f'*(cot-1)+'    '+io[0]
            ms=bot.send_photo(chat_id=chat_id, photo=i[0].split()[0], caption=cap, reply_markup=kb)

    elif message.text=='\u2728' or message.text=='вњЁ':
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('main',chat_id))
        con.commit()
        #del msg
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()

        curs.execute("SELECT like FROM auth WHERE log=?",(log,))
        io=curs.fetchone()[0]
        if io is not None:
            iy=io.split(', ')[0]
##            ids=None
##            if len(io.split(', '))>1:
##                ids =io.replace(iy+ ', ','')
##            curs.execute("""UPDATE auth SET like=? WHERE log=?""", (ids,log))
##            con.commit()
            curs.execute("SELECT photo FROM auth WHERE log=?",(iy,))
            i=curs.fetchone()
            cot=len(i[0].split())
            kb = types.InlineKeyboardMarkup(row_width=4)
            kb1=types.InlineKeyboardButton(text="\u274c", callback_data="mget dislike "+log)
            kb4=types.InlineKeyboardButton(text="\u2709\ufe0f", callback_data="mget like "+iy)
            if cot>1:
                kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data="nexts "+'0 '+iy)
                kb.add(kb1, kb2, kb4)
            else:
                kb.add(kb1, kb4)
            kb.row_width=4
            cap='\u25aa\ufe0f'+'\u25ab\ufe0f'*(cot-1)+'    '+iy
            ms=bot.send_photo(chat_id=chat_id, photo=i[0].split()[0], caption=cap, reply_markup=kb)
        
    elif message.text=='\ud83d\udc8c' or message.text== 'рџ’Њ':

        try:
            bot.delete_message(chat_id=chat_id,message_id=message.message_id)
        except:
            pass
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()

        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('main',chat_id))
        con.commit()
        curs.execute("SELECT user FROM message WHERE user LIKE ? or user LIKE ?",('% '+log,log+' %',))
        msg=curs.fetchall()
        user=set(msg)
        print(user,log)
        kb = types.InlineKeyboardMarkup(row_width=2)
        lt=None
        for i in user:
            us=i[0].replace(log,'').strip()
            if us != lt:
                kb1=types.InlineKeyboardButton(text=us, callback_data="my "+us)
                kb.add(kb1)
            lt=us
        ms=bot.send_message(chat_id, "РЎРїРёСЃРѕРє РІР°С€РёС… СЃРѕРѕР±С‰РµРЅРёР№:", reply_markup=kb)

    elif message.text== 'вњ–пёЏ':
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()
        curs.execute("""DELETE FROM users WHERE id=?""", (chat_id,))
        con.commit()

##    elif message.text=='РџСЂРѕРґРѕР»Р¶РёС‚СЊ':
##        kb = types.InlineKeyboardMarkup(row_width=2)
##        kb1=types.InlineKeyboardButton(text="РњСѓР¶С‡РёРЅР°", callback_data="sel girl")
##        kb2=types.InlineKeyboardButton(text="Р–РµРЅС‰РёРЅР°", callback_data="sel boy")
##        kb.add(kb1, kb2)
##        ms=bot.send_message(chat_id, "Р’С‹Р±РµСЂРёС‚Рµ СЃРІРѕР№ РїРѕР» РїРѕР¶Р°Р»СѓР№СЃС‚Р°:", reply_markup=kb)

    elif sts.startswith('msg'):
        mss=message.text
        if mss.startswith('%%'):
            mss='f'+message.text
        curs.execute("INSERT INTO message VALUES(?, ?)", (log+' '+sts.split()[-1],mss))
        con.commit()
        curs.execute("SELECT id,sts FROM users WHERE log=? and auth=?",(sts.split()[-1],'yes'))
        msg=curs.fetchone()
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,message.id))
        con.commit()
        if msg is not None and msg[1]=='msg '+log:
            msd=bot.send_message(msg[0], message.text)
            curs.execute("INSERT INTO msgs VALUES(?, ?)", (msg[0],msd.id))
            con.commit()
        elif msg is not None:
            kbu = types.InlineKeyboardMarkup()
            kbu1=types.InlineKeyboardButton(text="РџРѕРЅСЏС‚РЅРѕ", callback_data="del")
            kbu2=types.InlineKeyboardButton(text="Р‘Р°РЅ", callback_data="bas "+log)
            kbu.add(kbu1,kbu2)
            bot.send_message(chat_id=msg[0], text=f"РЈ РІР°СЃ РЅРѕРІР°СЏ СЃРѕРѕР±С‰РµРЅРёСЏ РѕС‚ {log}. РџРѕСЃРјРѕС‚СЂРёС‚Рµ РІ СЂР°Р·РґРµР»Рµ рџ’Њ", reply_markup=kbu)


    else:
        ms=bot.send_message(chat_id, "РќРµ РїСЂР°РІРёР»СЊРЅС‹Р№ С…РѕРґ")
    if ms!=0:
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,ms.id))
        con.commit()


@bot.message_handler(content_types=['photo'])
def ph(message):
    chat_id=message.chat.id
    con=sqlite3.connect('date.db')
    curs=con.cursor()
    try:
        bot.delete_message(chat_id=chat_id,message_id=message.message_id)
    except:
        pass
    curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
    msg=curs.fetchall()
    for i in msg:
        time.sleep(0.2)
        try:
            bot.delete_message(chat_id,message_id=int(i[0]))
        except Exception as e:
            print(e)
    curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
    con.commit()

    curs.execute("SELECT sts,log FROM users WHERE id=(?)",(chat_id,))
    stss=curs.fetchone()
    kb = types.InlineKeyboardMarkup()
    kb1=types.InlineKeyboardButton(text="РџСЂРѕРґРѕР»Р¶РёС‚СЊ", callback_data="start")
    kb.add(kb1)
    sts=None
    log=None
    if stss is not None:
        sts=stss[0]
        log=stss[1]
        if not sts.startswith('msg'):
            try:
                bot.delete_message(chat_id=chat_id,message_id=message.message_id)
            except:
                pass
            curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
            msg=curs.fetchall()
            for i in msg:
                time.sleep(0.2)
                try:
                    bot.delete_message(chat_id,message_id=int(i[0]))
                except Exception as e:
                    print(e)
            curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
            con.commit()

    if stss is None:
        start(message)
    elif sts=='rph':
        curs.execute("SELECT log,pass FROM users WHERE id=?",(chat_id,))
        log=curs.fetchone()
        curs.execute("SELECT photo FROM auth WHERE log=?",(log[0],))
        ph=curs.fetchone()
        if ph is None:
            curs.execute("INSERT INTO auth VALUES(?,?,?,?,?,?)", (log[0], log[1],'boy',message.photo[-1].file_id,None,None))
            con.commit()
            curs.execute("""UPDATE users SET auth=? WHERE id=?""", ('yes',chat_id))
            con.commit()
            msi=bot.send_message(chat_id, "Р’С‹ РјРѕР¶РµС‚Рµ РѕС‚РїСЂР°РІРёС‚СЊ РµС‰С‘ 4 С„РѕС‚РѕРіСЂР°С„РёРё", reply_markup=kb)
            curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,msi.id))
            con.commit()
        elif len(ph[0].split())>3:
            msi=bot.send_message(chat_id, "Р‘РѕР»СЊС€Рµ С„РѕС‚Рѕ РѕС‚РїСЂР°РІРёС‚СЊ РЅРёР»СЊР·СЏ", reply_markup=kb)
            curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,msi.id))
            con.commit()
        else:
            p=ph[0]+' '+message.photo[-1].file_id
            curs.execute("""UPDATE auth SET photo=? WHERE log=?""", (p,log[0]))
            con.commit()
            c=4-len(ph[0].split())
            if c >0:
                msi=bot.send_message(chat_id, f"Р’С‹ РјРѕР¶РµС‚Рµ РѕС‚РїСЂР°РІРёС‚СЊ РµС‰С‘ {c} С„РѕС‚РѕРіСЂР°С„РёРё", reply_markup=kb)
                curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,msi.id))
                con.commit()
            else:
                msi=bot.send_message(chat_id, "Р‘РѕР»СЊС€Рµ С„РѕС‚Рѕ РѕС‚РїСЂР°РІРёС‚СЊ РЅРёР»СЊР·СЏ", reply_markup=kb)
                curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,msi.id))
                con.commit()

    elif sts.startswith('msg'):
        curs.execute("INSERT INTO message VALUES(?, ?)", (log+' '+sts.split()[-1],'%%ph'+message.photo[-1].file_id))
        con.commit()
        curs.execute("SELECT id,sts FROM users WHERE log=? and auth=?",(sts.split()[-1],'yes'))
        msg=curs.fetchone()
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,message.id))
        con.commit()
        if msg is not None and msg[1]=='msg '+log:
            msd=bot.send_photo(msg[0], message.photo[-1].file_id)
            curs.execute("INSERT INTO msgs VALUES(?, ?)", (msg[0],msd.id))
            con.commit()
        elif msg is not None:
            kbu = types.InlineKeyboardMarkup()
            kbu1=types.InlineKeyboardButton(text="РџРѕРЅСЏС‚РЅРѕ", callback_data="del")
            kbu2=types.InlineKeyboardButton(text="Р‘Р°РЅ", callback_data="bas "+log)
            kbu.add(kbu1,kbu2)
            bot.send_message(chat_id=msg[0], text=f"РЈ РІР°СЃ РЅРѕРІР°СЏ С„РѕС‚Рѕ СЃРѕРѕР±С‰РµРЅРёСЏ РѕС‚ {log}. РџРѕСЃРјРѕС‚СЂРёС‚Рµ РІ СЂР°Р·РґРµР»Рµ рџ’Њ", reply_markup=kbu)

    else:
        ms=bot.send_message(chat_id, "РќРµ РїСЂР°РІРёР»СЊРЅС‹Р№ С…РѕРґ")
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,ms.id))
        con.commit()









@bot.message_handler(content_types=['video'])
def vd(message):
    chat_id=message.chat.id
    con=sqlite3.connect('date.db')
    curs=con.cursor()

    curs.execute("SELECT sts,log FROM users WHERE id=(?)",(chat_id,))
    stss=curs.fetchone()
    sts=None
    log=None
    if stss is not None:
        sts=stss[0]
        log=stss[1]
        if not sts.startswith('msg'):
            try:
                bot.delete_message(chat_id=chat_id,message_id=message.message_id)
            except:
                pass
            curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
            msg=curs.fetchall()
            for i in msg:
                time.sleep(0.2)
                try:
                    bot.delete_message(chat_id,message_id=int(i[0]))
                except Exception as e:
                    print(e)
            curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
            con.commit()

    if stss is None:
        start(message)
    elif sts.startswith('msg'):
        curs.execute("INSERT INTO message VALUES(?, ?)", (log+' '+sts.split()[-1],'%%vd'+message.video.file_id))
        con.commit()
        curs.execute("SELECT id,sts FROM users WHERE log=? and auth=?",(sts.split()[-1],'yes'))
        msg=curs.fetchone()
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,message.id))
        con.commit()
        if msg is not None and msg[1]=='msg '+log:
            msd=bot.send_video(msg[0], message.video.file_id)
            curs.execute("INSERT INTO msgs VALUES(?, ?)", (msg[0],msd.id))
            con.commit()
        elif msg is not None:
            kbu = types.InlineKeyboardMarkup()
            kbu1=types.InlineKeyboardButton(text="РџРѕРЅСЏС‚РЅРѕ", callback_data="del")
            kbu2=types.InlineKeyboardButton(text="Р‘Р°РЅ", callback_data="bas "+log)
            kbu.add(kbu1,kbu2)
            bot.send_message(chat_id=msg[0], text=f"РЈ РІР°СЃ РЅРѕРІР°СЏ РІРёРґРµРѕ СЃРѕРѕР±С‰РµРЅРёСЏ РѕС‚ {log}. РџРѕСЃРјРѕС‚СЂРёС‚Рµ РІ СЂР°Р·РґРµР»Рµ рџ’Њ", reply_markup=kbu)

    else:
        ms=bot.send_message(chat_id, "РќРµ РїСЂР°РІРёР»СЊРЅС‹Р№ С…РѕРґ")
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,ms.id))
        con.commit()

@bot.callback_query_handler(func= lambda call: True)
def answ (call):
    print(call.data)
    chat_id=call.message.chat.id
    con=sqlite3.connect('date.db')
    curs=con.cursor()
    curs.execute("SELECT sts,auth,log FROM users WHERE id=(?)",(chat_id,))
    stss=curs.fetchone()
    auth='no'
    log='no'
    sts='no'
    if stss is not None:
        sts=stss[0]
        auth=stss[1]
        log=stss[2]
    else:
        start(call.message)
    curs.execute("""UPDATE users SET last=? WHERE id=?""", (int(time.time()),chat_id))
    con.commit()
##    if sts is None or auth=='no':
##        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
##        msg=curs.fetchall()
##        for i in msg:
##            try:
##                bot.delete_message(chat_id,message_id=int(i[0]))
##            except Exception as e:
##                print(e)
##        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
##        con.commit()

    if call.data=='side':
        bot.answer_callback_query(call.id)
        kb = types.InlineKeyboardMarkup()
        kb1=types.InlineKeyboardButton(text="Р РµРіРёСЃС‚СЂР°С†РёСЏ", callback_data="reg")
        kb.add(kb1)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Р’РІРµРґРёС‚Рµ РІР°С€ Р»РѕРіРёРЅ РїРѕР¶Р°Р»СѓР№СЃС‚Р°:", reply_markup=kb)
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('log', chat_id))
        con.commit()

    elif call.data=='reg':
        bot.answer_callback_query(call.id)
        kb = types.InlineKeyboardMarkup()
        kb4=types.InlineKeyboardButton(text="Р’РѕР№С‚Рё", callback_data="side")
        kb.add( kb4)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="РџСЂРёРґСѓРјР°Р№С‚Рµ Р»РѕРіРёРЅ:", reply_markup=kb)
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('rlog', chat_id))
        con.commit()

    elif call.data=='start':
        bot.answer_callback_query(call.id)
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb1=types.InlineKeyboardButton(text="РњСѓР¶С‡РёРЅР°", callback_data="sel boy")
        kb2=types.InlineKeyboardButton(text="Р–РµРЅС‰РёРЅР°", callback_data="sel girl")
        kb.add(kb1, kb2)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Р’С‹Р±РµСЂРёС‚Рµ СЃРІРѕР№ РїРѕР» РїРѕР¶Р°Р»СѓР№СЃС‚Р°:", reply_markup=kb)

    elif call.data.startswith('sel'):
        bot.answer_callback_query(call.id)
        curs.execute("""UPDATE users SET gen=?,sts=? WHERE id=?""", (call.data.split()[-1],'main',chat_id))
        con.commit()
        curs.execute("""UPDATE auth SET gen=? WHERE log=?""", (call.data.split()[-1],log))
        con.commit()
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.row_width=4
        kb1=types.KeyboardButton('\u2764\ufe0f\u200d\ud83d\udd25')
        kb2=types.KeyboardButton('\u2728')
        kb3=types.KeyboardButton('\ud83d\udc8c')
        kb4=types.KeyboardButton('\u2716\ufe0f')
        kb.add(kb1, kb2, kb3, kb4)
        bot.delete_message(chat_id,message_id=call.message.message_id)
##
##        curs.execute("SELECT log FROM users WHERE id=?",(chat_id,))
##        log=curs.fetchone()[0]
        print(log)
        curs.execute("SELECT got,gen FROM auth WHERE log=?",(log,))
        gt=curs.fetchone()
        got=gt[0]
        ge='boy'
        if gt[1]=='boy':
            ge='girl'
        curs.execute("SELECT log FROM users WHERE gen=? and sts=?",(ge,'main'))
        io=curs.fetchone()
        if io is not None:
##            iy='"'+io[0]+'"'
##            if got is not None:
##                iy =got+ ', "'+io[0]+'"'
##            curs.execute("""UPDATE auth SET got=? WHERE log=?""", (iy,log))
##            con.commit()
            curs.execute("SELECT photo FROM auth WHERE log=?",(io[0],))
            i=curs.fetchone()
            cot=len(i[0].split())
            kb = types.InlineKeyboardMarkup(row_width=4)
            kb1=types.InlineKeyboardButton(text="\u274c", callback_data="sget dislike "+io[0])
            kb4=types.InlineKeyboardButton(text="\u2764\ufe0f", callback_data="sget like "+io[0])
            if cot>1:
                kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data="next "+'0 '+io[0])
                kb.add(kb1, kb2, kb4)
            else:
                kb.add(kb1, kb4)
            kb.row_width=4
            cap='\u25aa\ufe0f'+'\u25ab\ufe0f'*(cot-1)+'    '+io[0]
            kk=bot.send_photo(chat_id=chat_id, photo=i[0].split()[0], caption=cap, reply_markup=kb)
            curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,kk.id))
            con.commit()

    elif call.data.startswith('sget'):
        bot.answer_callback_query(call.id)
        curs.execute("SELECT log,gen FROM users WHERE id=?",(chat_id,))
        dat=curs.fetchone()
        log=dat[0]
        sg='boy'
        if dat[1]=='boy':
            sg='girl'
        curs.execute("SELECT got FROM auth WHERE log=?",(log,))
        got=curs.fetchone()[0]
        gt='"m","m"'
        if got is not None:
            gt=got+', "'+call.data.split()[-1]+'"'
        tx='main'
        print(gt,got)
        curs.execute(f"SELECT log FROM users WHERE gen=? and sts=? and log not in ({gt})",(sg,tx))
        io=curs.fetchone()
        if io is not None:
            curs.execute("""UPDATE auth SET got=? WHERE log=?""", (gt,log))
            con.commit()
            if call.data.split()[-2]=='like':
                curs.execute("SELECT like FROM auth WHERE log=?",(call.data.split()[-1],))
                lk=curs.fetchone()[0]
                if lk is None:
                    lk=log
                else:
                    lk=lk+', '+log
                curs.execute("""UPDATE auth SET like=? WHERE log=?""", (lk,call.data.split()[-1]))
                con.commit()
                curs.execute("SELECT id FROM users WHERE log=? and sts!=?",(call.data.split()[-1],'no'))
                ch=curs.fetchone()
                if ch is not None:
                    kbu = types.InlineKeyboardMarkup()
                    kbu1=types.InlineKeyboardButton(text="РџРѕРЅСЏС‚РЅРѕ", callback_data="del")
                    kbu.add(kbu1)
                    bot.send_message(chat_id=ch[0], text="РЈ РІР°СЃ РЅРѕРІС‹Р№ Р»Р°Р№Рє. РџРѕСЃРјРѕС‚СЂРёС‚Рµ РІ СЂР°Р·РґРµР»Рµ вњЁ", reply_markup=kbu)

            curs.execute("SELECT photo FROM auth WHERE log=?",(io[0],))
            i=curs.fetchone()
            cot=len(i[0].split())
            kb = types.InlineKeyboardMarkup(row_width=4)
            kb1=types.InlineKeyboardButton(text="\u274c", callback_data="sget dislike "+io[0])
            kb4=types.InlineKeyboardButton(text="\u2764\ufe0f", callback_data="sget like "+io[0])
            if cot>1:
                kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data="next "+'0 '+io[0])
                kb.add(kb1, kb2, kb4)
            else:
                kb.add(kb1, kb4)
            kb.row_width=4
            cap='\u25aa\ufe0f'+'\u25ab\ufe0f'*(cot-1)+'    '+io[0]
            bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=types.InputMediaPhoto(i[0].split()[0]))
            bot.edit_message_caption( chat_id=chat_id, message_id=call.message.message_id, caption=cap, reply_markup=kb)


    elif call.data.startswith('next'):
        bot.answer_callback_query(call.id)
        curs.execute("SELECT photo FROM auth WHERE log=?",(call.data.split()[-1],))
        i=curs.fetchone()
        ts=int(call.data.split()[-2])+1
        cot=len(i[0].split())
        xt="next "
        bk="back "
        kb1=types.InlineKeyboardButton(text="\u274c", callback_data="sget dislike "+call.data.split()[-1])
        kb4=types.InlineKeyboardButton(text="\u2764\ufe0f", callback_data="sget like "+call.data.split()[-1])
        if call.data.startswith('nexts'):
            xt="nexts "
            bk="backs "
            kb1=types.InlineKeyboardButton(text="\u274c", callback_data="mget dislike "+log)
            kb4=types.InlineKeyboardButton(text="\u2709\ufe0f", callback_data="mget like "+call.data.split()[-1])
        kb = types.InlineKeyboardMarkup(row_width=4)
        kb3=types.InlineKeyboardButton(text="\ud83d\udd19", callback_data=bk+str(ts)+' '+call.data.split()[-1])
        if cot>int(call.data.split()[-2])+2:
            kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data=xt+str(ts)+' '+call.data.split()[-1])
            kb.row(kb1, kb3, kb2, kb4)
        else:
            kb.row(kb1, kb3, kb4)
        kb.row_width=4
        cap=('\u25ab\ufe0f'*(int(call.data.split()[-2])+1))+'\u25aa\ufe0f'+('\u25ab\ufe0f'*(cot-int(call.data.split()[-2])-2))+'    '+call.data.split()[-1]
        bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=types.InputMediaPhoto(i[0].split()[ts]))
        bot.edit_message_caption( chat_id=chat_id, message_id=call.message.message_id, caption=cap, reply_markup=kb)
##            bot.send_photo(chat_id=chat_id, photo=types.InputMediaPhoto(i[0].split()[0]), reply_markup=kb)caption=message.caption

    elif call.data.startswith('back'):
        bot.answer_callback_query(call.id)
        curs.execute("SELECT photo FROM auth WHERE log=?",(call.data.split()[-1],))
        i=curs.fetchone()
        ts=int(call.data.split()[-2])-1
        cot=len(i[0].split())
        xt="next "
        bk="back "
        kb1=types.InlineKeyboardButton(text="\u274c", callback_data="sget dislike "+call.data.split()[-1])
        kb4=types.InlineKeyboardButton(text="\u2764\ufe0f", callback_data="sget like "+call.data.split()[-1])
        if call.data.startswith('backs'):
            xt="nexts "
            bk="backs "
            kb1=types.InlineKeyboardButton(text="\u274c", callback_data="mget dislike "+log)
            kb4=types.InlineKeyboardButton(text="\u2709\ufe0f", callback_data="mget like "+call.data.split()[-1])
        kb = types.InlineKeyboardMarkup(row_width=4)
        kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data=xt+str(ts)+' '+call.data.split()[-1])
        if 1<int(call.data.split()[-2]):
            kb3=types.InlineKeyboardButton(text="\ud83d\udd19", callback_data=bk+str(ts)+' '+call.data.split()[-1])
            kb.row(kb1, kb3, kb2, kb4)
        else:
            kb.row(kb1, kb2, kb4)
        cap=('\u25ab\ufe0f'*(int(call.data.split()[-2])-1))+'\u25aa\ufe0f'+('\u25ab\ufe0f'*(cot-int(call.data.split()[-2])))+'    '+call.data.split()[-1]
        bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=types.InputMediaPhoto(i[0].split()[ts]))
        bot.edit_message_caption( chat_id=chat_id, message_id=call.message.message_id, caption=cap, reply_markup=kb)

    elif call.data.startswith('mget dislike'):
        bot.answer_callback_query(call.id)
        #del msg
        log=call.data.split()[-1]
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()

        curs.execute("SELECT like FROM auth WHERE log=?",(log,))
        io=curs.fetchone()[0]
        if io is not None:
            iy=io.split(', ')[0]
            ids=None
            if len(io.split(', '))>1:
                ids =io.replace(iy+ ', ','')
                curs.execute("SELECT photo FROM auth WHERE log=?",(iy,))
                i=curs.fetchone()
                cot=len(i[0].split())
                kb = types.InlineKeyboardMarkup(row_width=4)
                kb1=types.InlineKeyboardButton(text="\u274c", callback_data="mget dislike "+iy)
                kb4=types.InlineKeyboardButton(text="\u2709\ufe0f", callback_data="mget like "+iy)
                if cot>1:
                    kb2=types.InlineKeyboardButton(text="\ud83d\udd1c", callback_data="next "+'0 '+iy)
                    kb.add(kb1, kb2, kb4)
                else:
                    kb.add(kb1, kb4)
                kb.row_width=4
                cap='\u25aa\ufe0f'+'\u25ab\ufe0f'*(cot-1)+'    '+iy
                bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=types.InputMediaPhoto(i[0].split()[0]))
                bot.edit_message_caption( chat_id=chat_id, message_id=call.message.message_id, caption=cap, reply_markup=kb)
            else:
                bot.delete_message(chat_id,message_id=call.message.message_id)

            curs.execute("""UPDATE auth SET like=? WHERE log=?""", (ids,log))
            con.commit()
            
    elif call.data.startswith('mget like'):
        bot.answer_callback_query(call.id)
        #del msg
        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
        msg=curs.fetchall()
        for i in msg:
            try:
                bot.delete_message(chat_id,message_id=int(i[0]))
            except Exception as e:
                print(e)
        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
        con.commit()

        gt=call.data.split()[-1]
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('msg '+gt,chat_id))
        con.commit()
        ms=bot.send_message(chat_id, "Р’РІРµРґРёС‚Рµ СЃРѕРѕР±С‰РµРЅРёСЏ:")
        curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,ms.id))
        con.commit()
        curs.execute("SELECT like FROM auth WHERE log=?",(log,))
        io=curs.fetchone()[0]
        if io is not None:
            iy=io.split(', ')[0]
            ids=None
            if len(io.split(', '))>1:
                ids =io.replace(gt+ ', ','')
            curs.execute("""UPDATE auth SET like=? WHERE log=?""", (ids,log))
            con.commit()
        print(io)

    elif call.data.startswith('my'):
        bot.answer_callback_query(call.id)
        #del msg
##        curs.execute("SELECT msg FROM msgs WHERE user=(?)",(chat_id,))
##        msg=curs.fetchall()
##        for i in msg:
##            try:
##                bot.delete_message(chat_id,message_id=int(i[0]))
##            except Exception as e:
##                print(e)
##        curs.execute("DELETE FROM msgs WHERE user=?", (chat_id,))
##        con.commit()

        gt=call.data.split()[-1]
        curs.execute("""UPDATE users SET sts=? WHERE id=?""", ('msg '+gt,chat_id))
        con.commit()
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="Р’РІРµРґРёС‚Рµ СЃРѕРѕР±С‰РµРЅРёСЏ:")
        curs.execute("SELECT user,msg FROM message WHERE user=? or user=?",(log+' '+gt,gt+' '+log))
        msg=curs.fetchall()
        ms=call.message
        ge="РћРЅ: "
        curs.execute("SELECT gen FROM auth WHERE log=?",(gt,))
        gx=curs.fetchone()
        if gx[0]=='girl':
            ge="РћРЅР°: "
        for i in msg:
            gy=ge
            if i[0]==log+' '+gt:
                gy="Р’С‹: "

            if not i[1].startswith('%%'):
                if i[1].startswith('f%%'):
                    ms=bot.send_message(chat_id, gy+i[1][1:])
                else:
                    ms=bot.send_message(chat_id, gy+i[1])
            elif i[1].startswith('%%ph'):
                ms=bot.send_photo(chat_id=chat_id, photo=i[1][4:], caption=gy)
            elif i[1].startswith('%%vd'):
                ms=bot.send_video(chat_id=chat_id, video=i[1][4:], caption=gy)

            curs.execute("INSERT INTO msgs VALUES(?, ?)", (chat_id,ms.id))
            con.commit()

    elif call.data=='del':
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(chat_id,message_id=call.message.id)
        except Exception as e:
            print(e)

    elif call.data.startswith('bas'):
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(chat_id,message_id=call.message.id)
        except Exception as e:
            print(e)
        curs.execute("DELETE FROM message WHERE user=? or user=?",(str(call.data.split()[-1])+' '+log,log+' '+str(call.data.split()[-1])))
        con.commit()
        curs.execute("""UPDATE users SET sts=? WHERE log=? and sts=?""", ('main',call.data.split()[-1],'msg '+log))
        con.commit()





bot.infinity_polling()
