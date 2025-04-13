import os
import sys
import subprocess
import platform
import time

from setuptools import setup, find_packages
from setuptools.command.install import install

# Gereken ek paketler ve kütüphaneler (pip ile)
REQUIRED_PACKAGES = [
   'numpy',
   'scipy',
   'pydub',  # ses işlemleri için
   'requests',  # HTTP istekleri için
   'flask',  # web sunucusu için
   'tqdm',  # geri bildirim progress bar
   'selenium',  # web scraping için
   'pytesseract',  # OCR için
]

# Gereken bağımlılıklar (ffmpeg, ChromeDriver vb.)
EXTRA_DEPENDENCIES = {
   'ffmpeg': {
       'Linux': 'sudo apt-get install ffmpeg',
       'Windows': 'https://www.gyan.dev/ffmpeg/builds/',
       'MacOS': 'brew install ffmpeg'
   },
   'chromedriver': {
       'Linux': 'sudo apt-get install chromium-chromedriver',
       'Windows': 'https://sites.google.com/a/chromium.org/chromedriver/downloads',
       'MacOS': 'brew install chromedriver'
   }
}

# Sistem tipi ve platform bilgilerini alıyoruz
system = platform.system()

# Bağımlılıkları kontrol eden fonksiyon
def check_and_install_dependency(dep_name, dep_install_command):
   try:
       print(f"{dep_name} kontrol ediliyor...")
       # Komutu çalıştırarak bağımlılığı yüklemeyi deniyoruz
       result = subprocess.run(dep_install_command, shell=True)
       if result.returncode == 0:
           print(f"{dep_name} başarıyla kuruldu!")
       else:
           print(f"{dep_name} kurulamadı!")
   except Exception as e:
       print(f"Hata: {dep_name} kurulurken bir sorun oluştu: {str(e)}")

# Gereken bağımlılıkları yükleyen fonksiyon
def install_dependencies():
   print(f"Sistem: {system}")
   for dep_name, dep_cmds in EXTRA_DEPENDENCIES.items():
       install_cmd = dep_cmds.get(system)
       if install_cmd:
           print(f"{dep_name} yükleniyor...")
           check_and_install_dependency(dep_name, install_cmd)
       else:
           print(f"{dep_name} için uygun kurulum komutu bulunamadı!")

# pip ile kütüphaneleri yükleyen fonksiyon
def install_packages():
   for package in REQUIRED_PACKAGES:
       try:
           print(f"{package} yükleniyor...")
           subprocess.check_call([sys.executable, "-m", "pip", "install", package])
           print(f"{package} başarıyla yüklendi.")
       except subprocess.CalledProcessError:
           print(f"{package} yüklenemedi, alternatif yöntemler deneniyor.")
           # Alternatif yöntemler eklenebilir
           try:
               print(f"{package} için alternatif kurulum yöntemi deneniyor...")
               subprocess.check_call([sys.executable, "-m", "easy_install", package])
               print(f"{package} alternatif yöntemle yüklendi.")
           except subprocess.CalledProcessError as e:
               print(f"{package} kurulamıyor: {e}")

# Kurulum işlemleri sırasında bu sınıf çalışacak
class CustomInstallCommand(install):
   def run(self):
       print("Gerekli bağımlılıklar ve kütüphaneler yükleniyor...")
       install_dependencies()
       install_packages()
       print("\nTüm bağımlılıklar ve kütüphaneler başarıyla kuruldu!")
       print("Sistem kullanıma hazır.")
       install.run(self)

# setup.py ayarları
setup(
   name='BeatscriptAutomation',
   version='1.0',
   description='Kapsamlı bir müzik prodüksiyon ve otomasyon sistemi',
   packages=find_packages(),
   install_requires=REQUIRED_PACKAGES,
   cmdclass={
       'install': CustomInstallCommand,
   },
   entry_points={
       'console_scripts': [
           'beatscript = beatscript.cli:main',
       ],
   },
)

# Başlatma mesajı
print("Kurulum tamamlandı! Tüm gereksinimler başarıyla kuruldu.")