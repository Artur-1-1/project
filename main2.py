""""
import telebot

TOKEN = '7237082682:AAF2OxYfftKvVIbg_Nc7tCJCV62AVSA01FU'  # Вставте токен, який надіслав BotFather
bot = telebot.TeleBot(TOKEN)

chat_id = 5064742315  # Введи ID чату (@userinfobot)

def convert_unit(value, from_units, to_units):
    conversions = {
        "сантиметр": {"міліметри": 10},
        "дициметр": {"міліметри": 100},
        "метр": {"міліметри": 1000},
        "кілометр": {"міліметри": 1000000},
        "літр": {"мілілітри": 1000},
        "кілограм": {"грами": 1000},
        "центнер": {"грами": 100000},
        "тонна": {"грами": 1000000}
    }
    
    if from_units in conversions and to_units in conversions[from_units]:
        return value * conversions[from_units][to_units]
    else:
        return None

@bot.message_handler(commands=["start"])
def send_hello(message):
    bot.send_message(message.chat.id, "Привіт мій маленький друже! Я допоможу тобі вивчити - кількість міліметрів, мілілітрів і грам в більших величинах.\n"
                                      "Напиши в такому форматі: 5 метр в міліметри.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    try:
        parts = text.split(" в ")
        value_and_from_unit = parts[0].split()
        to_unit = parts[1]

        value = float(value_and_from_unit[0])
        from_unit = " ".join(value_and_from_unit[1:])

        result = convert_unit(value, from_unit, to_unit)
        if result is not None:
            bot.send_message(message.chat.id, f"{value} {from_unit} = {result:.2f} {to_unit}")
        else:
            bot.send_message(message.chat.id, "Не можу конвертувати, спробуйте ще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, "Все погано, у тебе помилка в коді.")

bot.polling()


import random
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7237082682:AAF2OxYfftKvVIbg_Nc7tCJCV62AVSA01FU"
bot = telebot.TeleBot(TOKEN)

ssp2 = ["Камінь","Ножиці", "Папір"]
ssp = {"Камінь" : "Ножиці", "Ножиці" : "Папір", "Папір" : "Камінь"}

r = 0
n = 0

@bot.message_handler(commands=['start'])
def send_wellcome(message):
    bot.send_message(message.chat.id, "Привіт, я бот 'Камінь, Ножиці, Папір'")
# Команда /start
@bot.message_handler(commands=['play'])
def send_game(message):
    # Створення клавіатури
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Камінь")
    button2 = KeyboardButton("Ножиці")
    button3 = KeyboardButton("Папір")
    keyboard.add(button1, button2, button3)

    # Надсилання повідомлення з кнопками
    bot.send_message(message.chat.id, "Гра почалась!\nВибери: камінь, ножиці чи папір!", reply_markup=keyboard)

@bot.message_handler(commands=["result"])
def send_message(message):
    bot.send_message(message.chat.id, f"Ти виграв {r} разів з {n} раундів!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text in ssp2:
        answer = random.choice(ssp2)
        if message.text in ssp and answer in ssp[message.text]:
            global r
            global n
            r += 1
            n += 1
        else:
            n += 1
        bot.send_message(message.chat.id, f"{answer}")


bot.polling()



import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Рух об'єкта за допомогою стрілочок")

rect_position = pygame.math.Vector2(100, 100)
object_size = 100
object_color = (0, 0, 255)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect_position.x -= 50
            elif event.key == pygame.K_RIGHT:
                rect_position.x += 50
                

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, object_color, (rect_position.x, rect_position.y, object_size, object_size))
    pygame.display.flip()

pygame.quit()"""


import random
import pygame

pygame.init()
screen = pygame.display.set_mode((608, 605))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
background_img = pygame.image.load("snakeboard.png")

font = pygame.font.Font(None, 40)
position = []
n = pygame.Vector2(1, 0)
R = 16
g = 20
s = 0

def random_position(trail):
    trail_c = [(rect.x, rect.y) for rect in trail]
    while True:
        x = random.randint(1,17) * 32
        y = random.randint(4,15) * 32
        if (x, y) not in trail_c:
            return x, y
cirlce_x, cirlce_y = random_position(position)

barier1 = pygame.Rect(0, 64, 31, 537)
barier2 = pygame.Rect(30, 64, 608, 31)
barier3 = pygame.Rect(577, 64, 608, 537)
barier4 = pygame.Rect(0, 580, 608, 580)
rect = pygame.Rect(32, 96, 32, 32)
rect_position = pygame.math.Vector2(32, 96)
Object_size = 32
object_color = (0, 70, 255)

running = True
while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and n.y != 1:
            n = pygame.Vector2(0, -1)
            rect_position.x += 32
        elif keys[pygame.K_DOWN] and n.y != -1:
            n = pygame.Vector2(0, 1)
            rect_position.x -= 32
        elif keys[pygame.K_LEFT] and n.x != 1:
            n = pygame.Vector2(-1, 0)
            rect_position.y += 32
        elif keys[pygame.K_RIGHT] and n.x != -1:
            n = pygame.Vector2(1, 0)
            rect_position.y -= 32

    rect.x += int(n.x * 32)
    rect.y += int(n.y * 32)

    position.append(rect.copy())
    if len(position) > g:
        position.pop(0)
    
    # Якщо прямокутник доторкнувся до будь-якої тіні
    for i in range(len(position) - 1):  # останній — це сам прямокутник, його не перевіряємо
        if rect.colliderect(position[i]):
            running = False

    if (rect.x, rect.y) in position:
        running = False
    
    if rect.collidepoint(cirlce_x + 16, cirlce_y + 16):
        cirlce_x, cirlce_y = random_position(position)
        g += 1
        s += 1
          # нова позиція круга
    score = font.render(f"{s}", True, (255, 255, 255))
    screen.blit(score, (64, 30))

    if rect.colliderect(barier1) or rect.colliderect(barier2) or rect.colliderect(barier3) or rect.colliderect(barier4):
        pygame.quit()
        exit()

    for i, trail in enumerate(position):
        pygame.draw.rect(screen, (50, 100, 255), trail)   
    pygame.draw.rect(screen, (0, 70, 255), rect)
    pygame.draw.circle(screen, (255, 90, 40), (cirlce_x + 16, cirlce_y + 16), R)
    pygame.display.flip()
    clock.tick(7)
    


#мені треба:рандоомне число на x і y ,міняти кооринати
