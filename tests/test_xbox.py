import os
import time
from pathlib import Path
from typing import List

from src.xboxautomator.xbox_automator import XBoxAutomator
from src.xboxautomator.xbox_start_request import XBoxStartRequest
from src.common.locator_request import LocatorRequest
from src.common.enums.locator_type import LocatorType
from src.common.element import Element
from src.common.html_element import HTMLElement
from src.common.options_request import OptionsRequest
from src.xboxautomator.xbox_controller_press import XBoxControllerPress
from src.xboxautomator.xbox_controller_button import XBoxControllerButton
from src.xboxautomator.xbox_system_information import XBoxSystemInformation
from src.common.dimension import Dimension

class Test_XBoxTests:

    XBOX_AUTOMATOR_ADDRESS = "http://localhost:{port}"

    XBOX_IP_ADDRESS = "xbox_ip_address"
    APP_URL = "/path/or/url/to/xbox/package.appxbundle"
    APP_NAME = "friendly_app_name";
    TESSERACT_BIN = "/absolute/path/to/tesseract"
    TESSERACT_DATA_DIR = "/absolute/path/to/tesseract/tessdata/dir/tessdata"
    TESSERACT_LANGUAGE = "eng"
    FFMPEG_BIN = "/absolute/path/to/ffmpeg"
    WEB_PROFILER_ID = "your_unique_web_profiler_id"
    GOOGLE_VISION_OCR = "/absolute/path/to/google/vision/credentials.json"
    TEXTRACT_OCR = "/absolute/path/to/aws/credentials"

    xbox_automator = None

    def teardown_method(self):
        if not self.xbox_automator is None:
            self.xbox_automator.quit()
        
    def test_find_element_by_tesseract(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element by text on the screen
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(40000))
        assert len(elements) == 1

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() > 90.0
        assert element.get_width() > 120 and element.get_width() < 150
        assert element.get_height() > 10 and element.get_height() < 30
        assert element.get_x() > 190 and element.get_x() < 220
        assert element.get_y() > 440 and element.get_y() < 460

        # find multiple element matches
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_google_vision(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_google_vision_ocr(self.GOOGLE_VISION_OCR).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find multiple element matches
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_amazon_textract(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_amazon_textract_ocr(self.TEXTRACT_OCR).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find multiple element matches
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_amazon_rekognition(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_amazon_rekognition_ocr(self.TEXTRACT_OCR).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find multiple element matches
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").find_all(True).with_timeout(40000))
        assert len(elements) == 3

    def test_find_element_by_image(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # set a default image similarity
        self.xbox_automator.options().set(OptionsRequest().set_default_controller_delay(.90))

        # get a sub image from the screen which we will use as a locator
        sub_image = self.xbox_automator.display().get_sub_image(0, 0, 300, 300)
        
        # find an element using our sub image as a locator
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.IMAGE, sub_image).find_all(True).with_timeout(40000))
        assert len(elements) == 1

    def test_find_element_by_css(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_web_profiler_id(self.WEB_PROFILER_ID)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element by css
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.CSS, "div[class='locator-class']").with_timeout(40000))
        assert len(elements) == 1

        element: Element = elements[0]
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() == 100.0
        assert element.get_width() == 0
        assert element.get_height() == 0
        assert element.get_x() == 0
        assert element.get_y() == 0
        assert element.get_text() == "element text"

        # get the element attributes and css
        html_element: HTMLElement = element.to_html_element()
        assert html_element.get_attribute("class") == "locator-class"
        assert html_element.get_css_value("font-weight") == "700"

        # find all elements by css
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.CSS, "div[class='locator-class']").with_timeout(40000).find_all(True))
        assert len(elements) == 10

        element: Element = elements[2]
        assert element.get_text() == "element text"
    
    def test_find_element_by_xpath(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_web_profiler_id(self.WEB_PROFILER_ID).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        #self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(40000))
        
        # find an element by xpath
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.XPATH, "//div[@class='locator-class']").with_timeout(40000))
        assert len(elements) == 1

        element: Element = elements[0]
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() == 100.0
        assert element.get_width() == 0
        assert element.get_height() == 0
        assert element.get_x() == 0
        assert element.get_y() == 0
        assert element.get_text() == "element text"

        # get the element attributes and css
        html_element: HTMLElement = element.to_html_element()
        assert html_element.get_attribute("class") == "locator-class"
        assert html_element.get_css_value("font-weight") == "700"

        # find all elements by xpath
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.XPATH, "//div[@class='locator-class']").with_timeout(40000).find_all(True))
        assert len(elements) == 10

        element: Element = elements[2]
        assert element.get_text() == "element text"

    def test_remote_control_interact(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element
        elements: List[Element] = self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(40000))

        # set a delay between remote interactions
        self.xbox_automator.options().set(OptionsRequest().set_default_controller_delay(1000))

        # send a remote control press
        self.xbox_automator.controller().send_command(XBoxControllerPress(XBoxControllerButton.LEFT_ARROW))
        self.xbox_automator.controller().send_command(XBoxControllerPress(XBoxControllerButton.DOWN_ARROW))
        self.xbox_automator.controller().send_command(XBoxControllerPress(XBoxControllerButton.DOWN_ARROW))
        self.xbox_automator.controller().send_command(XBoxControllerPress(XBoxControllerButton.A))

        self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(15000))

    def test_web_profiler(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_web_profiler_id(self.WEB_PROFILER_ID)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element
        self.xbox_automator.locator().locate(LocatorRequest(LocatorType.CSS, "div[class='locator-class']").with_timeout(40000))
        
        # get the page source
        page_source: str = self.xbox_automator.web_profiler().get_page_source()
        assert "locator-class" in page_source

        # execute javascript against the application
        script_output = self.xbox_automator.web_profiler().execute_script("document.documentElement.innerHTML")
        assert "<span" in script_output

        # get the browser console logs
        console_logs = self.xbox_automator.web_profiler().get_console_logs()
        assert "Request received from testtrakt server" in console_logs

    def test_system_info(self):
        # create a start request with an app package that is a public url to a .appx or .appxbundle
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element
        self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(40000))
        
        # get the system information
        xbox_system_information: XBoxSystemInformation = self.xbox_automator.system().get_system_info()
        assert "Xbox One" == xbox_system_information.get_console_type()

    def test_pre_installed_app(self):
        # create a start request with an app that is already installed
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_name(self.APP_NAME).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element
        self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(40000))

    def test_screen_artifacts(self):
        # create a start request with an app that is already installed
        xbox_start_request = XBoxStartRequest(self.XBOX_IP_ADDRESS).with_app_package(self.APP_URL).with_app_name(self.APP_NAME).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the xbox automator session
        self.xbox_automator = XBoxAutomator(self.XBOX_AUTOMATOR_ADDRESS, xbox_start_request)

        # find an element
        self.xbox_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "locator_text_to_find").with_timeout(40000))

        # get the screen image and save to a file
        image = self.xbox_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the screen sub image and save to a file
        sub_image = self.xbox_automator.display().get_sub_image(0, 0, 500, 500)
        print("Sub image saved to: " + sub_image)
        assert os.path.exists(sub_image)

        # get the screen resolution
        dimension: Dimension = self.xbox_automator.display().get_resolution()
        assert 1920 == dimension.get_width()
        assert 1080 == dimension.get_height()

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.xbox_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)