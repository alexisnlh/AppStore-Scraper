import re
import time
import json
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup


@dataclass
class ScrapResult:
    """
        Estructura para los resultados del scraping
    """
    paid_apps: Dict[str, str]
    free_apps: List[str]
    failed_apps: List[str]


class AppStoreScraper:
    """
        Scraper optimizado para la AppStore
    """
    def __init__(self, delay: float = 1.0, max_retries: int = 3):
        self.delay = delay
        self.session = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> requests.Session:
        """
            Crea una sesión con retry automático
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Headers para simular navegador real
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        return session

    def _extract_price(self, soup: BeautifulSoup) -> Optional[Tuple[float, str]]:
        """
            Extrae el precio de la página parseada
            Returns:
                Tuple[precio, moneda]
        """
        # Busca el bloque JSON-LD para extraer el precio
        scripts = soup.find_all("script", type="application/ld+json")
        app_data = None

        for s in scripts:
            try:
                data = json.loads(s.string)
            except (json.JSONDecodeError, TypeError):
                continue

            # Si es el tipo que queremos (SoftwareApplication) lo tomamos
            if data.get("@type") == "SoftwareApplication":
                app_data = data
                break

        if not app_data:
            raise ValueError("No se encontró el bloque de SoftwareApplication en la página")

        offers = app_data.get("offers", {})
        price = offers.get("price")
        currency_value = offers.get("priceCurrency")

        if price is None:
            raise ValueError("No se encontró el precio en la página")

        try:
            price_value = float(price)
        except (ValueError, TypeError):
            price_value = 0.0

        return price_value, currency_value or ""

    def _scrape_app(self, app_name: str, url: str) -> Tuple[Optional[str], bool]:
        """
            Scrappea una app individual
            Returns:
                Tuple[precio, es_error_404]
        """
        try:
            response = self.session.get(url, timeout=10)

            # Manejo de error 404
            if response.status_code == 404:
                return None, None, True

            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            price, currency = self._extract_price(soup)

            return price, currency, False
        except requests.RequestException as e:
            print(f"Error al consultar {app_name}: {e}")
            return None, None, False

    def scrape_apps(self, apps: Dict[str, str]) -> ScrapResult:
        """
            Scrappea todas las apps del diccionario
            Args:
                apps: Diccionario con {nombre_app: url}
            Returns:
                ScrapResult con los resultados categorizados
        """
        paid_apps = dict()
        free_apps = list()
        failed_apps = list()

        total = len(apps)
        print(f"\n{'=' * 50}")
        print(f"Total de apps a buscar: {total}")
        print(f"{'=' * 50}\n")

        for idx, (app_name, url) in enumerate(apps.items(), 1):
            print(f"[{idx}/{total}] Consultando: {app_name}...", end=" ")

            price, currency, is_404 = self._scrape_app(app_name, url)

            if is_404:
                print("[ERROR] - Error 404")
                failed_apps.append(app_name)
            elif price is None:
                print("[ERROR] - Sin precio")
                failed_apps.append(app_name)
            elif isinstance(price, float):
                if price == 0.0:
                    print("✓ Gratis")
                    free_apps.append(app_name)
                else:
                    print(f"✓ {price} {currency}")
                    paid_apps[app_name] = f"{price} {currency}"
            elif isinstance(price, str):
                if price.lower() == "gratis":
                    print("✓ Gratis")
                    free_apps.append(app_name)
                else:
                    print("[ERROR] - Campo inválido")
                    failed_apps.append(app_name)
            else:
                print("[ERROR] - Campo inválido")
                failed_apps.append(app_name)

            # Delay para evitar rate limiting
            if idx < total:
                time.sleep(self.delay)

        return ScrapResult(
            paid_apps=paid_apps,
            free_apps=free_apps,
            failed_apps=failed_apps
        )

    def print_results(self, result: ScrapResult):
        """
            Imprime los resultados de forma legible
        """
        print(f"\n{'=' * 50}")
        print("RESUMEN DE RESULTADOS")
        print(f"{'=' * 50}\n")

        print(f"Aplicaciones de pago ({len(result.paid_apps)}):")
        if result.paid_apps:
            for app, price in result.paid_apps.items():
                print(f" • {app}: {price}")
        else:
            print(" (ninguna)")

        print(f"\nAplicaciones gratis ({len(result.free_apps)}):")
        if result.free_apps:
            for app in result.free_apps:
                print(f" • {app}")
        else:
            print(" (ninguna)")

        print(f"\nAplicaciones fallidas ({len(result.failed_apps)}):")
        if result.failed_apps:
            for app in result.failed_apps:
                print(f" • {app}")
        else:
            print(" (ninguna)")

        print(f"\n{'=' * 50}\n")
