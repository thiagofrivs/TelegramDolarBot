import json
import os
from typing import Dict, Optional

class UserConfig:
    """Maneja la configuración de usuarios para envío automático"""
    
    def __init__(self, config_file: str = "user_configs.json"):
        self.config_file = config_file
        self.configs = self._load_configs()
    
    def _load_configs(self) -> Dict:
        """Carga las configuraciones desde el archivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_configs(self):
        """Guarda las configuraciones en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.configs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar configuraciones: {e}")
    
    def set_user_config(self, user_id: int, interval_seconds: int) -> bool:
        """
        Configura el envío automático para un usuario
        
        Args:
            user_id: ID del usuario
            interval_seconds: Intervalo en segundos (mínimo 5, máximo 60)
        
        Returns:
            bool: True si se configuró correctamente
        """
        if interval_seconds < 5:
            return False  # Mínimo 5 segundos
        if interval_seconds > 60:  # Máximo 1 minuto
            return False
        
        self.configs[str(user_id)] = {
            'interval_seconds': interval_seconds,
            'enabled': True
        }
        self._save_configs()
        return True
    
    def get_user_config(self, user_id: int) -> Optional[Dict]:
        """
        Obtiene la configuración de un usuario
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Dict con la configuración o None si no existe
        """
        return self.configs.get(str(user_id))
    
    def disable_user_config(self, user_id: int) -> bool:
        """
        Desactiva el envío automático para un usuario
        
        Args:
            user_id: ID del usuario
        
        Returns:
            bool: True si se desactivó correctamente
        """
        if str(user_id) in self.configs:
            self.configs[str(user_id)]['enabled'] = False
            self._save_configs()
            return True
        return False
    
    def remove_user_config(self, user_id: int) -> bool:
        """
        Elimina completamente la configuración de un usuario
        
        Args:
            user_id: ID del usuario
        
        Returns:
            bool: True si se eliminó correctamente
        """
        if str(user_id) in self.configs:
            del self.configs[str(user_id)]
            self._save_configs()
            return True
        return False
    
    def get_all_active_configs(self) -> Dict:
        """
        Obtiene todas las configuraciones activas
        
        Returns:
            Dict con todas las configuraciones activas
        """
        active_configs = {}
        for user_id, config in self.configs.items():
            if config.get('enabled', False):
                active_configs[user_id] = config
        return active_configs
    
    def is_user_enabled(self, user_id: int) -> bool:
        """
        Verifica si un usuario tiene envío automático habilitado
        
        Args:
            user_id: ID del usuario
        
        Returns:
            bool: True si está habilitado
        """
        config = self.get_user_config(user_id)
        return config is not None and config.get('enabled', False)
