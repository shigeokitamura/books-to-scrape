import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import threading

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper")
        self.root.geometry("800x600")

        # Variables
        self.url_var = tk.StringVar(value="https://books.toscrape.com/catalogue/")
        self.start_page = tk.IntVar(value=1)
        self.end_page = tk.IntVar(value=50)
        self.is_scraping = False
        self.book_data = []

        self.create_widgets()

    def create_widgets(self):
        # URL Input
        url_frame = ttk.LabelFrame(self.root, text="URL Settings", padding=10)
        url_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(url_frame, text="Base URL:").pack(side="left")
        ttk.Entry(url_frame, textvariable=self.url_var, width=50).pack(side="left", padx=5)

        # Page Range
        page_frame = ttk.LabelFrame(self.root, text="Page Range", padding=10)
        page_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(page_frame, text="Start Page:").pack(side="left")
        ttk.Entry(page_frame, textvariable=self.start_page, width=5).pack(side="left", padx=5)

        ttk.Label(page_frame, text="End Page:").pack(side="left")
        ttk.Entry(page_frame, textvariable=self.end_page, width=5).pack(side="left", padx=5)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.start_btn = ttk.Button(btn_frame, text="Start Scraping", command=self.start_scraping)
        self.start_btn.pack(side="left", padx=5)

        self.save_btn = ttk.Button(btn_frame, text="Save Data", command=self.save_data)
        self.save_btn.pack(side="left", padx=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress.pack(fill="x", padx=10, pady=5)

        # Status Label
        self.status_var = tk.StringVar(value="Ready to start...")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=5)

        # Result Text Area
        self.result_text = scrolledtext.ScrolledText(self.root, height=20)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=5)

    def start_scraping(self):
        if self.is_scraping:
            return

        self.book_data = []
        self.result_text.delete(1.0, tk.END)
        self.is_scraping = True
        self.start_btn.config(text="Scraping...")

        # Start scraping in a separate thread
        thread = threading.Thread(target=self.scrape_data)
        thread.daemon = True
        thread.start()

    def scrape_data(self):
        try:
            start = self.start_page.get()
            end = self.end_page.get()
            total_pages = end - start + 1

            for page_num in range(start, end + 1):
                if not self.is_scraping:
                    break

                url = f"{self.url_var.get()}page-{page_num}.html"
                self.status_var.set(f"Scraping page {page_num}...")

                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")
                book_entries = soup.find_all("article", class_="product_pod")

                for entry in book_entries:
                    book = {
                        "title": entry.h3.a["title"],
                        "price": entry.find("p", class_="price_color").text.strip(),
                        "availability": entry.find("p", class_="instock availability").text.strip()
                    }
                    self.book_data.append(book)

                    # Update result text
                    self.result_text.insert(tk.END, f"Title: {book['title']}\n")
                    self.result_text.insert(tk.END, f"Price: {book['price']}\n")
                    self.result_text.insert(tk.END, f"Availability: {book['availability']}\n")
                    self.result_text.insert(tk.END, "-" * 50 + "\n")
                    self.result_text.see(tk.END)

                # Update progress
                progress = (page_num - start + 1) / total_pages * 100
                self.progress_var.set(progress)

            self.status_var.set("Scraping completed!")
            messagebox.showinfo("Complete", "Scraping process has finished!")

        except requests.exceptions.RequestException as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            self.is_scraping = False
            self.start_btn.config(text="Start Scraping")

    def save_data(self):
        if not self.book_data:
            messagebox.showwarning("Warning", "No data to save!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scraped_data_{timestamp}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.book_data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", f"Data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
