import discord
from discord import app_commands
import asyncio
from typing import List
import mysql.connector
from datetime import datetime, time, timedelta
import youtube_dl
import random


WHEN = time(19, 37, 0)  # 27:31 PM
#WHEN = time(19, 58, 40)  # pisac -2h

con = mysql.connector.connect(
    host = "161.97.78.70",
    user = "u9583_ZO9IVWbHlf",
    password = "yDirH1xEenEczcWS==HI8X2n",
    database = "s9583_database",
    port = 3306
)
cur = con.cursor()

class aClient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = 772531463051804692))
            self.synced = True
        
        client.loop.create_task(background_task())
        
        print("Bot jest gotowy")
    
    async def on_message(self, message):
        #await client.process_commands(message)

        # FRIEND BOT
        if (message.author.id == 418838382270218250):
            emotki = ['👍🏻', '👌🏻', '🦄', '🤮', '🍑', '🔞', '🖕🏻', '🤷🏻‍♂️', '❤', '✅', '🔥', '🤦🏻‍♂️', '😐', '😂', '😏', '😎', '😘', '😇', '💩', '🤡', '🤔', '😢', '🙄', '🥶', '🥵', '🤙🏻', '👎🏻', '🫡', '🆗', '💯', '🤓']
            await message.add_reaction(random.choice(emotki))

        # BUMP COUNTER BOT
        elif (message.channel.id == 926874863099084830 and message.author.id == 302050872383242240 and "Podbito serwer!" in message.embeds[0].description):
            # and "Podbito serwer!" in message.embeds[0].description
            author_name = message.interaction.user.name
            author_id = message.interaction.user.id
            user = message.interaction.user
            guild = message.guild
            role = guild.get_role(926875607143448636)
            channel = client.get_channel(926874863099084830)
            cur.execute(f"SELECT * FROM members WHERE ID = '0'") #wybieranie max
            max_exist = cur.fetchone()
            #print(max_exist)
            if max_exist:
                max = max_exist[3]
            
            cur.execute(f"SELECT * FROM members WHERE ID = '{str(author_id)}'")
            id_exist = cur.fetchone()
            if id_exist: #jesli id już istnieje
                row = id_exist
                #print(row)
                bump = row[2] + 1
                cur.execute(f"UPDATE members SET NAME = '{author_name}', BUMP = '{bump}' WHERE ID = '{str(author_id)}'") #aktualizowanie nazwy i bumpów osoby
            
                if bump > max:  #jesli osoba przebila najwyzszy wynik
                    cur.execute(f"UPDATE members SET ROLE = '1' WHERE ID = '{str(author_id)}'")  #dodanie X
                    cur.execute(f"UPDATE members SET ROLE = '{bump}' WHERE ID = '0'")  #zaktualizowanie najwyzszej liczby
                    if role not in user.roles:
                        await user.add_roles(role)  #dodanie roli

                    message = f"<@{author_id}> zrobił **{bump}** bumpów i zabrał rolę od: "
                    z = 0
                    cur.execute("SELECT * FROM members WHERE ROLE = '1'")
                    rows = cur.fetchall()
                    for row in rows:
                        if row[0] != str(author_id) and row[0] != '0' and row[0] != author_id: #wszyscy oprócz max i nowego najlepszego
                            z += 1
                            cur.execute(f"UPDATE members SET ROLE = '0' WHERE ID = '{row[0]}'")  #Usunięcie wszystkich znaczników roli
                            if role in user.roles:
                                await guild.get_member(int(row[0])).remove_roles(role)  #usuwanie roli
                            message += f"<@{row[0]}> "

                    if z == 0:
                        await channel.send(f"<@{author_id}> zrobił **{bump}** bumpów i nadal jako jedyny ma odznakę bumpera")
                    else:
                        await channel.send(message)

                elif bump == max:
                    cur.execute(f"UPDATE members SET ROLE = '1' WHERE ID = '{str(author_id)}'")  #dodanie X
                    if role not in user.roles:
                        await user.add_roles(role)
                    await channel.send(f"<@{author_id}> zrobił **{bump}** bumpów i zdobył odznakę bumpera")
                else:
                    await channel.send(f"<@{author_id}> zrobił **{bump}** bumpów")

            else:
                cur.execute(f"INSERT INTO members (ID, NAME, BUMP, ROLE) VALUES ('{str(author_id)}', '{author_name}', '1', '0')") #dodanie uzytkownika

                #cur.execute(f"SELECT * FROM members WHERE ID = 0")
                #max_exist = cur.fetchone()
                #if not max_exist: #jesli id już istnieje
                if not max_exist:
                    cur.execute("INSERT INTO members (ID, ROLE) VALUES ('0', '1')") #dodanie max
                    max = 1

                if max == 1:
                    cur.execute(f"UPDATE members SET ROLE = '1' WHERE ID = '{str(author_id)}'")  #dodanie X
                    if role not in user.roles:
                        await user.add_roles(role)  #dodanie roli

                await channel.send(f"<@{author_id}> zrobił pierwszego bumpa")

            con.commit() #zapisanie zmian


