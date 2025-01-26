from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class CaptchaSolver:
    def __init__(self):
        # Chrome options setup
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        
        # Additional options to prevent bot detection
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize ChromeDriver
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)

    def solve_captcha(self, url):
        try:
            # Go to website
            self.driver.get(url)
            print("Site opened")

            # Find and switch to reCAPTCHA iframe
            iframe = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "iframe[title*='reCAPTCHA']")
            ))
            self.driver.switch_to.frame(iframe)
            print("Switched to iframe")

            # Find and click checkbox
            checkbox = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".recaptcha-checkbox-border")
            ))
            time.sleep(1)  # Short wait
            checkbox.click()
            print("Captcha checkbox clicked")

            # Switch back to main frame
            self.driver.switch_to.default_content()
            
            # Wait for challenge iframe
            time.sleep(2)  # Wait for animation
            
            # Find all iframes and switch to the challenge one
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for frame in iframes:
                if "recaptcha challenge" in frame.get_attribute("title").lower():
                    self.driver.switch_to.frame(frame)
                    print("Switched to challenge frame")
                    break
            
            # Take screenshot of entire page
            self.driver.save_screenshot("captcha_challenge.png")
            print("Screenshot saved as 'captcha_challenge.png'")
            
            return True

        except TimeoutException:
            print("Timeout: Elements not found")
            return False
        except Exception as e:
            print(e)
            return False

    def close(self):
        # Close browser
        if self.driver:
            self.driver.quit()
            print("Browser closed")

def main():
    # Test usage
    solver = CaptchaSolver()
    try:
        # Enter URL here
        url = "URL"  # Replace with your target site URL
        result = solver.solve_captcha(url)
        
        if result:
            print("Captcha solved successfully!")
        else:
            print("Failed to solve captcha!")
            
        # Wait a bit after completion
        time.sleep(3)
        
    finally:
        solver.close()

if __name__ == "__main__":
    main() 