"""Steps and utility functions for taking screenshots."""

from lettuce import (
    step,
    world,
)
import os.path

def set_save_directory(base, source):
    """Sets the root save directory for saving screenshots.
    
    Screenshots will be saved in subdirectories under this directory by
    browser window size. """
    root = os.path.join(base, source)
    if not os.path.isdir(root):
        os.makedirs(root)

    world.screenshot_root = root


@step(r'I capture a screenshot named "(.*?)"$')
def capture_screenshot(step, name):
    window_size = world.browser.get_window_size()
    dir_path = os.path.join(
        world.screenshot_root,
        '{}x{}'.format(window_size['width'], window_size['height']),
    )
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filename = os.path.join(
        dir_path,
        '{}.png'.format(name)
    )
    world.browser.get_screenshot_as_file(filename)


@step(r'I capture a screenshot named "(.*?)" after (\d+) seconds?$')
def capture_screenshot_delay(step, name, delay):
    time.sleep(delay)
    capture_screenshot(name)
