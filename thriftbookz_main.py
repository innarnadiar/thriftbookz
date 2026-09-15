from datetime import date, datetime, timedelta
from tabulate import tabulate

# 1. Daftar Nilai/Kategori yang Dianggap Valid

# Kondisi, skala IOBA/ABAA (ioba.org/conditions-definitions):
# F  Fine       hampir sempurna
# VG Very Good  terlihat bekas pakai (kuning tipis, pudar, ttd pemilik), rapi, utuh
# G  Good       sangat terlihat bekas pakai (tekukan, jilid longgar, coretan), cacat wajib dicatat
# FR Fair       aus (kuning parah, jamur, air, robek kecil, serabut), teks lengkap
# P  Poor       rusak (jilid rontok, halaman lepas/hilang, noda parah, hanya layak reading copy
# Aturan IOBA: semua cacat harus dicatat mulai dari Good ke bawah.
# Kategori = satu kolom berformat BENTUK-PEMBACA-SUBJEK, contoh N-ANK-SAI.
# Format tetap, jadi pencarian per bagian cukup pakai substring.
#
# BENTUK  (BISAC)  F=Fiksi  N=Nonfiksi
# PEMBACA (BISAC)  ANK=anak 0-11  RMJ=remaja 12-18  DWS=dewasa
#                  SUM=semua umur
# SUBJEK  fiksi   : SAS sastra, HIS historis, FAN fantasi, MIS misteri,
#                   ROM romansa, KOM komik
#         nonfiksi: SEJ sejarah, POL politik, PDK pendidikan, BIO biografi,
#                   SAI sains, AGM agama, PRK praktis (bisnis, hobi, masak,
#                   pengembangan diri, kesehatan), LAI lainnya.
CONDITIONS = ("F", "VG", "G", "FR", "P") 
BOOK_STATUS = ("available", "booked", "sold", "depreciated")
SHELVES = ( "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10" )
FORMATS = ("FIC", "NON") 
AUDIENCES = ("KIDS", "TEEN", "ADULT", "ANYONE") 
TOPICS = ( 
    "LIT", "HISTFIC", "FANTASY", "MYSTERY", "ROMANCE", 
    "COMIC", "HISTORY", "POLITICS", "EDUCATION", "BIOGRAPHY", 
    "SCIENCE", "RELIGION", "PRACTICAL", "OTHER" 
    )

