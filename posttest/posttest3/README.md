# Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer

> **Nama:** Muhammad Alfauzi Syahputra
> **Mata Kuliah:** Pemrograman Berorientasi Objek (OOP)
> **Bahasa Pemrograman:** Python 3
> **Tugas:** Posttest 3 — Polimorfisme & Abstraksi

---

## Daftar Isi

1. [Deskripsi Program](#deskripsi-program)
2. [Struktur Proyek](#struktur-proyek)
3. [Class Diagram & Relasi UML](#1-class-diagram--relasi-uml)
4. [Abstraksi](#2-abstraksi-abstract-base-class)
5. [Polimorfisme](#3-polimorfisme)
6. [Nilai Plus: SOLID](#nilai-plus-prinsip-solid)
7. [Cara Menjalankan](#cara-menjalankan)
8. [Screenshot Output](#screenshot-output)

---

## Deskripsi Program

Aplikasi CLI untuk simulasi kasir dan manajemen toko komputer. Pengguna dapat login/register sebagai **Staff** atau **Customer**, mengelola produk, dan melakukan transaksi penjualan dengan diskon membership dan pajak.

Pada posttest ini ditambahkan **sistem pembayaran**: setiap transaksi dibayar lewat metode pembayaran (Tunai, Transfer Bank, E-Wallet) yang dimodelkan dengan **abstract class `PaymentMethod`**. Setelah pembayaran berhasil, pelanggan menerima notifikasi lewat kanal berbeda (Email, SMS, WhatsApp) yang dimodelkan dengan **duck typing**.

---

## Struktur Proyek

```text
posttest3/
├── main.py
├── README.md
├── requirements.txt
├── assets/                  # diagram & screenshot
├── models/
│   ├── person.py            # Superclass
│   ├── customer.py          # Subclass Person
│   ├── staff.py             # Subclass Person
│   ├── product.py           # + operator overloading __lt__ / __gt__
│   ├── store.py
│   ├── sale.py              # + checkout(payment), __len__
│   ├── sale_item.py
│   ├── payment.py           # BARU: PaymentMethod (ABC) + 3 subclass
│   └── notifier.py          # BARU: Email/SMS/WhatsApp (duck typing)
├── menus/
│   ├── payment_prompt.py    # BARU: pilihan pembayaran di menu
│   └── testing_menu.py      # + test Abstraksi, Polimorfisme, SOLID
└── utils/
```

---

## 1. Class Diagram & Relasi UML

![Class Diagram](assets/class_diagram.png)

Simbol: segitiga kosong = inheritance, belah ketupat kosong = agregasi, belah ketupat penuh = komposisi, panah terbuka = asosiasi (putus-putus = hanya lewat parameter method). Nama kelas abstrak ditulis *miring* dengan stereotype `«abstract»`.

### Penjelasan Relasi

| Relasi | Dari → Ke | Bukti di kode |
|---|---|---|
| **Asosiasi** | `Sale` → `Customer`, `Sale` → `PaymentMethod`, `SaleItem` → `Product`, `Staff` ⇢ `Sale` | `Sale.__init__` menyimpan `self.customer`; `Sale.checkout()` menyimpan `self.payment`; `Staff.process_transaction(sale, payment)` hanya menerima `Sale` sebagai parameter |
| **Agregasi** | `Store` ◇— `Product` dan `Store` ◇— `Staff` | `Store.add_product()` / `add_staff()` di `models/store.py` |
| **Komposisi** | `Sale` ◆— `SaleItem` | `SaleItem` dibuat di dalam `Sale.add_item()` |

- **Asosiasi** (`Sale` → `Customer`/`PaymentMethod`): sebuah transaksi *menggunakan/mengacu* pada pelanggan dan metode pembayaran, tetapi tidak memiliki siklus hidup mereka; pelanggan tetap ada walau transaksi dihapus.
- **Agregasi** (`Store` → `Product`/`Staff`): objek `Product` dan `Staff` dibuat **di luar** `Store` (di `main.py`) lalu didaftarkan. Jika `Store` dihapus, produk dan staff tetap ada (siklus hidup mandiri), sehingga dipilih agregasi.
- **Komposisi** (`Sale` → `SaleItem`): `SaleItem` dibuat **di dalam** `Sale.add_item()` dan tidak bermakna tanpa `Sale` induknya (nota). Jika `Sale` hilang, item ikut hilang, sehingga dipilih komposisi, bukan agregasi.

```python
# Agregasi (main.py): dibuat di luar, lalu dimasukkan ke Store
prod1 = Product("P001", "Mechanical Keyboard", 750000, 10, "Peripheral")
my_store.add_product(prod1)

# Komposisi (models/sale.py): SaleItem dibuat di dalam Sale
new_item = SaleItem(product, quantity)
self._items.append(new_item)

# Asosiasi (models/sale.py)
self.customer = customer
self.payment = payment      # di Sale.checkout()
```

---

## 2. Abstraksi (Abstract Base Class)

**Abstract class:** `PaymentMethod(ABC)` di `models/payment.py`.

| Bagian | Isi |
|---|---|
| **Abstract method (3)** | `validate()`, `calculate_fee()`, `execute()` — diberi `@abstractmethod` |
| **Method konkret** | `process(amount)` (alur validasi → eksekusi → status, sama untuk semua subclass, seperti `jalankan()` di materi), `get_total_charge()`, `describe()`, `__str__` |
| **Subclass (3)** | `CashPayment`, `BankTransferPayment`, `EWalletPayment` — ketiganya mengimplementasikan seluruh abstract method |

Konsep inheritance tetap dipakai: setiap subclass memanggil `super().__init__(payer_name)`, punya atribut unik (`cash_given`, `bank_name`, `provider`, ...), serta atribut protected/private:

| Level | Contoh |
|---|---|
| Protected | `_payer_name`, `_amount` (di parent), `_change` (`CashPayment`) |
| Private | `__reference_code` (parent), `__account_number` (`BankTransferPayment`), `__balance` (`EWalletPayment`) |

```python
class PaymentMethod(ABC):
    @abstractmethod
    def validate(self): ...
    @abstractmethod
    def calculate_fee(self): ...
    @abstractmethod
    def execute(self): ...

    def process(self, amount):          # method konkret bersama
        self._amount = amount
        if not self.validate():
            return False
        self.execute()
        ...
```

**Bukti abstract class tidak bisa diinstansiasi** (menu `OOP Testing` → `8`):

```python
try:
    PaymentMethod("Test")
except TypeError as e:
    print(f"TypeError: {e}")
# TypeError: Can't instantiate abstract class PaymentMethod without an implementation
#            for abstract methods 'calculate_fee', 'execute', 'validate'
```

Screenshot lengkap ada di bagian [Screenshot Output](#screenshot-output).

---

## 3. Polimorfisme

### a. Polimorfisme via Pewarisan
`calculate_fee()` (dan `describe()`, `validate()`, `execute()`) di-override oleh `CashPayment` (fee 0), `BankTransferPayment` (fee tetap Rp2.500), dan `EWalletPayment` (fee 1,5%). Dipanggil lewat satu loop:

```python
for payment in payments:     # Cash, BankTransfer, EWallet
    print(payment.method_name, payment.calculate_fee(), payment.describe())
```

Pola yang sama dipakai di `Sale.checkout()`: `payment.process(self.total)` tanpa mengecek jenis pembayaran. `Person.show_person_info()` dari posttest sebelumnya juga di-override oleh `Customer` dan `Staff`.

### b. Duck Typing
`EmailNotifier`, `SMSNotifier`, dan `WhatsAppNotifier` (`models/notifier.py`) **tidak berhubungan lewat pewarisan**, tetapi sama-sama punya `send(message)`. Semuanya dipanggil lewat satu fungsi:

```python
def notify_customer(channels, message):
    for channel in channels:
        channel.send(message)
```

Fungsi ini dipakai setelah pembayaran berhasil (`menus/payment_prompt.py → send_confirmation`).

### c. Operator Overloading

| Kelas | Magic method | Fungsi |
|---|---|---|
| `Product` | `__lt__`, `__gt__` | membandingkan harga; `sorted()`, `min()` bekerja otomatis (`Store.show_products_by_price()`) |
| `PaymentMethod` | `__str__`, `__lt__`, `__gt__` | tampilan teks & perbandingan biaya (fee) |
| `Sale` | `__len__` | `len(sale)` = jumlah item |

### d. Menghindari Anti-Pattern
Tidak ada rantai `if/elif` yang mengecek `type()` atau string jenis. Rantai `if/elif` berdasarkan string `membership_tier` pada `sale_menu.py` dari posttest sebelumnya **sudah dihapus**; diskon kini ditentukan oleh objek `Customer` sendiri lewat `customer.discount_percentage`. Menu pembayaran memakai tabel `PAYMENT_OPTIONS` (dictionary), bukan `if/elif`.

---

## Nilai Plus: Prinsip SOLID

| Prinsip | Penerapan |
|---|---|
| **DIP** (Dependency Inversion) | `Sale.checkout(payment)` bergantung pada abstraksi `PaymentMethod`, bukan kelas konkret seperti `CashPayment`. Objek pembayaran disuntikkan dari luar (dependency injection) |
| **OCP** (Open/Closed) | Metode pembayaran baru cukup dibuat sebagai subclass `PaymentMethod` (dan satu baris di `PAYMENT_OPTIONS`), tanpa mengubah `Sale`, `Staff`, maupun `PaymentMethod`. Dibuktikan di menu `OOP Testing → 10` dengan kelas `VoucherPayment` yang dibuat tanpa memodifikasi kode lama |

---

## Cara Menjalankan

```bash
pip install -r requirements.txt
python main.py
```

Akun default: Staff `admin` / `admin123`, Customer `rina_m` / `password1`.

Menu `3. OOP Testing`:

| Menu | Yang dibuktikan |
|---|---|
| 1–7 | Pengujian posttest sebelumnya (inheritance, encapsulation, class/static method, asosiasi, agregasi, komposisi) |
| 8 | **Abstraksi**: abstract class tidak bisa diinstansiasi, subclass tidak lengkap ditolak |
| 9 | **Polimorfisme**: pewarisan, duck typing, operator overloading |
| 10 | **SOLID**: OCP & DIP dengan `VoucherPayment` |
| 11 | Run all tests |

Pembayaran juga dapat dicoba lewat alur nyata: login → *Process New Sale* (staff) atau *Buy Product* (customer).

---

## Screenshot Output

**Abstraksi — abstract class tidak bisa diinstansiasi (menu 8)**

![Test Abstraction](assets/test_abstraction.png)

**Polimorfisme — pewarisan, duck typing, operator overloading (menu 9)**

![Test Polymorphism](assets/test_polymorphism.png)

**SOLID — OCP & DIP (menu 10)**

![Test SOLID](assets/test_solid.png)
