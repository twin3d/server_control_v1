# Task deskription

This is collaborative prototype of code for python for outsoursing tasks and server control.


Soon ansible will be integrated in our flow, however we need tool for discovering and updating host ip's I propose do interface_list tool which discover proper host IPs on the network. 


# Step 1 Minimal working ping tool
Task is to create python application launched on server control machine which scans in gateway network with intention to find machines where some specific port is open. Client application is also sysemctl launched on client machines. When it is asking on this port host and interface_list control server handshake on this port and if sucsessful, then if server sends interface_list special "ping" commands returns some specific information about the macine such as: prescripted scanner, it's ip, and other information which can be updated however we need.

`class`

## Клиентская часть: 
Создаю class listener(config file (файл в котором прописаны настройки - почитать про конфиг файлы в вики)
посмотреть inicofig (библиотека configparcer) yaml - стандарты написания конфиг файлов
ЧТо нужно прописать в конфиге: порт, 
1. Если в конфиге не указан порт - то дефолтное значение. Можно выдать варнинг.
1. Если есть, то записать из конфига. 
1. Реализовать возможность передачи порта в функцию напрямую

Как работает фукнция в питоне
`def gunc(positional, keyword=defaul,`
позишионал обязаны быть. 
В общем прочитать про функции в питоне

Миша рекомендует сделать позиционным конфиг файл, причем сделать дефолтным значением мой конфиг, но реализовать возможность передачи другого конфига

Пытаться писать максимально абстрактно, чтобы можно было расширять. Потом могут придти другие входные данные в аргументах функции.

Сделать конструктор

Функция должна взять порт и на нем создает сокет и слушает запросы. 





## Серверная часть:
Ищет все компы с открытым нужным портом
Проверка кодового слова: сервер посылает кодовое слово, клиент отвечает,и если слова совпадают - хенд шейк выполнен

`class controller(operation, config)`
в оператион прописывается задача для сервера

у меня будет только один оператион: ping
Что он делает: 
1. он обнаруживает все компы с открытыми портами (возможно это кем-то написано, поискать)
1. делает хендшейк
1. формирует отчет, в каком-нибудь правильном виде

Писать не много, а хорошо


Скорее всего эти задачи кем-то уже решены, поискать в интернете

Первый пункт разделяется:
узнать свой ип или шлюз
узнать маску - те узнать сеть
...





Первый шаг: на питоне написать скрипт, который выводит все ип с открытым определенным портом







