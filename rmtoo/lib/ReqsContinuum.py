#
# ReqsContinuum hold all the different requirement sets from the
# past. 
#
# (c) 2010 by flonatel
#
# For licencing details see COPYING
#

import os
from types import StringType

from rmtoo.lib.RMTException import RMTException
from rmtoo.lib.RequirementSet import RequirementSet
from rmtoo.lib.VersionControlSystem import VCSException, VersionControlSystem

#
# TODO: The following is not correct any more.
#  Do not use RequirementSet any more.
#  Instead use the TopicHandler here.
#

# The Continuum holds all the RequirementSets from the history,
# i.e. all which are known to git.  It also holds the current
# available (possible not checked in) pointer to the appropriate files
# in the file system.
#

class ReqsContinuum:

    commit_bulk_size = 10

    def __init__(self, mods, config):
        self.mods = mods
        self.config = config

        # This is the list of all requirements sets - ordered by time.
        # (The newest versions are on top - sorted backwards.)
        self.continuum_order = []
        # The continuum itself - accessable by the version.
        self.continuum = {}

        self.init_continuum()

    def continuum_add(self, cid, req_set):
        self.continuum_order.append(cid)
        self.continuum[cid] = req_set

    # The last is the first (backward order)
    def continuum_latest(self):
        return self.continuum[self.continuum_order[0]]

    # The version control system id of the latest
    def continuum_latest_id(self):
        return self.continuum_order[0]

    def repo_access_needed(self):
        # Only if FILES:FILES is specified, there is no need to access
        # the repo.
        return self.config.get_value(
                    'requirements.input.commit_interval.begin') != 'FILES' \
                    or self.config.get_value(
                    'requirements.input.commit_interval.end') != 'FILES'

    def init_continuum(self):
        start_vers = self.config.get_value(
            'requirements.input.commit_interval.begin')
        end_vers = self.config.get_value(
            'requirements.input.commit_interval.end')

        # Should the repo be accessed?
        if self.repo_access_needed():
            # Have a look, if there is a repo in the given directory.
            if not self.create_repo():
                raise RMTException(40, "Based on the config a "
                                   "repository is needed - but there is "
                                   "none")

        # Maybe add also the FILES:
        if end_vers == "FILES":
            self.create_continuum_from_file()
        # Maybe add also some old versions
        if start_vers != "FILES":
            # When there is FILES given as last parameter - get
            # everything from start_vers upto HEAD
            end_repo = end_vers
            if end_vers == "FILES":
                end_repo = "HEAD"
            self.create_continuum_from_vcs(start_vers, end_repo)

    # This method sets up the repository and splits out the repository
    # dir from the requirements dir.
    def create_repo(self):
        directory = self.config.get_value("requirements.input.directory")
        # When the directory is not absolute, convert it to an
        # absolute path that it can be compared to the outcome of the
        # git.Repo. 
        if not os.path.isabs(directory):
            directory = os.path.abspath(directory)

        # If this is None - there is no repo available.
        self.repo = None

        try:
            self.repo = VersionControlSystem.create(directory)
            return True
        except VCSException:
            # There is no vcs repo here - therefore nothing to do.
            pass
        return False


    ## The following functions read in the continuum - from the
    ## different I/O layers. 

    def create_continuum_from_vcs(self, start_vers, end_vers):
        self.repo.read_history(self, start_vers, end_vers)

    def create_continuum_from_file(self):
        rs = RequirementSet(self.mods, self.config)

        #print("UNICODE???? [%s]" % self.config.get_value('requirements.input.directory'))
        # TODO: Check if this is really unicode (already)
        # TODO: Add a test case.
        req_input_dir = self.config.get_value('requirements.input.directory')
        if type(req_input_dir) == StringType:
            req_input_dir = unicode(req_input_dir, "utf-8")
        rs.read_from_filesystem(req_input_dir)

#        rs.read_from_filesystem(
#                self.config.get_value('requirements.input.directory'))
        self.continuum_add("FILES", rs)

    # The cmad for the requirments set
    def cmad_write_reqs_list(self, ofile):
        # Write out the list
        reqs_dir = self.config.get_value('requirements.input.directory')
        ofile.write("REQS=")
        for r in self.continuum_latest().reqs:
            ofile.write("%s.req " % os.path.join(reqs_dir, r))
        ofile.write("\n")
