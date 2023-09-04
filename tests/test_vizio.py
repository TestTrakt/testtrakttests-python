import os
import time
from pathlib import Path
from typing import List

from src.vizioautomator.vizio_automator import VizioAutomator
from src.vizioautomator.vizio_start_request import VizioStartRequest
from src.common.locator_request import LocatorRequest
from src.common.enums.locator_type import LocatorType
from src.common.element import Element
from src.common.html_element import HTMLElement
from src.common.options_request import OptionsRequest
from src.vizioautomator.vizio_controller_press import VizioControllerPress
from src.vizioautomator.vizio_controller_button import VizioControllerButton
from src.vizioautomator.vizio_system_information import VizioSystemInformation
from src.common.dimension import Dimension

class Test_VizioTests:

    VIZIO_AUTOMATOR_ADDRESS = "http://localhost:{port}"

    VIZIO_IP_ADDRESS = "your_vizio_ip_address"
    APP_URL = "https://www.your_vizio_application_url_under_test"
    REMOTE_API_TOKEN = "your_vizio_remote_api_token";
    TESSERACT_BIN = "/absolute/path/to/tesseract"
    TESSERACT_DATA_DIR = "/absolute/path/to/tesseract/tessdata/dir/tessdata"
    TESSERACT_LANGUAGE = "eng"
    FFMPEG_BIN = "/absolute/path/to/ffmpeg"
    WEB_PROFILER_ID = "your_unique_web_profiler_id"
    GOOGLE_VISION_OCR = "/absolute/path/to/google/vision/credentials.json"
    TEXTRACT_OCR = "/absolute/path/to/aws/credentials"

    vizio_automator = None

    def teardown_method(self):
        if not self.vizio_automator is None:
            self.vizio_automator.quit()
        
    def test_find_element_by_tesseract(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element by text on the screen
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt Application Web Profiler Test Site").with_timeout(40000))
        assert len(elements) == 1

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() > 90.0
        assert element.get_width() > 13 and element.get_width() < 140
        assert element.get_height() > 10 and element.get_height() < 20
        assert element.get_x() > 10 and element.get_x() < 15
        assert element.get_y() > 15 and element.get_y() < 20

        # find multiple element matches
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_google_vision(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_google_vision_ocr(self.GOOGLE_VISION_OCR).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find multiple element matches
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_amazon_textract(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_amazon_textract_ocr(self.TEXTRACT_OCR).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find multiple element matches
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_amazon_rekognition(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_amazon_rekognition_ocr(self.TEXTRACT_OCR).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find multiple element matches
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_image(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # set a default image similarity
        self.vizio_automator.options().set(OptionsRequest().set_default_controller_delay(.90))

        # get a sub image from the screen which we will use as a locator
        sub_image = self.vizio_automator.display().get_sub_image(0, 0, 300, 300)
        
        # find an element using our sub image as a locator
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.IMAGE, sub_image).find_all(True).with_timeout(40000))
        assert len(elements) == 1

    def test_find_element_by_css(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element by css
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.CSS, "span[id='testtraktidentifier']").with_timeout(40000))
        assert len(elements) == 1

        element: Element = elements[0]
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() == 100.0
        assert element.get_width() == 0
        assert element.get_height() == 0
        assert element.get_x() == 0
        assert element.get_y() == 0
        assert element.get_text() == "TestTrakt Application Web Profiler Test Site"

        # get the element attributes and css
        html_element: HTMLElement = element.to_html_element()
        assert html_element.get_attribute("id") == "testtraktidentifier"
        assert html_element.get_css_value("align-content") == "normal"

        # find all elements by css
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.CSS, "span").with_timeout(40000).find_all(True))
        assert len(elements) == 2

        element: Element = elements[1]
        assert element.get_text() == "TestTrakt Application Web Profiler Test Site"
    
    def test_find_element_by_xpath(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element by xpath
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.XPATH, "//span[@id='testtraktidentifier']").with_timeout(40000))
        assert len(elements) == 1

        element: Element = elements[0]
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() == 100.0
        assert element.get_width() == 0
        assert element.get_height() == 0
        assert element.get_x() == 0
        assert element.get_y() == 0
        assert element.get_text() == "TestTrakt Application Web Profiler Test Site"

        # get the element attributes and css
        html_element: HTMLElement = element.to_html_element()
        assert html_element.get_attribute("id") == "testtraktidentifier"
        assert html_element.get_css_value("align-content") == "normal"

        # find all elements by xpath
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.XPATH, "//span").with_timeout(40000).find_all(True))
        assert len(elements) == 2

        element: Element = elements[1]
        assert element.get_text() == "TestTrakt Application Web Profiler Test Site"

    def test_remote_control_interact(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element
        elements: List[Element] = self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").with_timeout(40000))

        # set a delay between remote interactions
        self.vizio_automator.options().set(OptionsRequest().set_default_controller_delay(1000))

        # send a remote control press
        self.vizio_automator.controller().send_command(VizioControllerPress(VizioControllerButton.MENU))
        self.vizio_automator.controller().send_command(VizioControllerPress(VizioControllerButton.DOWN_ARROW))
        self.vizio_automator.controller().send_command(VizioControllerPress(VizioControllerButton.DOWN_ARROW))
        self.vizio_automator.controller().send_command(VizioControllerPress(VizioControllerButton.ENTER))

    def test_web_profiler(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element
        self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").with_timeout(40000))
        
        # get the page source
        page_source: str = self.vizio_automator.web_profiler().get_page_source()
        assert "<span" in page_source

        # execute javascript against the application
        script_output = self.vizio_automator.web_profiler().execute_script("document.documentElement.innerHTML")
        assert "<span" in script_output

        # get the browser console logs
        console_logs = self.vizio_automator.web_profiler().get_console_logs()
        assert "Request received from testtrakt server" in console_logs

    def test_system_info(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element
        self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").with_timeout(40000))
        
        # get the system information
        vizio_system_information: VizioSystemInformation = self.vizio_automator.system().get_system_info()
        assert "D24f-G1" == vizio_system_information.get_model_name()

    def test_screen_artifacts(self):
        # create a start request
        vizio_start_request = VizioStartRequest(self.VIZIO_IP_ADDRESS).with_app_url(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_remote_api_token(self.REMOTE_API_TOKEN).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the vizio automator session
        self.vizio_automator = VizioAutomator(self.VIZIO_AUTOMATOR_ADDRESS, vizio_start_request)

        # find an element
        self.vizio_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").with_timeout(40000))

        # get the screen image and save to a file
        image = self.vizio_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the screen sub image and save to a file
        sub_image = self.vizio_automator.display().get_sub_image(0, 0, 500, 500)
        print("Sub image saved to: " + sub_image)
        assert os.path.exists(sub_image)

        # get the screen resolution
        dimension: Dimension = self.vizio_automator.display().get_resolution()
        assert 1920 == dimension.get_width()
        assert 1080 == dimension.get_height()

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.vizio_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)