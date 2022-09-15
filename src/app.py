from tkinter import *
from tkinter.messagebox import showinfo, showwarning
from common import get_summary_payload, get_result_payload, get_export_payload, dict_to_csv
from common.constants import *
from widget import InputWidget, ButtonWidget, TableWidget, LabelWidget, ContainerWidget
from search import ShodanEngine
from report.generator import GenerateDocument
from datetime import datetime


class App:

    def __init__(self, title):
        self.shodan_engine = ShodanEngine()
        self.root = Tk()
        self.root.title(title)
        self.render()
        self.root.mainloop()

    def render(self):
        self.scanner()
        self.results()
        self.last_request()
        self.actions()

    def scanner(self):
        container = ContainerWidget(self.root, 'Scanner')
        parent = container.labelframe
        self.search_input = InputWidget(parent, 'Query')
        self.filter_input = InputWidget(parent, 'Net')

    def results(self):
        container = ContainerWidget(self.root, 'Results')
        parent = container.labelframe
        self.result_table_widget = TableWidget(parent, DEFAULT_HEADERS)

    def actions(self):
        container = ContainerWidget(self.root, 'Actions', True)
        parent = container.frame
        ButtonWidget(parent, 'Run scan', self.run_scan)
        ButtonWidget(parent, 'Clear', self.clear_input)
        ButtonWidget(parent, 'Export', self.export)
        ButtonWidget(parent, 'Report', self.report)
        ButtonWidget(parent, 'Exit', self.exit_action)

    def last_request(self):
        container = ContainerWidget(self.root, 'Last request details')
        parent = container.labelframe
        self.total_label_widget = LabelWidget(parent, 'Result(s) found: ')
        self.time_label_widget = LabelWidget(parent, 'Elapsed time: ')
        self.query_label_widget = LabelWidget(parent, 'Search query: ')

    def run_scan(self):
        shodan_engine = self.shodan_engine
        self.query = shodan_engine.build_query(
            self.search_input.get_entry(), self.filter_input.get_entry())
        raw = shodan_engine.search(self.query)
        if shodan_engine.has_failed:
            return
        if shodan_engine.last_total <= 0:
            self.result_table_widget.destroy()
            showinfo(title='Information', message='No result was found!')
            return
        data = get_result_payload(raw)
        self.result_table_widget.create(data)
        self.total_label_widget.update(
            f'Result(s) found: {shodan_engine.last_total}')
        self.time_label_widget.update(
            f'Elapsed time: {shodan_engine.last_time} seconds')
        self.query_label_widget.update(
            f'Search query: {shodan_engine.last_query}')

    def clear_input(self):
        self.search_input.delete_entry()
        self.filter_input.delete_entry()

    def export(self):
        shodan_engine = self.shodan_engine
        if not shodan_engine.last_response:
            showwarning(title='Warning',
                        message='There is no data for selected action')
            return
        data = get_export_payload(shodan_engine.last_response)
        dict_to_csv(data)
        showinfo(title='Information',
                 message='The result was exported successfully')

    def report(self):
        shodan_engine = self.shodan_engine
        if not shodan_engine.last_response:
            showwarning(title='Warning',
                        message='There is no data for selected action')
            return
        data = get_summary_payload(shodan_engine.last_response)
        timestamp = int(datetime.now().timestamp())
        doc = GenerateDocument(
            f"data/report_{timestamp}.pdf", 'ENTERPRISE SHODAN SCAN', data)
        doc.generate()
        showinfo(title='Information', message='Your report is ready')

    def exit_action(self):
        self.root.destroy()


def run():
    App('Enterprise Shodan Scan')
