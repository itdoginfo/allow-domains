Поможем провайдерам в эпоху дефицита сетевого оборудования: самостоятельно заблокируем ресурсы на своих роутерах и, таким образом, снизим нагрузку на их оборудование!

Зарубежные сервисы пусть знают, что их ресурсы никому не нужны и мы сами у себя их блокируем!

# Форматы списков
- Dnsmasq nfset. Для Dnsmasq в формате nftables set (OpenWrt >=23.05) `nftset=/showip.net/4#inet#fw4#vpn_domains`
- Dnsmasq ipset. Для Dnsmasq в формате ipset (OpenWrt <= 21.02) `ipset=/showip.net/vpn_domains` 
- Sing-box Source. Для Sing-box версии 1.11.0 и выше.
- Xray Dat. Общий файл geosite.dat с разбивкой по категориям.
- ClashX `DOMAIN-SUFFIX,showip.net`
- Mikrotik FWD `/ip dns static add name=fast.com type=FWD...`
- Kvas. Для Kvas 1.1.8 и новее. Просто отсортированный список доменов.
- RAW. Список "как есть"

Конфигурация для Dnsmasq добавляет все зарезолвенные IP-адреса в set `vpn-domain`. И можно оперировать этим списком. Заблокировать, конечно же, все эти IP к чертям.

# Сервисы, категории, страны
Для удобства блокировки списки разделены по категориям, сервисам и странам.

## Категории
- Anime
- Block
- GeoBlock
- News
- Porn

## Сервисы
- Cloudflare
- Discord
- HDRezka
- Meta* 
- Telegram
- Tik-Tok
- Twitter
- YouTube

## Страны
### Россия
Есть два списка: один - для пользователей в России, другой - для тех, кто находится за её пределами

#### Russia inside
Ресурсы, которые блокируются, в том числе и зарубежные ресурсы, которые сами блокируют российские подсети. Состоит из:
- Anime
- Block
- GeoBlock
- News
- Porn
- HDRezka
- Meta*
- Tik-Tok
- Twitter
- YouTube

#### Russia outside
Списки российских ресурсов, которые доступны только для российских подсетей. Для людей за границей, которым нужен доступ к российским сервисам.

### Украина
Список заблокированных ресурсов в Украине. Списки берутся с ресурсов https://uablacklist.net/ и https://zaborona.help/.

# Прямые ссылки на списки
Все ссылки спрятаны под спойлеры — нажмите на нужный список, чтобы раскрыть его.

Общий файл для Xray [geosite.dat](https://github.com/itdoginfo/allow-domains/releases/latest/download/geosite.dat)

<details>
  <summary>Russia inside</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-raw.lst)
- [Dnsmasq nfset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-nfset.lst)
- [Dnsmasq ipset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-ipset.lst)
- [ClashX](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-clashx.lst)
- [Kvas](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-kvas.lst)
- [Mikrotik](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Russia/inside-mikrotik-fwd.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/russia_inside.srs)
- geosite:russia-inside

</details>

<details>
  <summary>Russia Outside</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-raw.lst)
- [Dnsmasq nfset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-dnsmasq-nfset.lst)
- [Dnsmasq ipset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-dnsmasq-ipset.lst)
- [ClashX](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-clashx.lst)
- [Kvas](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/outside-kvas.lst)
- [Mikrotik](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Russia/outside-mikrotik-fwd.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/russia_outside.srs)
- geosite:russia-outside

</details>

<details>
  <summary>Ukraine</summary>

- [Dnsmasq nfset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-dnsmasq-nfset.lst)
- [Dnsmasq ipset](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-dnsmasq-ipset.lst)
- [ClashX](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-clashx.lst)
- [Kvas](https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Ukraine/inside-kvas.lst)
- [Mikrotik](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Ukraine/inside-mikrotik-fwd.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/ukraine_inside.srs)
- geosite:ukraine

</details>

<details>
  <summary>Anime</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/anime.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/anime.srs)
- geosite:russia-inside@anime

</details>

<details>
  <summary>Block</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/block.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/block.srs)
- geosite:russia-inside@block

</details>

<details>
  <summary>GeoBlock</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/geoblock.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/geoblock.srs)
- geosite:russia-inside@geoblock

</details>

<details>
  <summary>News</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/news.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/news.srs)
- geosite:russia-inside@news

</details>

<details>
  <summary>Porn</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/porn.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/porn.srs)
- geosite:russia-inside@porn

</details>

