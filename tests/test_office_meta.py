# -*- coding: utf-8 -*-

import mock

from base import TestBase

class TestOfficeMeta(TestBase):
    def assertMetaEqual(self, date, meta):
        resp = self.app.get('/19/office/meta/%s?beta=enabled' % date)
        self.assertEqual(200, resp.status_code)
        return self.assertItemsEqual([(u"Jour liturgique", meta)], resp.data)

    @mock.patch('utils.requests.get')
    def test_get_meta(self, m_get):
        m_get.side_effect = self.m_get

        # Nominal tests
        self.assertMetaEqual("2015-12-25", u"Année A. Nous fêtons la Nativité du Seigneur. La couleur liturgique est le Blanc.")
        self.assertMetaEqual("2016-03-27", u"Dimanche de l'année C. Nous fêtons la Résurrection du Seigneur. La couleur liturgique est le Blanc.")
        self.assertMetaEqual("2016-05-08", u"Dimanche, 7<sup>ème</sup> Semaine du Temps Pascal de l'année C. La couleur liturgique est le Blanc.")
        self.assertMetaEqual("2016-05-15", u"Dimanche de la Pentecôte, année C. La couleur liturgique est le Rouge.")
        self.assertMetaEqual("2016-05-25", u"Mercredi, 8<sup>ème</sup> Semaine du Temps Ordinaire de l'année Paire. Nous fêtons Saint Bède le Vénérable, prêtre et docteur de l'Eglise, Saint Grégoire VII, pape, Sainte Marie-Madeleine de Pazzi, vierge. La couleur liturgique est le Vert.")
        self.assertMetaEqual("2016-06-11", u"Samedi, 10<sup>ème</sup> Semaine du Temps Ordinaire de l'année Paire. Nous fêtons Saint Barnabé. La couleur liturgique est le Rouge.")
        self.assertMetaEqual("2016-08-15", u"Nous fêtons l'Assomption de la Vierge Marie. La couleur liturgique est le Blanc.")

        # Error: obviously invalid date
        resp = self.app.get('/0/office/meta/2016-42')
        self.assertEqual(400, resp.status_code)
        resp = self.app.get('/0/office/meta/2016-42-17')
        self.assertItemsEqual([(u"Cette date n\\est pas dans notre calendrier", u"La date n'a pas été renseignée dans le calendrier")], resp.data)

