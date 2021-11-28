from unittest import TestCase
from enums.models import FreeRentType
import warnings


class FreeRentTypeModelTest(TestCase):
    """
    フリーレント種別モデルのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')

    def test_limit_is_span(self):
        self.assertFalse(FreeRentType.objects.get(pk=0).limit_is_span)
        self.assertTrue(FreeRentType.objects.get(pk=1).limit_is_span)
        self.assertFalse(FreeRentType.objects.get(pk=2).limit_is_span)

    def test_limit_is_month(self):
        self.assertFalse(FreeRentType.objects.get(pk=0).limit_is_month)
        self.assertFalse(FreeRentType.objects.get(pk=1).limit_is_month)
        self.assertTrue(FreeRentType.objects.get(pk=2).limit_is_month)
