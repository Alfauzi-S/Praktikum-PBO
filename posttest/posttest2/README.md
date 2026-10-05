# Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer

> **Nama:** Muhammad Alfauzi Syahputra  
> **Mata Kuliah:** Pemrograman Berorientasi Objek (OOP)  
> **Bahasa Pemrograman:** Python 3

---

## 📋 Daftar Isi

1. [Deskripsi Proyek](#-deskripsi-proyek)
2. [Fitur Utama](#-fitur-utama)
3. [Struktur Proyek](#-struktur-proyek)
4. [Konsep OOP yang Diterapkan](#-konsep-oop-yang-diterapkan)
5. [Relasi UML (Posttest 2)](#-relasi-uml-posttest-2)
6. [Penjelasan Kelas](#-penjelasan-kelas)
7. [Cara Menjalankan Program](#-cara-menjalankan-program)
8. [Skenario Pengujian OOP](#-skenario-pengujian-oop)
9. [Kesimpulan](#-kesimpulan)

---

## 📝 Deskripsi Proyek

Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer adalah aplikasi berbasis Command Line Interface (CLI) yang dibangun menggunakan Python. Aplikasi ini mensimulasikan sistem kasir dan manajemen toko nyata, lengkap dengan sistem autentikasi (Login/Register), manajemen stok, pemrosesan transaksi dengan perhitungan pajak dan diskon otomatis, serta dashboard yang berbeda untuk peran (Role) Staff dan Customer.

Proyek ini dirancang khusus untuk memenuhi dan mendemonstrasikan pemahaman mendalam tentang prinsip-prinsip Object-Oriented Programming (OOP) dan Relasi UML Class Diagram.

---

## ✨ Fitur Utama

- Sistem Autentikasi & Role-Based Access: Login terpisah untuk Staff dan Customer, serta fitur Register khusus Customer.
- Manajemen Produk: Menambah, melihat, dan mengelola stok produk dengan validasi ketat.
- Manajemen Customer (Khusus Staff): Menambah dan melihat detail data pelanggan.
- Transaksi Penjualan (Kasir & Customer):
  - Pembuatan transaksi dengan perhitungan subtotal, diskon (berdasarkan tier membership), dan pajak (PPN) secara otomatis.
- Pengurangan stok otomatis saat transaksi berhasil.
- Pencatatan poin loyalitas dan total pengeluaran customer.
- Dashboard Staff: Ringkasan toko, pemrosesan transaksi, dan manajemen bonus karyawan.
- Menu Pengujian OOP: Menu khusus untuk mendemonstrasikan dan memvalidasi setiap konsep OOP dan Relasi UML secara langsung di terminal.

---

## 📂 Struktur Proyek

```text
posttest2/
├── main.py
├── README.md
├── requirements.txt
├── assets/
│   ├── main_menu.png
│   ���── login_menu.png
│   ├── register_menu.png
│   ├── staff_dashboard.png
│   ├── customer_dashboard.png
│   ├── sale_menu.png
│   └── oop_testing_menu.png
├── models/
│   ├── __init__.py
│   ├── person.py
│   ├── customer.py
│   ├── staff.py
│   ├── product.py
│   ├── store.py
│   ├── sale.py
│   └── sale_item.py
├── menus/
│   ├── __init__.py
│   ├── auth_menu.py
│   ├── staff_menu.py
│   ├── customer_menu.py
│   ├── product_menu.py
│   ├── sale_menu.py
│   └── testing_menu.py
├── utils/
│   ├── __init__.py
│   ├── helper.py
│   └── database.py
└── data/
    ├── customers.json
    ├── products.json
    ├── staff.json
    └── sales.json
```

---

## 🧠 Konsep OOP yang Diterapkan

- Class & Object: Pembuatan blueprint (class) dan instansiasi objek (object).
- Inheritance (Pewarisan): Customer dan Staff mewarisi atribut dan method dari Person.
- Encapsulation (Enkapsulasi):
  - Atribut Private (`__password`, `__salary`, `__total_spending`) hanya bisa diakses via getter/setter.
  - Atribut Protected (`_name`, `_phone`) untuk akses internal subclass.
- Polymorphism (Method Overriding): Method `show_person_info()` di-override di subclass untuk menambahkan data spesifik.
- Class, Instance, & Static Method:
  - Instance: Bekerja pada objek spesifik (misal: `add_stock`).
  - Class: Mengubah data yang dibagi semua objek (misal: `change_tax`).
  - Static: Fungsi bantu tanpa akses ke `self/cls` (misal: `validate_price`).
- Modularization: Pemisahan kode ke dalam package (`models`, `menus`, `utils`) untuk keterbacaan dan pemeliharaan yang baik.

---

## 🔗 Relasi UML (Posttest 2)

Aplikasi ini mengimplementasikan 4 jenis relasi UML sesuai modul:

| Relasi | Implementasi dalam Kode | Bukti Konsep |
|---|---|---|
| Inheritance | `Person -> Customer, Staff` | `Customer` memanggil `super().__init__()` dan menggunakan method `show_person_info()` milik `Person`. |
| Agregasi | `Store` "memiliki" `Product` & `Staff` | Objek `Product` dan `Staff` dibuat di luar class `Store`, lalu didaftarkan via method `add_product()`. Jika objek `Store` dihapus, objek `Product` tetap ada di memori (siklus hidup mandiri). |
| Komposisi | `Sale` "terdiri dari" `SaleItem` | Objek `SaleItem` dibuat langsung di dalam method `Sale.add_item()`. `SaleItem` tidak dapat berdiri sendiri dan akan ikut musnah jika objek `Sale` dihapus (siklus hidup terikat). |
| Asosiasi | `Staff` "menggunakan" `Sale` | Method `Staff.process_transaction(sale)` menerima objek `Sale` sebagai parameter. `Staff` tidak menyimpannya sebagai atribut permanen (`self.sale`), menunjukkan hubungan sementara. |

---

## 📦 Penjelasan Kelas

### Person (Superclass)

Menyimpan data dasar seperti `_name`, `__password`, `username`, `_phone`, dan `__gmail`. Dilengkapi getter/setter untuk validasi format email dan nomor HP.

### Customer (Subclass)

Menambahkan:

- `id_customer`
- `address`
- `membership_tier`
- `loyalty_points`
- `__total_spending`

Memiliki logika otomatis `_auto_upgrade_membership()` berdasarkan total belanja.

### Staff (Subclass)

Menambahkan:

- `employee_id`
- `_role`
- `__salary`
- `__total_bonus`

Memiliki method `process_transaction()` untuk mendemokan relasi Asosiasi.

### Product

Menyimpan:

- `id_product`
- `name`
- `category`
- `_price`
- `_stock`

Setter-nya mencegah harga <= 0 dan stok < 0.

### Store

Bertindak sebagai penampung (Agregasi) untuk list `_products` dan `_staffs`. Memiliki method ringkasan seperti `get_total_products_value()`.

### Sale & SaleItem

- `Sale` mengelola ID transaksi, diskon, dan pajak.
- `SaleItem` adalah detail item (produk & qty) yang dibuat secara internal oleh `Sale` (Komposisi).

---

## 🚀 Cara Menjalankan Program

### Prasyarat

Pastikan Python 3.x sudah terinstal di komputer Anda.

### Langkah-langkah

1. Buka terminal atau Command Prompt.
2. Arahkan direktori ke folder `posttest2`.
3. Jalankan perintah berikut:

```bash
python main.py
```

### Akun Default untuk Pengujian

- Staff (Admin): Username: `admin` | Password: `admin123`
- Customer: Username: `rina_m` | Password: `password1`

---

## 🧪 Skenario Pengujian OOP

Pilih menu `3. OOP Testing` pada Main Menu untuk melihat bukti langsung implementasi konsep:

- Inheritance Test: Memanggil `customer.show_person_info()`. Output akan menampilkan data dari parent (Name, Username) dan child (ID Customer, Membership).
- Encapsulation Test: Mencoba mengatur `product.stock = -10`. Program akan menangkap `ValueError` dan menolak perubahan, membuktikan atribut protected/private aman dari data tidak valid.
- Class Method Test: Memanggil `Sale.change_tax(15)`. Nilai pajak akan berubah secara global untuk semua objek `Sale` yang akan dibuat.
- Static Method Test: Memanggil `Product.validate_price(-500)` yang akan mengembalikan `False` tanpa perlu membuat objek `Product` terlebih dahulu.
- Association Test: Mendemonstrasikan bagaimana `Staff` memproses `Sale` yang diterima sebagai parameter, lalu membuktikan dengan `hasattr` bahwa `Staff` tidak menyimpan objek `Sale` tersebut secara permanen.
- Aggregation Test: Membuat `Store` sementara, menambahkan produk, lalu menghapus objek `Store` (`del`). Dibuktikan bahwa objek `Product` tetap dapat diakses setelahnya.
- Composition Test: Membuat `Sale` sementara dan memanggil `add_item()`. Dijelaskan bahwa objek `SaleItem` tercipta di dalam scope method tersebut dan tidak memiliki referensi di luar.

---

## 💡 Kesimpulan

Proyek Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer ini berhasil mengimplementasikan seluruh persyaratan Posttest 2. Aplikasi tidak hanya berjalan secara fungsional sebagai sistem kasir CLI, tetapi juga dirancang dengan arsitektur OOP yang bersih, modular, dan aman (melalui enkapsulasi ketat).

Pemilihan relasi UML (Inheritance, Agregasi, Komposisi, dan Asosiasi) telah diterapkan sesuai dengan definisi akademis dan logika bisnis dunia nyata, yang semuanya dapat dibuktikan melalui menu OOP Testing yang disediakan.

> Catatan: Dokumen ini dibuat sebagai pengganti screenshot untuk memberikan penjelasan yang lebih terstruktur, dapat dicari (searchable), dan profesional mengenai implementasi kode.
