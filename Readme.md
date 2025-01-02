# Kurulum

Bu server yazılımı private network'de çalışacağından HTTPS için geçerli genel sertifika kullanılmamıştır. İstenirse geçerli bir sertifika alınıp onun dosyaları da kullanılabilir.

## Sertifika Dosyası Oluşturmak için OpenSSL Kurulumu

### Linux
```bash
sudo apt update
sudo apt install openssl

# Sertifika dosyalarının oluşturulacağı klasör
md certificates
cd certificates

# 10 yıl geçerli sertifika dosyalarını oluştur
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 3650 -out server.crt
```

### Windows 11
1. OpenSSL'i kurun: Windows üzerinde OpenSSL kurulumunu yapmak için Win32 OpenSSL ya da OpenSSL for Windows gibi bir dağıtım seçebilirsiniz. Kurulumdan sonra, OpenSSL'in `bin` dizininin PATH çevresel değişkenine eklendiğinden emin olun.
2. Komut İstemi veya PowerShell'i açın (yönetici modunda).

```bash
md certificates
cd certificates

# Kendinden imzalı bir sertifika ve anahtar oluşturun:
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 3650 -out server.crt
```

## Projenin İndirilmesi ve Kurulumu

### Home Klasörüne Dönüş ve Projeyi Çekme
```bash
cd
git clone git@github.com:drcoskun/BT_RestAPI_Server.git
```

### Gerekli Altyapı Kurulumları

#### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install flask flask_jwt_extended flask_cors
```

#### Windows 11
1. Python’u [resmi web sitesinden](https://www.python.org) indirin ve yükleyin.
2. Kurulum sırasında "Add Python 3.x to PATH" seçeneğini işaretleyin.
3. Yönetici modunda Komut İstemi veya PowerShell'i açarak aşağıdaki komutları çalıştırın:

```bash
pip3 install flask flask_jwt_extended flask_cors
```

## BT_RestAPI_Server'ın Kullanımı

### Komut Dosyası

```bash
cd ~/BT_RestAPI_Pub_Server
nano command.json
```

**Boş Komut İçeriği:**
```json
{
    "command": ""
}
```

**Reboot Komutu İçeriği:**
```json
{
    "command": "reboot"
}
```

> "reboot" komutu girildikten en fazla 60 saniye sonra cihaz yeniden başlatılacaktır (bu süre client'da set edilmiştir).

**RFID Kart Listesi Güncelleme Örneği:**
```json
{
    "command": "rfidListUpdate",
    "rfidList": [
        "0262363499",
        "0123593937"
    ]
}
```

### Sunucunun Çalıştırılması
```bash
python3 app.py
```

> **Not:** İstenirse `app.py`, bir sistem servisi olarak da yapılandırılabilir.

### Kayıt Dosyası
`app.py` ile BT_RestAPI_Server çalıştırıldıktan sonra şarj cihazından gelen raporlar `saved_data.json` dosyasına kaydedilir. Bu dosyanın silinmesi, sistem çalışmasını etkilemez.

## Konfigürasyon

Sunucunun çalışması için gerekli tanımlar `serversettings.json` dosyasında düzenlenmelidir. Örnek yapı aşağıda verilmiştir:

```json
{
    "API_KEY": "Your_ApiKey",
    "JWT_SECRET_KEY": "Your_SecretKey",
    "jwt_token_duration": 48,
    "certificate_crt_path": "C:/your_path/server.crt",
    "certificate_key_path": "C:/your_path/server.key",
    "command_file": "command.json",
    "report_file": "saved_data.json"
}
```

Başka bir örnek:

```json
{
    "API_KEY": "Your_ApiKey",
    "JWT_SECRET_KEY": "Your_SecretKey",
    "jwt_token_duration": 48,
    "certificate_crt_path": "C:/your_path/server.crt",
    "certificate_key_path": "C:/your_path/server.key",
    "command_file": "command.json",
    "report_file": "saved_data.json"
}
```

## Notlar

- BT_RestAPI_Server, mümkün olduğunca basit bir yapıda tutulmuştur.
- İstenirse komut yollama veya gelen raporu okuma kısımları, kullanıcı tarafından değiştirilebilir ve sisteme entegre edilebilir.