# 2. Data Awal 
DATA = [
    {"id": "BK001", "title": "Bumi Manusia", "author": "Pramoedya A. Toer",
     "category": "FIC-ADULT-HISTFIC", "condition": "VG", "shelf": "S1",
     "paid": 45000, "price": 95000, "status": "sold",
     "date_in": "2026-03-02", "date_out": "2026-04-10",
     "notes": "pencil underlining on pages 40-42"},
 
    {"id": "BK002", "title": "Animal Farm", "author": "George Orwell",
     "category": "FIC-ANYONE-LIT", "condition": "G", "shelf": "S2",
     "paid": 40000, "price": 90000, "status": "available",
     "date_in": "2026-05-18", "date_out": "",
     "notes": "dog-eared corners, faded spine"},
 
    {"id": "BK003", "title": "Animal Farm", "author": "George Orwell",
     "category": "FIC-ANYONE-LIT", "condition": "F", "shelf": "S2",
     "paid": 55000, "price": 120000, "status": "booked",
     "date_in": "2026-06-01", "date_out": "",
     "notes": "buyer agreed, waiting on the transfer"},
 
    {"id": "BK004", "title": "Dinosaur Encyclopedia", "author": "Tim BIP",
     "category": "NON-KIDS-SCIENCE", "condition": "G", "shelf": "S5",
     "paid": 35000, "price": 80000, "status": "available",
     "date_in": "2026-02-14", "date_out": "",
     "notes": "crayon marks, mostly cleaned off"},
 
    {"id": "BK005", "title": "Sapiens", "author": "Yuval Noah Harari",
     "category": "NON-ADULT-HISTORY", "condition": "FR", "shelf": "S6",
     "paid": 50000, "price": 110000, "status": "available",
     "date_in": "2026-07-21", "date_out": "",
     "notes": "torn cover, all pages there"},
 
    {"id": "BK006", "title": "Laut Bercerita", "author": "Leila S. Chudori",
     "category": "FIC-TEEN-HISTFIC", "condition": "P", "shelf": "S10",
     "paid": 30000, "price": 55000, "status": "depreciated",
     "date_in": "2026-01-09", "date_out": "2026-02-01",
     "notes": "water damage, not sellable"},
 
    {"id": "BK007", "title": "Kubah", "author": "Ahmad Tohari",
     "category": "FIC-ADULT-LIT", "condition": "VG", "shelf": "S1",
     "paid": 35000, "price": 78000, "status": "available",
     "date_in": "2026-08-30", "date_out": "",
     "notes": "old shop stamp on the title page"},
 
    {"id": "BK008", "title": "Tuesdays With Morrie", "author": "Mitch Albom",
     "category": "NON-ADULT-BIOGRAPHY", "condition": "G", "shelf": "S7",
     "paid": 25000, "price": 60000, "status": "available",
     "date_in": "2026-04-05", "date_out": "",
     "notes": "front cover creased, pages 12-15 highlighted"},
 
    {"id": "BK009", "title": "Nexus", "author": "Yuval Noah Harari",
     "category": "NON-ADULT-HISTORY", "condition": "F", "shelf": "S6",
     "paid": 85000, "price": 165000, "status": "booked",
     "date_in": "2026-08-02", "date_out": "",
     "notes": "agreed but never transferred"},
 
    {"id": "BK010", "title": "The Demon-Haunted World", "author": "Carl Sagan",
     "category": "NON-ADULT-SCIENCE", "condition": "FR", "shelf": "S8",
     "paid": 40000, "price": 85000, "status": "available",
     "date_in": "2026-06-15", "date_out": "",
     "notes": "cracked spine, first 20 pages yellowed"},
 
    {"id": "BK011", "title": "The Alchemist", "author": "Paulo Coelho",
     "category": "FIC-ANYONE-LIT", "condition": "VG", "shelf": "S3",
     "paid": 30000, "price": 70000, "status": "sold",
     "date_in": "2026-05-02", "date_out": "2026-05-20",
     "notes": "previous owner's name inside the front cover"},
 
    {"id": "BK012", "title": "Filosofi Teras", "author": "Henry Manampiring",
     "category": "NON-ADULT-PRACTICAL", "condition": "VG", "shelf": "S7",
     "paid": 40000, "price": 88000, "status": "sold",
     "date_in": "2026-06-10", "date_out": "2026-06-22",
     "notes": "shrink wrap still intact"},
 
    {"id": "BK013", "title": "Laskar Pelangi", "author": "Andrea Hirata",
     "category": "FIC-ANYONE-LIT", "condition": "G", "shelf": "S3",
     "paid": 28000, "price": 65000, "status": "sold",
     "date_in": "2026-04-18", "date_out": "2026-05-06",
     "notes": "loose binding, reinforced with book tape"},
 
    {"id": "BK014", "title": "Atomic Habits", "author": "James Clear",
     "category": "NON-ADULT-PRACTICAL", "condition": "F", "shelf": "S7",
     "paid": 60000, "price": 130000, "status": "sold",
     "date_in": "2026-07-05", "date_out": "2026-07-13",
     "notes": "almost like new"},
 
    {"id": "BK015", "title": "Rumah Kaca", "author": "Pramoedya A. Toer",
     "category": "FIC-ADULT-HISTFIC", "condition": "VG", "shelf": "S1",
     "paid": 48000, "price": 99000, "status": "sold",
     "date_in": "2026-02-20", "date_out": "2026-04-02",
     "notes": "paper evenly yellowed"},
 
    {"id": "BK016", "title": "High School Maths Year 10",
     "author": "Tim Erlangga",
     "category": "NON-TEEN-EDUCATION", "condition": "G", "shelf": "S9",
     "paid": 15000, "price": 35000, "status": "available",
     "date_in": "2026-01-15", "date_out": "",
     "notes": "lots of pencil working in the exercises"},
]

RECYCLE_BIN = []


#########################################################################
# MENU 1. CREATE & INPUT - Add new books into catalog and ask user inputs
#########################################################################

