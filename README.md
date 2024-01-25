Создать каталог и перейти в него
```
mkdir project && cd project
```
Склонировать репозиторий
```
git clone https://github.com/Ligh7Fun/Aiohttp_HW.git .
```


Установить docker
```
curl -sSL https://get.docker.com/ | sh
```
Установить docker-compose
```
apt install -y docker-compose
```

Проверить что все установилось, в ответе должны быть версии
```
docker-compose -v && docker -v
```

Запустить
```
docker-compose up -d
```
Проверить контейнеры
```
docker ps
```
Использовать запросы из clients.http заменив адрес сервера