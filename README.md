# Bot de Telegram - Cotización del Dólar Oficial 💰

Un bot de Telegram que obtiene y envía la cotización del dólar oficial en tiempo real usando la API de [dolarapi.com](https://dolarapi.com).

## Características

- 🏛️ Obtiene la cotización del dólar oficial
- 🤖 Comandos fáciles de usar
- ⏰ Envío automático de cotizaciones (opcional)
- 🚀 Listo para deploy en Railway
- 📱 Interfaz amigable con emojis

## Comandos Disponibles

- `/start` - Iniciar el bot
- `/help` - Mostrar ayuda
- `/cotizacion` - Ver la cotización del dólar oficial

## Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd telegram_dolares
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   
   Editar `.env` y agregar tu token de Telegram:
   ```
   TELEGRAM_BOT_TOKEN=tu_token_aqui
   ```

4. **Ejecutar el bot**
   ```bash
   python main.py
   ```

## Configuración

### Variables de Entorno

- `TELEGRAM_BOT_TOKEN` (requerido): Token del bot obtenido de @BotFather
- `CHAT_ID` (opcional): ID del chat para envíos automáticos
- `DOLARAPI_URL` (opcional): URL de la API (por defecto: https://dolarapi.com)
- `AUTO_SEND_INTERVAL` (opcional): Intervalo en minutos para envíos automáticos

### Obtener Token de Telegram

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Usa el comando `/newbot`
3. Sigue las instrucciones para crear tu bot
4. Copia el token que te proporciona

### Obtener Chat ID (para envíos automáticos)

1. Envía un mensaje a tu bot
2. Visita: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Busca el `chat.id` en la respuesta

## Deploy en Railway

1. **Conectar repositorio**
   - Ve a [Railway](https://railway.app)
   - Conecta tu repositorio de GitHub

2. **Configurar variables de entorno**
   - En el dashboard de Railway
   - Ve a Variables
   - Agrega `TELEGRAM_BOT_TOKEN` con tu token

3. **Deploy automático**
   - Railway detectará automáticamente que es un proyecto Python
   - El bot se desplegará automáticamente

## Estructura del Proyecto

```
telegram_dolares/
├── main.py              # Archivo principal del bot
├── dolar_service.py     # Servicio para obtener cotizaciones
├── config.py            # Configuración y constantes
├── requirements.txt     # Dependencias de Python
├── .env.example        # Ejemplo de variables de entorno
├── .gitignore          # Archivos a ignorar en git
└── README.md           # Este archivo
```

## API Utilizada

Este bot utiliza la API gratuita de [dolarapi.com](https://dolarapi.com) que proporciona la cotización del dólar oficial en tiempo real para Argentina.

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún bug o tienes una idea para mejorar el bot, no dudes en crear un issue o pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
