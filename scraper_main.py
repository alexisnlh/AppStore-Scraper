import sys
import json
from config import ConfigLoader
from appstore_scraper import AppStoreScraper


def main():
    """
        Función principal con carga de configuración
    """
    print("\n🚀 Iniciando scraper de AppStore...\n")

    # Carga la configuración
    try:
        config_loader = ConfigLoader()

        # Valida antes de cargar
        if not config_loader.validate_config():
            sys.exit(1)

        apps_dict = config_loader.load_apps_dict()

        if not apps_dict:
            print("[WARNING] - No hay apps para buscar")
            return

        # Ejecuta el scraper
        scraper = AppStoreScraper(delay=1.0, max_retries=3)
        result = scraper.scrape_apps(apps_dict)
        scraper.print_results(result)

    except FileNotFoundError as e:
        print(f"\n[ERROR] - {e}\n")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] - JSON inválido: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] - Error inesperado: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
