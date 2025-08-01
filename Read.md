
 # 🕷️ Web Scraper Project – GitHub Repo Extractor

This project is a powerful, stealth-enabled web scraper built using **Python + Selenium** to automate the process of extracting repository details from GitHub collections.

---

## ✨ Features

- 🔍 **Automated Web Scraping** – Extracts data like repo names, stars, forks, and languages.
- 🧠 **Stealth Mode Enabled** – Avoids bot detection using ChromeDriver stealth configuration.
- 🌐 **Handles JavaScript-Heavy Pages** – Scrapes dynamic content by rendering the full page.
- 📊 **Data Analytics** – Visualizes data with charts and graphs via Streamlit.
- 💾 **Export Options** – Save scraped results directly as CSV.
- 📁 **Download-Free Setup** – Uses `webdriver-manager`, so no need to manually install ChromeDriver.

---

## 📸 Screenshots
<img width="1911" height="882" alt="ouptut result 1" src="https://github.com/user-attachments/assets/eb30c344-5d01-4318-a485-7722b68fda4a" /><br><br>

<img width="1861" height="701" alt="output result 2" src="https://github.com/user-attachments/assets/a83164a8-b7b7-4092-a45f-90427f4da8f0" /><br><br>

<img width="1910" height="750" alt="output result 3" src="https://github.com/user-attachments/assets/2147674b-54a9-427b-b380-4e1edcd9fa0b" /><br><br>


 

---

## 💡 Use Cases

- 📈 Market & Trend Analysis
- 🧑‍💻 GitHub-based Research & Repo Discovery
- 🏢 Competitor & Project Intelligence
- 🤖 Dataset creation for AI/ML Models

---

## 🛠️ Setup & Installation

### 1. Clone the Repository

git clone https://github.com/yokodrea/scraper-project.git
cd scraper-project


### 2. Install Dependencies

pip install -r requirements.txt

✅ No need to download ChromeDriver manually — it's handled by webdriver-manager.

### 3. 🚀 Run the Scraper
   streamlit run scrape.py
   You can customize the GitHub collection URL inside scrape.py.

### 4. 📂 Output
The scraped data will be saved as:
> project_list.csv

### 5. 🔧 Tech Stack

**Language**: Python <br><br>
**Core Libraries**: selenium (for automation), pandas (for data handling), streamlit (for UI) ,webdriver-manager (auto-handles ChromeDriver)<br><br>
**Scraping Mode** : Headless browser via Chrome<br><br>
**Export Format**: CSV

## 📅 Future Enhancements

⏱️ Multi-threading for speed boost

📬 Real-time alerts on repo updates

🕒 Scheduler for auto-scraping (cron jobs)

🌐 Deploy as a hosted scraping service

## 🧪 Requirements
📌 To be filled in once final dependencies are set.
👉 See requirements.txt for more info.

## 📄 License
    This project is licensed under the MIT License.

