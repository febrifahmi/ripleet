# Ripleet

[Ripleet](http://www.rippleet.com), a social media "ripple" miner and Business Intelligence platform.

# Tentang Rippleet

**Rippleet** merupakan platform analytics yang menggabungkan antara *social media analytics*, *online mainstream media analytics*, dengan indikator-indikator sosial, ekonomi, dan lingkungan dalam suatu *Dashboard monitoring* yang dapat disesuaikan dengan kebutuhan pengguna.

Rippleet mengombinasikan sumber data seperti **Twitter Streaming API**, artikel terkini dari mainstream *news media online*, data kejadian bencana dan kondisi cuaca maupun lingkungan terkini dari BMKG, dan data indikator sosial ekonomi masyarakat dari BPS.

Kami di Rippleet melihat bahwa organisasi khususnya organisasi yang bergerak di sektor kebijakan publik perlu memiliki *'agility'* dan *'responsiveness'* sebagaimana sektor privat dan dunia usaha. Para pemangku kepentingan di sektor publik perlu memiliki kemampuan melihat sinyal-sinyal keberhasilan maupun kegagalan pembangunan sedini mungkin melalui berbagai 'sensor' dan indikator yang ada/sudah tersedia.

Nama 'Rippleet', berasal dari kata *'ripple'* dan *'fleet'* yang bermakna bahwa Rippleet memiliki visi menjadi 'armada' yang mampu menangkap 'gelombang-gelombang' maupun 'riak' informasi dan sinyal dari suatu fenomena ataupun persepsi publik terhadap suatu produk dan layanan. Data dan informasi yang ditangkap dan dikumpulkan melalui Rippleet ini akan diolah sehingga dapat dimanfaatkan organisasi untuk segera melakukan pembenahan dan perbaikan layanan tanpa harus menunggu *feedback* melalui kanal tradisional seperti Kotak Pos Aduan dan Saran maupun *Complaint Handling System* tradisional lainnya yang mensyaratkan bahwa masyarakat aktif untuk memberikan feedback melalui kanal khusus yang disediakan.

Di Rippleet, kami melakukan 'jemput bola' dengan langsung mengumpulkan berbagai sinyal yang telah tersedia secara aktif. Kami tidak menunggu publik untuk memberikan *feedback*, namun kami langsung membaca fenomena dan persepsi yang berkembang di tengah masyarakat. Kami memanfaatkan berbagai metode pengumpulan data dan informasi terkini dalam sebuah *'data pipeline'* yang mutakhir dan memanfaatkan sepenuhnya teknologi Big Data yang telah berkembang.

# Tech Stack

Rippleet's technology stack (*subject to change in the near future*):

<img src="https://github.com/febrifahmi/ripleet/blob/master/rippleet_techstack_rev1.png"></img>

Saat ini, hanya `TwitterStreamingAPI`->`tweepy`->`PostgreSQL`/`ElasticSearch`->`Grafana` dan `Online News`->`scraper`->`PostgreSQL`/`ElasticSearch`->`Grafana` yang diimplementasikan di Rippleet. Namun, mesin ES *most of the time* tidak operasional karena keterbatasan storage dan bandwidth VPS yang saya sewa. Anda dapat menghubungi saya via email untuk mengajukan permohonan akses ke [Rippleet](http://www.rippleet.com). 

# Tentang Dashboard Rippleet

Dashboard ini dikhususkan untuk memberikan sedikit gambaran tentang bagaimana Anda dapat memanfaatkan data yang terdapat di server rippleet.

Data di server rippleet dikumpulkan dan disimpan dalam dua format: index document dan database PostgreSQL.

Untuk dapat memanfaatkan data yang telah kami kumpulkan, Anda perlu memahami dahulu dua tipe query, yaitu: **lucene query** untuk memanggil data dari index ES, dan **PostgreSQL query** untuk memanggil data yang disimpan dalam tabel PostgreSQL.

*Saat ini kami mengalami 'kehabisan resource' untuk mesin indexing ES, sehingga ES cluster biasanya tidak akan bisa diakses dan dijadikan source data dan menampilkan tanda seru merah.

Saat ini hanya data dari database PostgreSQL yang dapat anda panggil.

Untuk itu anda harus mengetahui beberapa informasi berikut:

1. Data tweet yang dikumpulkan terletak di Tabel "rippleet_twit";
2. Data berita online yang dikumpulkan terletak di Tabel "rippleet_news";
3. Kami saat ini sedang mencoba menambahkan data indikator pembangunan dari BPS API, dan data monitoring dan prediksi kondisi cuaca dan bencana dari BMKG;
4. Anda memanggil data dengan format misalnya seperti berikut:

`SELECT timecol AS "time", tweet AS "raw_tweet", FROM rippleet_tweet WHERE tweet LIKE '%infrastruktur%' OR tweet LIKE '%jalan tol%' GROUP BY timecol`

# Rippleet Bot/Scraper

Rippleet menambahkan Tweet scaper di dalam kodenya (`rippleet_bot.py`). Berikut ini beberapa operators yang dapat digunakan dalam Twitter search:

| Operators                         | Finds tweest...                                                           |
|-----------------------------------|---------------------------------------------------------------------------|
| twitter search                    | containing both "twitter" and "search". This is the default operator.     |
| "happy hour"                      | containing the exact phrase "happy hour".                                 |
| love OR hate                      | containing either "love" or "hate" (or both).                             |
| beer -root                        | containing "beer" but not "root".                                         |
| #haiku                            | containing the hashtag "haiku".                                           |
| from:alexiskold                   | sent from person "alexiskold".                                            |
| to:techcrunch                     | sent to person "techcrunch".                                              |
| @mashable                         | referencing person "mashable".                                            |
| "happy hour" near:"san francisco" | containing the exact phrase "happy hour" and sent near "san francisco".   |
| near:NYC within:15mi              | sent within 15 miles of "NYC".                                            |
| superhero since:2010-12-27        | containing "superhero" and sent since date "2010-12-27" (year-month-day). |
| ftw until:2010-12-27              | containing "ftw" and sent up to date "2010-12-27".                        |
| hilarious filter:links            | containing "hilarious" and linking to URLs.                               |
| news source:"Twitter Lite"        | containing "news" and entered via Twitter Lite                            |


# Code

Kode yang terdapat dalam Rippleet sebagian besar merupakan modifikasi dari berbagai sumber. Pada umumnya implementasi kode tersebut dimodifikasi dari kode solusi yang terdapat di Stackoverflow, kecuali yang tertulis eksplisit dalam kode. Hanya bagian-bagian kecil saja yang saya tulis dari nol dan digabungkan dengan kode lain.
Untuk itu, kredit untuk para penulis kode aslinya.  
