import pytest
# from testCases.test_companySignUp import TestSignUp
# from testCases.test_login import TestLogin
# from testCases.test_configuration import TestConfiguration
# from testCases.test_AddEmployees import TestaddEmployees
# from testCases.test_EmployeeSignUp import TestEmployeeSignUp
# from testCases.test_networks import TestNetworks
# from SunithaTestCase.test_profilePage import TestMyProfile
# from SunithaTestCase.test_CompanyProfile import TestCompanyProfile
# from krishnatestCases.test_newsfeed import TestNewsFeed
# from krishnatestCases.test_resources import Test_Resources
# # from krishnatestCases.test_certification import Test_Certification
# from Anand_TestCases.test_DealRegistrations import Test_Create_DealwithNetworkCompany
# from Anand_TestCases.test_Recognitions import Test_Create_Recognition
## from SunithaTestCase.test_Webinar import Test_Webinar
# from testCases.test_MediaDrive import TestMediaDrive
# from krishnatestCases.test_mediadrive1 import TestMediadrive
# from krishnatestCases.test_newsfeed1 import TestNewsFeed1
# from testCases.test_PW import Test_PW
# from krishnatestCases.test_reportabuse import TestReportabuse
# #from testCases.test_forgotPassword import TestForgotPassword
# from krishnatestCases.test_customsystemmenu import TestCustomsystemmenu

# Run the TestLogin class directly
if __name__ == '__main__':
    pytest.main(['-v', '-p', 'pytest_ordering', 'testCases/test_companySignUp.py', 'testCases/test_login.py', 'testCases/test_configuration.py',
                 'testCases/test_AddEmployees.py', 'testCases/test_EmployeeSignUp.py', 'testCases/test_networks.py',
                 'testCases/test_profilePage.py', 'testCases/test_CompanyProfile.py', 'testCases/test_newsfeed.py',
                 'testCases/test_resources.py', 'testCases/test_certification.py', 'testCases/test_DealRegistrations.py',
                 'testCases/Test_Create_Recognition.py', 'testCases/test_Webinar.py', 'testCases/test_MediaDrive.py',
                 'krishnatestCases/test_mediadrive1.py', 'krishnatestCases/test_newsfeed1.py', 'testCases/test_PW.py',
                 'krishnatestCases/test_reportabuse.py',])