import sys
if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import aiohttp
import asyncio
import os
from telethon import TelegramClient
from dotenv import load_dotenv
from datetime import datetime
from colorama import Fore, Style

# ===== Muat Konfigurasi dari .env =====
load_dotenv()

API_ID = os.getenv('API_ID', 'your_api_id')
API_HASH = os.getenv('API_HASH', 'your_api_hash')
SESSION_DIR = './session/'
PROXIES_FILE = 'proxies.txt'  # Nama file untuk daftar proxies
USE_PROXIES = os.getenv('USE_PROXIES', 'True') == 'True'  # Gunakan proxies jika True
AUTO_TASK = os.getenv('AUTO_TASK', 'False') == 'True'
BASE_URL = 'https://api.unisvg.com'

# ===== Fungsi Utilitas =====
def parse_proxy(proxy_line):
    """Mengurai baris proxy ke dalam format yang dapat digunakan."""
    proxy_parts = proxy_line.split('@')
    if len(proxy_parts) == 2:
        credentials, address = proxy_parts
        proxy_type, proxy_host = address.split('://')
        username, password = credentials.split(':')
        return {
            'proxy_type': proxy_type,
            'address': proxy_host,
            'username': username,
            'password': password
        }
    else:
        proxy_type, proxy_host = proxy_line.split('://')
        return {
            'proxy_type': proxy_type,
            'address': proxy_host,
            'username': None,
            'password': None
        }

def load_proxies():
    """Memuat proxies dari file."""
    if not os.path.exists(PROXIES_FILE) or not USE_PROXIES:
        return []
    with open(PROXIES_FILE, 'r') as f:
        return [parse_proxy(line.strip()) for line in f.readlines()]

async def get_proxy_connector(proxy):
    """Mengembalikan connector untuk proxy dengan kredensial."""
    if not proxy:
        return None
    if proxy['username'] and proxy['password']:
        return aiohttp.ProxyConnector.from_url(
            f"{proxy['proxy_type']}://{proxy['username']}:{proxy['password']}@{proxy['address']}"
        )
    else:
        return aiohttp.ProxyConnector.from_url(
            f"{proxy['proxy_type']}://{proxy['address']}"
        )

# ===== Fungsi untuk Memanggil API Developer =====
async def call_api(endpoint, method='GET', payload=None, proxy=None):
    """Memanggil API dengan endpoint dan payload."""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}

    connector = await get_proxy_connector(proxy)

    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            if method == 'GET':
                async with session.get(url, headers=headers) as response:
                    if response.status == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                        return await response.json()
                    print(f"Unexpected response: {response.status} {await response.text()}")
            elif method == 'POST':
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                        return await response.json()
                    print(f"Unexpected response: {response.status} {await response.text()}")
        except Exception as e:
            print(f"❌ Error saat memanggil {url}: {e}")
            return None

# ===== Fungsi Mining dan API =====
async def fetch_engine_info():
    """Mengambil informasi mesin dari API."""
    data = await call_api('/engine/info')
    if data:
        print(f"✅ Informasi mesin: {data}")
    else:
        print("❌ Gagal mengambil informasi mesin.")

async def contribute_engine_data():
    """Mengirim kontribusi data ke API."""
    payload = {
        'from_date': datetime.now().isoformat(),
        'quality_connection': 75
    }
    data = await call_api('/engine/contribute', method='POST', payload=payload)
    if data:
        print(f"✅ Data kontribusi berhasil: {data}")
    else:
        print("❌ Gagal berkontribusi data.")

async def fetch_daily_tasks():
    """Mengambil tugas harian dari API."""
    data = await call_api('/daily-tasks')
    if data:
        print(f"✅ Tugas harian: {data}")
    else:
        print("❌ Gagal mengambil tugas harian.")

async def fetch_user_modes():
    """Mengambil mode pengguna dari API."""
    data = await call_api('/users/modes')
    if data:
        print(f"✅ Mode pengguna: {data}")
    else:
        print("❌ Gagal mengambil mode pengguna.")

async def fetch_activities():
    """Mengambil aktivitas dari API."""
    data = await call_api('/engine/activities')
    if data:
        print(f"✅ Aktivitas pengguna: {data}")
    else:
        print("❌ Gagal mengambil aktivitas pengguna.")

async def complete_mission(mission_id):
    """Menyelesaikan misi."""
    data = await call_api('/missions/complete', method='POST', payload={'mission_id': mission_id})
    if data and data.get('result') == 'done':
        print(f"✅ Misi {mission_id} berhasil diselesaikan.")
    else:
        print(f"❌ Gagal menyelesaikan misi {mission_id}.")

# ===== Fungsi Utama untuk Tugas =====
async def run_daily_tasks():
    """Menjalankan semua tugas yang diperlukan."""
    await fetch_engine_info()
    await contribute_engine_data()
    await fetch_daily_tasks()
    await fetch_user_modes()
    await fetch_activities()

# ===== Fungsi Telegram =====
async def run_session(session_name, index, proxies):
    """Menjalankan sesi Telegram."""
    session_path = os.path.join(SESSION_DIR, session_name)
    proxy = proxies[index] if index < len(proxies) else None

    proxy_settings = None
    if proxy:
        proxy_settings = {
            'proxy_type': proxy['proxy_type'],
            'addr': proxy['address'].split(':')[0],
            'port': int(proxy['address'].split(':')[1]),
            'username': proxy['username'],
            'password': proxy['password']
        }

    client = TelegramClient(session_path, API_ID, API_HASH, proxy=proxy_settings)
    await client.start()

    print(Fore.LIGHTMAGENTA_EX + f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Berhasil login ke sesi {session_name}" + Style.RESET_ALL)

    await client.disconnect()

async def main():
    """Mengatur sesi, proxies, dan tugas harian untuk dijalankan."""
    print(Fore.LIGHTMAGENTA_EX + "\nHIVERA\nBY: GOODBYE\n" + Style.RESET_ALL)

    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    proxies = load_proxies()
    sessions = [f"session_{i}" for i in range(len(proxies))]

    # Jalankan tugas harian secara langsung
    await run_daily_tasks()

    # Jalankan sesi Telegram
    tasks = [run_session(session, index, proxies) for index, session in enumerate(sessions)]
    try:
        await asyncio.gather(*tasks)
    except (KeyboardInterrupt, SystemExit):
        print('📴 Bot dihentikan.')

if __name__ == '__main__':
    asyncio.run(main())
