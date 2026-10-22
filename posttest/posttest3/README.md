# Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer

> **Nama:** Muhammad Alfauzi Syahputra
> **Mata Kuliah:** Pemrograman Berorientasi Objek (OOP)
> **Bahasa Pemrograman:** Python 3 (hanya standard library)
> **Tugas:** Posttest 3 — Polimorfisme & Abstraksi

---

## Daftar Isi

1. [Deskripsi Program](#deskripsi-program)
2. [Role & Hak Akses](#role--hak-akses)
3. [Alur Belanja](#alur-belanja)
4. [Struktur Proyek](#struktur-proyek)
5. [Class Diagram & Relasi UML](#1-class-diagram--relasi-uml)
6. [Abstraksi](#2-abstraksi-abstract-base-class)
7. [Polimorfisme](#3-polimorfisme)
8. [Nilai Plus: SOLID](#nilai-plus-prinsip-solid)
9. [Cara Menjalankan](#cara-menjalankan)
10. [Screenshot Output](#screenshot-output)

---

## Deskripsi Program

Aplikasi CLI manajemen toko komputer multi-cabang dengan tiga role: **Customer**, **Admin** (per cabang), dan **Super Admin**. Customer memilih barang, admin cabang memproses pesanan dan memvalidasi pembayaran, sedangkan super admin mengelola admin, profil toko, dan cabang. Semua kejadian penting tercatat di log/history.

## Role & Hak Akses

| Role | Hak akses |
|---|---|
| **Customer** | Melihat produk per cabang, belanja (membuat request), melihat status pesanan, notifikasi, ubah profil dan akun (username & password) |
| **Admin** | Notifikasi request, memproses request customer (buat pesanan + validasi pembayaran / tolak), membuat pesanan langsung (walk-in), kelola produk cabang, kelola customer (tambah, ubah profil/akun, reset password, aktif/nonaktif), history/log, ubah profil dan akun sendiri |
| **Super Admin** | Semua akses Admin (di semua cabang) + membuat & mengelola akun admin, ubah profil toko, tambah/ubah/hapus cabang |

Hak akses ditentukan oleh method `get_permissions()` pada tiap kelas role, dan menu dashboard dibangun otomatis dari situ (tanpa `if/elif` role).

## Alur Belanja

```text
Customer pilih barang → Request dibuat + notifikasi ke admin cabang
        → Admin membuat pesanan & memvalidasi pembayaran
        → Tercatat di log/history (+ notifikasi ke customer)
```

1. **Customer** memilih cabang dan barang, lalu mengirim request (`OrderService.submit_request`). Sistem membuat `Notification` untuk admin cabang tersebut.
2. **Admin** membuka *Customer Requests*, memilih request, lalu memilih metode pembayaran dan memasukkan data pembayaran. `PaymentMethod.process()` memvalidasi pembayaran; jika valid, `Sale` (pesanan resmi) dibuat, stok berkurang, diskon membership dan poin diterapkan. Admin juga dapat **menolak** request dengan alasan.
3. Hasilnya masuk ke `ActivityLog` (history) dan `Sale` disimpan; customer menerima notifikasi (dalam aplikasi + Email/SMS).

## Struktur Proyek

```text
posttest3/
├── main.py
├── seed.py                    # data awal (dibuat lewat alur aplikasi)
├── models/
│   ├── person.py              # Person (ABC)
│   ├── customer.py            # Customer(Person)
│   ├── admin.py               # Admin(Person), SuperAdmin(Admin)
│   ├── store.py  branch.py    # profil toko & cabang
│   ├── product.py
│   ├── order_request.py       # request dari customer
│   ├── sale.py  sale_item.py  # pesanan resmi
│   ├── payment.py             # PaymentMethod (ABC) + 3 subclass
│   ├── notifier.py            # Email/SMS/WhatsApp (duck typing)
│   ├── notification.py  activity_log.py
│   ├── app_data.py            # penyimpanan data (in-memory)
│   └── order_service.py       # alur request -> order -> log
├── menus/
│   ├── dashboard.py           # menu dibangun dari permission
│   ├── customer_actions.py  admin_actions.py  superadmin_actions.py
│   ├── profile_actions.py  payment_prompt.py  auth.py  testing_menu.py
├── utils/helper.py
└── assets/                    # diagram & screenshot
```

---

## 1. Class Diagram & Relasi UML

![Class Diagram](assets/class_diagram.png)

Simbol: segitiga kosong = inheritance, belah ketupat kosong = agregasi, belah ketupat penuh = komposisi, panah terbuka = asosiasi. Kelas abstrak ditulis miring dengan `«abstract»`.

| Relasi | Dari → Ke | Bukti di kode |
|---|---|---|
| **Asosiasi** | `Sale` → `Customer`, `Admin`, `PaymentMethod`; `OrderRequest` → `Customer`; `SaleItem` → `Product` | `Sale.__init__` menyimpan `customer` dan `handled_by`, `Sale.checkout()` menyimpan `payment` |
| **Agregasi** | `Branch` ◇— `Product`, `Branch` ◇— `Admin` | `Branch.add_product()` / `add_admin()`; objek dibuat di luar (`seed.py`) lalu didaftarkan |
| **Komposisi** | `Store` ◆— `Branch`, `Sale` ◆— `SaleItem`, `OrderRequest` ◆— `SaleItem` | `Store.add_branch()` membuat `Branch`; `Sale.add_item()` dan `OrderRequest.add_item()` membuat `SaleItem` |

- **Asosiasi:** `Sale` hanya *mengacu* ke customer, admin pemroses, dan metode pembayaran; objek-objek itu hidup mandiri dan dipakai bersama banyak transaksi.
- **Agregasi (Branch → Product/Admin):** produk dan admin dibuat di luar cabang lalu didaftarkan. Jika cabang dihapus, objek `Admin` dan `Product` tetap ada dan bisa dipindahkan (admin bisa dipindah cabang oleh super admin), sehingga hubungannya "memiliki" yang longgar.
- **Komposisi:** `Branch` tidak bermakna tanpa `Store`, dan dibuat hanya lewat `Store.add_branch()`. `SaleItem` hanya ada sebagai baris dari satu `Sale`/`OrderRequest` dan dibuat di dalamnya. Keduanya ikut hilang bersama induknya, maka dipilih komposisi, bukan agregasi.

## 2. Abstraksi (Abstract Base Class)

Ada dua abstract class:

| Abstract class | Abstract method | Method konkret | Subclass |
|---|---|---|---|
| `PaymentMethod(ABC)` | `validate()`, `calculate_fee()`, `execute()` | `process(amount)` (alur sama untuk semua, seperti `jalankan()` di materi), `get_total_charge()`, `describe()`, `__str__` | `CashPayment`, `BankTransferPayment`, `EWalletPayment` |
| `Person(ABC)` | `get_role()`, `get_permissions()`, `can_see(notification)` | `set_password()`, `verify_password()`, `update_profile()`, `show_person_info()` | `Customer`, `Admin` → `SuperAdmin` |

Inheritance dipertahankan: semua subclass memakai `super().__init__(...)`, punya atribut unik, dan atribut **protected** (`_name`, `_amount`, `_change`) serta **private** (`__password`, `__gmail`, `__reference_code`, `__account_number`, `__balance`, `__total_spending`).

**Bukti abstract class tidak bisa diinstansiasi** (menu `OOP Testing → 3`):

```python
try:
    PaymentMethod("x")
except TypeError as e:
    print(e)
# Can't instantiate abstract class PaymentMethod without an implementation
# for abstract methods 'calculate_fee', 'execute', 'validate'
```

## 3. Polimorfisme

- **Via pewarisan:** `get_permissions()`, `can_see()`, dan `accessible_branches()` di-override oleh `Customer`, `Admin`, dan `SuperAdmin` (Admin hanya cabangnya, SuperAdmin semua cabang). `calculate_fee()` di-override oleh tiga metode pembayaran (fee Rp0, Rp2.500, 1,5%). Dipanggil lewat satu loop (lihat menu testing 4) dan di `Sale.checkout()` serta `build_menu()`.
- **Duck typing:** `EmailNotifier`, `SMSNotifier`, `WhatsAppNotifier` tidak berpewarisan tetapi sama-sama punya `send()`, dipanggil lewat `notify_customer(channels, message)`. Dipakai setelah pembayaran divalidasi.
- **Operator overloading:** `Product.__lt__/__gt__` (`sorted()`, `min()` bekerja, dipakai di *View Products → sort by price*); `Sale.__len__/__lt__/__gt__/__str__`; `OrderRequest.__len__/__str__`; `PaymentMethod.__str__/__lt__/__gt__`; `Branch.__len__`, `Store.__len__`.
- **Tanpa anti-pattern:** tidak ada `if/elif` yang mengecek `type()` atau string jenis/role. Menu dibangun dari `user.get_permissions()`, tier customer dari tabel `Customer.TIERS`, pilihan pembayaran dari tabel `PAYMENT_OPTIONS`.

## Nilai Plus: Prinsip SOLID

| Prinsip | Penerapan |
|---|---|
| **DIP** | `Sale.checkout(payment)` bergantung pada abstraksi `PaymentMethod`, bukan kelas konkret; objek pembayaran disuntikkan dari luar |
| **OCP** | Metode pembayaran baru = subclass baru (+ satu baris di `PAYMENT_OPTIONS`) tanpa mengubah `Sale`/`OrderService`; role atau aksi baru = tambah permission dan satu baris registry menu. Dibuktikan oleh `VoucherPayment` di menu testing 5 |
| **SRP** | Penyimpanan data (`AppData`) dipisah dari alur bisnis (`OrderService`) dan dari tampilan (`menus/`) |

---

## Cara Menjalankan

```bash
python main.py
```

| Role | Username | Password |
|---|---|---|
| Super Admin | `superadmin` | `super123` |
| Admin Samarinda | `admin_smr` | `admin123` |
| Admin Balikpapan | `admin_bpn` | `admin123` |
| Customer | `rina_m` / `daffa_p` / `nadia_putri` | `password1` / `password2` / `password3` |

Skenario cepat: login `rina_m` → *Shop* → kirim request → logout → login `admin_smr` → *Notifications* / *Customer Requests* → buat pesanan & bayar → *History / Log*.

Data disimpan di memori, jadi kembali ke data awal tiap program dijalankan.

Menu `OOP Testing`: 1 Encapsulation, 2 Relasi (asosiasi/agregasi/komposisi), 3 Abstraksi, 4 Polimorfisme, 5 SOLID, 6 Run all.

---

## Screenshot Output

**Customer mengirim request**

![Customer request](assets/flow_1_customer_request.png)

**Admin memproses request, validasi pembayaran, pesanan dibuat**

![Admin order](assets/flow_3_admin_order_payment.png)

**History / log**

![Log](assets/flow_4_history_log.png)

**Abstraksi: abstract class tidak bisa diinstansiasi**

![Abstraction](assets/test_abstraction.png)

**Polimorfisme (pewarisan, duck typing, operator overloading)**

![Polymorphism](assets/test_polymorphism.png)

**Relasi UML dibuktikan di kode**

![Relations](assets/test_relations.png)

**SOLID (OCP & DIP)**

![SOLID](assets/test_solid.png)
