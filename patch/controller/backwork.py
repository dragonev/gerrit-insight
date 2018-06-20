import os, sys
from django.conf import settings

from patch.controller.common import Logger
from patch.controller.analyzer import PatchAnalyzer
from patch.controller.gerrit import PatchManager
from patch.controller.excel import PatchReport

def init_web_server():
    debug = getattr(settings, 'DEBUG', True)
    log_dir = getattr(settings, 'LOG_DIR', 'logs')
    log_name = getattr(settings, 'LOG_NAME', 'patch-spy.py')
    cache_dir = getattr(settings, 'CACHE_DIR', 'caches')
    project_set = getattr(settings, 'PROJECT_SET', None)
    patch_cache_name = getattr(settings, 'PATCH_CACHE_NAME', 'patches.cache')

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    if not project_set:
        print 'project set can not be empty.'
        sys.exit(1)

    Logger.init_logger(log_dir, log_name)
    patchManager = PatchManager(cache_dir, patch_cache_name, debug)
    patchManager.cleanup_patch_cache()
    patchManager.get_patches_with_status_of_all_projects(project_set, 'open')
    patchManager.get_patches_with_status_of_all_projects(project_set, 'merged')
    generate_statistical_data_report()

def generate_statistical_data_report():
    debug = getattr(settings, 'DEBUG', True)
    cache_dir = getattr(settings, 'CACHE_DIR', 'caches')
    patch_cache_name = getattr(settings, 'PATCH_CACHE_NAME', 'patches.cache')

    patchManager = PatchManager(cache_dir, patch_cache_name, debug)
    patchAnalyzer = PatchAnalyzer(patchManager.get_all_projects_patches())
    patchReport = PatchReport()
    patchReport.open_excel(os.path.join(cache_dir, 'Patch_Ranking.xls'))

    ranking = patchAnalyzer.get_submitted_patch_ranking(days=1024)
    excel_sheet = 'Submitted_Patch_Ranking'
    excel_title = ['Project', 'Author', excel_sheet]
    patchReport.write_excel(ranking, excel_sheet, excel_title)

    ranking = patchAnalyzer.get_reviewed_patch_ranking(days=1024)
    excel_sheet = 'Reviewed_Patch_Ranking'
    excel_title = ['Project', 'Author', excel_sheet]
    patchReport.write_excel(ranking, excel_sheet, excel_title)

    ranking = patchAnalyzer.get_submitted_line_ranking(days=1024)
    excel_sheet = 'Submitted_Line_Ranking'
    excel_title = ['Project', 'Author', excel_sheet]
    patchReport.write_excel(ranking, excel_sheet, excel_title)

    ranking = patchAnalyzer.get_submitted_patchset_ranking(days=1024)
    excel_sheet = 'Submitted_Patchset_Ranking'
    excel_title = ['Project', 'Author', excel_sheet]
    patchReport.write_excel(ranking, excel_sheet, excel_title)

    # ranking = patchAnalyzer.get_excellent_submitter_ranking(days=1024)
    # excel_sheet = 'Excellent_Submitter_Ranking'
    # excel_title = ['Project', 'Author', excel_sheet]
    # patchReport.write_excel(ranking, excel_sheet, excel_title)

    patchReport.close_excel()
