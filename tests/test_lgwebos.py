import os
from pathlib import Path
from typing import List

from src.lgautomator.lg_automator import LGAutomator
from src.lgautomator.lg_start_request import LGStartRequest
from src.common.locator_request import LocatorRequest
from src.common.enums.locator_type import LocatorType
from src.common.element import Element
from src.common.html_element import HTMLElement
from src.common.options_request import OptionsRequest
from src.lgautomator.lg_controller_press import LGControllerPress
from src.lgautomator.lg_controller_button import LGControllerButton
from src.common.dimension import Dimension

class Test_LGTests:

    LG_AUTOMATOR_ADDRESS = "http://localhost:9012"

    LG_IP_ADDRESS = "LG_TV_IP_ADDRESS"
    APP_URL = "PATH_OR_URL_TO_YOUR_LG_APP_PACKAGE.ipk"
    TESSERACT_BIN = "PATH_TO_TESSERACT_BINARY"
    TESSERACT_DATA_DIR = "PATH_TO_TESSDATA_DIR"
    TESSERACT_LANGUAGE = "eng"
    FFMPEG_BIN = "PATH_TO_FFMPEG_BINARY"
    WEB_PROFILER_ID = "YOUR_WEBPROFILER_ID"
    GOOGLE_VISION_OCR = "PATH_TO_GOOGLE_VISION_CRED.json"
    TEXTRACT_OCR = "PATH_TO_AWS_CREDENTIALS"
    LG_CLI_DIR = "PATH_TO_LG_CLI_BINARY_DIR" # optional if this directory is in your PATH
    IP_CAMERA = "ONVIF_WIFI_CAMERA_IP_ADDRESS"
  
    lg_automator = None

    def teardown_method(self):
        if not self.lg_automator is None:
            self.lg_automator.quit()
        
    def test_find_element_by_tesseract(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_ip_camera(self.IP_CAMERA)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # find an element by text on the screen
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt Application Web Profiler Test Site").with_timeout(40000))
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
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_google_vision(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_google_vision_ocr(self.GOOGLE_VISION_OCR).with_web_profiler_id(self.WEB_PROFILER_ID).with_ip_camera(self.IP_CAMERA)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # find multiple element matches
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_amazon_textract(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_amazon_textract_ocr(self.TEXTRACT_OCR).with_web_profiler_id(self.WEB_PROFILER_ID).with_ip_camera(self.IP_CAMERA)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # find multiple element matches
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_amazon_rekognition(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_amazon_rekognition_ocr(self.TEXTRACT_OCR).with_web_profiler_id(self.WEB_PROFILER_ID).with_ip_camera(self.IP_CAMERA)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # find multiple element matches
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").find_all(True).with_timeout(40000))
        assert len(elements) == 2

    def test_find_element_by_image(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_web_profiler_id(self.WEB_PROFILER_ID).with_ip_camera(self.IP_CAMERA)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # set a default image similarity
        self.lg_automator.options().set(OptionsRequest().set_default_controller_delay(.90))

        # get a sub image from the screen which we will use as a locator
        sub_image = self.lg_automator.display().get_sub_image(0, 0, 300, 300)
        
        # find an element using our sub image as a locator
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.IMAGE, sub_image).find_all(True).with_timeout(40000))
        assert len(elements) == 1

    def test_find_element_by_css(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_web_profiler_id(self.WEB_PROFILER_ID)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)
        
        # find an element by css
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.CSS, "span[id='testtraktidentifier']").with_timeout(40000))
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
        assert html_element.get_css_value("align-content") == "stretch"

        # find all elements by css
        elements: List[Element] = self.lg_automator.locator().locate(LocatorRequest(LocatorType.CSS, "span").with_timeout(40000).find_all(True))
        for element in elements:
            print("Element: " + str(element.element_data))

        assert len(elements) == 4

        element: Element = elements[1]
        assert element.get_text() == "TestTrakt Application Web Profiler Test Site"

    def test_remote_control_interact(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # set a delay between remote interactions
        self.lg_automator.options().set(OptionsRequest().set_default_controller_delay(1000))

        # send a remote control press
        self.lg_automator.controller().send_command(LGControllerPress(LGControllerButton.MENU))
        self.lg_automator.controller().send_command(LGControllerPress(LGControllerButton.DOWN_ARROW))
        self.lg_automator.controller().send_command(LGControllerPress(LGControllerButton.DOWN_ARROW))
        self.lg_automator.controller().send_command(LGControllerPress(LGControllerButton.ENTER))

    def test_web_profiler(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)
        
        # get the page source
        page_source: str = self.lg_automator.web_profiler().get_page_source()
        assert "<span" in page_source

        # execute javascript against the application
        script_output = self.lg_automator.web_profiler().execute_script("document.documentElement.innerHTML")
        assert "<span" in script_output

    def test_screen_artifacts(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package(self.APP_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_web_profiler_id(self.WEB_PROFILER_ID).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # find an element
        self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "TestTrakt").with_timeout(40000))

        # get the screen image and save to a file
        image = self.lg_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the screen sub image and save to a file
        sub_image = self.lg_automator.display().get_sub_image(0, 0, 500, 500)
        print("Sub image saved to: " + sub_image)
        assert os.path.exists(sub_image)

        # get the screen resolution
        dimension: Dimension = self.lg_automator.display().get_resolution()
        assert 1920 == dimension.get_width()
        assert 1080 == dimension.get_height()

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.lg_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)

    def test_with_ip_camera(self):
        # create a start request
        lg_start_request = LGStartRequest(self.LG_IP_ADDRESS).with_app_package("https://www.google.com").with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN).with_ip_camera(self.IP_CAMERA)
        
        # start the lg automator session
        self.lg_automator = LGAutomator(self.LG_AUTOMATOR_ADDRESS, lg_start_request)

        # find an element
        self.lg_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "Google").with_timeout(20000))

        # get the screen image and save to a file using our ip camera with ONVIF
        image = self.lg_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.lg_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)