def add_book(books, bin_books):
    """Add one second-hand book after validating its required details."""
    print("\n=== ADD BOOK ===")

    book = {}
    book["id"] = f"BK{max([int(b['id'][2:]) for b in books + bin_books] + [0]) + 1:03d}"
    book["title"] = get_user_input("Title", 1)
    book["author"] = get_user_input("Author", 1).title()

    # Make sure no duplicates
    for old in books:
        if (old["title"].lower() == book["title"].lower()
                and old["author"].lower() == book["author"].lower()):
            print("There is same title book already available - make sure this is a different copy.")
            if not get_confirmation_YN("Carry on?"):
                print("Nothing saved.\n")
                return
            break

    book["category"] = get_user_input("Category", 7)
    book["condition"] = get_user_input("Condition grade", 3, CONDITIONS)
    book["notes"] = get_user_input(book["condition"], 6)
    book["shelf"] = get_user_input("Which shelf", 3, SHELVES)
    book["paid"] = get_user_input("Buy Price", 2)
    book["price"] = get_user_input("Sell Price", 2)

    # Make sure reasonable selling price
    if book["price"] <= book["paid"]:
        print("  That price doesn't clear what we paid for it.")

    book["date_in"] = get_user_input("Date it came in", 4)
    book["date_out"] = ""
    book["status"] = "available"

    # Confirmation step
    show_book_details(book)
    if get_confirmation_YN("Save it?"):
        books.append(book)
        print(f"Saved. {book['id']} is on shelf {book['shelf']}.\n")
    else:
        print("Process canceled. Nothing saved.\n")

        
def get_user_input(label, input_type, choices=None):
    """ 
    Get different type of user inputs.

    input_type : 1=text 2=number 3=collection 
    4=date 5=optional text 6=notes 7=category 
    choice : collections
    """
    while True:

        if input_type == 1:
            answer = input(f"Enter {label}: ").strip()
            if answer != "":
                return answer
            print(f"{label} for book cannot be blank. Try again.")

        elif input_type == 2:
            answer = input(f"Enter {label} (digits only, e.g. 45000): ").strip()
            if not answer.isdigit() or int(answer) <= 0:
                print(f"{label} number for book have to be digits and more than 0. Try again.")
                continue
            return int(answer)

        elif input_type == 3:
            print(f"\n  {label}:")
            n = 1

            # If collection too long, split into 2 columns
            if len(choices) <= 8:
                for n, i in enumerate(choices, start=1):
                    print(f"    {n:>2}. {i}")
            else:
                half = (len(choices) + 1) // 2
                width = max(len(i) for i in choices) + 2
                for n in range(half):
                    left = f"{n + 1:>2}. {choices[n]:<{width}}"
                    right = f"{n + half + 1:>2}. {choices[n + half]}" if n + half < len(choices) else ""
                    print(f"    {left}{right}".rstrip())

            # Taking user input    
            answer = input("  Pick a number: ").strip()
            if answer.isdigit() and 1 <= int(answer) <= len(choices):
                return choices[int(answer) - 1]
            print(f"{label} for book have to be based on options. Try again.")

        elif input_type == 4:
              while True:
                answer = input(f"  {label} (YYYYMMDD, blank = today): ").strip()
                if not answer:
                    return datetime.today().strftime("%Y-%m-%d")

                try:
                    datetime.strptime(answer, "%Y-%m-%d")
                    return answer
                except ValueError:
                    print(f"{label} for book does not match format. Try again.")

        elif input_type == 5:
            return input(f"  {label} (can be blank): ").strip()

        elif input_type == 6:
            # label holds the grade
            if label in ('FR','G','P'):
                return get_user_input("Describe the damage", 1)
            return get_user_input("Notes", 5)

        else:
            book_format = get_user_input("Fiction or nonfiction", 3, FORMATS)
            audience = get_user_input("Who's it for", 3, AUDIENCES)
            topic = get_user_input("What's it about", 3, TOPICS)
            return book_format + "-" + audience + "-" + topic


def get_confirmation_YN(question):
    """
    Confirms before anything is saved.

    Input : question (str)
    Output: bool, True when the answer is Y
    """
    while True:
        answer = input(f"{question} (Y/N): ").strip().upper()
        if answer == "Y":
            return True
        if answer == "N":
            return False
        print("Input doesn't match format Y or N. Try again.")


