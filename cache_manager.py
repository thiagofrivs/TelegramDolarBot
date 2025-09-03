import json
import os
import time
from typing import Dict, Optional, Any

class CacheManager:
    """Maneja el cache de cotizaciones y tiempos de envío"""
    
    def __init__(self, cache_file: str = "bot_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Carga el cache desde el archivo"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._get_default_cache()
        return self._get_default_cache()
    
    def _get_default_cache(self) -> Dict:
        """Retorna la estructura por defecto del cache"""
        return {
            'last_quotation': None,
            'user_last_sent': {},
            'last_updated': None
        }
    
    def _save_cache(self):
        """Guarda el cache en el archivo"""
        try:
            self.cache['last_updated'] = time.time()
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar cache: {e}")
    
    def get_last_quotation(self) -> Optional[Dict]:
        """Obtiene la última cotización guardada"""
        return self.cache.get('last_quotation')
    
    def set_last_quotation(self, quotation: Dict):
        """Guarda la última cotización"""
        self.cache['last_quotation'] = quotation
        self._save_cache()
    
    def get_user_last_sent(self, user_id: int) -> float:
        """Obtiene el último tiempo de envío para un usuario"""
        user_last_sent = self.cache.get('user_last_sent', {})
        return user_last_sent.get(str(user_id), 0)
    
    def set_user_last_sent(self, user_id: int, timestamp: float):
        """Actualiza el último tiempo de envío para un usuario"""
        if 'user_last_sent' not in self.cache:
            self.cache['user_last_sent'] = {}
        
        self.cache['user_last_sent'][str(user_id)] = timestamp
        self._save_cache()
    
    def get_all_user_times(self) -> Dict[str, float]:
        """Obtiene todos los tiempos de último envío"""
        return self.cache.get('user_last_sent', {})
    
    def clear_user_data(self, user_id: int):
        """Elimina los datos de un usuario del cache"""
        if 'user_last_sent' in self.cache:
            user_id_str = str(user_id)
            if user_id_str in self.cache['user_last_sent']:
                del self.cache['user_last_sent'][user_id_str]
                self._save_cache()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Obtiene información del cache"""
        return {
            'cache_file': self.cache_file,
            'last_updated': self.cache.get('last_updated'),
            'has_quotation': self.cache.get('last_quotation') is not None,
            'users_count': len(self.cache.get('user_last_sent', {}))
        }
    
    def reset_cache(self):
        """Resetea completamente el cache"""
        self.cache = self._get_default_cache()
        self._save_cache()
