import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandBuilder, MessageHandler, filters, ContextTypes

# ---------- Генерация случайных данных ----------
MALE_NAMES = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Иван", "Артём", "Никита", "Роман"]
FEMALE_NAMES = ["Анна", "Мария", "Елена", "Ольга", "Наталья", "Татьяна", "Ирина", "Юлия", "Анастасия", "Ксения"]
LAST_NAMES = ["Иванов", "Петров", "Смирнов", "Кузнецов", "Васильев", "Попов", "Новиков", "Морозов", "Фёдоров", "Волков"]
CITIES = [{"city":"Москва","streets":["Ленинский просп.","Тверская ул.","Арбат"]},
          {"city":"СПб","streets":["Невский просп.","Лиговский просп.","Садовая ул."]}]
CAR_MODELS = ["Toyota Camry","BMW 5","Kia Rio","Hyundai Solaris","VW Polo","Lada Vesta"]

def pick(arr): return random.choice(arr)
def rand(a,b): return random.randint(a,b)

def gen_name():
    is_male = random.random()>0.45
    first = pick(MALE_NAMES if is_male else FEMALE_NAMES)
    last = pick(LAST_NAMES)
    patr = pick(["Александрович","Дмитриевич","Сергеевич","Алексеевич","Андреевич"] if is_male else ["Александровна","Дмитриевна","Сергеевна","Алексеевна"])
    return f"{last} {first} {patr}"

def gen_birth(): return f"{rand(1,28):02d}.{rand(1,12):02d}.{rand(1975,2005)}"
def gen_passport():
    s = rand(1000,9999); n = rand(100000,999999)
    d = f"{rand(1,28):02d}.{rand(1,12):02d}.{rand(2010,2023)}"
    dept = pick(["ГУ МВД Москвы","УМВД Краснодар","ОМВД Хамовники","УФМС СПб"])
    return f"{s} №{n}, выдан {d} {dept}"
def gen_snils():
    d = ''.join(str(rand(0,9)) for _ in range(11))
    return f"{d[0:3]}-{d[3:6]}-{d[6:9]} {d[9:11]}"
def gen_address():
    loc = pick(CITIES); st = pick(loc["streets"])
    h = rand(1,150); apt = rand(1,200); zipc = rand(100000,199999)
    return f"{zipc}, г.{loc['city']}, {st}, д.{h}, кв.{apt}"
def gen_car():
    car = pick(CAR_MODELS); l="АВЕКМНОРСТУХ"
    plate = f"{pick(l)}{rand(100,999)}{pick(l)}{pick(l)} {rand(1,799)}"
    return f"{car} (гос.номер: {plate})"
def gen_ip(): return f"{rand(10,223)}.{rand(0,255)}.{rand(0,255)}.{rand(1,254)}"
def gen_phone(): return f"+7 (9{rand(10,99)}) {rand(100,999)}-{rand(10,99)}-{rand(10,99)}"
def gen_email():
    letters = "abcdefghijklmnopqrstuvwxyz"
    login = ''.join(pick(letters) for _ in range(rand(5,8)))
    return f"{login}@{pick(['mail.ru','gmail.com','yandex.ru','bk.ru'])}"

def get_all():
    name = gen_name()
    return (f"👤 ФИО: {name}\n"
            f"📅 Дата рождения: {gen_birth()}\n"
            f"📘 Паспорт: {gen_passport()}\n"
            f"📗 СНИЛС: {gen_snils()}\n"
            f"🏠 Адрес: {gen_address()}\n"
            f"🚗 Авто: {gen_car()}\n"
            f"🌐 IP: {gen_ip()}\n"
            f"📞 Тел: {gen_phone()}\n"
            f"✉️ Email: {gen_email()}")

# ---------- Обработчики ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Пришли @username, я сгенерирую случайные данные.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lstrip('@')
    if not text:
        await update.message.reply_text("Пожалуйста, пришли @username")
        return

    msg = await update.message.reply_text("🔎 Начинаю поиск...")
    duration = random.randint(25, 35)
    total_steps = 20
    step_time = duration / total_steps

    for i in range(1, total_steps+1):
        percent = i * 100 // total_steps
        bar = "█" * (percent//5) + "░" * (20 - percent//5)
        if percent < 30: status = "Подключение к базам..."
        elif percent < 60: status = "Сбор цифрового следа..."
        elif percent < 90: status = "Формирование досье..."
        else: status = "Завершение..."
        try:
            await msg.edit_text(f"🔎 Поиск...\n[{bar}] {percent}%\n{status}")
        except:
            pass
        await asyncio.sleep(step_time)

    result = get_all()
    
    await msg.edit_text(f"📁 *Данные найдены:*\n\n{result}{disclaimer}", parse_mode="Markdown")

def main():
    TOKEN = "8668419847:AAHh5pO90I8LKPkh-SF8Ty38ntZOt9NJB2M"   # ← замените на токен от BotFather
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandBuilder("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
