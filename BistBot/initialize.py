from functions import *

createTables()
shareList = getShareList()
startupMessage = """
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
- Her gün saat 19:00'da Bis100'deki temettü dağıtacak hisselerin bilgileri Telegram bot'a gönderilecektir.
"""