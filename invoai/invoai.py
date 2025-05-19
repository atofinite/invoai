import os
from dotenv import load_dotenv
import pyautogui
import openai
from plyer import notification
import logging

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(filename='app.log', level=logging.INFO)

def capture_screenshot(filename="assets/screenshot.png"):
    try:
        print("Capturing screenshot...")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}")
        logging.info(f"Screenshot saved as {filename}")
        return filename
    except pyautogui.FailSafeException as e:
        logging.error(f"PyAutoGUI fail-safe triggered: {e}")
        print(f"PyAutoGUI fail-safe triggered: {e}")
        return None
    except Exception as e:
        logging.error(f"Error capturing screenshot: {e}")
        print(f"Error capturing screenshot: {e}")
        return None

def analyze_screenshot(image_path):
    if not image_path or not os.path.exists(image_path):
        print("Invalid image path provided.")
        logging.error("Invalid image path provided.")
        return None
    try:
        print("Analyzing screenshot...")
        with open(image_path, "rb") as f:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You analyze screenshots."},
                    {"role": "user", "content": "Analyze this image."}
                ],
                files=[{"name": "image.png", "data": f.read()}]
            )
        print("Analysis complete.")
        logging.info("Analysis complete.")
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        print(f"OpenAI API error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during analysis: {e}")
        print(f"Unexpected error during analysis: {e}")
        return None

def main():
    img_path = capture_screenshot()
    if img_path:
        result = analyze_screenshot(img_path)
        if result:
            print("AI Analysis:", result)
        else:
            print("Failed to get AI analysis.")
    else:
        print("Screenshot capture failed.")

if __name__ == "__main__":
    main()
    notification.notify(
        title="Prototype",
        message="Script executed successfully!",
        timeout=5
    )
    print("Script executed successfully!")
