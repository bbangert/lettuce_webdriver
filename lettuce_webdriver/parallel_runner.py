from lettuce.core import Feature, TotalResult

from lettuce.terrain import after
from lettuce.terrain import before
from lettuce.terrain import world

from lettuce.decorators import step
from lettuce.registry import call_hook
from lettuce.registry import STEP_REGISTRY
from lettuce.registry import CALLBACK_REGISTRY
from lettuce.exceptions import StepLoadingError
from lettuce.plugins import (
    xunit_output,
    autopdb
)
from lettuce import fs
from lettuce import exceptions

from multiprocessing import Pool
from cStringIO import StringIO
from itertools import chain
import os.path
import sys
import traceback
import copy

from importlib import import_module

try:
    from colorama import init as ms_windows_workaround
    ms_windows_workaround()
except ImportError:
    pass

try:
    terrain = fs.FileSystem._import("terrain")
    reload(terrain)
except Exception, e:
    if not "No module named terrain" in str(e):
        string = 'Lettuce has tried to load the conventional environment ' \
            'module "terrain"\nbut it has errors, check its contents and ' \
            'try to run lettuce again.\n\nOriginal traceback below:\n\n'

        sys.stderr.write(string)
        sys.stderr.write(exceptions.traceback.format_exc(e))
        raise SystemExit(1)


class ParallelRunner(object):
    """Parallel lettuce test runner. Runs each feature in a separate process,
    up to a fixed number in parallel.

    Takes a base path as parameter (string), so that it can look for
    features and step definitions on there.
    """
    def __init__(self, base_path, parallelization=5, scenarios=None,
                 verbosity=0, random=False, enable_xunit=False,
                 xunit_filename=None, tags=None, failfast=False,
                 auto_pdb=False):
        """ lettuce.Runner will try to find a terrain.py file and
        import it from within `base_path`
        """

        self.tags = tags
        self.explicit_features = []

        if isinstance(base_path, list):
            self.explicit_features = base_path
            base_path = os.path.dirname(base_path[0])

        sys.path.insert(0, base_path)
        self.loader = fs.FeatureLoader(base_path)
        self.verbosity = verbosity
        self.scenarios = scenarios and map(int, scenarios.split(",")) or None
        self.failfast = failfast
        if auto_pdb:
            autopdb.enable(self)

        sys.path.remove(base_path)

        if verbosity is 0:
            output = 'non_verbose'
        elif verbosity is 1:
            output = 'dots'
        elif verbosity is 2:
            output = 'scenario_names'
        elif verbosity is 3:
            output = 'shell_output'
        else:
            output = 'colored_shell_output'

        self.random = random

        if enable_xunit:
            xunit_output.enable(filename=xunit_filename)

        self._output = output

        self.parallelization = parallelization

    @property
    def output(self):
        module = import_module('.' + self._output, 'lettuce.plugins')
        reload(module)
        return module

    def run(self):
        """ Find and load step definitions, and them find and load
        features under `base_path` specified on constructor
        """
        try:
            self.loader.find_and_load_step_definitions()
        except StepLoadingError, e:
            print "Error loading step definitions:\n", e
            return

        results = []
        if self.explicit_features:
            features_files = self.explicit_features
        else:
            features_files = self.loader.find_feature_files()
        if self.random:
            random.shuffle(features_files)

        if not features_files:
            self.output.print_no_features_found(self.loader.base_dir)
            return

        processes = Pool(processes=self.parallelization)
        test_results_it = processes.imap_unordered(
            worker_process, [(self, filename) for filename in features_files]
        )
        
        all_total = ParallelTotalResult()
        for result in test_results_it:
            all_total += result['total']
            sys.stdout.write(result['stdout'])
            sys.stderr.write(result['stderr'])

        return all_total

def worker_process(args):
    self, filename = args
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    failed = False
    results = []
    try:
        self.output
        call_hook('before', 'all')
        feature = Feature.from_file(filename)
        results.append(
            feature.run(self.scenarios,
                        tags=self.tags,
                        random=self.random,
                        failfast=self.failfast))

    except exceptions.LettuceSyntaxError, e:
        sys.stderr.write(e.msg)
        failed = True
    except:
        if not self.failfast:
            e = sys.exc_info()[1]
            print "Died with %s" % str(e)
            traceback.print_exc()
        else:
            print
            print ("Lettuce aborted running any more tests "
                   "because was called with the `--failfast` option")

        failed = True

    finally:
        total = TotalResult(results)
        call_hook('after', 'all', total)
    
    return {
        'stdout': sys.stdout.getvalue(),
        'stderr': sys.stderr.getvalue(),
        'failed': failed,
        'total': ParallelTotalResult(total),
    }

class ParallelTotalResult(object):
    def __init__(self, total=None):
        self.steps_passed = 0
        self.steps_failed = 0
        self.steps_skipped = 0
        self.steps_undefined = 0
        self.steps = 0
        scenario_results = []
        if total:
            feature_results = total.feature_results
            self.features_ran = len(feature_results)
            self.features_passed = len([result for result in feature_results if result.passed])
            for feature_result in feature_results:
                for scenario_result in feature_result.scenario_results:
                    self.steps_passed += len(scenario_result.steps_passed)
                    self.steps_failed += len(scenario_result.steps_failed)
                    self.steps_skipped += len(scenario_result.steps_skipped)
                    self.steps_undefined += len(scenario_result.steps_undefined)
                    self.steps += scenario_result.total_steps
                    scenario_results.append(scenario_result)
            self.scenarios_ran = len(scenario_results)
            self.scenarios_passed = len([result for result in scenario_results if result.passed])
        else:
            self.features_ran = 0
            self.features_passed = 0
            self.scenarios_ran = 0
            self.scenarios_passed = 0

    def _filter_proposed_definitions(self):
        raise NotImplementedError()

    @property
    def proposed_definitions(self):
        raise NotImplementedError()
    
    def __add__(self, other):
        new_ptr = copy.copy(self)
        for attr in new_ptr.__dict__:
            if isinstance(getattr(new_ptr, attr), int):
                setattr(new_ptr, attr,
                        getattr(new_ptr, attr) + getattr(other, attr))
        return new_ptr

