# 📲 AppStore Scraper
> ℹ️ Script para búsqueda de Apps en la AppStore de Europa (€ como moneda). Si se desea cambiar la AppStore se debe modificar la moneda en circulación.

Script desarrollado en Python para ayudar a usuarios de dispositivos **Apple** a buscar las Apps que deseen conocer si son de pago o son gratuitas.

## Setup

1. Clonar el repositorio:
```bash
git clone https://github.com/alexisnlh/AppStore-Scraper.git
cd appstore-scraper
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar las apps:
```bash
cp apps_config.example.json apps_config.json
```

5. Editar `apps_config.json` con tus apps

6. Ejecutar:
```bash
python scraper_main.py
```

## Estructura de archivos

```
appstore-scraper/
├── appstore_scraper.py         # Clase principal del scraper
├── config.py           # Cargador de configuración
├── scraper_main.py         # Script principal
├── apps_config.example.json        # Ejemplo de configuración
├── apps_config.json        # Configuración real
├── .gitignore          # Archivos a ignorar
├── requirements.txt        # Dependencias
└── README.md
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Alexis NLH**

- GitHub: [@alexisnlh](https://github.com/alexisnlh)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
