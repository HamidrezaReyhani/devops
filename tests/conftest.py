import sys
import os

# اضافه کردن ریشه پروژه به مسیر پایتون
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

import pytest
from unittest import mock

@pytest.fixture
def mock_db_connection():
    """فیکسچر برای mock کردن اتصال دیتابیس"""
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_conn = mock.Mock()
        mock_cursor = mock.Mock()
        
        # تغییر این خط: باید دقیقاً همان مقداری را برگرداند که تست انتظار دارد
        mock_cursor.fetchone.return_value = ('test_data',)  # نه timestamp
        
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        yield mock_cursor