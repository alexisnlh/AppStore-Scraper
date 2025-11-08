import json
from pathlib import Path
from typing import Dict, Optional


class ConfigLoader:
    """
        Cargador de configuración para el scraper
    """
    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = "apps_config.json"

        self.config_path = Path(config_path)

    def load_apps_dict(self) -> Dict[str, str]:
        """
            Carga el diccionario de apps desde el archivo JSON
            Returns:
                Dict con {nombre_app: url}
            Raises:
                FileNotFoundError: Si no existe el archivo de configuración
                json.JSONDecodeError: Si el JSON está mal formado
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"No se encuentra el archivo de configuración: {self.config_path}\n"
                f"Copia 'apps_config.example.json' a 'apps_config.json' y configúralo."
            )

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            apps = data.get('apps', {})

            if not apps:
                print("[WARNING] - El archivo de configuración está vacío")

            return apps
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Error al parsear el JSON: {e.msg}",
                e.doc,
                e.pos
            )

    def validate_config(self) -> bool:
        """
            Valida que el archivo de configuración sea correcto
            Returns:
                True si la configuración es válida
        """
        try:
            apps = self.load_apps_dict()
            
            # Valida que todas las URLs sean strings
            for app_name, url in apps.items():
                if not isinstance(url, str):
                    print(f"[ERROR] - URL inválida para {app_name}: {url}")
                    return False

                if not url.startswith('http'):
                    print(f"[ERROR] - URL no válida para {app_name}: {url}")
                    return False

            print(f"[SUCCESSFUL] - Configuración válida: {len(apps)} apps cargadas")
            return True
        except Exception as e:
            print(f"[ERROR] - Error en la configuración: {e}")
            return False