client = aClient()
tree = app_commands.CommandTree(client)

"""@tree.command(name='test', description='Do testowania rzeczy', guild = discord.Object(id = 772531463051804692))
async def self(interaction: discord.Interaction, komenda: str):
    for category in interaction.guild.categories:
        print(category.name)"""



# RPG HELPER BOT
async def kategoria(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    choices = []
    for x in interaction.guild.categories:
        if x.name == 'Archiwum sesji':
            break
        elif x.name.lower() not in ['statystyki serwera', 'sprawy organizacyjne', 'kanały tekstowe', 'rpg', 'kanały głosowe']:
            choices.append(x.name)
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in choices if current.lower() in choice.lower()
    ]

@tree.command(name='kanał', description='Utworzenie nowego kanału', guild = discord.Object(id = 772531463051804692))
@app_commands.autocomplete(kategoria=kategoria)
        
async def self(interaction: discord.Interaction, nazwa_kanału: str, kategoria: str):
    role = discord.utils.get(interaction.guild.roles, id=780071975232995338)
    if role in interaction.user.roles:
        guild = interaction.guild
        category = discord.utils.get(interaction.guild.categories, name=kategoria)
        kanal = await guild.create_text_channel('_'.join(nazwa_kanału.split()), category = category)
        await interaction.response.send_message(f'Utworzono kanał: <#{kanal.id}>', ephemeral = True)
    else:
        await interaction.response.send_message('Nie masz roli Mistrz gry', ephemeral = True)


@tree.command(name='kampania', description='Edytowanie lub tworzenie roli kampanii i dodanie jej graczom', guild = discord.Object(id = 772531463051804692))
async def self(interaction: discord.Interaction, nazwa_kampanii: str, gracze: str, kolor: str = 'random'):
    if interaction.guild.get_role(780071975232995338) in interaction.user.roles:
        if kolor == "random":
            color = discord.Colour.random()
        elif ',' in kolor:
            try:
                color = discord.Colour.from_rgb(kolor)
            except:
                color = discord.Colour.random()
        else:
            try:
                color = discord.Colour.from_str(kolor)
            except:
                color = discord.Colour.random()

        if '@' in nazwa_kampanii: #jesli kampania jest oznaczona
            role = discord.utils.get(interaction.guild.roles, id=int(nazwa_kampanii[3:-1]))
            if kolor != 'random':
                try:
                    await role.edit(colour=color)
                except:
                    pass
            msg = 'Zaktualizowano kampanię'
        elif nazwa_kampanii in str(interaction.guild.roles): #jesli rola o takiej nazwie juz istnie
            role = discord.utils.get(interaction.guild.roles, name=nazwa_kampanii)
            if kolor != 'random':
                try:
                    await role.edit(colour=color)
                except:
                    pass
            msg = 'Zaktualizowano kampanię'
        else:
            role = await interaction.guild.create_role(name = nazwa_kampanii, mentionable=True, colour=color)
            msg = 'Utworzono kampanię'
              
        try:
            await interaction.user.add_roles(role)
        except:
            pass
      
        for player in gracze.split():
            player = interaction.guild.get_member(int(player[-19:-1]))
            try:
                await player.add_roles(role)
            except:
                msg += f'\n<@{player.id}>'
                print(f'nie dano roli {player.nick}')
        if '\n' in msg:
            msg += 'Nie dostali roli'
        await interaction.response.send_message(msg, ephemeral = True)
    else:
        await interaction.response.send_message('Nie masz roli Mistrz gry', ephemeral = True)


