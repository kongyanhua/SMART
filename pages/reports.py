import unittest, time
from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.by import By
from common import settings, actions, smart_driver
from selenium.webdriver.common.action_chains import ActionChains
from tools import common_tools
from parameterized import parameterized
from modals.report_test_result import result_report


class Reports(object):
    driver = ''

    def __init__(self, driver):

        self.driver = driver

    def find_report_double_click(self, report_name):

        if report_name.endswith('#'):
            standard_or_enterprise = 'enterprise'
            report_name = report_name.rstrip('#')
        else:
            standard_or_enterprise = 'standard'

        self.report_name = report_name
        self.driver.get(settings.url)

        login_ele = self.driver.find_element_(By.ID, 'txtLoginid')
        password_ele = self.driver.find_element_(By.ID, 'txtPassword')
        login_ele_btn = self.driver.find_element_(By.ID, 'btnloginText')

        login_ele.clear()
        login_ele.send_keys('admin')

        password_ele.clear()
        password_ele.send_keys('Admin')
        login_ele_btn.click()

        # click Inpatient
        actions.wait_element_clickable(self.driver, By.ID, 'aSlideMenuSelModuleSIP101')
        actions.wait_element_invisibility(self.driver, By.CLASS_NAME, 'modalOverlay')
        inpatient = self.driver.find_element_(By.ID, 'aSlideMenuSelModuleSIP101')
        inpatient.click()

        # Click "report"
        report = self.driver.find_element_(By.ID, 'aIPModuleWorkplans')
        report.click()

        # click enterprise_reports_link
        standard_reports_link_xpath = '//span[text()="Inpatient Standard Reports"]'
        enterprise_reports_link = '//span[text()="Inpatient Enterprise Reports"]'

        if standard_or_enterprise in 'standard':
            reports_link_xpath = standard_reports_link_xpath
        else:
            reports_link_xpath = enterprise_reports_link

        actions.wait_element_clickable(self.driver, By.XPATH, reports_link_xpath)
        reports_link = self.driver.find_element_by_xpath(reports_link_xpath)
        reports_link.click()

        # enter report name
        report_name_input_id = 'txtSearch'
        report_name_input = self.driver.find_element_(By.ID, report_name_input_id)
        actions.wait_element_clickable(self.driver, By.ID, report_name_input_id)
        report_name_input.clear()
        report_name_input.send_keys(report_name)

        # click search button
        report_search_btn_id = 'spnSearch'
        report_search_btn = self.driver.find_element_(By.ID, report_search_btn_id)
        actions.wait_element_clickable(self.driver, By.ID, report_search_btn_id)
        report_search_btn.click()

        # find and Open report
        actions.wait_element_clickable(self.driver, By.PARTIAL_LINK_TEXT, report_name)
        report_enter_link = self.driver.find_element_by_partial_link_text(report_name)
        ActionChains(self.driver).double_click(report_enter_link).perform()

        return report_name

    def report_data_validation(self, report_name):
        actions.wait_element_visibility(self.driver, By.ID, 'dvContentBody')
        # actions.wait_document_completed(self.driver)
        # actions.wait_element_presence(self.driver, By.ID, 'dvBody')

        # assert
        assert 'Enterprise Data Validation' in self.driver.page_source
        # self.assertIn(member='Enterprise Data Validation', container=self.driver.page_source)

        # click import date, after
        dataope_id = 'dataOpe'
        # actions.wait_element_clickable(self.driver, By.ID, dataope_id)
        # actions.wait_element_presence(self.driver, By.ID, dataope_id)
        dataope = self.driver.find_element(By.ID, value=dataope_id)
        dataope.click()

        # cycle the options
        dataope_option_after_xpath = '//select[@id="dataOpe"]/option[text()="After"]'
        dataope_option_after = self.driver.find_element_(By.XPATH, value=dataope_option_after_xpath)
        dataope_option_after.click()

        # enter date
        dataope_input_after_id = 'importStart'
        dataope_input_after = self.driver.find_element_(By.ID, value=dataope_input_after_id)
        dataope_input_after.clear()
        dataope_input_after.send_keys('1/1/2018')

        # Click search
        dataope_search_id = 'btnSearch'
        dataope_search = self.driver.find_element_(By.ID, value=dataope_search_id)
        dataope_search.click()

        common_tools.save_html_resource(self.driver.page_source.__str__().encode("utf-8").__str__(), report_name)

    def click_save_search(self, save_search_name):
        pass

    def wait_until_title_contains(self, report_name):
        if report_name == 'DRG Change Condition Detail':
            smart_pass = actions.wait_report_title_contains(self.driver, 'DRG Change Detail')
            self.assertIn('DRG Change Detail', container=self.driver.title,
                          msg=report_name + settings.error_report_generate)
            assert 'DRG Change Detail' in self.driver.title
        elif report_name == 'Top 50 Diagnoses by Present on Admission(POA)':
            smart_pass = actions.wait_report_title_contains(self.driver,
                                                            'Top 50 Other Diagnoses by Present on Admission(POA)')
            assert 'Top 50 Other Diagnoses' in self.driver.title
        elif report_name == 'Management Clinical Profile':
            smart_pass = actions.wait_report_title_contains(self.driver, 'Evaluation')
            assert 'Evaluation' in self.driver.title
        elif 'Frequency' in report_name:
            smart_pass = actions.wait_report_title_contains(self.driver, 'Frequency')
            assert 'Frequency' in self.driver.title
        elif 'DRG Contribution to Payer CMI' in report_name:
            smart_pass = actions.wait_report_title_contains(self.driver, 'DRG Contribution to CMI by Payer')
            assert 'DRG Contribution to CMI by Payer' in self.driver.title
        elif report_name in report_name:
            smart_pass = actions.wait_report_title_contains(self.driver, report_name)
            assert report_name in self.driver.title
        else:
            smart_pass = False

        return smart_pass

        # if not smart_pass:
        #     self.result_report.report_test_result = 'Fail'
        # else:
        #     self.result_report.report_test_result = 'Pass'


class ReportAssist(object):

    def handle_error_occur(self):
        pass

    def handle_out_of_memory(self):
        pass

    def handle_no_data(self):
        pass