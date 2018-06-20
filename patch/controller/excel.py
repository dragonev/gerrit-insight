import os
import xlwt
from abc import ABCMeta, abstractmethod
from patch.controller.common import Logger


class _Excel(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def _get_title_style(self):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        return style

    def _get_cell_style(self):
        style = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_TOP
        style.alignment = alignment
        return style

    def reset_excel_profile(self, excel_path):
        self.excel_path = excel_path

    def open_excel(self, excel_path):
        self.excel_path = excel_path
        self.write_excel_object = xlwt.Workbook(encoding='utf-8')

    @abstractmethod
    def write_excel(self):
        pass

    def close_excel(self):
        self.write_excel_object.save(self.excel_path)


class PatchReport(_Excel):

    def __init__(self):
        super(PatchReport, self).__init__()
        self.init_style()

    def init_style(self):
        self.title_style = self._get_title_style()
        self.cell_style = self._get_cell_style()

    def write_excel(self, ranking, excel_sheet, excel_title):
        row_index = 0
        write_sheet_object = self.write_excel_object.add_sheet(
            excel_sheet, cell_overwrite_ok=True)

        for index in range(len(excel_title)):
            write_sheet_object.write(
                row_index, index, excel_title[index], self.title_style)
        row_index += 1

        for project, author_ranking_list in ranking.items():
            write_sheet_object.write_merge(row_index, row_index+len(author_ranking_list)-1, 0, 0, project, self.cell_style)
            for author_ranking in author_ranking_list:
                for index in xrange(len(author_ranking)):
                    write_sheet_object.write(row_index, index+1, author_ranking[index], self.cell_style)
                row_index += 1
