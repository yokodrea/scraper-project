import streamlit as st
import plotly.express as px
import pandas as pd
import time
import random


from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures


from selenium import webdriver  # allows launch web browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Github scraper", layout="wide")
st.title("GitHub Machine Learning Scraper")
st.sidebar.header("Customization Scraper")

# if the url is not provided it'll take this as default url
github_url = st.sidebar.text_input(
    "Enter the GitHub repository URL", "https://github.com/collections/machine-learning"
)
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None


def create_webdriver():
    """Creates and returns a Selenium WebDriver instance with configured options.
    The driver is set up to bypass automation detection and run in incognito mode.
    """

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("-incognito")
    driver_options.add_argument("--ignore-certificate-error")
    driver_options.add_argument("--ignore-ssl-errors")
    driver_options.add_argument("--disable-gpu")
    driver_options.add_argument("--headless")  # it won't open pop chrome
    driver_options.add_argument("--disable-popup-blocking")
    driver_options.add_argument("--disable-blink-features=AutomationControlled")
    driver_options.add_argument("--disable-extensions")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver_options.add_argument("--start-maximized")
    driver_options.add_argument("--no-sandbox")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]
    user_agent = random.choice(user_agents)
    driver_options.add_argument(f"user-agent={user_agent}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=driver_options)


    #if you are running locally and want to run with chromedrive just delete the above line and use this
    # chromedriver_path = r"C:\Users\sabar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    # service = Service(chromedriver_path)
    # driver = webdriver.Chrome(service=service, options=driver_options)

    # Apply stealth settings
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver


def scrap_git_repo(url):
    """
     Scrapes GitHub repositories from the given URL.
    Extracts project name, URL, description, stars, forks, and technologies used.

    """

    browser = create_webdriver()
    browser.get(url)

    if "Page not found" in browser.title:
        st.error(
            "Error: The GitHub page does not exist (404 Not Found). Please check the URL."
        )
        browser.quit()
        return pd.DataFrame()

    # Check if the page loaded successfully
    if "GitHub" not in browser.title:
        st.error("Error: The provided URL is not a valid GitHub page.")
        browser.quit()
        return pd.DataFrame()

    # for scrolling ifinite or if it has load button
    wait = WebDriverWait(browser, 10)
    action = ActionChains(browser)
    scroll_pause_time = 1
    screen_height = browser.execute_script("return window.screen.height;")
    i = 1

    while True:
        browser.execute_script("window.scrollTo(0, {});".format(i * screen_height))
        i += 1
        time.sleep(scroll_pause_time)

        try:

            # load_more_button = wait.until(
            #     expected_conditions.element_to_be_clickable(
            #         (By.XPATH, "//button[contains(text(),'Load more')]")
            #     )
            # )

            # action.move_to_element(load_more_button).click().perform()
            # time.sleep(2)
            # Wait until the button is visible
            load_more_button = wait.until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//button[contains(text(),'Load more')]")
                )
            )

            # Ensure the button is clickable
            load_more_button = wait.until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Load more')]")
                )
            )

            # Scroll to button and click using JavaScript
            browser.execute_script("arguments[0].scrollIntoView();", load_more_button)
            browser.execute_script("arguments[0].click();", load_more_button)

            time.sleep(2)

        except Exception as e:
            print(f"Load more button not found or not clickable: {e}")

        scroll_height = browser.execute_script("return document.body.scrollHeight;")
        if (screen_height * i) > scroll_height:
            print("Reached bottom of the page.")
            st.write("🔄 Done scrolling through GitHub page...")
            break

    projects = browser.find_elements(
        By.XPATH,
        "//article[@class='height-full border color-border-muted rounded-2 p-3 p-md-5 my-5']",
    )
    if not projects:
        st.warning("No repositories found. The page structure might have changed.")
        return []

    # extracting info of projects
    # project_list = {}
    project_list = []
    for i in projects:
        try:
            project_name = i.text
            project_url = i.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
            desc_ele = i.find_elements(
                By.XPATH, ".//div[@class='color-fg-muted mb-2 ws-normal']"
            )
            description = desc_ele[0].text if desc_ele else "N/A"
            star_ele = i.find_elements(By.XPATH, ".//a[contains(@href,'stargazers')]")
            star_count = star_ele[0].text if star_ele else "0"
            fork_ele = i.find_elements(By.XPATH, ".//a[contains(@href,'forks')]")
            forks = fork_ele[0].text if fork_ele else "0"
            tech_ele = i.find_elements(
                By.XPATH, ".//span[@itemprop='programmingLanguage']"
            )
            technology_used = tech_ele[0].text if tech_ele else "None"
            # appending scraped details
            project_list.append(
                {
                    "Project Name": project_name,
                    "Project URL": project_url,
                    "Description": description,
                    "Stars": star_count,
                    "Forks": forks,
                    "Technology Used": technology_used,
                }
            )
        except Exception as e:
            print(f"Error extracting data: {e}")

    browser.quit()
    return pd.DataFrame(project_list)


if st.sidebar.button("Start Scraping"):
    with st.spinner("Scraping GitHub Collection..."):
        df = scrap_git_repo(github_url)

        if df.empty:  # If scraping failed or returned no data
            st.error("No valid data found. Please check the URL and try again.")
        else:
            st.success("Scraping Completed!")

            # Show Data
            st.write("### Scraped Repositories")
            st.dataframe(df)

            # CSV Download Button
            csv = df.to_csv(index=False)
            st.download_button(
                " Download CSV",
                data=csv,
                file_name="github_projects.csv",
                mime="text/csv",
            )

            # Filters
            df["Stars"] = (
                pd.to_numeric(df["Stars"], errors="coerce").fillna(0).astype(int)
            )
            max_stars = int(df["Stars"].max())
            min_stars = st.sidebar.slider(
                "Minimum Stars:", min_value=0, max_value=max_stars, value=0
            )

            df_filtered = df[df["Stars"] >= min_stars]

            # Check if df_filtered is empty before plotting
            if not df_filtered.empty:
                st.write("### Top Starred Repositories")
                fig = px.bar(
                    df_filtered.sort_values(by="Stars", ascending=False)[:10],
                    x="Stars",
                    y="Project Name",
                    orientation="h",
                    title="Top Starred Repositories",
                )
                st.plotly_chart(fig)

            # Most Used Technologies
            st.write("### Most Used Technologies")
            lang_counts = df["Technology Used"].value_counts().reset_index()
            lang_counts.columns = ["Technology", "Count"]
            fig2 = px.pie(
                lang_counts,
                names="Technology",
                values="Count",
                title="Most Popular Technologies",
            )
            st.plotly_chart(fig2)
