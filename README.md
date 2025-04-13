
# NBA Oyuncu İstatistikleri Çekme ve Görselleştirme Projesi

Bu proje, [NBA'in resmi istatistik sayfasından](https://www.nba.com/stats/players/traditional) oyuncu istatistiklerini çeker, bu verileri işler, oyuncu avatarlarını ekler ve sonunda etkileşimli bir grafik oluşturur.

## Özellikler

-   Güncel NBA oyuncu istatistiklerini web'den kazıma (scraping).
-   Çekilen ham veriyi işleyerek temizleme ve yapılandırma.
-   Oyuncu isimlerine göre avatarlarını bulup veriye ekleme.
-   İşlenmiş veriyi kullanarak [Altair](https://altair-viz.github.io/) kütüphanesi ile etkileşimli bir grafik oluşturma.
-   Oluşturulan grafiği HTML dosyası olarak kaydetme.

## Dosya Yapısı

.
├── data/                     # Script'ler tarafından oluşturulan ve kullanılan veriler
│   ├── nba_player_stats.csv
│   ├── nba_player_stats.json
│   ├── nba_player_stats_with_images.csv
│   ├── nba_stats_page.html
│   └── processed_players_for_visualization.csv
├── scrape_nba_stats.py       # NBA web sitesinden verileri çeker ve kaydeder.
├── process_data.py           # Ham veriyi işler.
├── add_avatars.py            # Oyuncu avatarlarını bulur ve CSV'ye ekler.
├── create_chart.py           # İşlenmiş veriden Altair grafiğini oluşturur.
├── finalize_visualization.py # Oluşturulan grafiği sonlandırır ve kaydeder.
├── requirements.txt          # Gerekli Python kütüphaneleri (Aşağıya bakın)
└── README.md                 # Bu dosya


*(Not: `setup.py.py` dosyası listede görünmektedir, ancak genellikle bu dosyanın adı `setup.py` olur. Eğer paket kurulumu için kullanılacaksa, adını düzeltmek ve içeriğini uygun şekilde doldurmak gerekebilir.)*

## Gereksinimler

Projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyacınız vardır:

-   `pandas`
-   `requests`
-   `beautifulsoup4`
-   `Pillow` (PIL)
-   `altair`
-   `altair_saver` (Grafiği dosya olarak kaydetmek için)
-   `selenium` (Eğer `altair_saver` için `vl-convert` gerekiyorsa)

Bu kütüphaneleri yüklemek için bir `requirements.txt` dosyası oluşturup aşağıdaki komutu kullanabilirsiniz:

```bash
pip install -r requirements.txt

requirements.txt içeriği:

pandas
requests
beautifulsoup4
Pillow
altair
altair-saver
selenium # veya vl-convert kurulumu için gerekli diğer adımlar

Not: altair_saver'ın çalışması için sisteminizde vl-convert (ve dolayısıyla Node.js) veya selenium (ve bir webdriver) kurulu olması gerekebilir. Kurulum detayları için Altair Saver dokümantasyonuna bakınız.
Kullanım

Grafiği oluşturmak için script'leri aşağıdaki sırayla çalıştırmanız gerekmektedir:

    Veriyi Çekme:
    Bash

python scrape_nba_stats.py

Bu script, data klasörü içine nba_stats_page.html, nba_player_stats.csv ve nba_player_stats.json dosyalarını oluşturur/günceller.

Veriyi İşleme:
Bash

python process_data.py

Bu script, nba_player_stats.csv dosyasını okur ve işler. (Script'in çıktıyı nereye kaydettiğini kontrol edin, muhtemelen üzerine yazar veya yeni bir dosya oluşturur).

Avatarları Ekleme:
Bash

python add_avatars.py

Bu script, işlenmiş oyuncu verisine avatarları ekler ve data/nba_player_stats_with_images.csv dosyasını oluşturur/günceller.

Grafiği Oluşturma:
Bash

python create_chart.py

Bu script, avatarlı veriyi kullanarak Altair grafiğini hazırlar ve data/processed_players_for_visualization.csv gibi bir ara dosya oluşturabilir.

Grafiği Kaydetme:
Bash

    python finalize_visualization.py

    Bu script, oluşturulan Altair grafiğini alır ve muhtemelen nba_player_stats_visualization.html (veya benzer bir isimde) bir HTML dosyası olarak kaydeder.

Çıktı

Script'ler başarıyla çalıştırıldıktan sonra, projenin ana dizininde (veya finalize_visualization.py script'inde belirtilen yerde) nba_player_stats_visualization.html gibi bir HTML dosyası bulacaksınız. Bu dosya, oyuncu istatistiklerini gösteren etkileşimli grafiği içerir.
