import unittest
from unittest.mock import Mock, ANY
from kassapaate import Kassapaate, HINTA
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()

    def test_kortilta_velotetaan_hinta_jos_rahaa_on(self):
        """
        jos kortilla on riittävästi rahaa, kassapäätteen metodin osta_lounas kutsuminen veloittaa summan kortilta.
        """

        maksukortti_mock = Mock(Maksukortti)
        maksukortti_mock.saldo = 10
        maksukortti_mock.osta.return_value = True

        self.kassa.osta_lounas(maksukortti_mock)

        maksukortti_mock.osta.assert_called_with(HINTA)

    def test_kortilta_ei_veloteta_jos_raha_ei_riita(self):
        """
        jos kortilla ei ole riittävästi rahaa, kassapäätteen metodin osta_lounas kutsuminen ei veloita kortilta rahaa.
        """
    
        maksukortti_mock = Mock(Maksukortti)
        maksukortti_mock.saldo = 4

        kassapaate_mock = Mock(self.kassa)

        kassapaate_mock.osta_lounas = Mock(return_value=False)
        kassapaate_mock.osta_lounas(maksukortti_mock)

        maksukortti_mock.osta.assert_not_called()
