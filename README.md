# ripleet
Ripleet, a social media "ripple" miner and Business Intelligence platform.

The technology stack:

<img src="https://github.com/febrifahmi/ripleet/blob/master/rippleet_techstack_rev1.png"></img>

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
