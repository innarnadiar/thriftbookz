# THRIFTBOOKZ - CRUD Application for Secondhand Bookshop Stock Management

ThriftBookz - a Python application for managing physical secondhand book stock with Create, Read, Update, Delete, and Search operations.

## Business Understanding

Digital Independent secondhand (preloved/thrift) book sellers usually sell on multiple social media such as Instagram, e-commerce or even through Whatsapp groups. Although require manual effort, their current system actually works well. They post a photo of the book on Instagram, using hashtags like #stillavailable to mark books status, and put comment "booked" if someone buys the book. Most of the time, buyers must confirm by DM first ("is this still available?") before paying. From customer pov, sotrefront side of the business is fine.

The problem is everything a storefront cannot see. 1) Sellers don't know their real profit. The cost of each secondhand book might differ, with variation of margin. Sellers know their sales, but not their profit exactly. 2) A feed cannot answer big-picture questions like "how many books are available now?" "How much money is stuck in books that never sell?" or conduct a fast search on a specific title. 3) Secondhand book depreciate, how they monitor things such as cost of depreciated books, they're not gonna show on Instagram feeds.

**Benefits:**

- Answer "is this book still available?" in seconds, for every copy of a title.
- Know the real profit, because the buying cost of every book is recorded.
- Depreciated or lost books stay in the report as losses, so profit numbers stay honest.
- See which category sells fastest, to decide what to buy next.

**Target Users:**

Secondhand book sellers or admins ( with > 100 books), who sells their books online

## Features
    1. Tambah buku masuk      (Create)
    2. Lihat stok & laporan   (Read + Report)
    3. Cari / cek stok        (Search)
    4. Ubah data buku         (Update)
    5. Hapus data salah input (Delete)
    0. Keluar

* **Create:** record a book entering the warehouse: title, author, category, condition, buying price, selling price.
* **Read:** see all stock and the money report.
* **Search:** answer a buyer's DM ("is Animal Farm still available?"). It shows every copy with its status, price, and condition.
* **Update:** mark a booking, a sale, a discount, or a damaged book.
* **Delete:** remove a duplicate or mistyped row, with typed-ID confirmation.

## Installation

1. **Prerequisites:**
    * Python version 3.6 or newer
    * No extra packages needed

2. **Installation:**
    ```bash
    git clone https://github.com/<your-username>/thriftbookz.git
    cd thriftbookz
    ```

## Usage

1. **Run the application:**
    ```bash
    python thriftbookz_main.py
    ```

2. **CRUD Operations:**
    * **Create:** record a book entering the warehouse — title, author, category, condition, buying price, selling price.
   * **Read:** see all stock and the money report.
   * **Search:** answer a buyer's DM ("is Animal Farm still available?") — shows every copy with its status, price, and condition.
   * **Update:** mark a booking, a sale, a discount, or a damaged book.
   * **Delete:** remove a duplicate or mistyped row, with typed-ID confirmation.

## Data Model
Data is stored as a list of dictionaries in memory. one dictionary per physical book:
- id (str) — book ID, e.g. BK001.
- title (str) — title.
- author (str) — author.
- category (str) — one code, format FORM-AUDIENCE-TOPIC.
-     Form: FIC/NON (Fiction/Nonfiction).
-     Audience: ANK/RMJ/DWS/SUM (children 0–11 / teens 12–18 / adult / all ages).
-     Topic: 14 codes for fiction genres and nonfiction fields, such as LIT Literature, HIST History, plus LAI (other) as a catch-all.
- condition (str) — IOBA/ABAA grade: F, VG, G, FR, P (ioba.org/conditions-definitions).
- paid (int) — buying cost in rupiah. Cannot be changed after entry.
- price (int) — selling price in rupiah.
- status (str) — book lifecycle: available, booked, sold, depreciated.
- date_in (date) — YYYY-MM-DD: date when the book in.
- date_out (date) — YYYY-MM-DD: date when the book sold.
- notes (str) — free note; required defect note for grades G/FR/P.


## Contributing
Contributions are welcome! Please open a pull request or submit an issue if you find problems or have ideas. You can also reach me at innarnadiar@gmail.com.

