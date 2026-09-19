# Sistem Manajemen Penjualan Perangkat dan Aksesori Komputer

> **Nama:** Muhammad Alfauzi Syahputra  
> **Mata Kuliah:** Pemrograman Berorientasi Objek  
> **Bahasa Pemrograman:** Python

Aplikasi CLI berbasis Python untuk mengelola produk, stok, pelanggan, dan transaksi penjualan. Proyek ini menerapkan class dan object, encapsulation, getter/setter, validation, inheritance, class method, static method, package, dan modularization.

## Struktur Proyek

```text
posttest1/
├── main.py
├── requirements.txt
├── README.md
├── assets/
│   ├── main_menu.png
│   ├── menu_test.png
│   ├── object_test.png
│   ├── instance_test.png
│   ├── class_method_test.png
│   ├── static_method_test.png
│   ├── getterandsetter_test.png
│   ├── inheritance_test.png
│   ├── all_test.png
│   ├── sale_menu.png
│   └── create_sale.png
├── models/
│   ├── person.py
│   ├── customer.py
│   ├── product.py
│   └── sale.py
├── menus/
│   ├── product_menu.py
│   ├── customer_menu.py
│   ├── sale_menu.py
│   └── testing_menu.py
└── utils/
    └── helper.py
```

## Arsitektur OOP

`Customer` merupakan turunan dari `Person`. `Sale` menggunakan object `Customer` dan `Product` untuk membentuk transaksi penjualan.

```text
Person
  └── Customer

Sale ── menggunakan ── Customer
  └── menggunakan ──── Product
```

Atribut penting seperti stok dan status disimpan sebagai private attribute, kemudian diakses melalui property atau method yang menyediakan validasi. Kode dipisahkan ke dalam package `models`, `menus`, dan `utils` agar setiap modul memiliki tanggung jawab yang jelas.

## Fitur Aplikasi

- Menampilkan data produk dan pelanggan.
- Menambah serta mengurangi stok produk.
- Mengubah alamat dan status pelanggan.
- Membuat dan menampilkan transaksi penjualan.
- Menghitung total transaksi serta menampilkan struk.
- Mengubah nama toko, tipe pelanggan, dan pajak melalui class method.
- Menguji konsep OOP melalui menu **OOP Testing**.

## Cara Menjalankan

Pastikan Python 3 dan pip telah terinstal, lalu jalankan dari folder `posttest1`:

```bash
pip install -r requirements.txt
python main.py
```

## Pengujian OOP

Pilih menu **4. OOP Testing** pada menu utama. Pengujian yang tersedia:

1. Test Objects
2. Test Instance Method
3. Test Class Method
4. Test Static Method
5. Test Getter and Setter
6. Test Inheritance
7. Run All Tests

## Screenshot Pengujian

Semua screenshot menggunakan path absolut ke branch `main` agar tetap tampil dengan benar ketika README dibuka dari halaman repository maupun dari halaman edit GitHub.

### Menu OOP Testing

![Menu OOP Testing](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/menu_test.png?raw=true)

### Test Objects

![Test Objects](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/object_test.png?raw=true)

### Test Instance Method

![Test Instance Method](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/instance_test.png?raw=true)

### Test Class Method

![Test Class Method](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/class_method_test.png?raw=true)

### Test Static Method

![Test Static Method](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/static_method_test.png?raw=true)

### Test Getter dan Setter

![Test Getter dan Setter](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/getterandsetter_test.png?raw=true)

### Test Inheritance

![Test Inheritance](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/inheritance_test.png?raw=true)

### Run All Tests

![Run All Tests](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/all_test.png?raw=true)

## Contoh Penggunaan

### Main Menu

![Main Menu](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/main_menu.png?raw=true)

### Sales Menu

![Sales Menu](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/sale_menu.png?raw=true)

### Create Sale

![Create Sale](https://github.com/Alfauzi-S/Praktikum-PBO/blob/main/posttest/posttest1/assets/create_sale.png?raw=true)

## Kesimpulan

Sistem ini mendemonstrasikan penerapan konsep OOP pada aplikasi penjualan sederhana berbasis CLI. Screenshot dokumentasi telah menggunakan URL asset yang valid dan label yang sesuai dengan isi gambar.
