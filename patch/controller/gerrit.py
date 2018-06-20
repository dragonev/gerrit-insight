import os
import sys
import time
import json

from django.conf import settings
from patch.utils.serializer import Serializer
from subprocess import check_call, check_output, CalledProcessError


class PatchManager():

    def __init__(self, cache_dir, patch_cache_name, debug=True):
        self.cache_dir = cache_dir
        self.patch_cache_name = patch_cache_name
        self.debug = debug
        self.serializer = None
        self.patch_cache_path = os.path.join(cache_dir, patch_cache_name)

    def cleanup_patch_cache(self):
        """
        If not in debug mode and patch_cache_path exists, delete all files under the
        patch_cache_path directory.
        """
        if not self.debug and os.path.exists(self.patch_cache_path):
            os.remove(self.patch_cache_path)

    def _get_pacthes_of_project(self, project_dict, project, status, limit=None):
        """
        Parse the string of patches.
        reference link  : https://review.gerrithub.io/Documentation/cmd-index.html
        query patch cmd : sshpass -p 'bu!ldb0t' ssh sys_sgsw@spdk-ci-003.ch.intel.com
        'ssh -p 29418 spdk.intel.com gerrit query project:spdk status:merged 
        --patch-sets --all-reviewers --files --format=JSON limit:2'
        """
        try:
            query_patch_cmd = ['sshpass', '-p', 'bu!ldb0t',
                               'ssh', 'sys_sgsw@spdk-ci-003.ch.intel.com',
                               'ssh', '-p', '29418', 'spdk.intel.com', 'gerrit',
                               'query',
                               'project:{}'.format(project),
                               'status:{}'.format(status),
                               '--patch-sets',
                               '--all-reviewers',
                               '--files',
                               '--format=JSON']
            patches = check_output(query_patch_cmd)
        except CalledProcessError as e:
            print e.message
            return

        # There are lots of newline in the patches, so write patches info into cache file
        project_patch_json_path = os.path.join(self.cache_dir, '{}.patches.{}.json'.format(project, status))
        with open(project_patch_json_path, 'w') as fo:
            fo.write(patches)

        # Parse the json_string to json format
        with open(project_patch_json_path) as fo:
            for patch_str in fo:
                patch_json = json.loads(patch_str)
                if patch_json.has_key('project'):
                    revision = patch_json['patchSets'][-1]['revision']
                    project_dict[status][revision] = patch_json
        if not self.debug:
            os.remove(project_patch_json_path)

    def get_patches_with_status_of_all_projects(self, project_set, status='merged', limit=None):
        """
        project-set : projects which need to get patches.
        status      : patch status of each project.
        limit       : the numbder of patches of each project.
        If patches.cache exists, get all patches from it, otherwise from gerrit.

        STRUCTURE OF CACHE:
                                   +-status.timeout
                                   |
                         +-project-+        +-patch
                         |         |        |
                         |         +-status-+
        serialized_cache-+-...              |
                         |                  +-...
                         +-...
        """
        if not self.serializer:
            self.serializer = Serializer()
            self.serializer.set_serialized_filename(self.patch_cache_path)
            if os.path.exists(self.patch_cache_path):
                self.serializer.load_objects_from_file()

        for project in project_set:
            if not self.serializer.test_object_in_cache(project):
                self.serializer.save_object_to_cache(project, dict())

            project_dict = self.serializer.get_object_from_cache(project)
            status_timeout = status + '.timeout'
            if not project_dict.has_key(status):
                project_dict[status] = dict()
                self._get_pacthes_of_project(project_dict, project, status)
                project_dict[status_timeout] = time.time()

            if not self.debug:
                timeout = time.time() - project_dict[status_timeout]
                if int(timeout) > 60 * 3:
                    self._get_pacthes_of_project(project_dict, project, status)
                    project_dict[status_timeout] = time.time()

        self.serializer.save_objects_to_file()
        return self.serializer.get_all_objects_in_caches()

    def get_all_projects_patches(self):
        """
        Return all patches of all project.
        """
        if not self.serializer:
            self.serializer = Serializer()
            self.serializer.set_serialized_filename(self.patch_cache_path)
            if os.path.exists(self.patch_cache_path):
                self.serializer.load_objects_from_file()
        return self.serializer.get_all_objects_in_caches()

    def get_a_certain_project_patches(self, project):
        """
        Return all patches of a certain project. If the project does not exist,
        the empty dict will be returned.
        """
        if not self.serializer:
            self.serializer = Serializer()
            self.serializer.set_serialized_filename(self.patch_cache_path)
            if os.path.exists(self.patch_cache_path):
                self.serializer.load_objects_from_file()

        if self.serializer.test_object_in_cache(project):
            return self.serializer.get_object_from_cache(project)
        return {}
