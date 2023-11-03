import os
import time
from pathlib import Path
from typing import List

from src.skytvautomator.sky_tv_automator import SkyTVAutomator
from src.skytvautomator.sky_tv_start_request import SkyTVStartRequest
from src.common.locator_request import LocatorRequest
from src.common.enums.locator_type import LocatorType
from src.common.element import Element
from src.common.html_element import HTMLElement
from src.common.options_request import OptionsRequest
from src.skytvautomator.sky_tv_controller_press import SkyTVControllerPress
from src.skytvautomator.sky_tv_controller_button import SkyTVControllerButton
from src.common.dimension import Dimension

class Test_SkyTVTests:

    SKY_TV_AUTOMATOR_ADDRESS = "http://localhost:9073"

    SKY_TV_IP_ADDRESS = "{SKY_TV_IP_ADDRESS}"
    APP_ID = "YouTube"
    ENCODER_URL = "rtsp://{HDMI_ENCODER_IP}/0"
    TESSERACT_BIN = "{PATH_TO_TESSERACT_BIN}"
    TESSERACT_DATA_DIR = "{PATH_TO_TESSDATA_DIR}"
    TESSERACT_LANGUAGE = "eng"
    FFMPEG_BIN = "{PATH_TO_FFMPEG_BIN}"
    WEB_PROFILER_ID = "{WEB_PROFILER_ID}"
    GOOGLE_VISION_OCR = "{PATH_TO_JSON_GOOGLE_CRED_FILE}"
    TEXTRACT_OCR = "{PATH_TO_AWS_CRED_FILE}"

    sky_tv_automator = None

    def teardown_method(self):
        if not self.sky_tv_automator is None:
            self.sky_tv_automator.quit()
        
    def test_find_element_by_tesseract(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find an element by text on the screen
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "recommended").with_timeout(40000))
        assert len(elements) == 1

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() > 90.0
        assert element.get_width() == 179
        assert element.get_height() == 21
        assert element.get_x() == 158
        assert element.get_y() == 92

        # find multiple element matches
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "views").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_google_vision(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_google_vision_ocr(self.GOOGLE_VISION_OCR).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find multiple element matches
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "text to find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_amazon_textract(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_amazon_textract_ocr(self.TEXTRACT_OCR).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find multiple element matches
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "text to find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_amazon_rekognition(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_amazon_rekognition_ocr(self.TEXTRACT_OCR).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find multiple element matches
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "text to find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_image(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # set a default image similarity
        self.sky_tv_automator.options().set(OptionsRequest().set_default_image_find_similarity(.90))

        # get a sub image from the screen which we will use as a locator
        sub_image = self.sky_tv_automator.display().get_sub_image(0, 0, 300, 300)
        
        # find an element using our sub image as a locator
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.IMAGE, sub_image).find_all(True).with_timeout(30000))
        assert len(elements) == 1

    def test_find_element_by_css(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_web_profiler_id(self.WEB_PROFILER_ID)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find an element by css
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.CSS, "div[class='featured-title']").with_timeout(40000))
        assert len(elements) == 1

        element: Element = elements[0]
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() == 100.0
        assert element.get_width() == 0
        assert element.get_height() == 0
        assert element.get_x() == 0
        assert element.get_y() == 0
        assert element.get_text() == "text of element"

        # get the element attributes and css
        html_element: HTMLElement = element.to_html_element()
        assert html_element.get_attribute("class") == "featured-title"
        assert html_element.get_css_value("font-weight") == "700"

        # find all elements by css
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.CSS, "div[class='featured-title']").with_timeout(40000).find_all(True))
        assert len(elements) == 10

        element: Element = elements[2]
        assert element.get_text() == "text of element"
    
    def test_find_element_by_xpath(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_web_profiler_id(self.WEB_PROFILER_ID).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find an element by xpath
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.XPATH, "//div[@class='featured-title']").with_timeout(40000))
        assert len(elements) == 1

        element: Element = elements[0]
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() == 100.0
        assert element.get_width() == 0
        assert element.get_height() == 0
        assert element.get_x() == 0
        assert element.get_y() == 0
        assert element.get_text() == "text of element"

        # get the element attributes and css
        html_element: HTMLElement = element.to_html_element()
        assert html_element.get_attribute("class") == "featured-title"
        assert html_element.get_css_value("font-weight") == "700"

        # find all elements by xpath
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.XPATH, "//div[@class='featured-title']").with_timeout(40000).find_all(True))
        assert len(elements) == 10

        element: Element = elements[2]
        assert element.get_text() == "text of element"

    def test_remote_control_interact(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find an element
        elements: List[Element] = self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "Recommended").with_timeout(40000))

        # set a delay between remote interactions
        self.sky_tv_automator.options().set(OptionsRequest().set_default_controller_delay(1000))

        # send a remote control press
        self.sky_tv_automator.controller().send_command(SkyTVControllerPress(SkyTVControllerButton.DOWN))
        self.sky_tv_automator.controller().send_command(SkyTVControllerPress(SkyTVControllerButton.LEFT))
        self.sky_tv_automator.controller().send_command(SkyTVControllerPress(SkyTVControllerButton.SELECT))

    def test_web_profiler(self):
        # create a start request with the app id of your app to launch
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_web_profiler_id(self.WEB_PROFILER_ID).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find an element
        self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.CSS, "div[class='featured-title']").with_timeout(40000))
        
        # get the page source
        page_source: str = self.sky_tv_automator.web_profiler().get_page_source()
        assert "featured-title" in page_source

        # execute javascript against the application
        script_output = self.sky_tv_automator.web_profiler().execute_script("document.documentElement.innerHTML")
        assert "<span" in script_output

        # get the browser console logs
        console_logs = self.sky_tv_automator.web_profiler().get_console_logs()
        assert "Request received from testtrakt server" in console_logs

    def test_screen_artifacts(self):
        # create a start request with an app that is already installed
        sky_tv_start_request = SkyTVStartRequest(self.SKY_TV_IP_ADDRESS).with_app_id(self.APP_ID).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN).with_hdmi_encoder(self.ENCODER_URL)
        
        # start the sky tv automator session
        self.sky_tv_automator = SkyTVAutomator(self.SKY_TV_AUTOMATOR_ADDRESS, sky_tv_start_request)

        # find an element
        self.sky_tv_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "Recommended").with_timeout(40000))

        # get the screen image and save to a file
        image = self.sky_tv_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the screen sub image and save to a file
        sub_image = self.sky_tv_automator.display().get_sub_image(0, 0, 500, 500)
        print("Sub image saved to: " + sub_image)
        assert os.path.exists(sub_image)

        # get the screen resolution
        dimension: Dimension = self.sky_tv_automator.display().get_resolution()
        assert 1920 == dimension.get_width()
        assert 1080 == dimension.get_height()

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.sky_tv_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)