@tree.command(name='roll', description='Rzut kostką', guild = discord.Object(id = 772531463051804692))
async def self(interaction: discord.Interaction, komenda: str):
    if "d" in komenda:
        dice = komenda.split('d')
    elif "k" in komenda:
        dice = komenda.split('k')
    dice_number = int(dice[0])
    dice_value = int(dice[1])

    msg = ''
    add = 0
    for x in range(dice_number):
        r = random.randint(1, dice_value)
        msg += f'[{r}] '
        add += r
    if interaction.user.nick != None:
        await interaction.response.send_message(f'**{interaction.user.nick}** rzucił: `{msg}= {add}`')
    else:
        await interaction.response.send_message(f'**{interaction.user.name}** rzucił: `{msg}= {add}`')



# BUMP COUNTER BOT
@tree.command(name='max', description='Wyświetlanie i edytowanie najwyższej liczby bumpów', guild = discord.Object(id = 772531463051804692))
async def self(interaction: discord.Interaction, liczba: int = -1):
    cur.execute(f"SELECT * FROM members WHERE ID = '0'") #wybieranie max
    max_exist = cur.fetchone()
    if liczba == -1 and max_exist:
        max_bump = max_exist[3]

        cur.execute(f"SELECT * FROM members WHERE ROLE = '1'") #wybieranie wszystkich osób z rolą
        bumperzy = ''
        for row in cur.fetchall():
            if id != '0':
                bumperzy += f"<@{int(row[0])}> "
        await interaction.response.send_message(f"Najwięcej bumpów to **{max_bump}**, zrobione przez: {bumperzy}")
    
    elif liczba >= 0:
        if interaction.guild.get_role(867415999447040020) in interaction.user.roles:
            try:
                cur.execute(f"UPDATE members SET ROLE = '{liczba}' WHERE ID = '0'")  #zmiana max liczby
                await interaction.response.send_message(f"Zmieniono max na: **{liczba}**")
            except:
                pass
    con.commit() #zapisanie zmian


async def opcja(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name="add", value="add"),
        app_commands.Choice(name="delete", value="delete")
    ]

@tree.command(name='user', description='Zarządzanie użytkownikami', guild = discord.Object(id = 772531463051804692))
@app_commands.autocomplete(opcja=opcja)

