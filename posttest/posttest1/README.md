# Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer

> **Nama:** Muhammad Alfauzi Syahputra
>
> **Mata Kuliah:** Pemrograman Berorientasi Objek
>
> **Bahasa Pemrograman:** Python

---

## Daftar Isi

1. [Deskripsi Proyek](#deskripsi-proyek)
2. [Struktur Proyek](#struktur-proyek)
3. [Arsitektur & Desain OOP](#arsitektur--desain-oop)
4. [Penjelasan Kelas](#penjelasan-kelas)
5. [Fitur Aplikasi](#fitur-aplikasi)
6. [Alur Program](#alur-program)
7. [Cara Menjalankan](#cara-menjalankan)
8. [Pengujian OOP](#pengujian-oop)
9. [Contoh Penggunaan](#contoh-penggunaan)

---

## Deskripsi Proyek

Proyek ini merupakan **Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer** berbasis Command Line Interface (CLI) yang dibangun menggunakan Python.

Aplikasi ini digunakan untuk mengelola data **product**, **customer**, dan **sales transaction**. Program menyediakan beberapa fitur seperti menampilkan product, mengelola stock, mengelola customer, membuat transaksi penjualan, menghitung total transaksi, serta menampilkan sales receipt.

Proyek ini dibuat sebagai implementasi konsep **Object-Oriented Programming (OOP)** dengan menerapkan beberapa konsep seperti:

* Class dan Object
* Class Attribute
* Instance Attribute
* Public Attribute
* Private Attribute
* Instance Method
* Class Method
* Static Method
* Encapsulation
* Getter dan Setter
* Data Validation
* Inheritance
* Modularization

---

## Struktur Proyek

```text
computer_sales_management/
│
├── main.py                         # File utama program
├── requirements.txt                # Library yang digunakan
├── README.md                       # Dokumentasi project
│
├── models/
│   ├── __init__.py
│   ├── person.py                   # Parent class Person
│   ├── customer.py                 # Class Customer
│   ├── product.py                  # Class Product
│   └── sale.py                     # Class Sale
│
├── menus/
│   ├── __init__.py
│   ├── product_menu.py             # Menu Product Management
│   ├── customer_menu.py            # Menu Customer Management
│   ├── sale_menu.py                # Menu Sales Management
│   └── testing_menu.py             # Menu OOP Testing
│
└── utils/
    ├── __init__.py
    └── helper.py                   # Helper functions
```

---

## Arsitektur & Desain OOP

Program menggunakan beberapa class yang memiliki tugas masing-masing.

Struktur hubungan class:

```text
                 Person
                    │
                    │ Inheritance
                    ▼
                Customer


                Product


                  Sale
             /             \
            ▼               ▼
       Customer          Product
```

Class `Customer` merupakan turunan dari class `Person`.

Sedangkan class `Sale` menggunakan object `Customer` dan `Product` untuk membentuk sebuah transaksi penjualan.

### Encapsulation

Program menggunakan private attribute dengan double underscore `__`.

Contoh pada class `Product`:

```python
self.__stock = stock
```

Data tersebut tidak diakses secara langsung dari luar class, tetapi melalui `property`.

Contoh:

```python
@property
def stock(self):
    return self.__stock
```

Setter juga digunakan untuk melakukan validasi:

```python
@stock.setter
def stock(self, new_stock):
    if new_stock < 0:
        raise ValueError(
            "Stock cannot be negative!"
        )
    else:
        self.__stock = new_stock
```

Dengan demikian, nilai `stock` tidak dapat diubah menjadi nilai negatif.

### Inheritance

Program menerapkan inheritance antara:

```text
Person
   │
   └── Customer
```

Implementasinya:

```python
class Customer(Person):
```

Constructor dari parent class dipanggil menggunakan:

```python
super().__init__(name, phone)
```

Dengan inheritance tersebut, `Customer` dapat menggunakan attribute dan method yang berasal dari `Person`.

### Package / Modularization

Program dibagi menjadi beberapa folder agar kode lebih terorganisir.

* `models` bertanggung jawab terhadap class dan data.
* `menus` bertanggung jawab terhadap menu dan interaksi pengguna.
* `utils` berisi helper function yang digunakan oleh beberapa bagian program.
* `main.py` digunakan untuk menjalankan program.

---

## Penjelasan Kelas

### 1. `Person`

`Person` merupakan parent class yang digunakan sebagai dasar untuk class `Customer`.

| Attribute | Type     | Description   |
| --------- | -------- | ------------- |
| `__name`  | `String` | Nama person   |
| `phone`   | `String` | Nomor telepon |

### Method

```python
def show_person_info(self):
```

Method ini digunakan untuk menampilkan informasi dasar person.

### Property

```python
@property
def name(self):
    return self.__name
```

Property digunakan sebagai getter untuk private attribute `__name`.

---

### 2. `Customer`

`Customer` merupakan class yang digunakan untuk menyimpan data pelanggan.

Class ini merupakan child class dari `Person`.

```python
class Customer(Person):
```

| Attribute     | Type     | Description            |
| ------------- | -------- | ---------------------- |
| `id_customer` | `String` | ID unik customer       |
| `name`        | `String` | Nama customer          |
| `phone`       | `String` | Nomor telepon customer |
| `address`     | `String` | Alamat customer        |
| `__status`    | `String` | Status customer        |

### Class Attributes

```python
total_customers
customer_type
application_name
```

### Method penting

```python
show_info()
change_address()
```

`show_info()` digunakan untuk menampilkan data customer.

`change_address()` digunakan untuk mengubah address customer dengan validasi agar address tidak boleh kosong.

### Class Method

```python
@classmethod
def change_customer_type(cls, new_type):
```

Method ini digunakan untuk mengubah `customer_type`.

### Static Method

```python
@staticmethod
def validate_phone(phone):
```

Method ini digunakan untuk melakukan validasi nomor telepon.

---

### 3. `Product`

`Product` digunakan untuk menyimpan data perangkat dan aksesori komputer.

| Attribute    | Type     | Description          |
| ------------ | -------- | -------------------- |
| `id_product` | `String` | ID unik product      |
| `name`       | `String` | Nama product         |
| `price`      | `int`    | Harga product        |
| `category`   | `String` | Kategori product     |
| `__stock`    | `int`    | Jumlah stock product |

### Class Attributes

```python
store_name
store_category
total_products
```

### Method penting

```python
show_info()
add_stock()
reduce_stock()
```

`add_stock()` digunakan untuk menambahkan stock.

`reduce_stock()` digunakan untuk mengurangi stock ketika terjadi transaksi.

### Class Method

```python
@classmethod
def change_store_name(cls, new_name):
```

Method ini digunakan untuk mengubah nama store.

### Static Method

```python
@staticmethod
def validate_price(price):
```

Digunakan untuk melakukan validasi harga.

Method lainnya:

```python
@staticmethod
def format_price(price):
```

Digunakan untuk mengubah format angka menjadi format Rupiah.

### Getter dan Setter

Private attribute `__stock` diakses menggunakan property:

```python
@property
def stock(self):
    return self.__stock
```

Setter:

```python
@stock.setter
def stock(self, new_stock):
    if new_stock < 0:
        raise ValueError(
            "Stock cannot be negative!"
        )
    else:
        self.__stock = new_stock
```

---

### 4. `Sale`

`Sale` merupakan class yang digunakan untuk mengelola transaksi penjualan.

| Attribute  | Type       | Description           |
| ---------- | ---------- | --------------------- |
| `id_sale`  | `String`   | ID transaksi          |
| `customer` | `Customer` | Object customer       |
| `product`  | `Product`  | Object product        |
| `quantity` | `int`      | Jumlah product        |
| `__total`  | `int`      | Total biaya transaksi |

### Class Attributes

```python
total_sales
tax
currency
```

### Method penting

```python
calculate_total()
process_sale()
show_receipt()
```

`calculate_total()` digunakan untuk menghitung total transaksi berdasarkan:

```text
product price × quantity
```

Contoh:

```python
def calculate_total(self):
    self.__total = (
        self.product.price * self.quantity
    )
```

`process_sale()` digunakan untuk memproses transaksi dan mengurangi stock product.

`show_receipt()` digunakan untuk menampilkan sales receipt.

### Class Method

```python
@classmethod
def change_tax(cls, new_tax):
```

Digunakan untuk mengubah nilai tax.

### Static Method

```python
@staticmethod
def calculate_discount(total, percentage):
```

Digunakan untuk menghitung discount berdasarkan persentase tertentu.

---

## Fitur Aplikasi

| No | Feature                 | Description                      |
| -- | ----------------------- | -------------------------------- |
| 1  | **Product Management**  | Mengelola data dan stock product |
| 2  | **Show Products**       | Menampilkan daftar product       |
| 3  | **Add Stock**           | Menambahkan jumlah stock         |
| 4  | **Reduce Stock**        | Mengurangi jumlah stock          |
| 5  | **Customer Management** | Mengelola data customer          |
| 6  | **Change Address**      | Mengubah address customer        |
| 7  | **Change Status**       | Mengubah status customer         |
| 8  | **Sales Management**    | Mengelola transaksi penjualan    |
| 9  | **Create Sale**         | Membuat transaksi baru           |
| 10 | **Show Sales**          | Menampilkan data transaksi       |
| 11 | **Sales Receipt**       | Menampilkan receipt transaksi    |
| 12 | **OOP Testing**         | Menguji konsep OOP               |
| 13 | **Exit**                | Mengakhiri program               |

---

## Alur Program

```text
[Start]
    |
    v
[Main Menu]
    |
    ├── [1] Product Management
    │       |
    │       ├── Show Products
    │       ├── Add Stock
    │       ├── Reduce Stock
    │       ├── Change Store Name
    │       └── Back
    │
    ├── [2] Customer Management
    │       |
    │       ├── Show Customers
    │       ├── Change Address
    │       ├── Change Status
    │       ├── Change Customer Type
    │       └── Back
    │
    ├── [3] Sales Management
    │       |
    │       ├── Create Sale
    │       ├── Show Sales
    │       ├── Change Tax
    │       └── Back
    │
    ├── [4] OOP Testing
    │       |
    │       ├── Test Objects
    │       ├── Test Instance Method
    │       ├── Test Class Method
    │       ├── Test Static Method
    │       ├── Test Getter and Setter
    │       ├── Test Inheritance
    │       └── Run All Tests
    │
    └── [5] Exit
```

---

## Cara Menjalankan

### Prasyarat

Sebelum menjalankan program, pastikan:

* **Python 3** sudah terinstal.
* `pip` sudah tersedia.
* Terminal atau Command Prompt dapat digunakan.
* Library `tabulate` sudah diinstal.

Untuk mengecek versi Python:

```bash
python --version
```

### Install Library

Masuk ke folder project kemudian jalankan:

```bash
pip install -r requirements.txt
```

Atau install langsung:

```bash
pip install tabulate
```

### Menjalankan Program

Jalankan file utama:

```bash
python main.py
```

---

## Pengujian OOP

Program menyediakan menu khusus untuk menguji requirement OOP.

Pilih:

```text
4. OOP Testing
```

Kemudian akan muncul:

```text
==========================================
               OOP TESTING
==========================================
1. Test Objects
2. Test Instance Method
3. Test Class Method
4. Test Static Method
5. Test Getter and Setter
6. Test Inheritance
7. Run All Tests
8. Back
==========================================
```

### 1. Test Objects

Digunakan untuk menunjukkan object yang telah dibuat.

Program memiliki minimal dua object untuk setiap main class:

```python
product1
product2

customer1
customer2

sale1
sale2
```

### 2. Test Instance Method

Digunakan untuk menguji method yang menggunakan `self`.

Contoh:

```python
product.show_info()
customer.show_info()
sale.show_receipt()
```

### 3. Test Class Method

Digunakan untuk menguji method yang menggunakan `cls`.

Contoh:

```python
Product.change_store_name()
Customer.change_customer_type()
Sale.change_tax()
```

### 4. Test Static Method

Digunakan untuk menguji method yang tidak menggunakan `self` maupun `cls`.

Contoh:

```python
Product.validate_price()
Product.format_price()
Customer.validate_phone()
Sale.calculate_discount()
```

### 5. Test Getter and Setter

Digunakan untuk menguji getter dan setter pada private attribute.

Contoh valid:

```python
product.stock = 20
```

Contoh invalid:

```python
product.stock = -10
```

Nilai negatif akan ditolak oleh setter.

### 6. Test Inheritance

Digunakan untuk menunjukkan hubungan inheritance:

```text
Person
   │
   └── Customer
```

Contoh:

```python
customer.show_person_info()
```

Method tersebut berasal dari parent class `Person`.

### 7. Run All Tests

Menu ini menjalankan seluruh pengujian OOP sekaligus, meliputi:

* Object
* Instance Method
* Class Method
* Static Method
* Getter
* Setter
* Invalid Setter
* Inheritance

---

## Contoh Penggunaan

### Main Menu

```text
==============================================
       COMPUTER SALES MANAGEMENT SYSTEM
==============================================
Store : Alfauzi Computer
Devices and Accessories
==============================================
1. Product Management
2. Customer Management
3. Sales Management
4. OOP Testing
5. Exit
==============================================
Choose menu:
```

### Product Management

```text
==========================================
          PRODUCT MANAGEMENT
==========================================
1. Show Products
2. Add Stock
3. Reduce Stock
4. Change Store Name
5. Back
==========================================
Choose menu: 1
```

Output:

```text
ID Product  Name                  Price       Stock  Category
---------------------------------------------------------------
P001        Mechanical Keyboard   Rp750,000   10     Keyboard
P002        Gaming Mouse          Rp350,000   15     Mouse
```

### Customer Management

```text
==========================================
         CUSTOMER MANAGEMENT
==========================================
1. Show Customers
2. Change Address
3. Change Status
4. Change Customer Type
5. Back
==========================================
Choose menu: 1
```

Output:

```text
ID Customer  Name   Phone          Address      Status
---------------------------------------------------------
C001         Andi   081234567890   Samarinda    Active
C002         Budi   082345678901   Balikpapan   Active
```

### Sales Management

```text
==========================================
           SALES MANAGEMENT
==========================================
1. Create Sale
2. Show Sales
3. Change Tax
4. Back
==========================================
Choose menu: 1
```

Contoh transaksi:

```text
Customer ID : C001
Product ID  : P001
Quantity    : 1

Sale processed successfully!
```

Sales receipt:

```text
==========================================
              SALES RECEIPT
==========================================
Sale ID     : S003
Customer    : Andi
Product     : Mechanical Keyboard
Price       : Rp750,000
Quantity    : 1
Total       : Rp750,000
==========================================
```

---

## Contoh Screenshot Output

Screenshot hasil program dapat ditempatkan pada folder `assets`.

Contoh struktur:

```text
computer_sales_management/
│
├── assets/
│   ├── main_menu.png
│   ├── product_menu.png
│   ├── customer_menu.png
│   ├── sales_menu.png
│   └── oop_testing.png
│
└── README.md
```

Kemudian ditampilkan di README menggunakan:

```html
<img src="assets/main_menu.png" alt="Main Menu" width="500"/>
```

---

## Kesimpulan

**Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer** merupakan program berbasis Python yang menerapkan konsep Object-Oriented Programming untuk mengelola product, customer, dan sales transaction.

Program telah menerapkan **Class & Object, Attributes, Methods, Encapsulation, Getter & Setter, Validation, Inheritance, serta Modularization**.

Program juga dilengkapi dengan **OOP Testing Menu** untuk mendemonstrasikan setiap konsep OOP yang digunakan dalam project.