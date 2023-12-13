import os
import time
from pathlib import Path
from typing import List

from src.rokuautomator.roku_automator import RokuAutomator
from src.rokuautomator.roku_start_request import RokuStartRequest
from src.common.locator_request import LocatorRequest
from src.common.enums.locator_type import LocatorType
from src.common.element import Element
from src.common.html_element import HTMLElement
from src.common.options_request import OptionsRequest
from src.rokuautomator.roku_controller_press import RokuControllerPress
from src.rokuautomator.roku_controller_button import RokuControllerButton
from src.rokuautomator.roku_system_information import RokuSystemInformation
from src.rokuautomator.roku_locator_request import RokuLocatorRequest
from src.rokuautomator.roku_locator_type import RokuLocatorType
from src.common.dimension import Dimension
from src.rokuautomator.roku_media_player_data import RokuMediaPlayerData
from src.rokuautomator.roku_element import RokuElement

class Test_RokuTests:

    ROKU_AUTOMATOR_ADDRESS = "http://localhost:9070"

    ROKU_IP_ADDRESS = "{roku_ip_address}"
    ROKU_USERNAME = "{roku_dev_username}"
    ROKU_PASSWORD = "{roku_dev_password}"
    APP_PACKAGE = "https://testtraktresources.s3.amazonaws.com/channelwebcall.zip"
    ENCODER_URL = "rtsp://{hdmi_encoder_ip}/0"
    TESSERACT_BIN = "{/path/to/tesseract/binary}"
    TESSERACT_DATA_DIR = "{/path/to/tessdata/directory}"
    TESSERACT_LANGUAGE = "eng"
    FFMPEG_BIN = "{/path/to/ffmpeg/binary}"

    roku_automator = None

    def teardown_method(self):
        if not self.roku_automator is None:
            self.roku_automator.quit()
        
    def test_find_element_by_ocr(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # find an element by text on the screen
        elements: List[Element] = self.roku_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "roku").with_timeout(10000))
        assert len(elements) == 1

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        self.verify_element_details(element, 25.0, 102, 63, 135, 42)

    def test_find_element_by_native_locators(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # find all roku elements by tag name
        elements: List[Element] = self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.TAG, "RowListItem").find_all(True).with_timeout(10000))
        assert len(elements) == 6

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        self.verify_element_details(element, 100.0, 165, 44, 1920, 800)

        # find all roku elements by xpath
        elements: List[Element] = self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//RowListItem").find_all(True).with_timeout(10000))
        assert len(elements) == 6

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        self.verify_element_details(element, 100.0, 165, 44, 1920, 800)

        # more complicated xpath
        elements: List[Element] = self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//Label[@text='Big Hits']").with_timeout(10000))
        assert len(elements) == 1

        # get the element from the collection
        element: Element = elements[0]

        # assert the element details
        self.verify_element_details(element, 100.0, 0, 0, 0, 0)

        # get all the attribute name/value pairs of the element
        roku_element: RokuElement = RokuElement(element)
        assert "color" in roku_element.get_attributes()

        # get a specific attribute value from the element
        assert "#ffffffff" == roku_element.get_attribute("color")
    
    def test_get_page_source(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # get the application page source
        page_source: str = self.roku_automator.get_page_source();
        assert "Big Hits" in page_source

    def test_get_media_player_data(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # get the roku media player data
        roku_media_player_data: RokuMediaPlayerData = self.roku_automator.get_media_player_data()
        assert roku_media_player_data.get_current_playback_state() == "none"

    def test_send_remote_control_command(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # wait for an element
        self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//RowListItem").find_all(True).with_timeout(10000))

        # set a default button interact delay
        self.roku_automator.options().set(OptionsRequest().set_default_controller_delay(1000))

        # send remote control commands to the device
        self.roku_automator.controller().send_command(RokuControllerPress(RokuControllerButton.DOWN_ARROW))
        self.roku_automator.controller().send_command(RokuControllerPress(RokuControllerButton.RIGHT_ARROW))
        self.roku_automator.controller().send_command(RokuControllerPress(RokuControllerButton.SELECT))

    def test_screen_artifacts(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # wait for an element
        self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//RowListItem").find_all(True).with_timeout(10000))

        # get the screen image and save to a file
        image = self.roku_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the screen sub image and save to a file
        sub_image = self.roku_automator.display().get_sub_image(0, 0, 500, 500)
        print("Sub image saved to: " + sub_image)
        assert os.path.exists(sub_image)

        # get the screen resolution
        dimension: Dimension = self.roku_automator.display().get_resolution()
        assert 1920 == dimension.get_width()
        assert 1080 == dimension.get_height()

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.roku_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)

    def test_console_logs(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # get the console logs
        console_logs = self.roku_automator.system().get_console_logs()
        assert "HeroGridChannel" in console_logs

    def test_run_in_background(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # background the app for a duration in milliseconds and then resume
        self.roku_automator.run_app_in_background(5000)

        # wait for an element
        self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//RowListItem").with_timeout(10000))

    def test_get_performance_data(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_performance_profiling_enabled(True)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # get the performance data - can be used with the roku brightscript visual profiler tool to evaluate cpu and memory usage - https://developer.roku.com/en-ca/docs/developer-program/dev-tools/brightscript-profiler.md
        performanceFile = self.roku_automator.get_performance_data();
        print("Performance file saved to: " + performanceFile)

    def test_encoder(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_hdmi_encoder(self.ENCODER_URL).with_tesseract_ocr(self.TESSERACT_BIN, self.TESSERACT_DATA_DIR, self.TESSERACT_LANGUAGE).with_ffmpeg(self.FFMPEG_BIN)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # wait for an element
        self.roku_automator.locator().locate(LocatorRequest(LocatorType.TEXT, "roku").find_all(True).with_timeout(10000))

        # get the screen image and save to a file
        image = self.roku_automator.display().get_image()
        print("Image saved to: " + image)
        assert os.path.exists(image)

        # get the screen sub image and save to a file
        sub_image = self.roku_automator.display().get_sub_image(0, 0, 500, 500)
        print("Sub image saved to: " + sub_image)
        assert os.path.exists(sub_image)

        # get the screen resolution
        dimension: Dimension = self.roku_automator.display().get_resolution()
        assert 1920 == dimension.get_width()
        assert 1080 == dimension.get_height()

        # get the video recording - requires the with_ffmpeg start request option
        recording = self.roku_automator.display().get_recording()
        print("Recording saved to: " + recording)
        assert os.path.exists(recording)

    def test_system_info(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # get the system information from the roku
        roku_system_information: RokuSystemInformation = self.roku_automator.system().get_system_info()
        assert "Roku Ultra" == roku_system_information.get_model_name()
    
    def test_get_active_element(self):
        # create a start request with an app package (channel) .zip
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE)
        
        # start the roku automator session
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # get the current active/focused element
        active_element: Element = self.roku_automator.get_active_element()
        self.verify_element_details(active_element, 100, 3260, 0, 1600, 700)

    def test_deep_link(self):
        # create a start request with an app package (channel) .zip with a deep link
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_deep_link("contentID", "mediaType")
        
        # start the roku automator session and deep link to our content
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # wait for element
        self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//RowListItem").with_timeout(10000))

    def test_proxy(self):
        # create a start request with an app package (channel) .zip with a deep link
        roku_start_request = RokuStartRequest(self.ROKU_IP_ADDRESS, self.ROKU_USERNAME, self.ROKU_PASSWORD).with_app_package(self.APP_PACKAGE).with_proxy("192.168.1.85", 8888)
        
        # start the roku automator session and deep link to our content
        self.roku_automator = RokuAutomator(self.ROKU_AUTOMATOR_ADDRESS, roku_start_request)

        # wait for element
        self.roku_automator.locator().locate(RokuLocatorRequest(RokuLocatorType.XPATH, "//RowListItem").with_timeout(10000))

    def verify_element_details(self, element, confidence, x, y, width, height):
        print("Element: " + str(element.get_element_data()))
        assert element.get_confidence() >= confidence
        assert element.get_width() == width
        assert element.get_height() == height
        assert element.get_x() == x
        assert element.get_y() == y
