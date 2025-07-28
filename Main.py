import discord
from discord.ext import commands, tasks
import datetime
import pytz # Importiere pytz für Zeitzonen
import asyncio
import os # Wird benötigt, falls du Umgebungsvariablen nutzt (optional, aber gute Praxis)

# --- Token aus Datei laden ---
# Dies ist die bevorzugte Methode für lokale Entwicklung
try:
    with open('token.txt', 'r') as f:
        TOKEN = f.read().strip() # .strip() entfernt Leerzeichen/Zeilenumbrüche
except FileNotFoundError:
    # Fallback: Wenn token.txt nicht gefunden wird, versuche eine Umgebungsvariable
    # Das ist nützlich für das Hosting auf Plattformen wie Heroku, Render etc.
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if TOKEN is None:
        print("FEHLER: Bot-Token nicht gefunden! Stelle sicher, dass 'token.txt' existiert ODER die Umgebungsvariable 'DISCORD_BOT_TOKEN' gesetzt ist.")
        exit() # Beende das Skript, wenn kein Token gefunden wird

# Definieren Sie die Intents, die Ihr Bot benötigt
intents = discord.Intents.default()
# intents.message_content = True # Nur aktivieren, wenn Sie Nachrichteninhalt lesen müssen

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Konfiguration der automatischen Nachrichten ---
# Verwende die Zeitzone für Deutschland
GERMAN_TIMEZONE = pytz.timezone('Europe/Berlin')

scheduled_messages = [
    {
        # 10:00 Uhr morgens in deutscher Zeit
        "time": datetime.time(hour=0, minute=0),
        "channel_id": 1287830586114703400, # ERSETZE DIES MIT DER ECHTEN CHANNEL-ID
        "message": "Guten Morgen, Leute! Zeit für den täglichen Check-in (deutsche Zeit)."
    },
    {
        # 15:30 Uhr nachmittags in deutscher Zeit
        "time": datetime.time(hour=15, minute=30),
        "channel_id": 987654321098765432, # ERSETZE DIES MIT EINER ANDEREN CHANNEL-ID
        "message": "Kurzes Update: Das Projekt läuft gut! Weiter so! (deutsche Zeit)"
    }
]

# --- Events ---
@bot.event
async def on_ready():
    print(f'{bot.user.name} ist online und bereit!')
    check_scheduled_messages.start()

# --- Geplante Aufgabe ---
@tasks.loop(minutes=1) # Überprüft jede Minute, ob eine Nachricht gesendet werden soll
async def check_scheduled_messages():
    # Hole die aktuelle Zeit in der deutschen Zeitzone
    now_in_german_tz = datetime.datetime.now(GERMAN_TIMEZONE)
    current_hour = now_in_german_tz.hour
    current_minute = now_in_german_tz.minute

    for msg_config in scheduled_messages:
        target_time = msg_config["time"]
        channel_id = msg_config["channel_id"]
        message_content = msg_config["message"]

        if current_hour == target_time.hour and current_minute == target_time.minute:
            channel = bot.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(message_content)
                    print(f"Nachricht gesendet in Channel {channel.name} ({channel_id}) um {now_in_german_tz.strftime('%H:%M')} (DE): {message_content}")
                except discord.Forbidden:
                    print(f"Fehler: Keine Berechtigung, Nachrichten in Channel {channel_id} zu senden.")
                except Exception as e:
                    print(f"Ein Fehler ist aufgetreten beim Senden der Nachricht in Channel {channel_id}: {e}")
            else:
                print(f"Channel mit ID {channel_id} nicht gefunden.")

# --- Bot starten ---
bot.run(TOKEN)
