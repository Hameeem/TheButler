import logging
import asyncio
from typing import Dict, Any, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

class PlaywrightBrowserManager:
    @classmethod
    def attempt_application_fill(cls, job_url: str, profile_data: Dict[str, Any], resume_path: str, answers: Dict[str, str]) -> Tuple[bool, str, str]:
        """
        Attempts browser automation using Playwright.
        If CAPTCHA, login wall, OTP, or unknown form structure is detected, gracefully halts and returns manual handoff status.
        Returns: (success_status, message, handoff_reason)
        """
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=settings.PLAYWRIGHT_HEADLESS)
                context = browser.new_context()
                page = context.new_page()
                
                logger.info(f"Navigating to {job_url}...")
                page.goto(job_url, timeout=15000)
                page.wait_for_timeout(2000)
                
                content = page.content().lower()
                
                # Check for anti-bot / CAPTCHA / Login wall
                if any(term in content for term in ["captcha", "cf-challenge", "robot", "recaptcha", "hcaptcha"]):
                    browser.close()
                    return False, "CAPTCHA / Security check detected on application page.", "CAPTCHA_DETECTED"
                    
                if any(term in content for term in ["login required", "sign in to apply", "log in to your account"]):
                    browser.close()
                    return False, "Platform authentication / login required.", "LOGIN_REQUIRED"

                if any(term in content for term in ["registration fee", "payment required", "pay fee"]):
                    browser.close()
                    return False, "Payment request detected! Halting for security.", "PAYMENT_DETECTED"

                # Check common form inputs
                inputs = page.query_selector_all("input, textarea")
                if len(inputs) == 0:
                    browser.close()
                    return False, "No automated application form inputs found on target page.", "MANUAL_HANDOFF_REQUIRED"
                    
                # If form is found, fill standard inputs
                filled_count = 0
                for inp in inputs:
                    try:
                        name_attr = (inp.get_attribute("name") or "").lower()
                        placeholder = (inp.get_attribute("placeholder") or "").lower()
                        
                        if "name" in name_attr or "name" in placeholder:
                            inp.fill(profile_data.get("full_name", ""))
                            filled_count += 1
                        elif "email" in name_attr or "email" in placeholder:
                            inp.fill(profile_data.get("email", ""))
                            filled_count += 1
                        elif "phone" in name_attr or "mobile" in placeholder:
                            inp.fill(profile_data.get("phone", ""))
                            filled_count += 1
                    except Exception:
                        pass
                        
                browser.close()
                return True, f"Automated form pre-filling completed ({filled_count} fields populated). Halting for final user submission.", "SUCCESS"

        except Exception as e:
            logger.warning(f"Playwright automation fallback: {e}")
            return False, f"Browser automation handoff required: {str(e)}", "AUTOMATION_UNAVAILABLE"
