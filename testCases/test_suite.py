import pytest

from testCases.test_login import TestLogin


if __name__ == '__main__':
    pytest.main(['-v', '-p', 'pytest_ordering','testCases/test_login.py',])