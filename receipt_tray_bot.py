import discord
import aiohttp
import os
import threading
from pystray import Icon as TrayIcon, Menu as TrayMenu, MenuItem as Item
from PIL import Image, ImageDraw

TOKEN = "MTM5NDEzMTI5NjU0Mzk2OTMyMA.GdviUH.gvBSfHwpRFHLfOgG396-BtyZUVeC_OZFdN9Z1k"
CHANNEL_ID = 1394128069052207106  # Replace with your #receipts channel ID
SAVE_FOLDER = r"C:\Receipts\New Receipts"     # Change this to your desired save path
ICON_PATH = os.path.join(os.path.dirname(__file__), "icon.png")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Start Discord bot in a background thread
def run_bot():
    client.run(TOKEN)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID and message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png", ".pdf")):
                file_path = os.path.join(SAVE_FOLDER, attachment.filename)
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(file_path, "wb") as f:
                                f.write(await resp.read())
                            print(f"📸 Saved {attachment.filename}")

# Define tray icon menu
def setup_tray_icon():
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)

    try:
        image = Image.open(ICON_PATH)
    except FileNotFoundError:
        print("⚠️ icon.png not found, using fallback icon.")
        image = get_fallback_icon()

    menu = TrayMenu(Item("Quit", on_exit))
    tray_icon = TrayIcon("ReceiptBot", image, "Receipt Bot Running", menu)
    tray_icon.run()

def get_fallback_icon():
    image = Image.new('RGB', (32, 32), color='white')
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 24, 24), fill='gray')
    return image

# Run everything
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    setup_tray_icon()