from patch.controller.common import Logger
from patch.controller.common import DateSet


class PatchAnalyzer(object):

    def __init__(self, raw_project_patch_dict):
        """
        arg1: These patch states pulled from the gerrit are mostly open and merged.
        """
        self.project_patch_dict = dict()
        self.raw_project_patch_dict = raw_project_patch_dict
        self._preprocesse_raw_patches()

    def _preprocesse_raw_patches(self):
        """
        Remove those keys ends with timeout.
        """
        for project in self.raw_project_patch_dict.keys():
            for key in self.raw_project_patch_dict[project].keys():
                if key.endswith('timeout'):
                    self.raw_project_patch_dict[project].pop(key)

    def _get_patchset_info(self, patch):
        """
        Return the total number of patchsets and change in the number of lines.
        """
        delta_line = 0
        for changed_file in patch['patchSets'][-1]['files'][1:]:
            delta_line = changed_file['insertions'] + changed_file['deletions']
        return len(patch['patchSets']), delta_line

    def _get_reviewer_list(self, patch):
        """
        Return the reviewers who reviewed other submitters's patches.
        """
        if not patch.has_key("allReviewers"):
            return {}
        reviewers = []
        for reviewer_name in patch['allReviewers']:
            reviewers.append(reviewer_name['name'])
        return reviewers

    def get_all_patches_submitted_by_sbmts(self, days=30):
        """
        Get all projects patches submitted by submitters within specified days.
        """
        # Traverse all projects.
        for project in self.raw_project_patch_dict.keys():
            self.project_patch_dict[project] = dict()

            # traverse all patches of echo project.
            for status, status_patch_dict in self.raw_project_patch_dict[project].items():
                for revision, patch in status_patch_dict.items():
                    if DateSet.get_local_second() - patch['createdOn'] > days * 86400:
                        continue
                    author = patch['owner']['name']
                    if not self.project_patch_dict[project].has_key(author):
                        self.project_patch_dict[project][author] = dict()
                    if not self.project_patch_dict[project][author].has_key(status):
                        self.project_patch_dict[project][author][status] = dict()
                    self.project_patch_dict[project][author][status][revision] = {
                        'date': DateSet.convert_second_to_date(patch['createdOn']),
                        'patch-set': self._get_patchset_info(patch),
                        'reviewers': self._get_reviewer_list(patch),
                        'commit-messge': patch['commitMessage'],
                    }
        return self.project_patch_dict

    def get_submitted_patch_ranking(self, status='all', days=30):
        """
        status : patch status.
        days   : patches within specified days
        Return having submitted the number of patches ranking for each project.
        """
        if len(self.project_patch_dict.keys()) == 0:
            self.get_all_patches_submitted_by_sbmts(days).keys()

        stat_patch_dict = dict()
        for project, author_dict in self.project_patch_dict.items():
            stat_patch_dict[project] = dict()
            for author, patch_status_dict in author_dict.items():
                if status in patch_status_dict.keys():
                    stat_patch_dict[project][author] = len(patch_status_dict[status].keys())
                else:
                    stat_patch_dict[project][author] = 0
                    for _, patch_dict in patch_status_dict.items():
                        stat_patch_dict[project][author] += len(patch_dict.keys())

        ranking_dict = dict()
        for project in stat_patch_dict.keys():
            ranking_dict[project] = sorted(stat_patch_dict[project].items(), key=lambda items: items[1], reverse=True)
        return ranking_dict

    def get_reviewed_patch_ranking(self, status='all', days=30):
        """
        status : patch status.
        days   : patches within specified days
        Return having reviewed the number of patches ranking for each project.
        """
        if len(self.project_patch_dict.keys()) == 0:
            self.get_all_patches_submitted_by_sbmts(days).keys()

        stat_patch_dict = dict()
        for project, author_dict in self.project_patch_dict.items():
            stat_patch_dict[project] = dict()
            for author, patch_status_dict in author_dict.items():
                if status in patch_status_dict.keys():
                    for _, patch in patch_status_dict[status].items():
                        for reviewer in patch['reviewers']:
                            if not stat_patch_dict[project].has_key(reviewer):
                                stat_patch_dict[project][reviewer] = 1
                            else:
                                stat_patch_dict[project][reviewer] += 1
                else:
                    for _, patch_dict in patch_status_dict.items():
                        for _, patch in patch_dict.items():
                            for reviewer in patch['reviewers']:
                                if not stat_patch_dict[project].has_key(reviewer):
                                    stat_patch_dict[project][reviewer] = 1
                                else:
                                    stat_patch_dict[project][reviewer] += 1

        ranking_dict = dict()
        for project in stat_patch_dict.keys():
            ranking_dict[project] = sorted(stat_patch_dict[project].items(), key=lambda items: items[1], reverse=True)
        return ranking_dict

    def get_submitted_line_ranking(self, status='all', days=30):
        """
        status : patch status.
        days   : patches within specified days
        Return having submitted the number of lines ranking for each project.
        """
        if len(self.project_patch_dict.keys()) == 0:
            self.get_all_patches_submitted_by_sbmts(days).keys()

        stat_patch_dict = dict()
        for project, author_dict in self.project_patch_dict.items():
            stat_patch_dict[project] = dict()
            for author, patch_status_dict in author_dict.items():
                if status in patch_status_dict.keys():
                    for _, patch in patch_status_dict[status].items():
                        if not stat_patch_dict[project].has_key(author):
                            stat_patch_dict[project][author] = 0
                        stat_patch_dict[project][author] += patch['patch-set'][1]
                else:
                    for _, patch_dict in patch_status_dict.items():
                        for _, patch in patch_dict.items():
                            if not stat_patch_dict[project].has_key(author):
                                stat_patch_dict[project][author] = 0
                            stat_patch_dict[project][author] += patch['patch-set'][1]

        ranking_dict = dict()
        for project in stat_patch_dict.keys():
            ranking_dict[project] = sorted(stat_patch_dict[project].items(), key=lambda items: items[1], reverse=True)
        return ranking_dict    
        

    def get_submitted_patchset_ranking(self, status='all', days=30):
        """
        status : patch status.
        days   : patches within specified days
        Return having submitted the number of patches ranking for each project.
        """
        if len(self.project_patch_dict.keys()) == 0:
            self.get_all_patches_submitted_by_sbmts(days).keys()

        stat_patch_dict = dict()
        for project, author_dict in self.project_patch_dict.items():
            stat_patch_dict[project] = dict()
            for author, patch_status_dict in author_dict.items():
                if status in patch_status_dict.keys():
                    for _, patch in patch_status_dict[status].items():
                        if not stat_patch_dict[project].has_key(author):
                            stat_patch_dict[project][author] = 0
                        stat_patch_dict[project][author] += patch['patch-set'][0]
                else:
                    for _, patch_dict in patch_status_dict.items():
                        for _, patch in patch_dict.items():
                            if not stat_patch_dict[project].has_key(author):
                                stat_patch_dict[project][author] = 0
                            stat_patch_dict[project][author] += patch['patch-set'][0]

        ranking_dict = dict()
        for project in stat_patch_dict.keys():
            ranking_dict[project] = sorted(stat_patch_dict[project].items(), key=lambda items: items[1], reverse=True)
        return ranking_dict

    def get_excellent_submitter_ranking(self, status='all', days=30):
        """
        status : patch status.
        days   : patches within specified days
        Return the excellent submitter ranking for each project.
        """
        print 'get_excellent_submitter_ranking'
