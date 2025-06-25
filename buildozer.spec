[app]
title = MeCloneApp
package.name = meclone
package.domain = org.meclone.app
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,json,db,ttf,mp3,wav,ogg,ini,txt
version = 1.0
icon.filename = assets/icon.png

requirements = python3,kivy,kivymd>=1.1.0,sqlite3,sounddevice,wavio,plyer,requests,jnius,Pillow

orientation = portrait
fullscreen = 1

android.permissions = RECORD_AUDIO,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK,FOREGROUND_SERVICE,VIBRATE

android.api = 31
android.minapi = 21
android.target = 31
android.ndk = 23b

android.private_storage = True
android.allow_backup = True

log_level = 2

entrypoint = main.py

presplash.filename = assets/icon.png

include_files = config/,database/,assets/,data/

android.services = routine_service

android.opengl_es2 = True
android.multitouch = on
android.keyboard_mode = systemanddock
android.wakelock = True
android.foreground_service = True
android.uses_cleartext_traffic = True

[buildozer]
log_level = 2
warn_on_root = 1
