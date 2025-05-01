from data_interactive import app  
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


def test_header_exists(dash_duo):
    dash_duo.start_server(app, port=8051)
    dash_duo.wait_for_element("#header", timeout=10)

def test_visualization_exists(dash_duo):
    dash_duo.start_server(app, port=8051)
    dash_duo.wait_for_element("#visualization", timeout=10)

def test_region_picker_exists(dash_duo):
    dash_duo.start_server(app, port=8051)
    dash_duo.wait_for_element("#region_picker", timeout=10)
