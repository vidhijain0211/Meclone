[app]
title = MeCloneApp
package.name = meclone
package.domain = org.meclone.app
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,json,db,ttf,mp3,wav
version = 1.0
icon.filename = assets/icon.png

requirements = python3,kivy,kivymd>=1.1.0,sqlite3,sounddevice,wavio

orientation = portrait
fullscreen = 1

android.permissions = RECORD_AUDIO, INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Include sqlite3
android.sqlite_support = True

# Entry point
entrypoint = main.py

# Enable logcat output
log_level = 2

# Android SDK/API settings
android.minapi = 21
android.target = 31
android.ndk = 23b

# To include additional files
presplash.filename = assets/icon.png

# Store user data
android.private_storage = True

# Lock screen and session config
include_files = config/,database/,assets/

[buildozer]
log_level = 2
warn_on_root = 1
