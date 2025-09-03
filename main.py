import logging
import asyncio
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from dolar_service import DolarService
from user_config import UserConfig
from cache_manager import CacheManager
from config import BOT_TOKEN, CHAT_ID, AUTO_SEND_INTERVAL, MESSAGES

# Estados de la conversación
WAITING_MINUTES = 1

# Configurar logging profesional
logging.basicConfig(
    format='\033[94m%(asctime)s\033[0m | \033[92m%(levelname)-8s\033[0m | \033[96m%(name)s\033[0m | %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configurar logging para aiohttp (menos verboso)
logging.getLogger('aiohttp').setLevel(logging.WARNING)
logging.getLogger('telegram').setLevel(logging.WARNING)

# Inicializar servicios
dolar_service = DolarService()
user_config = UserConfig()
cache_manager = CacheManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /start"""
    await update.message.reply_text(MESSAGES['start'])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /help"""
    await update.message.reply_text(MESSAGES['help'])

async def cotizacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /cotizacion - muestra la cotización del dólar oficial"""
    try:
        quotation = await dolar_service.get_quotation()
        if quotation:
            message = dolar_service.format_single_quotation(quotation)
            await update.message.reply_text(message, parse_mode='HTML')
        else:
            await update.message.reply_text(MESSAGES['no_data'])
    except Exception as e:
        logger.error(f"Error en cotizacion: {e}")
        await update.message.reply_text(MESSAGES['error'])

async def configurar_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia el proceso de configuración"""
    await update.message.reply_text(MESSAGES['config_start'])
    return WAITING_MINUTES

async def configurar_minutes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Procesa los minutos ingresados por el usuario"""
    user_id = update.effective_user.id
    user_input = update.message.text.strip()
    
    try:
        interval = int(user_input)
        
        if user_config.set_user_config(user_id, interval):
            message = MESSAGES['config_success'].format(minutes=interval)
            await update.message.reply_text(message)
            logger.info(f"Usuario {user_id} configuró envío automático cada {interval} segundos")
            return ConversationHandler.END
        else:
            await update.message.reply_text("❌ El intervalo debe estar entre 5 y 60 segundos (1 minuto)\n\n🔄 Intenta nuevamente:")
            return WAITING_MINUTES
            
    except ValueError:
        await update.message.reply_text(MESSAGES['config_error'])
        return WAITING_MINUTES

async def configurar_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela el proceso de configuración"""
    await update.message.reply_text(MESSAGES['config_cancel'])
    return ConversationHandler.END

async def parar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /parar - detiene envío automático"""
    user_id = update.effective_user.id
    
    if user_config.disable_user_config(user_id):
        await update.message.reply_text(MESSAGES['stop_success'])
        logger.info(f"Usuario {user_id} detuvo envío automático")
    else:
        await update.message.reply_text(MESSAGES['no_config'])

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /estado - muestra configuración actual"""
    user_id = update.effective_user.id
    config = user_config.get_user_config(user_id)
    
    if config and config.get('enabled', False):
        status = "🟢 Activo"
        message = MESSAGES['current_config'].format(
            minutes=config['interval_seconds'],
            status=status
        )
    else:
        message = MESSAGES['no_config']
    
    await update.message.reply_text(message)

async def send_auto_quotations_to_users(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Verifica cambios en cotización y envía solo cuando hay cambios"""
    try:
        # Obtener cotización actual
        current_quotation = await dolar_service.get_quotation()
        if not current_quotation:
            logger.warning("No se pudo obtener cotización para verificación")
            return
        
        # Obtener última cotización del cache
        last_quotation = cache_manager.get_last_quotation()
        
        # Verificar si la cotización cambió
        quotation_changed = False
        if last_quotation is None:
            # Primera vez, no enviar pero guardar la cotización
            cache_manager.set_last_quotation(current_quotation)
            logger.info("Primera cotización obtenida, monitoreo iniciado")
            return
        
        # Comparar precios (compra y venta)
        current_compra = current_quotation.get('compra', 0)
        current_venta = current_quotation.get('venta', 0)
        last_compra = last_quotation.get('compra', 0)
        last_venta = last_quotation.get('venta', 0)
        
        if current_compra != last_compra or current_venta != last_venta:
            quotation_changed = True
            logger.info(f"¡Cambio detectado! Compra: {last_compra} → {current_compra}, Venta: {last_venta} → {current_venta}")
            cache_manager.set_last_quotation(current_quotation)  # Actualizar cotización en cache
        
        # Solo enviar si hubo cambio
        if not quotation_changed:
            return
        
        # Formatear mensaje súper amigable con indicación de cambio
        message = dolar_service.format_single_quotation(current_quotation)
        message += "\n\n🎉🎊 ¡COTIZACIÓN ACTUALIZADA! 🎊🎉"
        message += "\n\n💸 ¡Tu botito detectó un cambio en el precio! 💸"
        message += "\n🕵️‍♂️ ¡Estaba vigilando como un detective! 🕵️‍♂️"
        message += "\n\n😊 ¡Espero que esta información te sea útil! 😊"
        message += "\n🚀 ¡Seguiré monitoreando para ti! 🚀"
        
        active_configs = user_config.get_all_active_configs()
        if not active_configs:
            logger.info("No hay usuarios con monitoreo configurado")
            return
        
        # Enviar a cada usuario configurado
        sent_count = 0
        current_time = time.time()
        
        for user_id_str, config in active_configs.items():
            try:
                user_id = int(user_id_str)
                interval_seconds = config.get('interval_seconds', 5)
                
                # Obtener último tiempo de envío del cache
                last_sent_time = cache_manager.get_user_last_sent(user_id)
                
                # Verificar si ha pasado el tiempo suficiente
                if current_time - last_sent_time >= interval_seconds:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=message,
                        parse_mode='HTML'
                    )
                    cache_manager.set_user_last_sent(user_id, current_time)
                    sent_count += 1
                    logger.info(f"Cambio de cotización enviado a usuario {user_id} (verificación cada {interval_seconds}s)")
                
            except Exception as e:
                logger.error(f"Error enviando a usuario {user_id_str}: {e}")
        
        if sent_count > 0:
            logger.info(f"Cambios de cotización enviados a {sent_count} usuarios")
        
    except Exception as e:
        logger.error(f"Error en monitoreo de cotización: {e}")

async def send_auto_quotations(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía cotizaciones automáticamente (compatibilidad con sistema anterior)"""
    # Mantener compatibilidad con CHAT_ID global si está configurado
    if CHAT_ID:
        try:
            quotation = await dolar_service.get_quotation()
            if quotation:
                message = dolar_service.format_single_quotation(quotation)
                await context.bot.send_message(
                    chat_id=CHAT_ID, 
                    text=message, 
                    parse_mode='HTML'
                )
                logger.info("Cotización enviada automáticamente a CHAT_ID global")
        except Exception as e:
            logger.error(f"Error en envío automático global: {e}")
    
    # También enviar a usuarios configurados individualmente
    await send_auto_quotations_to_users(context)

def main() -> None:
    """Función principal del bot"""
    print("\n" + "="*60)
    print("🤖 BOT DE TELEGRAM - COTIZACIÓN DÓLAR OFICIAL")
    print("="*60)
    
    if not BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN no está configurado")
        print("💡 Crea un archivo .env con tu token de Telegram")
        return

    logger.info("🚀 Iniciando bot de cotizaciones...")
    logger.info("📊 Configurado para obtener cotización del dólar oficial")
    
    # Crear aplicación
    application = Application.builder().token(BOT_TOKEN).build()

    # Crear ConversationHandler para configuración paso a paso
    configurar_handler = ConversationHandler(
        entry_points=[CommandHandler("configurar", configurar_start)],
        states={
            WAITING_MINUTES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, configurar_minutes),
                CommandHandler("cancelar", configurar_cancel),
            ],
        },
        fallbacks=[CommandHandler("cancelar", configurar_cancel)],
    )

    # Agregar handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cotizacion", cotizacion))
    application.add_handler(configurar_handler)  # ConversationHandler para /configurar
    application.add_handler(CommandHandler("parar", parar))
    application.add_handler(CommandHandler("estado", estado))
    
    logger.info("✅ Comandos registrados: /start, /help, /cotizacion, /configurar, /parar, /estado")

    logger.info("⏰ Sistema de envío automático configurado (verificación cada 5 segundos)")

    logger.info("🔄 Bot iniciado y escuchando mensajes...")
    print("="*60)
    print("💡 Presiona Ctrl+C para detener el bot")
    print("="*60 + "\n")
    
    # Configurar envío automático usando asyncio (sin dependencias adicionales)
    async def auto_send_loop():
        """Loop para enviar cotizaciones automáticamente"""
        while True:
            try:
                # Crear contexto temporal
                class TempContext:
                    def __init__(self, bot):
                        self.bot = bot
                
                temp_context = TempContext(application.bot)
                await send_auto_quotations_to_users(temp_context)
                await asyncio.sleep(5)  # Verificar cada 5 segundos
            except Exception as e:
                logger.error(f"Error en auto_send_loop: {e}")
                await asyncio.sleep(5)
    
    # Callback para iniciar el loop después de que el bot esté listo
    async def post_init(application):
        """Se ejecuta después de que el bot esté inicializado"""
        asyncio.create_task(auto_send_loop())
        logger.info("✅ Loop de envío automático iniciado")
    
    # Configurar el callback
    application.post_init = post_init
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por el usuario")
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        print(f"\n💥 Error: {e}")

if __name__ == '__main__':
    main()
