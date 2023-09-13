Поможем провайдерам в эпоху дефицита сетевого оборудования, заблокируем самостоятельно ресурсы на своих роутерах и, таким образом, снизим нагрузку на их оборудование!

Зарубежные сервисы пусть знают, что их ресурсы никому не нужны и мы сами у себя их блокируем!

# Списки заблокированных ресурсов
Списки доступны в нескольких форматах:
- RAW - это список доменов и субдоменов
- Dnsmasq-ipset - список для Dnsmasq в формате ipset (OpenWrt <= 21.02)
- Dnsmasq-nfset - список для Dnsmasq в формате nftables set (OpenWrt >=22.03). Для работы c доменами в 22.03 требуется [установить](https://t.me/itdoginfo/12) dnsmasq-full из snapshot версии.

Конфигурация для Dnsmasq добавляет все зарезолвенные IP-адреса в set `vpn-domain`. И можно оперировать этим списком. Заблокировать, конечно же, все эти IP к чертям.

## Россия
Есть два списка, один для людей, находящихся в России, второй для людей заграницей.

- Ресурсы, которые блокирует провайдеры по наводке РКН, и зарубежные ресурсы, которые сами блокируют российские подсети. (inside)
- Списки российских ресурсов, которые доступны только для российских подсетей.  Для людей за границей, которым нужен доступ к российским сервисам. Использовать вместе с VPN расположенным в России. (outside)

Находятся в каталоге **Russia**.

Inside:
- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-raw.lst)
- [Dnsmasq nfset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-nfset.lst)
- [Dnsmasq ipset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-ipset.lst)
- [ClashX](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-clashx.lst)

Outside:
- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-raw.lst)
- [Dnsmasq nfset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-dnsmasq-nfset.lst)
- [Dnsmasq ipset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-dnsmasq-ipset.lst)
- [ClashX](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-clashx.lst)

## Украина
Список заблокированных ресурсов в Украине. Списки берутся с ресурса https://uablacklist.net/, который предоставляет их в RAW формате.

Преобразуются в формат Dnsmasq. При этом удаляются домены с кириллическими буквами. 

Находятся в каталоге **Ukraine**.

- [Dnsmasq nfset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-dnsmasq-nfset.lst)
- [Dnsmasq ipset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-dnsmasq-ipset.lst)
- [ClashX](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-clashx.lst)

# Как добавить домены в списки?
Приветствуется добавление новых доменов и удаление неактуальных.
Есть несколько вариантов:

1. Для каждого списка создана тема в Discussion. Пишите туда отдельные домены или прям список доменов сервиса
- [Россия inside](https://github.com/itdoginfo/allow-domains/discussions/1)
- [Россия outside](https://github.com/itdoginfo/allow-domains/discussions/2)

2. Сделать PR. Списки находятся в `src`. Если у ресурса больше двух доменов, сгруппируйте их отдельным списком и вставьте заголовок ресурса с помощью `#`. Ориентируйтесь на то, как уже сделаны другие

3. Напишите в [чат](https://t.me/itdogchat)

# Как устроено?
Список **Russia inside** формируются из списка https://community.antifilter.download/ и списка `src/Russia-domains-inside.lst`. Они объединяются, удаляются повторы и сортируются по алфавиту. 

Список **Russia outside** формируется из списка `src/Russia-domains-outside.lst`. Также происходит сортировка по алфавиту.

Dnmasq работает по wildcard. Это означает, что при добавлении домена `domain.com`, в списки IP-адресов будут добавляться также все поддомены `subdomain.domain.com`. Поэтому Dnsmasq списки состоят только из доменов второго уровня. Повторы удаляются, удаляются субдомены с `google.com` и происходит сортировка.

Списки обновляются при каждом коммите в репозитории с помощью GitHub Actions. Также скрипт `convert.py` запускается каждые 8 часов, чтобы синхронизировать списки со сторонними сервисами.

При формировании Dnsmasq списков происходит тестирование конфигов с помощью [Dnsmasq action](https://github.com/marketplace/actions/dnsmasq-configuration-check).

# Можно ли добавить другие форматы и страны?
Да, это приветствуется. Для этого создайте issue или напишите в чат.

## Для добавления новой страны необходимо указать
- Название страны
- Список заблокированных ресурсов. Нет ограничений на количество, их может быть хоть 5, хоть 100. Можно будет пополнять со временем
- Есть ли ресурсы, которые уже собирают такие списки

## Для добавления нового формата необходимо указать
- Название формата и пример форматирования доменов в этом формате
- Как этот формат можно использовать, с примером (Программа, конфигурация)
- Можно ли как-то тестировать список, если да, то как. Это нужно, чтобы пользователи всегда имели рабочий конфиг

Также вы можете создать PR с уже необходимыми правками. В этом случае опишите это всё в его Description.

---

[Telegram-канал с обновлениями](https://t.me/itdoginfo)
