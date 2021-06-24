# BistBot
Python yfinance kütüphanesi kullanılarak bist hisselerini takip edip Telegram botuna mesaj gönderen uygulama

BistBot ***
Bist100'deki bütün hisseler endeksin açık olduğu saatler içerisinde taranacak ve herhangi bir hissede
- Fiyat son 50 günlük ortalamanın üzerine çıktığında veya altına düştüğünde
- Fiyat son 200 günlük ortalamanın üzerine çıktığında veya altına düştüğünde
- Hacim 10 günlük hacmin üzerine çıktığında veya altına indiğinde
- Hacim 3 aylık hacmin üzerine çıktığında veya altına indiğinde
- Fiyat defter değerinin üzerine çıktığında veya altına düştüğünde
- Fiyat 52 haftalık en yüksek veya en düşük değerse
bildirim gönderecek. Ayrıca eğer bir hissede 
- Fiyat 50 günlük ve 200 günlük ortalama fiyatların altında ve defter değerinin altındaysa
- Fiyat 50 günlük ortalamanın altında ve hacim 10 günlük ve 3 aylık ortalama hacmin üzerindeyse
o hisse takip listesine eklenecek ve bu takip listesi gün içerisinde her iki saatte bir bildirim olarak iletilecektir.
- Ayrıca her gün saat 19:00'da Bis100'deki temettü dağıtacak hisselerin bilgileri bota gönderilecektir.

Bot Pazartesi - Cuma saat 10:00 - 18:20 arasında hisse senetlerindeki fiyat değişimlerini takip edecek ve saat 19:00'da temettü bilgilerini gönderecek şekilde ayarlanmıştır.
Bu saatler dışında her hangi bir takip yapmayacaktır.

Gerekli Kütüphaneler:
- Python yfinance; pip install yfinance
- Python requests; pip install requests

Ayrıca telegram üzerinden bot oluşturarak bu botun token ve chat id'leri config.py dosyasında gerekli yere yazılmalıdır.
