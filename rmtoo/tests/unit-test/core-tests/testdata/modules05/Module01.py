#
# Requirement Management Toolset
#  Test Module
#
# (c) 2010-2011 by flonatel
#
# For licencing details see COPYING
#

from rmtoo.lib.digraph.Digraph import Digraph

class Module01(Digraph.Node):
    depends_on = []

    def __init__(self, config):
        Digraph.Node.__init__(self, "Module01")

    def type(self):
        return set(["reqtag", ])

    def set_modules(self, mods):
        pass

    def rewrite(self, rid, reqs):
        return "SameTag", None