#########################################################################
# MENU 2. READ, SHOW & SEARCH - Show all books, search, and reports
#########################################################################

def show_book(data):
    """Read stock, search books, and view simple inventory reports."""
    while True:
        print("\n=== SHOW BOOKS & REPORTS ===")
        print("1. Show all books")
        print("2. Search")
        print("3. Show only available books (catalog)")
        print("4. Show only bookings (to follow-up)")
        print("5. Show only depreciated books (to follow-up)")
        print("6. Financial reports")
        print("7. Back")

        # Prompt KPI Monitor - for books that are depreciated (90d <) and bookings that expired (24hr <)
        check_depreciation(DATA)
        expired = expired_booking(DATA)
        if expired:
            print(f"\nWARNING: {len(expired)} booking(s) have expired.")
            print("Check them from the Show Books & Reports menu.\n")

        # Input user choice of menu
        choice = input("Type menu number: ").strip()
        if choice == "1":
            show_table(data,"ALL BOOKS")
        elif choice == "2":
            find_a_book(data)
        elif choice == "3":
            available = [book for book in data if book["status"] == "available"]
            show_table(available, "AVAILABLE BOOKS")
            select_and_manage(available,data)
        elif choice == "4":
            booked = [book for book in data if book["status"] == "booked"]
            show_table(booked, "BOOKED BOOKS")
            select_and_manage(booked,data)
        elif choice == "5":
            depreciated = [book for book in data if book["status"] == "depreciated"]
            show_table(depreciated, "DEPRECIATED BOOKS")
            select_and_manage(depreciated,data)
        elif choice == "6":
            finance_report(data)
        elif choice == "7":
            return
        else:
            print("Menu number not available")


def show_table(books, heading):
    print(f"=== {heading} ===")

    if not books:
        print("No books found.\n")
        return

    # Arrange how the values printed: add Rp on book price, limit title to 22char, etc.
    rows = []
    for book in books:
        rows.append([book["id"], book["title"][:22], book["category"],
                     book["condition"], book["shelf"],
                     f"Rp{book['price']:,}", book["status"], book["date_in"],
                     book["date_out"] or "-"])

    # Display on tabulate
    print(
        tabulate(rows, headers=["ID", "Title", "Category", 
                                 "Grade", "Shelf", "Price", "Status","Date In","Date Out"],
            tablefmt="grid")
        )

    # show number of books inside this table
    print(f"{len(books)} book(s)\n")


def show_book_details(book):
    print("-"*20," Book Information ","-"*20)
    print(f"ID        : {book['id']}")
    print(f"Title     : {book['title']}")
    print(f"Author    : {book['author']}")
    print(f"Category  : {book['category']}")
    print(f"Condition : {book['condition']}")
    print(f"Shelf     : S{book['shelf']}")
    print(f"Paid      : Rp{book['paid']:,}")
    print(f"Price     : Rp{book['price']:,}")
    print(f"Profit    : Rp{book['price'] - book['paid']:,}")
    print(f"Status    : {book['status']}")
    print(f"Date in   : {book['date_in']}")
    if book["status"] == "available":
        print(f"Days in   : {days_in_stock(book)} of 90")
    print(f"Notes     : {book['notes']}")
    print("-"*50)

def days_in_stock(book):
    return (date.today() - datetime.strptime(book["date_in"], "%Y-%m-%d").date()).days

def expired_booking(books):
 
    return [
        book for book in books
        if book["status"] == "booked"
        and book["date_out"]
        and datetime.strptime(book["date_out"],"%Y-%m-%d").date()< datetime.today().date()
    ]

def check_depreciation(books):
    """If 90 days after date_in an unsold copy status change into depreciated."""

    for book in books:
        if book["status"] == "available" and days_in_stock(book) > 90:
            book["status"] = "depreciated"
            


