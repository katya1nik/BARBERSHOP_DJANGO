# Gunicorn конфигурация для production
import multiprocessing

# Количество рабочих процессов
workers = multiprocessing.cpu_count() * 2 + 1

# Тип рабочих процессов
worker_class = 'sync'

# Время ожидания для рабочих процессов
timeout = 120

# Максимальное количество запросов на рабочий процесс
max_requests = 1000
max_requests_jitter = 100

# Перезапуск рабочих процессов
preload_app = True

# Логирование
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Биндинг
bind = '127.0.0.1:8000'

# Пользователь и группа (для Linux)
# user = 'www-data'
# group = 'www-data'

# PID файл
pidfile = '/tmp/gunicorn.pid'

# Перезапуск при изменении кода
reload = False