<details>
  <summary>H.O.D.C.A (Hetzner, OVH, DO, Cloudflare, AWS</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Categories/hodca.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/hodca.srs)
- geosite:russia-inside@hodca

</details>

<details>
  <summary>Cloudflare</summary>

- [Subnets](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/cloudflare.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/cloudflare.srs)

</details>

<details>
  <summary>Discord</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/discord.lst)
- [Subnets](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/discord.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/discord.srs)

</details>

<details>
  <summary>HDRezka</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/hdrezka.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/hdrezka.srs)
- geosite:russia-inside@hdrezka

</details>

<details>
  <summary>Meta*</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/meta.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/meta.srs)
- [Subnets](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/meta.lst)
- geosite:russia-inside@meta

</details>

<details>
  <summary>Telegram</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/telegram.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/telegram.srs)
- [Subnets](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/telegram.lst)

</details>

<details>
  <summary>Tik-Tok</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/tiktok.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/tiktok.srs)
- geosite:russia-inside@tiktok

</details>

<details>
  <summary>Twitter</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/twitter.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/twitter.srs)
- [Subnets](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Subnets/IPv4/twitter.lst)
- geosite:russia-inside@twitter

</details>

<details>
  <summary>YouTube</summary>

- [RAW](https://raw.githubusercontent.com/itdoginfo/allow-domains/refs/heads/main/Services/youtube.lst)
- [SRS](https://github.com/itdoginfo/allow-domains/releases/latest/download/youtube.srs)
- geosite:russia-inside@youtube

</details>

# Как найти все-все домены ресурса?
https://itdog.info/analiziruem-trafik-i-opredelyaem-domeny-kotorye-ispolzuyut-sajty-i-prilozheniya/

# Ресурсы, которых намеренно нет в общих списках

1. В списке GeoBlock больше нет доменов, относящихся к Google AI. Они идут [отдельным списком](https://github.com/itdoginfo/allow-domains/blob/main/Services/google_ai.lst). Это сделано по причине, что многие иностранные серверы Google помечает как RU. 

# Как добавить домены в списки?
Приветствуется добавление новых доменов и удаление неактуальных.

Для каждого списка создана тема в Discussion. Правила оформления указаны в первом сообщении
- [Россия inside](https://github.com/itdoginfo/allow-domains/discussions/75)
- [Россия outside](https://github.com/itdoginfo/allow-domains/discussions/2)

# Как заблокировать на своём роутере?
1. В Podkop выберите mode **Block**

2. Пример блокировки по списку доменов на роутере с OpenWrt 23.05.

Нужен dnsmasq-full. Загружаем конфиг в tmp/dnsmasq.d. Создаём ipset, все пакеты к ip-адресам из этого ipset будут дропаться.

```
cd /tmp/ && opkg download dnsmasq-full
opkg remove dnsmasq && opkg install dnsmasq-full --cache /tmp/
cp /etc/config/dhcp /etc/config/dhcp-old && mv /etc/config/dhcp-opkg /etc/config/dhcp

cd /tmp/dnsmasq.d && wget https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-dnsmasq-nfset.lst -O domains.conf

uci add firewall ipset
uci set firewall.@ipset[-1].name='vpn_domains'
uci set firewall.@ipset[-1].match='dst_net'
uci add firewall rule
uci set firewall.@rule[-1]=rule
uci set firewall.@rule[-1].name='block_domains'
uci set firewall.@rule[-1].src='lan'
uci set firewall.@rule[-1].dest='*'
uci set firewall.@rule[-1].proto='all'
uci set firewall.@rule[-1].ipset='vpn_domains'
uci set firewall.@rule[-1].family='ipv4'
uci set firewall.@rule[-1].target='DROP'
uci commit

service firewall restart && service dnsmasq restart
```

# Можно ли добавить другие форматы и страны?
Да, это приветствуется. Для этого создайте issue.

## Для добавления новой страны необходимо указать
- Название страны
- Список заблокированных ресурсов. Нет ограничений на количество, их может быть хоть 5, хоть 100. Можно будет пополнять со временем
- Есть ли ресурсы, которые уже собирают такие списки

## Для добавления нового формата необходимо указать
- Название формата и пример форматирования доменов в этом формате
- Как этот формат можно использовать, с примером (Программа, конфигурация)
- Можно ли как-то тестировать список, если да, то как. Это нужно, чтобы пользователи всегда имели рабочий конфиг

*Meta признана экстремистской и террористической организацией в России

---

[Telegram-канал с обновлениями](https://t.me/itdoginfo)
