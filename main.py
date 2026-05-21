from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import config
import database
from commands import basic, weather

def main():
    database.init_db()

    app = ApplicationBuilder().token(config.TOKEN).build()

    app.add_handler(CommandHandler("start", basic.start_command))
    app.add_handler(CommandHandler("help", basic.help_command))
    app.add_handler(CommandHandler("about", basic.about_command))
    app.add_handler(CommandHandler("status", basic.status_command))
    app.add_handler(CommandHandler("humidity", basic.humidity_info))
    app.add_handler(CommandHandler("wind", basic.wind_info))
    app.add_handler(CommandHandler("source", basic.source_info))
    
    app.add_handler(CommandHandler("weather", weather.weather_command))
    app.add_handler(CommandHandler("setcity", weather.set_city_command))
    app.add_handler(CommandHandler("myweather", weather.my_weather_command))
    app.add_handler(CommandHandler("tips", weather.tips_command))

    # Обработка любого другого некорректного текстового ввода
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather.unknown_message_handler))

    print("🚀 Bot is successfully running...")
    app.run_polling()

if __name__ == "__main__":
    main()