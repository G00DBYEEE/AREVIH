# HIVERA Bot

HIVERA adalah bot berbasis Python untuk mengotomatisasi tugas-tugas Telegram, termasuk login ke beberapa sesi, menjalankan tugas harian, dan mengirimkan data ke API developer. Proyek ini menggunakan **TelegramClient**, **aiohttp**, dan pustaka lainnya untuk mendukung operasi berbasis asynchronous.

## Fitur Utama

- **Dukungan Proxies dengan Password**: Memuat proxies dari file `proxies.txt`, mendukung tipe `http` dan `socks` dengan autentikasi username dan password.
- **Auto Referal**: Mengirimkan referal secara otomatis ke URL yang ditentukan.
- **Tugas Harian**: Menjalankan beberapa tugas harian seperti pengambilan informasi mesin, kontribusi data, dan tugas harian lainnya dari API.
- **Informasi Akun Telegram**: Mengambil informasi dasar akun Telegram dari setiap sesi.
- **Konfigurasi Asynchronous**: Menjalankan beberapa sesi secara paralel dengan menggunakan `asyncio`.

## Instalasi

1. **Kloning Repository**:

   ```bash
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```

2. **Buat Virtual Environment** (opsional):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate   # Untuk Windows
   ```

3. **Instal Dependensi**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Buat File Konfigurasi .env:**

   Buat file `.env` di root proyek dan tambahkan variabel berikut:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   USE_PROXIES=True        # Atur ke False jika tidak ingin menggunakan proxy
   AUTO_TASK=False         # Atur ke True untuk mengaktifkan tugas otomatis
   REFF_URL=https://example.com/referal
   ```

5. **Siapkan Folder Sesi**:

   Pastikan ada folder `./session/` di root proyek untuk menyimpan file sesi Telegram. Jika belum ada, buat dengan perintah:

   ```bash
   mkdir session
   ```

6. **Siapkan File Proxies**:

   Buat file `proxies.txt` di root proyek dan tambahkan daftar proxies Anda. Contoh:

   ```
   http://username:password@127.0.0.1:8080
   socks5://username:password@127.0.0.1:1080
   ```

## Penggunaan

1. **Jalankan Bot**:

   ```bash
   python bot.py
   ```

2. **Hasil Output**:

   - Informasi tentang keberhasilan login ke sesi Telegram.
   - Tugas harian seperti:
     - Informasi mesin
     - Kontribusi data
     - Tugas harian lainnya dari API
   - Tugas referal otomatis jika diaktifkan.

## Struktur Proyek

- **bot.py**: Skrip utama untuk menjalankan bot.
- **proxies.txt**: File berisi daftar proxies yang akan digunakan.
- **requirements.txt**: Daftar dependensi Python.
- **.env**: File konfigurasi untuk API dan variabel lainnya.
- **session/**: Folder untuk menyimpan file sesi Telegram.

## Catatan Penting

- Pastikan Anda memiliki kredensial API Telegram yang valid.
- Jangan lupa untuk menjaga keamanan file `.env` Anda.
- Jika Anda mengalami kendala dengan proxies, pastikan format dan koneksi proxies sudah benar.

## Kontribusi

Jika Anda ingin berkontribusi, silakan fork repository ini dan kirim pull request Anda.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

---

Dikembangkan dengan ❤️ oleh **GOODBYE**.

