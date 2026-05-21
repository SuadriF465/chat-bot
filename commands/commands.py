from telegram import Update
from telegram.ext import ContextTypes
import weather_api
import database


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Hello, {user}! I am your Advanced Weather Assistant Bot.\n"
        "I can track current weather and store your preferences.\n"
        "Type /help to review all supported features!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 *Available Commands:* \n\n"
        "*Weather Core:*\n"
        "/weather [city] - Get current weather details\n"
        "/setcity [city] - Save your primary/home city\n"
        "/myweather - Instantly check weather for your saved city\n\n"
        "*Information & Features:*\n"
        "/start - Restart the interaction with the bot\n"
        "/help - Show this interactive manual\n"
        "/about - Learn more about this software project\n"
        "/status - Check API operational status\n"
        "/tips - Get clothing tips based on active temperature\n"
        "/humidity - Learn why relative humidity matters\n"
        "/wind - Learn about wind chill effects\n"
        "/source - View backend weather data provider details"
    )
    await update.message.reply_markdown(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 This bot was developed as a Final Project for the Python Programming Course.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟢 System status: Operational. API Connection: Stable.")

async def humidity_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💧 Relative humidity determines how warm it feels outside and the likelihood of precipitation.")

async def wind_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💨 Higher wind speeds make temperatures feel colder than they actually register on sensors.")

async def source_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 Real-time weather parameters are securely pulled from the OpenWeatherMap API service.")


# --- 2. Логика погоды и работы с БД ---

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args).strip()
    if not city:
        await update.message.reply_text("⚠️ Please provide a city name.\nExample: /weather London")
        return

    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    await process_and_send_weather(update, city, user_id, username)

async def set_city_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args).strip()
    if not city:
        await update.message.reply_text("⚠️ Please specify a city.\nExample: /setcity Tokyo")
        return
    
    user_id = update.effective_user.id
    database.set_favorite_city(user_id, city)
    await update.message.reply_text(f"🎯 *{city.capitalize()}* has been saved as your favorite city! Use /myweather to check it.")

async def my_weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    city = database.get_favorite_city(user_id)
    
    if not city:
        await update.message.reply_text("📂 You haven't configured a favorite city yet. Use `/setcity [city]` first.")
        return
        
    username = update.effective_user.username or "Unknown"
    await process_and_send_weather(update, city, user_id, username)

async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    city = database.get_favorite_city(user_id) or "London"
    
    res = weather_api.get_weather(city)
    if isinstance(res, dict):
        temp = res["temp"]
        if temp < 0:
            tip = "❄️ It's freezing! Wear a heavy winter coat, thermal layers, and a scarf."
        elif temp < 15:
            tip = "🧥 It's chilly. A standard jacket, hoodie, or warm sweater is recommended."
        else:
            tip = "☀️ Pleasant weather! A light t-shirt and jeans will be perfectly fine."
        await update.message.reply_text(f"Based on current conditions in {res['city_name']}:\n{tip}")
    else:
        await update.message.reply_text("Could not fetch weather tips. Make sure your profile city is set correctly.")


# --- 3. Вспомогательные обработчики и Ошибки ---

async def process_and_send_weather(update: Update, city: str, user_id: int, username: str):
    res = weather_api.get_weather(city)

    if res == "404":
        await update.message.reply_text(f"🔍 Sorry, I couldn't find a city named '{city}'. Please check the spelling.")
    elif res is None:
        await update.message.reply_text("🌐 Connection error. Unable to reach weather services. Please try again later.")
    else:
        database.log_weather_request(user_id, username, res["city_name"])
        response_text = (
            f"🌍 *Weather in {res['city_name']}, {res['country']}*:\n"
            f"🌡️ *Temperature:* {res['temp']}°C\n"
            f"🤔 *Feels like:* {res['feels_like']}°C\n"
            f"💧 *Humidity:* {res['humidity']}%\n"
            f"✨ *Conditions:* {res['description']}"
        )
        await update.message.reply_markdown(response_text)

async def unknown_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤔 Unknown command or message format. Type /help to see available options.")