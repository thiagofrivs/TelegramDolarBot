import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del bot
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Configuración de la API
DOLARAPI_URL = os.getenv('DOLARAPI_URL', 'https://dolarapi.com')

# Configuración de envíos automáticos
AUTO_SEND_INTERVAL = int(os.getenv('AUTO_SEND_INTERVAL', '60'))

# URL de la API de dolarapi para dólar oficial
API_ENDPOINT = f'{DOLARAPI_URL}/v1/dolares/oficial'

# Mensajes del bot
MESSAGES = {
    'start': '''🎉🎊 ¡HOLA! ¡BIENVENIDO! 🎊🎉

🤖 ¡Soy tu botito súper inteligente de cotización del dólar oficial! 💰

📊 ¡Te ayudo a mantenerte informado! 📊
Te mantengo al día con la cotización del dólar oficial en tiempo real, ¡como un detective financiero! 🕵️‍♂️💸

🔧 ¡Comandos disponibles! 🔧
• /cotizacion - Ver cotización actual 📈
• /configurar - Configurar envío automático ⚙️
• /parar - Detener envío automático 🛑
• /estado - Ver configuración actual 📊
• /help - Mostrar ayuda completa 📚

🚀 ¡Empecemos esta aventura juntos! 🚀
¡Estoy súper emocionado de ayudarte! 😊✨''',
    
    'help': '''📚 ¡AYUDA COMPLETA! 📚

🔹 ¡Comandos principales! 🔹
• /cotizacion - Ver la cotización del dólar oficial 📈
• /configurar - Configurar envío automático de cotizaciones ⚙️
• /parar - Detener envío automático 🛑
• /estado - Ver configuración actual 📊
• /help - Mostrar esta ayuda 📚

💡 ¡Cómo configurar envío automático! 💡
1. ✍️ Escribe /configurar
2. 🤖 El bot te pedirá los segundos (para probar)
3. 🔢 Responde con un número (ej: 30)
4. 🎉 ¡Listo! Recibirás cotizaciones automáticamente

⏰ ¡Intervalos permitidos! ⏰
5 segundos a 60 segundos (1 minuto) - ¡Perfecto para probar!

🎯 ¡Ejemplos súper claros! 🎯
• 🔟 10 segundos = revisa cada 10 segundos si cambió
• 🕐 30 segundos = revisa cada 30 segundos si cambió
• ⏰ 60 segundos = revisa cada 1 minuto si cambió

🧠 ¡Lo mejor! Solo te envío mensajes cuando el precio realmente cambie, ¡no más spam! 🧠

¡Estoy aquí para ayudarte! 😊🤖''',
    
    'error': '❌ Error al obtener la cotización\n\n🔄 Intenta nuevamente en unos minutos.\n\n💡 Si el problema persiste, verifica tu conexión a internet.',
    'no_data': '⚠️ No se pudo obtener la cotización\n\n🕐 Intenta nuevamente en unos minutos.',
    
    # Mensajes de configuración paso a paso
    'config_start': '''🤖✨ ¡HOLA! VAMOS A CONFIGURAR TU MONITOREO INTELIGENTE! ✨🤖

🎯 ¡Te explico cómo funciona esta magia! 🎯
Tu botito favorito va a estar vigilando el dólar oficial cada X segundos, pero solo te va a molestar cuando realmente pase algo interesante! 🕵️‍♂️💸

📝 ¡Dime cada cuántos segundos quieres que revise! 📝

💡 Ejemplos súper claros:
• 🔟 10 = revisa cada 10 segundos si cambió
• 🕐 30 = revisa cada 30 segundos si cambió  
• ⏰ 60 = revisa cada 1 minuto si cambió

⏰ Rango permitido: 5 segundos a 60 segundos (1 minuto)

🎯 ¡La ventaja es GENIAL! Solo recibirás mensajes cuando el precio realmente cambie, ¡no más spam molesto! 🚫📱

✍️ ¡Escribe solo el número que quieras! ✍️''',
    
    'config_success': '''🎉🎊 ¡MONITOREO INTELIGENTE ACTIVADO! 🎊🎉

🎯 ¡Tu configuración está lista! 🎯
⏰ Verificación: cada {minutes} segundos ⏰
🔄 Estado: ¡SUPER ACTIVO! 🔄
🧠 Modo: Solo envía cuando cambie el precio (¡súper inteligente!) 🧠

💬 ¡Tu botito va a estar súper atento! 💬
Revisará si la cotización cambió cada {minutes} segundos, pero solo te va a molestar cuando detecte cambios reales en el precio del dólar oficial. ¡Qué considerado! 😊💸

🛑 Para detener el monitoreo: usa /parar 🛑
💡 Para ver el estado: usa /estado 💡

¡Disfruta de tu monitoreo inteligente! 🚀✨''',
    
    'config_error': '''😅 ¡Ups! Algo salió mal 😅

⚠️ Problema: El valor que ingresaste no es válido ⚠️

📝 ¡Recuerda estas reglas! 📝
• Debe ser un número entre 5 y 60 🔢
• Solo números, sin texto adicional ✍️
• Ejemplos válidos: 10, 30, 60 💡

🔄 ¡Intenta nuevamente! /configurar 🔄

¡No te preocupes, todos nos equivocamos! 😊✨''',
    
    'config_cancel': '''😔 ¡Configuración cancelada! 😔

❌ No se guardó ninguna configuración.

💡 ¡No te preocupes! Si quieres configurar el envío automático más tarde, usa: /configurar 💡

¡Estaré aquí cuando quieras! 😊🤖''',
    
    'stop_success': '''🛑 ¡ENVÍO AUTOMÁTICO DETENIDO! 🛑

✅ ¡Listo! Ya no recibirás cotizaciones automáticamente.

💡 ¡No te preocupes! Para reactivar el envío automático, usa: /configurar 💡

¡Estaré aquí cuando quieras volver a activarlo! 😊🤖''',
    
    'no_config': '''📭 ¡Sin configuración activa! 📭

😊 No tienes envío automático configurado.

🔧 ¡Vamos a configurarlo! Para configurarlo, usa: /configurar 🔧

💡 ¡Te guiaré paso a paso! Te ayudo a configurar cuándo quieres recibir las cotizaciones 💡

¡Será súper fácil! 🚀✨''',
    
    'current_config': '''📊 ¡Aquí está tu configuración actual! 📊

⏰ Verificación: cada {minutes} segundos ⏰
🔄 Estado: {status} 🔄
🧠 Modo: Solo envía cuando cambie el precio (¡súper inteligente!) 🧠

💡 ¡Te explico qué significa! 💡
Tu botito revisa si la cotización cambió cada {minutes} segundos, pero solo te va a molestar cuando detecte cambios reales. ¡Qué considerado! 😊💸

🛑 Para detener: /parar 🛑
⚙️ Para cambiar: /configurar ⚙️

¡Tu monitoreo está funcionando perfectamente! 🚀✨'''
}