def find_a_book(books, manage=True):
    """
    Find books using one of four criteria:
    ID, title, author, or category.

    Output: one book dict, or None when the user go back from menu.
    """
    while True:
        search_type = get_user_input("=== FIND BOOK ===",3,("ID", "Title", "Author", "Category", "Back"))

        if search_type == "Back":
            return None

        keyword = get_user_input("Insert search keyword", 1).lower()
        results=[]
        field = {"ID":"id","Title":"title","Author":"author","Category":"category"}[search_type]
        results = [book for book in books if keyword in book[field].lower()]
        if not results:
            print("Sorry. No matching books found.")
            continue

        print(f"SUCCESS: Found {len(results)} matching book(s) in the ThriftBookz stock.") 
        select_and_manage(results, books) if manage else None

        if manage:
            return None
        if len(results) == 1:
            return results[0]

        show_table(results, "MATCHING BOOKS")
        book_id = get_user_input("Book ID", 1).upper()

        for book in results:
            if book["id"] == book_id:
                return book

        print(f"ERROR: Book ID {book_id} is not in the matching results.")

def select_and_manage(results, books):
    """Select one book from search results and open its management (edit or delete) menu."""
    if len(results) == 1:
        manage_book(books, results[0])
        return

    book_id = get_user_input("Select Book ID", 1).upper()

    for book in results:
        if book["id"] == book_id:
            manage_book(books, book)
            return

    print(f"ERROR: Book ID {book_id} was not found in the search results.")


def finance_report(books):
    sales_income = 0
    purchase_cost = 0
    unsold_cost = 0
    depreciated_cost = 0
    by_topic = []

    for book in books:
        if book["status"] == "sold":
            sales_income += book["price"]
            purchase_cost += book["paid"]

            topic = book["category"].split("-")[2]
            profit = book["price"] - book["paid"]

            found = False

            for item in by_topic:
                if item[0] == topic:
                    item[1] += profit
                    found = True
                    break

            if not found:
                by_topic.append([topic, profit])

        elif book["status"] == "available":
            unsold_cost += book["paid"]
        elif book["status"] == "depreciated":
            depreciated_cost += book["paid"]

    profit = sales_income - purchase_cost

    print("\n=== PERFORMANCE REPORT ===")
    print(f"Profit from sold books      : Rp{profit:,}")
    print(f"Money spent on unsold books : Rp{unsold_cost:,}")
    print(f"Money might lost to depreciation  : Rp{depreciated_cost:,}")
  

    print("\n=== PROFIT BY TOPIC ===")
    for item in by_topic:
        print(f"Topic: {item[0]:<15} --> Profit: Rp{item[1]:,}")



#########################################################################
# MENU 3. MANAGE BOOK: EDIT & DELETE
#########################################################################

def manage_book(books, book=None):
    """
    Manage one book can be update or delete.
    By updating selected attributes or deleting identified book.

    If no book is provided, the user is asked to find one.
    """
    # Show all books before edit or delete
    if book is None:
        if not books:
            print("ERROR: There are no books to manage.")
            return
        show_table(books, "ALL BOOKS")
        

    while True:
        # Display book details if it is continue from menu search
        if book is not None:
            print("\n--- SELECTED BOOK ---")
            show_book_details(book)
        
        choice = get_user_input("What do you want to do?",3,
            (
                "Update status",
                "Update price",
                "Update condition and notes",
                "Update category",
                "Update shelf",
                "Delete book",
                "Batch delete",
                "Back"
            )
        )

        if choice == "Back":
            return

        if choice == "Batch delete":
            batch_delete_menu(books, RECYCLE_BIN)
            if not books:
                return
            book = None
            continue

        if book is None:
            book = find_a_book(books, manage=False)
            if book is None:
                continue
            print("\n--- SELECTED BOOK ---")
            show_book_details(book)

        if choice == "Update status":
            if book["status"] == "sold":
                print(f"  {book['id']} is already sold. Status cannot be changed.")
            else:
                new_status = get_user_input("New status",3,BOOK_STATUS)
                if new_status == "sold":
                    book["date_out"] = date.today().isoformat()
                update_fields(book,[("status",new_status,"Status")])
        elif choice == "Update price":
            new_price = get_user_input("New price",2)
            update_fields(book,[("price",new_price,"Price")])
        elif choice == "Update condition and notes":
            new_condition = get_user_input("New condition grade",3,CONDITIONS)
            if new_condition in ("G","FR","P"):
                print("Notes are required for condition G, FR, or P.")
                new_notes = get_user_input("New notes",1)
            update_fields(book,[("condition",new_condition,"Condition"),("notes",new_notes,"Notes")])
        elif choice == "Update category":
            new_category = get_user_input("New Category",7)
            update_fields(book,[("category",new_category,"Category")])
        elif choice == "Update shelf":
            new_shelf = get_user_input("New shelf", 3, SHELVES)
            update_fields(book,[("shelf",new_shelf,"Shelf")])
        elif choice == "Delete book":
            show_book_details(book)
            if get_confirmation_YN("Delete this book?"):               
                RECYCLE_BIN.append(book)
                books.remove(book)
                print(f"\nSUCCESS: {book['id']} has been moved to recycle bin.")
                return
        elif choice == "Batch delete":
            batch_delete_menu(books, RECYCLE_BIN)
        elif choice == "Back":
            return


