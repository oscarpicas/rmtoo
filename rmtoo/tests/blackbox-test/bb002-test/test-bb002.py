#
# rmtoo
#   Free and Open Source Requirements Management Tool
#
# Blackbox rmtoo test
#
# (c) 2010-2011 by flonatel
#
# For licencing details see COPYING
#

import os
import time

from rmtoo.lib.RmtooMain import main
from rmtoo.tests.lib.BBHelper import prepare_result_is_dir, \
    compare_results, cleanup_std_log, delete_result_is_dir, check_file_results

mdir = "tests/blackbox-test/bb002-test"

class TestBB001:

    def test_pos_001(self):
        "BB Hotspot in the middle of the graph 2"

        os.environ['TZ'] = 'Europe/Zurich'
        time.tzset()

        def myexit(n):
            pass

        mout, merr = prepare_result_is_dir()
        main(["-f", mdir + "/input/Config2.py", "-m", ".."], mout, merr,
             exitfun=myexit)
        cleanup_std_log(mout, merr)
        check_file_results(mdir)
        delete_result_is_dir()

        del os.environ['TZ']
        time.tzset()