async def self(interaction: discord.Interaction, osoba: str, opcja: str = 'default'):
    if '@' in osoba:
        osoba = osoba[-19:-1]
        cur.execute(f"SELECT * FROM members WHERE ID = '{osoba}'")
        row = cur.fetchone()
    else:
        row = None

    if osoba == 'all' and opcja == 'delete':
        if interaction.guild.get_role(867415999447040020) in interaction.user.roles:
            cur.execute("SELECT * FROM members WHERE ROLE = '1'")
            for key in cur.fetchall():
                role = interaction.guild.get_role(926875607143448636)
                user = interaction.guild.get_member(int(key[0]))
                if role in user.roles:
                    await user.remove_roles(role)
            cur.execute("DELETE FROM members WHERE ID <> '0'")
            await interaction.response.send_message("Usunięto wszystkich")
        else:
            await interaction.response.send_message("Nie jesteś imperatorem", ephemeral=True)
            
    elif row != None and opcja == 'add':
        if interaction.guild.get_role(867415999447040020) in interaction.user.roles:
            user = interaction.guild.get_member(int(osoba))
            role = interaction.guild.get_role(926875607143448636)

            cur.execute(f"INSERT INTO members (ID, NAME, BUMP) VALUES ('{osoba}', '{user.name}', '1')") #dodanie uzytkownika

            cur.execute(f"SELECT * FROM members WHERE ID = '0'") #wybieranie max
            max_exist = cur.fetchone()
            if max_exist and max_exist[3] == 1:
                cur.execute(f"UPDATE members SET ROLE = '1' WHERE ID = '{osoba}'")  #dodanie X
                if interaction.guild.get_role(926875607143448636) not in user.roles:
                    await user.add_roles(role)
                
            await interaction.response.send_message(f"Dodano użytkownika **{user.name}**")
        else:
            await interaction.response.send_message("Nie jesteś imperatorem", ephemeral=True)
            
    elif osoba == 'all':
        message = ''
        cur.execute(f"SELECT * FROM members WHERE ID <> '0'") #wybieranie wszystkich poza max
        rows = cur.fetchall()
        for row in rows:
            user_name = row[1]
            user_number = row[2]
            for x in range(5 - len(str(user_number))):
                user_number = " " + str(user_number)
            if row[3] == 1:
                have_role = "X"
            else:
                have_role = " "
            message += f"| `{user_number}` | `{have_role}` | `{user_name}` |\n"
        await interaction.response.send_message(message)
        
    elif row != None:
        user_id = row[0]
        user_name = row[1]
        user_number = row[2]
        have_role = row[3]
                
        if opcja == 'delete':
            if interaction.guild.get_role(867415999447040020) in interaction.user.roles:
                cur.execute(f"DELETE FROM members WHERE ID = '{user_id}'")
                role = interaction.guild.get_role(926875607143448636)
                if role in interaction.user.roles:
                    await interaction.guild.get_member(int(user_id)).remove_roles(role)
                await interaction.response.send_message(f"Usunięto użytkownika **{user_name}**")
            else:
                await interaction.response.send_message("Nie jesteś imperatorem", ephemeral=True)

        elif opcja == 'default':
            message = f"| `{user_name}` | `{user_number}` | `{have_role}` |\n"
            await interaction.response.send_message(message)

        elif int(opcja) >= 0:
            if interaction.guild.get_role(867415999447040020) in interaction.user.roles:
                cur.execute(f"UPDATE members SET BUMP = '{int(opcja)}' WHERE ID = '{user_id}'")  #zmiana max liczby
                await interaction.response.send_message(f"Zmieniono liczbę bumpów użytkownika **{user_name}** na **{int(opcja)}**")
            else:
                await interaction.response.send_message("Nie jesteś imperatorem", ephemeral=True)

    con.commit() #zapisanie zmian



# RANDOM BAN BOT
@tree.command(name='ban', description='Wylosowanie losowych osób do bana', guild = discord.Object(id = 772531463051804692))
async def self(interaction: discord.Interaction, liczba: int = 1):
    ban_list = []
    ban = ""
    for x in range(liczba):
        ban_list.append(interaction.guild.members[random.randint(1, len(interaction.guild.members))].id)

    for ban_id in ban_list:
        ban += f" <@{ban_id}>"

    await interaction.response.send_message(f"Do bana wylosowano:{ban}")



# BARKOBOT
@tree.command(name='barka', description='Puszczenie barki na eventach', guild = discord.Object(id = 772531463051804692))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(f"Puszczam barkę na <#916729309123723296> 😀")
    await called_once_a_day(False)


@client.event
async def called_once_a_day(msg):  # Fired every day
    await client.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    if (msg):
        channel = client.get_channel(772531463522091018) # eventy
        await channel.send("<@&1023352481578750052> Czas na barkę 😀\nZapraszam na <#916729309123723296>")

    voice_channel = client.get_channel(916729309123723296)
    await voice_channel.connect() #podlaczenie do czatu glosowego

    voice = discord.utils.get(client.voice_clients, guild=client.get_guild(772531463051804692))

    url = 'https://www.youtube.com/watch?v=t2i3hmVzypI&ab_channel=Avatarka73'
    #url = 'https://www.youtube.com/watch?v=fC7oUOUEEi4&ab_channel=StackMan'

    ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} #ponowne laczenie
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False) #tylko odtwarzanie (bez pobierania na pc)
        URL = info['formats'][0]['url']
    voice.play(discord.FFmpegPCMAudio(URL, **ffmpeg_opts), after=lambda e: asyncio.run_coroutine_threadsafe(voice.disconnect(), client.loop)) #puszczanie muzyki
    voice.source = discord.PCMVolumeTransformer(voice.source, volume=0.1)


async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day(True)  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration




client.run("TOKEN")
