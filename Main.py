import discord
from discord.ext import commands, tasks
import datetime
import asyncio # Für die asynchrone Planung

# ERSETZEN SIE DIES MIT IHREM BOT-TOKEN
# Es ist besser, das Token aus Umgebungsvariablen zu laden, aber für den Anfang ist dies ok.
TOKEN = 'IHR_BOT_TOKEN_HIER_EINFÜGEN'

# Definieren Sie die Intents, die Ihr Bot benötigt
# Für das Senden von Nachrichten in Channels sind standardmäßige Intents oft ausreichend.
# Wenn Sie jedoch auf Nachrichteninhalte zugreifen möchten, müssen Sie 'Message Content Intent' aktivieren.
intents = discord.Intents.default()
# intents.message_content = True # Nur aktivieren, wenn Sie Nachrichteninhalt lesen müssen

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Konfiguration der automatischen Nachrichten ---
# Sie können dies erweitern, um Nachrichten aus einer Datei oder Datenbank zu laden
scheduled_messages = [
    {
        "time": datetime.time(hour=10, minute=0), # 10:00 Uhr morgens (UTC oder Serverzeit)
        "channel_id": 123456789012345678, # ERSETZEN SIE DIES MIT DER ECHTEN CHANNEL-ID
        "message": "Guten Morgen, Leute! Zeit für den täglichen Check-in."
    },
    {
        "time": datetime.time(hour=15, minute=30), # 15:30 Uhr nachmittags
        "channel_id": 987654321098765432, # ERSETZEN SIE DIES MIT EINER ANDEREN CHANNEL-ID
        "message": "Kurzes Update: Das Projekt läuft gut! Weiter so!"
    }
]

# --- Events ---
@bot.event
async def on_ready():
    print(f'{bot.user.name} ist online und bereit!')
    # Starten Sie die geplante Aufgabe, sobald der Bot bereit ist
    check_scheduled_messages.start()

# --- Geplante Aufgabe ---
@tasks.loop(minutes=1) # Überprüft jede Minute, ob eine Nachricht gesendet werden soll
async def check_scheduled_messages():
    now = datetime.datetime.now()
    current_time = now.time()

    for msg_config in scheduled_messages:
        target_time = msg_config["time"]
        channel_id = msg_config["channel_id"]
        message_content = msg_config["message"]

        # Überprüfen, ob die aktuelle Minute und Stunde mit der Zielzeit übereinstimmen
        # und ob die Nachricht noch nicht für heute gesendet wurde
        # (Dies ist eine einfache Implementierung, die keine Persistenz hat.
        # Bei einem Neustart des Bots könnte die Nachricht am selben Tag erneut gesendet werden.)
        
        # Um zu verhindern, dass die Nachricht mehrmals pro Minute gesendet wird,
        # können wir einen kleinen Zeitbereich überprüfen oder einen Flag setzen.
        # Hier prüfen wir nur auf die genaue Minute.
        
        # Eine robustere Lösung würde ein System verwenden, das verfolgt, wann die letzte Nachricht gesendet wurde.
        # Für diesen einfachen Fall:
        
        # Prüfen, ob die aktuelle Stunde und Minute mit der geplanten Zeit übereinstimmen
        if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
            channel = bot.get_channel(channel_id)
            if channel:
                try:
                    # Hier könnten Sie eine Logik hinzufügen, um zu prüfen, ob die Nachricht
                    # bereits an diesem Tag gesendet wurde, um Duplikate zu vermeiden.
                    # Für den Anfang senden wir sie einfach.
                    await channel.send(message_content)
                    print(f"Nachricht gesendet in Channel {channel.name} ({channel_id}) um {now.strftime('%H:%M')}: {message_content}")
                    # Optional: Entfernen Sie die Nachricht aus der Liste für heute,
                    # oder setzen Sie ein Flag "sent_today = True" und resetten Sie es um Mitternacht.
                    # Für eine einfache Demo lassen wir es so, wie es ist.
                except discord.Forbidden:
                    print(f"Fehler: Keine Berechtigung, Nachrichten in Channel {channel_id} zu senden.")
                except Exception as e:
                    print(f"Ein Fehler ist aufgetreten beim Senden der Nachricht in Channel {channel_id}: {e}")
            else:
                print(f"Channel mit ID {channel_id} nicht gefunden.")

# --- Bot starten ---
bot.run(TOKEN)
