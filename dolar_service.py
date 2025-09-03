import aiohttp
import logging
from datetime import datetime
from config import API_ENDPOINT

# Configurar logger para el servicio
logger = logging.getLogger(__name__)

class DolarService:
    """Servicio para obtener cotizaciones del dólar desde dolarapi"""
    
    def __init__(self):
        self.session = None
    
    async def _get_session(self):
        """Obtiene o crea una sesión HTTP"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        """Cierra la sesión HTTP"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def get_quotation(self) -> dict:
        """
        Obtiene la cotización del dólar oficial
        
        Returns:
            dict: Datos de la cotización o None si hay error
        """
        try:
            session = await self._get_session()
            async with session.get(API_ENDPOINT) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.warning(f"Error HTTP {response.status} al obtener cotización oficial")
                    return None
        except Exception as e:
            logger.error(f"Error al obtener cotización oficial: {e}")
            return None
    
    async def get_all_quotations(self) -> dict:
        """
        Obtiene la cotización del dólar oficial (mantiene compatibilidad con el nombre)
        
        Returns:
            dict: Diccionario con la cotización oficial
        """
        quotation = await self.get_quotation()
        if quotation:
            return {'oficial': quotation}
        return {}
    
    def format_single_quotation(self, quotation: dict) -> str:
        """
        Formatea la cotización del dólar oficial para mostrar
        
        Args:
            quotation: Datos de la cotización
        
        Returns:
            str: Mensaje formateado
        """
        if not quotation:
            return "❌ No se pudo obtener la cotización"
        
        # Extraer datos
        compra = quotation.get('compra', 'N/A')
        venta = quotation.get('venta', 'N/A')
        fecha_actualizacion = quotation.get('fechaActualizacion', 'N/A')
        
        # Formatear precios
        if compra != 'N/A':
            compra = f"${compra:,.2f}"
        if venta != 'N/A':
            venta = f"${venta:,.2f}"
        
        # Formatear fecha actual
        fecha_actual = datetime.now().strftime('%H:%M %d/%m/%Y')
        
        message = f"🏛️ <b>Dólar Oficial</b>\n\n"
        message += f"🟢 <b>Compra:</b> {compra}\n"
        message += f"🔴 <b>Venta:</b> {venta}\n"
        message += f"🕐 <b>Actualizado:</b> {fecha_actual}"
        
        return message
    
    def format_all_quotations(self, quotations: dict) -> str:
        """
        Formatea la cotización del dólar oficial para mostrar
        
        Args:
            quotations: Diccionario con la cotización oficial
        
        Returns:
            str: Mensaje formateado con la cotización
        """
        if not quotations or 'oficial' not in quotations:
            return "❌ No se pudo obtener la cotización del dólar oficial"
        
        quotation = quotations['oficial']
        
        # Extraer datos
        compra = quotation.get('compra', 'N/A')
        venta = quotation.get('venta', 'N/A')
        fecha_actualizacion = quotation.get('fechaActualizacion', 'N/A')
        
        # Formatear precios
        if compra != 'N/A':
            compra = f"${compra:,.2f}"
        if venta != 'N/A':
            venta = f"${venta:,.2f}"
        
        # Formatear fecha actual
        fecha_actual = datetime.now().strftime('%H:%M %d/%m/%Y')
        
        message = "🏛️ <b>COTIZACIÓN DÓLAR OFICIAL</b>\n"
        message += f"🕐 <i>Actualizado: {fecha_actual}</i>\n\n"
        message += f"🟢 <b>Compra:</b> {compra}\n"
        message += f"🔴 <b>Venta:</b> {venta}\n"
        message += f"🕐 <b>Última actualización API:</b> {fecha_actualizacion}"
        
        return message
