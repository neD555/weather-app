## Weather app

Простое веб-приложение на Flask, показывает текущую температуру по данным Open-Meteo. Упаковано в Docker. Мониторинг реализован через Prometheus и blackbox-exporter.

Запуск:

docker compose up -d

URL:
http://localhost:8000/
http://localhost:8000/weather
http://localhost:8000/health
http://localhost:8000/metrics
http://localhost:9090/