def update_fields(book, changes):
    print("\n--- UPDATE CONFIRMATION ---")
    print(f"Book ID     : {book['id']}")
    print(f"Title       : {book['title']}")
    for field, new_value, label in changes: print(f"{label:<12}: {book[field]} → {new_value}")
    if get_confirmation_YN("Update this book?"):
        for field, new_value, label in changes: 
            book[field] = new_value
            if field == "status" and new_value == "sold":
                book["date_out"] = date.today().isoformat()
        print(f"\nSUCCESS: {book['id']} has been updated.")
        return True
    print("\nCANCELLED: no changes were made.")
    return False


def batch_delete_menu(books, bin_books):
    """Delete several books using comma-separated IDs."""
    if not books:
        print("ERROR: There are no books in the active stock to delete.")
        return
    ids = get_user_input("Book IDs (e.g. BK002, BK004)", 1).upper().replace(" ", "").split(",")
    valid = [book["id"] for book in books if book["id"] in ids]
    invalid = [book_id for book_id in ids if book_id not in [book["id"] for book in books]]
    if not valid:
        print("ERROR: None of the entered book IDs were found in the active stock.")
        return
    if invalid:
        print(f"WARNING: These IDs were not found: {', '.join(invalid)}")
    if get_confirmation_YN(f"Delete {len(valid)} selected book(s)?"):
        count = batch_delete_books(books, bin_books, valid)
        print(f"SUCCESS: {count} book(s) were removed from active stock and moved to the recycle bin.")
    else:
        print("CANCELLED: No books were deleted.")

def batch_delete_books(books, bin_books, book_ids):
    """Move selected book IDs from stock to the recycle bin."""
    selected = [book for book in books if book["id"] in book_ids]
    for book in selected:
        books.remove(book)
        bin_books.append(book)
    return len(selected)


def trash_bin_menu(books, bin_of_deleted):
    """
    Shows the bin and puts a book back if asked.
 
    Input : books (list of dicts), bin_of_deleted (list of dicts)
    Output: None
    """
    show_table(bin_of_deleted, "Bin")
    if len(bin_of_deleted) == 0:
        return
    if not get_confirmation_YN("Put any of those back?"):
        return
 
    book = find_a_book(bin_of_deleted, "Which one?")
    if book is None:
        return
 
    if get_confirmation_YN(f"Restore {book['id']}?"):
        bin_of_deleted.remove(book)
        books.append(book)
        print(f"{book['id']} is back on shelf {book['shelf']}.\n")
    else:
        print("Nothing changed.\n")


#########################################################################
# MAIN MENU - THRIFTBOOKZ
#########################################################################

def main():
    while True:
        print("\n" + "=" * 50)
        print("======= THRIFTBOOKZ - PRELOVED BOOK STOCK =======")
        print("=" * 50)
        print("1. Register a book we just bought")
        print("2. Books status, search, and reports")
        print("3. Edit a book (update & delete)")
        print("4. Recycle bin")
        print("5. Exit")
        choice = input("Type menu number: ").strip()
        if choice == "1":
            add_book(DATA, RECYCLE_BIN)
        elif choice == "2":
            show_book(DATA)
        elif choice == "3":
            manage_book(DATA)
        elif choice == "4":
            trash_bin_menu(DATA, RECYCLE_BIN)
        elif choice == "5":
            print("\nProgram closed. Remember none of today's edits were saved.\n")
            break
        else:
            print("  Pick a number from 1 to 5.")

if __name__ == "__main__":
    main()