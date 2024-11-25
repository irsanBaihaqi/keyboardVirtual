#!/bin/bash

# Skrip untuk mengatur proyek dan mengunggah ke GitHub

# Cek jika Git diinstal
if ! [ -x "$(command -v git)" ]; then
  echo "Git tidak ditemukan. Silakan instal Git terlebih dahulu."
  exit 1
fi

# Inisialisasi Git
git init

# Tambahkan file ke staging area
git add .

# Buat commit awal
git commit -m "Initial commit"

# Buat file requirements.txt
echo -e "opencv-python\ncvzone\npynput" > requirements.txt

# Periksa apakah remote GitHub sudah ada
read -p "Masukkan URL remote GitHub: " github_url
git remote add origin $github_url

# Push ke GitHub
git branch -M main
git push -u origin main

echo "Proyek berhasil diatur dan diunggah ke GitHub!"
