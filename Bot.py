
import telebot
from telebot import types
import sqlite3
import datetime
import random
import string

TOKEN = "8692003062:AAHU0n6yX39LNt-NgdNQXubpVf1RvXEqWqk"
ADMIN_ID = 7879820766

bot = telebot.TeleBot(TOKEN)

def db():
    return sqlite3.connect('mlbot.db')

def setup():
    conn = db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS akun (id INTEGER PRIMARY KEY AUTOINCREMENT, penjual_id INTEGER, penjual_nama TEXT, rank TEXT, hero INTEGER, skin INTEGER, harga INTEGER, info TEXT, status TEXT, tgl TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS trx (id INTEGER PRIMARY KEY AUTOINCREMENT, trx_id TEXT, buyer_id INTEGER, buyer_nama TEXT, seller_id INTEGER, akun_id INTEGER, harga INTEGER, status TEXT, tgl TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS banned (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, tgl TEXT)''')
    conn.commit()
    conn.close()

setup()

def buat_trx():
    return "TRX" + ''.join(random.choices(string.digits, k=8))

def is_banned(uid):
    conn = db()
    c = conn.cursor()
    c.execute("SELECT id FROM banned WHERE user_id=?", (uid,))
    r = c.fetchone()
    conn.close()
    return r is not None

def menu(uid):
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(types.KeyboardButton("🏪 Katalog"), types.KeyboardButton("💰 Jual Akun"))
    m.row(types.KeyboardButton("📋 Transaksi"), types.KeyboardButton("👤 Profil"))
    m.row(types.KeyboardButton("⭐ Testimoni"), types.KeyboardButton("📞 CS"))
    if uid == ADMIN_ID:
        m.row(types.KeyboardButton("👑 Admin Panel"))
    return m

state = {}

@bot.message_handler(commands=['start'])
def start(msg):
    if is_banned(msg.from_user.id):
        bot.reply_to(msg, "🚫 Akun dibanned! Hubungi CS.")
        return
    bot.reply_to(msg,
        "⚔️ ML ACCOUNT STORE ⚔️\n"
        "━━━━━━━━━━━━━━━\n"
        "👋 Halo " + msg.from_user.first_name + "!\n\n"
        "✅ Rekber Otomatis\n"
        "✅ Garansi 24 Jam\n"
        "✅ Anti Penipuan\n"
        "✅ Proses Cepat\n"
        "━━━━━━━━━━━━━━━\n"
        "Pilih menu di bawah!",
        reply_markup=menu(msg.from_user.id))

@bot.message_handler(commands=['id'])
def get_id(msg):
    bot.reply_to(msg, "🆔 ID kamu: " + str(msg.from_user.id))

@bot.message_handler(func=lambda m: m.text == "🏪 Katalog")
def katalog(msg):
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM akun WHERE status='tersedia'")
    list_akun = c.fetchall()
    conn.close()
    if not list_akun:
        bot.reply_to(msg, "🏪 KATALOG AKUN ML\n━━━━━━━━━━━━━━━\n📭 Belum ada akun!\nTitipkan akun kamu!", reply_markup=menu(msg.from_user.id))
        return
    teks = "🏪 KATALOG AKUN ML\n━━━━━━━━━━━━━━━\n\n"
    for a in list_akun:
        teks += "🆔 ID    : #" + str(a[0]) + "\n"
        teks += "⚔️ Rank  : " + str(a[3]) + "\n"
        teks += "🦸 Hero  : " + str(a[4]) + " hero\n"
        teks += "✨ Skin  : " + str(a[5]) + " skin\n"
        teks += "💰 Harga : Rp " + str(a[6]) + "\n"
        teks += "📝 Info  : " + str(a[7]) + "\n"
        teks += "━━━━━━━━━━━━━━━\n\n"
    teks += "Beli? Ketik /beli [ID]\nContoh: /beli 1"
    bot.reply_to(msg, teks, reply_markup=menu(msg.from_user.id))

@bot.message_handler(func=lambda m: m.text == "💰 Jual Akun")
def jual(msg):
    if is_banned(msg.from_user.id):
        bot.reply_to(msg, "🚫 Akun dibanned!")
        return
    state[msg.from_user.id] = {'step': 'rank'}
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(types.KeyboardButton("Master"), types.KeyboardButton("Grandmaster"))
    m.row(types.KeyboardButton("Epic"), types.KeyboardButton("Legend"))
    m.row(types.KeyboardButton("Mythic"), types.KeyboardButton("Mythical Honor"))
    m.row(types.KeyboardButton("Mythical Glory"), types.KeyboardButton("Mythical Immortal"))
    m.row(types.KeyboardButton("❌ Batal"))
    bot.reply_to(msg, "💰 FORM JUAL AKUN ML\n━━━━━━━━━━━━━━━\n📊 Step 1/6\nPilih rank:", reply_markup=m)

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'rank')
def step_rank(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    valid = ["Master","Grandmaster","Epic","Legend","Mythic","Mythical Honor","Mythical Glory","Mythical Immortal"]
    if msg.text not in valid:
        bot.reply_to(msg, "⚠️ Pilih rank yang tersedia!")
        return
    state[msg.from_user.id]['rank'] = msg.text
    if msg.text == "Master":
        state[msg.from_user.id]['step'] = 'divisi'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("Master I"), types.KeyboardButton("Master II"))
        m.row(types.KeyboardButton("Master III"), types.KeyboardButton("Master IV"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Master\n📊 Step 2/6\nPilih Divisi:", reply_markup=m)
    elif msg.text == "Grandmaster":
        state[msg.from_user.id]['step'] = 'divisi'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("GM I"), types.KeyboardButton("GM II"))
        m.row(types.KeyboardButton("GM III"), types.KeyboardButton("GM IV"))
        m.row(types.KeyboardButton("GM V"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Grandmaster\n📊 Step 2/6\nPilih Divisi:", reply_markup=m)
    elif msg.text == "Epic":
        state[msg.from_user.id]['step'] = 'divisi'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("Epic I"), types.KeyboardButton("Epic II"))
        m.row(types.KeyboardButton("Epic III"), types.KeyboardButton("Epic IV"))
        m.row(types.KeyboardButton("Epic V"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Epic\n📊 Step 2/6\nPilih Divisi:", reply_markup=m)
    elif msg.text == "Legend":
        state[msg.from_user.id]['step'] = 'divisi'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("Legend I"), types.KeyboardButton("Legend II"))
        m.row(types.KeyboardButton("Legend III"), types.KeyboardButton("Legend IV"))
        m.row(types.KeyboardButton("Legend V"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Legend\n📊 Step 2/6\nPilih Divisi:", reply_markup=m)
    elif msg.text == "Mythic":
        state[msg.from_user.id]['step'] = 'bintang'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("1-5 bintang"), types.KeyboardButton("6-10 bintang"))
        m.row(types.KeyboardButton("11-15 bintang"), types.KeyboardButton("16-20 bintang"))
        m.row(types.KeyboardButton("21-25 bintang"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Mythic\n📊 Step 2/6\n⭐ Pilih range bintang:", reply_markup=m)
    elif msg.text == "Mythical Honor":
        state[msg.from_user.id]['step'] = 'bintang'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("25-30 bintang"), types.KeyboardButton("31-40 bintang"))
        m.row(types.KeyboardButton("41-50 bintang"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Mythical Honor\n📊 Step 2/6\n⭐ Pilih range bintang:", reply_markup=m)
    elif msg.text == "Mythical Glory":
        state[msg.from_user.id]['step'] = 'bintang'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("50-60 bintang"), types.KeyboardButton("61-70 bintang"))
        m.row(types.KeyboardButton("71-80 bintang"), types.KeyboardButton("81-90 bintang"))
        m.row(types.KeyboardButton("91-100 bintang"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Mythical Glory\n📊 Step 2/6\n⭐ Pilih range bintang:", reply_markup=m)
    elif msg.text == "Mythical Immortal":
        state[msg.from_user.id]['step'] = 'bintang'
        m = types.ReplyKeyboardMarkup(resize_keyboard=True)
        m.row(types.KeyboardButton("100-150 bintang"), types.KeyboardButton("151-200 bintang"))
        m.row(types.KeyboardButton("201-300 bintang"), types.KeyboardButton("300+ bintang"))
        m.row(types.KeyboardButton("❌ Batal"))
        bot.reply_to(msg, "✅ Rank: Mythical Immortal\n📊 Step 2/6\n⭐ Pilih range bintang:", reply_markup=m)

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'divisi')
def step_divisi(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    state[msg.from_user.id]['divisi'] = msg.text
    state[msg.from_user.id]['step'] = 'bintang'
    rank = state[msg.from_user.id]['rank']
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if rank == "Master":
        m.row(types.KeyboardButton("1 bintang"), types.KeyboardButton("2 bintang"))
        m.row(types.KeyboardButton("3 bintang"), types.KeyboardButton("4 bintang"))
    else:
        m.row(types.KeyboardButton("1 bintang"), types.KeyboardButton("2 bintang"))
        m.row(types.KeyboardButton("3 bintang"), types.KeyboardButton("4 bintang"))
        m.row(types.KeyboardButton("5 bintang"))
    m.row(types.KeyboardButton("❌ Batal"))
    bot.reply_to(msg, "✅ Divisi: " + msg.text + "\n📊 Step 3/6\n⭐ Pilih jumlah bintang:", reply_markup=m)

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'bintang')
def step_bintang(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    state[msg.from_user.id]['bintang'] = msg.text
    state[msg.from_user.id]['step'] = 'hero'
    rank = state[msg.from_user.id]['rank']
    divisi = state[msg.from_user.id].get('divisi', '')
    if divisi:
        rank_full = divisi + " " + msg.text
    else:
        rank_full = rank + " " + msg.text
    state[msg.from_user.id]['rank_full'] = rank_full
    m = types.ReplyKeyboardMarkup(resize_keyboard=True)
    m.row(types.KeyboardButton("❌ Batal"))
    bot.reply_to(msg, "✅ Rank: " + rank_full + "\n📊 Step 4/6\n🦸 Jumlah hero? (ketik angka)", reply_markup=m)

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'hero')
def step_hero(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    try:
        hero = int(msg.text)
        if hero < 1 or hero > 132:
            raise ValueError
    except:
        bot.reply_to(msg, "⚠️ Masukkan angka 1-132!")
        return
    state[msg.from_user.id]['hero'] = hero
    state[msg.from_user.id]['step'] = 'skin'
    bot.reply_to(msg, "✅ Hero: " + str(hero) + "\n📊 Step 5/6\n✨ Jumlah skin? (ketik angka)")

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'skin')
def step_skin(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    try:
        skin = int(msg.text)
        if skin < 0 or skin > 500:
            raise ValueError
    except:
        bot.reply_to(msg, "⚠️ Masukkan angka yang valid!")
        return
    state[msg.from_user.id]['skin'] = skin
    state[msg.from_user.id]['step'] = 'harga'
    bot.reply_to(msg, "✅ Skin: " + str(skin) + "\n📊 Step 6/6\n💰 Harga jual? (Rupiah)\nContoh: 500000")

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'harga')
def step_harga(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    try:
        harga = int(msg.text)
        if harga < 10000:
            bot.reply_to(msg, "⚠️ Harga minimal Rp 10.000!")
            return
    except:
        bot.reply_to(msg, "⚠️ Masukkan angka!")
        return
    state[msg.from_user.id]['harga'] = harga
    state[msg.from_user.id]['step'] = 'info'
    bot.reply_to(msg, "✅ Harga: Rp " + str(harga) + "\n📝 Tulis deskripsi akun!\nContoh: Akun sultan, hero lengkap!")

@bot.message_handler(func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'info')
def step_info(msg):
    if msg.text == "❌ Batal":
        state.pop(msg.from_user.id, None)
        bot.reply_to(msg, "❌ Dibatalkan!", reply_markup=menu(msg.from_user.id))
        return
    data = state[msg.from_user.id]
    data['info'] = msg.text
    data['step'] = 'done'
    rank_full = data.get('rank_full', data.get('rank', ''))
    mk = types.InlineKeyboardMarkup()
    mk.row(types.InlineKeyboardButton("✅ Submit", callback_data="submit_jual"), types.InlineKeyboardButton("❌ Batal", callback_data="batal_jual"))
    bot.reply_to(msg,
        "📋 KONFIRMASI AKUN\n━━━━━━━━━━━━━━━\n"
        "⚔️ Rank  : " + rank_full + "\n"
        "🦸 Hero  : " + str(data['hero']) + " hero\n"
        "✨ Skin  : " + str(data['skin']) + " skin\n"
        "💰 Harga : Rp " + str(data['harga']) + "\n"
        "📝 Info  : " + str(data['info']) + "\n"
        "━━━━━━━━━━━━━━━\nData sudah benar?",
        reply_markup=mk)

@bot.callback_query_handler(func=lambda c: True)
def callback(call):
    uid = call.from_user.id
    nama = call.from_user.first_name
    if call.data == "submit_jual":
        if uid not in state:
            bot.answer_callback_query(call.id, "Session habis!")
            return
        data = state[uid]
        rank_full = data.get('rank_full', data.get('rank', ''))
        tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = db()
        c = conn.cursor()
        c.execute("INSERT INTO akun VALUES (NULL,?,?,?,?,?,?,?,?,?)", (uid, nama, rank_full, data['hero'], data['skin'], data['harga'], data['info'], 'menunggu_verifikasi', tgl))
        akun_id = c.lastrowid
        conn.commit()
        conn.close()
        state.pop(uid, None)
        bot.edit_message_text("✅ Akun disubmit!\nMenunggu verifikasi\nID: #" + str(akun_id), call.message.chat.id, call.message.message_id)
        if ADMIN_ID != 0:
            bot.send_message(ADMIN_ID, "📦 Akun baru!\nID: #" + str(akun_id) + "\nPenjual: " + nama + "\nRank: " + rank_full + "\nHero: " + str(data['hero']) + "\nSkin: " + str(data['skin']) + "\nHarga: Rp " + str(data['harga']) + "\n/verif " + str(akun_id) + "\n/tolak " + str(akun_id))
        bot.send_message(uid, "Kembali ke menu!", reply_markup=menu(uid))
    elif call.data == "batal_jual":
        state.pop(uid, None)
        bot.edit_message_text("❌ Dibatalkan!", call.message.chat.id, call.message.message_id)
        bot.send_message(uid, "Kembali ke menu!", reply_markup=menu(uid))
    elif call.data.startswith("beli_"):
        akun_id = int(call.data.split("_")[1])
        conn = db()
        c = conn.cursor()
        c.execute("SELECT * FROM akun WHERE id=? AND status='tersedia'", (akun_id,))
        akun = c.fetchone()
        conn.close()
        if not akun:
            bot.answer_callback_query(call.id, "Akun tidak tersedia!")
            return
        tid = buat_trx()
        tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = db()
        c = conn.cursor()
        c.execute("INSERT INTO trx VALUES (NULL,?,?,?,?,?,?,?,?)", (tid, uid, nama, akun[1], akun_id, akun[6], 'menunggu_bayar', tgl))
        c.execute("UPDATE akun SET status='pending' WHERE id=?", (akun_id,))
        conn.commit()
        conn.close()
        bot.edit_message_text("🛒 STRUK ORDER\n━━━━━━━━━━━━━━━\n🆔 ID: " + tid + "\n⚔️ Akun: #" + str(akun_id) + " " + str(akun[3]) + "\n💰 Harga: Rp " + str(akun[6]) + "\n━━━━━━━━━━━━━━━\n💳 Transfer ke:\nDANA: 085649642594\nBCA: 1234567890\n━━━━━━━━━━━━━━━\nSetelah transfer ketik:\n/bayar " + tid, call.message.chat.id, call.message.message_id)
        if ADMIN_ID != 0:
            bot.send_message(ADMIN_ID, "🔔 Ada pembeli!\nID: " + tid + "\nPembeli: " + nama + "\nAkun: #" + str(akun_id) + "\nHarga: Rp " + str(akun[6]))
    elif call.data.startswith("oke_"):
        tid = call.data.split("_")[1]
        conn = db()
        c = conn.cursor()
        c.execute("UPDATE trx SET status='selesai' WHERE trx_id=?", (tid,))
        conn.commit()
        conn.close()
        bot.edit_message_text("✅ Transaksi Selesai!\nID: " + tid + "\nTerima kasih!", call.message.chat.id, call.message.message_id)
        if ADMIN_ID != 0:
            bot.send_message(ADMIN_ID, "✅ Transaksi " + tid + " selesai!")
    elif call.data.startswith("masalah_"):
        tid = call.data.split("_")[1]
        conn = db()
        c = conn.cursor()
        c.execute("UPDATE trx SET status='dispute' WHERE trx_id=?", (tid,))
        conn.commit()
        conn.close()
        bot.edit_message_text("⚠️ Laporan diterima!\nID: " + tid + "\nAdmin investigasi 1x24 jam!", call.message.chat.id, call.message.message_id)
        if ADMIN_ID != 0:
            bot.send_message(ADMIN_ID, "🚨 DISPUTE!\nTransaksi: " + tid + "\nSegera investigasi!")

@bot.message_handler(commands=['beli'])
def beli(msg):
    try:
        akun_id = int(msg.text.split()[1])
    except:
        bot.reply_to(msg, "⚠️ Format: /beli [ID]\nContoh: /beli 1")
        return
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM akun WHERE id=? AND status='tersedia'", (akun_id,))
    akun = c.fetchone()
    conn.close()
    if not akun:
        bot.reply_to(msg, "❌ Akun tidak ditemukan!")
        return
    if msg.from_user.id == akun[1]:
        bot.reply_to(msg, "❌ Tidak bisa beli akun sendiri!")
        return
    mk = types.InlineKeyboardMarkup()
    mk.row(types.InlineKeyboardButton("✅ Lanjut Beli", callback_data="beli_" + str(akun_id)), types.InlineKeyboardButton("❌ Batal", callback_data="batal"))
    bot.reply_to(msg, "🎮 DETAIL AKUN ML\n━━━━━━━━━━━━━━━\n⚔️ Rank  : " + str(akun[3]) + "\n🦸 Hero  : " + str(akun[4]) + " hero\n✨ Skin  : " + str(akun[5]) + " skin\n💰 Harga : Rp " + str(akun[6]) + "\n📝 Info  : " + str(akun[7]) + "\n━━━━━━━━━━━━━━━\nLanjutkan pembelian?", reply_markup=mk)

@bot.message_handler(commands=['bayar'])
def bayar(msg):
    try:
        tid = msg.text.split()[1]
    except:
        bot.reply_to(msg, "⚠️ Format: /bayar [ID Transaksi]")
        return
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM trx WHERE trx_id=? AND buyer_id=?", (tid, msg.from_user.id))
    trx = c.fetchone()
    conn.close()
    if not trx:
        bot.reply_to(msg, "❌ Transaksi tidak ditemukan!")
        return
    state[msg.from_user.id] = {'step': 'bukti', 'trx_id': tid}
    bot.reply_to(msg, "💳 KONFIRMASI BAYAR\n━━━━━━━━━━━━━━━\n🆔 ID: " + tid + "\n💰 Harga: Rp " + str(trx[6]) + "\n━━━━━━━━━━━━━━━\n📸 Kirim foto bukti transfer!")

@bot.message_handler(content_types=['photo'], func=lambda m: m.from_user.id in state and state[m.from_user.id].get('step') == 'bukti')
def bukti(msg):
    tid = state[msg.from_user.id]['trx_id']
    nama = msg.from_user.first_name
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM trx WHERE trx_id=?", (tid,))
    trx = c.fetchone()
    c.execute("UPDATE trx SET status='menunggu_admin' WHERE trx_id=?", (tid,))
    conn.commit()
    conn.close()
    state.pop(msg.from_user.id, None)
    bot.reply_to(msg, "✅ Bukti diterima!\n🆔 ID: " + tid + "\nMenunggu konfirmasi admin!", reply_markup=menu(msg.from_user.id))
    if ADMIN_ID != 0:
        foto_id = msg.photo[-1].file_id
        bot.send_photo(ADMIN_ID, foto_id, caption="💳 Bukti Bayar!\n🆔 ID: " + tid + "\n👤 Pembeli: " + nama + "\n💰 Harga: Rp " + str(trx[6]) + "\nKetik /konfirm " + tid)

@bot.message_handler(func=lambda m: m.text == "👑 Admin Panel")
def admin_panel(msg):
    if msg.from_user.id != ADMIN_ID:
        bot.reply_to(msg, "🚫 Bukan admin!")
        return
    conn = db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM akun WHERE status='tersedia'")
    stok = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM akun WHERE status='menunggu_verifikasi'")
    pending = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM trx WHERE status='menunggu_admin'")
    bayar_pending = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM trx WHERE status='selesai'")
    selesai = c.fetchone()[0]
    conn.close()
    bot.reply_to(msg, "👑 ADMIN PANEL\n━━━━━━━━━━━━━━━\n📦 Stok: " + str(stok) + "\n⏳ Pending: " + str(pending) + "\n💳 Bayar pending: " + str(bayar_pending) + "\n✅ Selesai: " + str(selesai) + "\n━━━━━━━━━━━━━━━\n/verif [ID]\n/tolak [ID]\n/konfirm [TRX]\n/kirim [TRX] [detail]\n/ban [ID]")

@bot.message_handler(commands=['verif'])
def verif(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        akun_id = int(msg.text.split()[1])
    except:
        bot.reply_to(msg, "⚠️ Format: /verif [ID]")
        return
    conn = db()
    c = conn.cursor()
    c.execute("UPDATE akun SET status='tersedia' WHERE id=?", (akun_id,))
    c.execute("SELECT penjual_id FROM akun WHERE id=?", (akun_id,))
    penjual = c.fetchone()
    conn.commit()
    conn.close()
    bot.reply_to(msg, "✅ Akun #" + str(akun_id) + " diverifikasi!")
    if penjual:
        bot.send_message(penjual[0], "✅ Akun kamu #" + str(akun_id) + " sudah di katalog!")

@bot.message_handler(commands=['tolak'])
def tolak(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        akun_id = int(msg.text.split()[1])
    except:
        bot.reply_to(msg, "⚠️ Format: /tolak [ID]")
        return
    conn = db()
    c = conn.cursor()
    c.execute("UPDATE akun SET status='ditolak' WHERE id=?", (akun_id,))
    c.execute("SELECT penjual_id FROM akun WHERE id=?", (akun_id,))
    penjual = c.fetchone()
    conn.commit()
    conn.close()
    bot.reply_to(msg, "❌ Akun #" + str(akun_id) + " ditolak!")
    if penjual:
        bot.send_message(penjual[0], "❌ Akun kamu #" + str(akun_id) + " ditolak!")

@bot.message_handler(commands=['konfirm'])
def konfirm(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        tid = msg.text.split()[1]
    except:
        bot.reply_to(msg, "⚠️ Format: /konfirm [TRX_ID]")
        return
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM trx WHERE trx_id=?", (tid,))
    trx = c.fetchone()
    if not trx:
        bot.reply_to(msg, "❌ Transaksi tidak ditemukan!")
        conn.close()
        return
    c.execute("UPDATE trx SET status='menunggu_akun' WHERE trx_id=?", (tid,))
    conn.commit()
    conn.close()
    bot.reply_to(msg, "✅ Bayar " + tid + " dikonfirmasi!\n/kirim " + tid + " [detail]")
    bot.send_message(trx[2], "✅ Pembayaran dikonfirmasi!\nID: " + tid + "\nAkun sedang disiapkan!")

@bot.message_handler(commands=['kirim'])
def kirim(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        parts = msg.text.split(None, 2)
        tid = parts[1]
        detail = parts[2]
    except:
        bot.reply_to(msg, "⚠️ Format:\n/kirim [TRX] [detail]")
        return
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM trx WHERE trx_id=?", (tid,))
    trx = c.fetchone()
    if not trx:
        bot.reply_to(msg, "❌ Transaksi tidak ditemukan!")
        conn.close()
        return
    c.execute("UPDATE trx SET status='akun_terkirim' WHERE trx_id=?", (tid,))
    conn.commit()
    conn.close()
    mk = types.InlineKeyboardMarkup()
    mk.row(types.InlineKeyboardButton("✅ Akun Oke!", callback_data="oke_" + tid), types.InlineKeyboardButton("❌ Ada Masalah", callback_data="masalah_" + tid))
    bot.send_message(trx[2], "🎮 Detail Akun ML!\n━━━━━━━━━━━━━━━\nID: " + tid + "\n━━━━━━━━━━━━━━━\n" + detail + "\n━━━━━━━━━━━━━━━\n⚠️ Segera ganti password!\nAkun sudah sesuai?", reply_markup=mk)
    bot.reply_to(msg, "✅ Detail akun terkirim!")

@bot.message_handler(commands=['ban'])
def ban(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    try:
        target = int(msg.text.split()[1])
    except:
        bot.reply_to(msg, "⚠️ Format: /ban [USER_ID]")
        return
    tgl = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = db()
    c = conn.cursor()
    c.execute("INSERT INTO banned VALUES (NULL,?,?)", (target, tgl))
    conn.commit()
    conn.close()
    bot.reply_to(msg, "🚫 User " + str(target) + " dibanned!")

@bot.message_handler(func=lambda m: m.text == "📋 Transaksi")
def transaksi(msg):
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM trx WHERE buyer_id=? ORDER BY id DESC LIMIT 5", (msg.from_user.id,))
    list_trx = c.fetchall()
    conn.close()
    if not list_trx:
        bot.reply_to(msg, "📋 Belum ada transaksi!", reply_markup=menu(msg.from_user.id))
        return
    teks = "📋 TRANSAKSI TERAKHIR\n━━━━━━━━━━━━━━━\n\n"
    for t in list_trx:
        teks += "🆔 ID: " + str(t[1]) + "\n💰 Harga: Rp " + str(t[6]) + "\n📊 Status: " + str(t[7]) + "\n━━━━━━━━━━━━━━━\n"
    bot.reply_to(msg, teks, reply_markup=menu(msg.from_user.id))

@bot.message_handler(func=lambda m: m.text == "👤 Profil")
def profil(msg):
    conn = db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM trx WHERE buyer_id=? AND status='selesai'", (msg.from_user.id,))
    beli = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM akun WHERE penjual_id=? AND status='terjual'", (msg.from_user.id,))
    jual = c.fetchone()[0]
    conn.close()
    bot.reply_to(msg, "👤 PROFIL KAMU\n━━━━━━━━━━━━━━━\n📛 Nama: " + msg.from_user.first_name + "\n🆔 ID: " + str(msg.from_user.id) + "\n━━━━━━━━━━━━━━━\n✅ Total Beli: " + str(beli) + "\n💰 Total Jual: " + str(jual), reply_markup=menu(msg.from_user.id))

@bot.message_handler(func=lambda m: m.text == "⭐ Testimoni")
def testimoni(msg):
    bot.reply_to(msg, "⭐ TESTIMONI\n━━━━━━━━━━━━━━━\nBudi - Akun sesuai!\nSari - Terpercaya!\nAndi - 3x beli aman!\n━━━━━━━━━━━━━━━\nJadilah pembeli berikutnya!", reply_markup=menu(msg.from_user.id))

@bot.message_handler(func=lambda m: m.text == "📞 CS")
def cs(msg):
    bot.reply_to(msg, "📞 CUSTOMER SERVICE\n━━━━━━━━━━━━━━━\n⏰ Jam: 08.00-22.00 WIB\n📱 Telegram: @FXT82828\n━━━━━━━━━━━━━━━\n🤖 Bot aktif 24 jam!", reply_markup=menu(msg.from_user.id))

bot.delete_webhook()
print("ML Store Bot aktif!")
print("Ketik /id untuk dapat ID admin!")
bot.polling(none_stop=True)
