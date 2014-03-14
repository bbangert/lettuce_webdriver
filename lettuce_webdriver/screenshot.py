"""Steps and utility functions for taking screenshots."""

import uuid

from lettuce import (
    after,
    step,
    world,
)
import os.path
import json

def set_save_directory(base, source):
    """Sets the root save directory for saving screenshots.
    
    Screenshots will be saved in subdirectories under this directory by
    browser window size. """
    root = os.path.join(base, source)
    if not os.path.isdir(root):
        os.makedirs(root)

    world.screenshot_root = root


def resolution_path(world):
    window_size = world.browser.get_window_size()
    return os.path.join(
        world.screenshot_root,
        '{}x{}'.format(window_size['width'], window_size['height']),
    )


@step(r'I capture a screenshot$')
def capture_screenshot(step):
    feature = step.scenario.feature
    step.shot_name = '{}.png'.format(uuid.uuid4())
    if getattr(feature, 'dir_path', None) is None:
        feature.dir_path = resolution_path(world)
    if not os.path.isdir(feature.dir_path):
        os.makedirs(feature.dir_path)
    filename = os.path.join(
        feature.dir_path,
        step.shot_name,
    )
    world.browser.get_screenshot_as_file(filename)


@step(r'I capture a screenshot after (\d+) seconds?$')
def capture_screenshot_delay(step, delay):
    time.sleep(delay)
    capture_screenshot()


@after.each_feature
def record_run_feature_report(feature):
    if getattr(feature, 'dir_path', None) is None:
        return
    feature_name_json = '{}.json'.format(os.path.splitext(
        os.path.basename(feature.described_at.file)
    )[0])
    report = {}
    for scenario in feature.scenarios:
        scenario_report = []
        for step in scenario.steps:
            shot_name = getattr(step, 'shot_name', None)
            if shot_name is not None:
                scenario_report.append(shot_name)
        if scenario_report:
            report[scenario.name] = scenario_report

    if report:
        with open(os.path.join(feature.dir_path, feature_name_json), 'w') as f:
            json.dump(report, f)
