from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def get_restaurant_urls(location_query):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for faster scraping
    driver = webdriver.Chrome(options=chrome_options)
    
    # Google Maps search query URL
    search_url = f"https://www.google.com/maps/search/restaurants+near+{location_query.replace(' ', '+')}"
    
    driver.get(search_url)
    time.sleep(3)  # Allow time for the page to load
    
    restaurant_urls = []

    # Scroll down to load more restaurants (Google Maps loads results in batches)
    for _ in range(5):  # Adjust based on how many restaurants you need
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)  # Wait for new results to load

        # Scrape restaurant links
        restaurants = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/place/"]')
        for restaurant in restaurants:
            url = restaurant.get_attribute('href')
            restaurant_urls.append(url)

    driver.quit()

    return restaurant_urls

# Example usage
restaurant_urls = get_restaurant_urls("New York City")

def scrape_reviews_from_restaurants(restaurant_urls):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    all_reviews = []

    for url in restaurant_urls:
        print(f"Scraping reviews for: {url}")
        driver.get(url)
        time.sleep(2)

        reviews = driver.find_elements(By.CLASS_NAME, 'review-class')  # Adjust class based on actual element
        for review in reviews:
            review_text = review.text
            all_reviews.append({'url': url, 'review': review_text})

        # Optional: Scroll to load more reviews if needed, e.g., driver.execute_script("window.scrollBy(0, 1000);")

    driver.quit()
    
    return all_reviews

# Example usage
reviews = scrape_reviews_from_restaurants(restaurant_urls)
print(reviews)