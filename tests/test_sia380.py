import unittest
from pyheat.sia380 import SIAWaermespeicherfaehigkeit
from pyheat.sia380 import SIAConf, reduktionsfaktor_erdreich_wand, \
    reduktionsfaktor_erdreich_boden
import pyheat.sia380


class Test(unittest.TestCase):

    def testBauDirZH(self):
        """
        Sia input / ouput based on:

        Einfuehrungskurs Systemnachweis
        für Baufachleute, Ausgabe 2009
        Baudirektion Kanton Zuerich

        """

        days = [
            31.0,
            28.0,
            31.0,
            30.0,
            31.0,
            30.0,
            31.0,
            31.0,
            30.0,
            31.0,
            30.0,
            31.0]

        config = SIAConf()
        # Energiebezugsflache m^2
        config.A_E = 190.9

        # Dach gegen Aussenluft m^2
        config.A_Re = 80.4

        # Decke gegen unbeheizte Raeume m^2
        config.A_Ru = 0.0

        # Wand gegen Aussenluft m^2
        config.A_We = 28.6 + 48.3 + 42.3 + 50.1
        #         config.A_We = 30.1 + 54.4 + 54.4 + 62.2

        # Wand gegen unbeheizte Raueme m^2
        config.A_Wu = 0.0

        # Wand gegen Erdreich m^2
        config.A_WG = 46.1 + 41.4

        # Wand gegen benachbarten beheitzten Raum
        config.A_Wn = 0.0

        # Boden gegen Aussenluft m^2
        config.A_Fe = 0.0

        # Boden gegen unbeheizte Raume m^2
        config.A_Fu = 0.0

        # Boden gegen Erdreich mit Bauteilheizung m^2
        config.A_FG = 56.2 + 21.8

        # Waermebruecke Decke/Wand m
        config.l_RW = 0.0

        # Waermebruecke Gebaudesockel m
        config.l_WF = 0.0

        # Waermebruecke Balkon m
        config.l_B = 0.0

        # Waermebruecke Fensteranschlag m
        config.l_w = 94.0

        # Waermebruecke Boden / Keller-Innenwand m
        config.l_F = 0.0

        # Waermebruecke Stuetzen, Traeger, Konsolen
        config.z = 0.0

        # Diverses
        # Dach gegen Aussenluft W / (m^2 * K)

        config.U_Re = 0.27

        # Decke gegen unbeheizte Raeume W / (m^2 * K)
        config.U_Ru = 0.0

        # Reduktionsfaktor Decke gegen unbeheizte Raeume -
        '''
        unbeheizter Raum :    b uR , b uW , b uF
        Estrichraum, Schraegdach ungedaemmt: 0.9
        Estrichraum, Schraegdach gedaemmt: U e < 0.4 W/m K: 0.7
        Kellerraum ganz im Erdreich: 0.7
        Kellerraum teilweise oder ganz ueber dem Erdreich: 0.8
        angebauter Raum: 0.8
        Glasvorbau: 0.9
        '''
        config.b_uR = 1.0

        # Wand gegen Aussenluft W / (m^2 * K)
        config.U_We = ((28.6 + 48.3 + 42.3 + 47.2) * 0.26 + 2.9 *
                       1.6) / (28.6 + 48.3 + 42.3 + 47.2 + 2.9)

        # Wand gegen unbehizte Raume W / (m^2 * K)
        config.U_Wu = 0.0

        # Reduktionsfaktor Wand gegen unbehizte Raume
        config.b_uW = 1.0

        # Wand gegen Erdreich W / (m^2 * K)
        config.U_WG0 = 0.21

        # Reduktionsfaktor Wand gegen Erdreich -

        b1 = reduktionsfaktor_erdreich_wand(4.55, 0.21)
        self.assertAlmostEqual(round(b1, 1), 0.7)

        b2 = reduktionsfaktor_erdreich_wand(2.4, 0.21)
        self.assertAlmostEqual(round(b2, 1), 0.8)

        config.b_GW = (46.1 * 0.7 + 41.4 * 0.8) / (46.1 + 41.4)

        # Wand gegen benachbarten beheizten Raum W / (m^2 * K)
        config.U_Wh = 0.0

        # Raumteperatur des benachbarten beheizten Raumes C
        config.theta_on = 20.0

        # Boden gegen Aussenluft W / (m^2 * K)
        config.U_Fe = 0.0

        # Boden gegen unbeheizte Raeume W / (m^2 * K)
        config.U_Fu = 0.0

        # Reduktionsfaktor Boden gegen unbeheizte Raume -
        config.b_uF = 1.0

        # Boden gegen Erdreich mit Bauteilheizung W / (m^2 * K)
        config.U_FG0 = 0.23

        # Reduktionsfaktor Boden gegen Erdreich -
        b3 = reduktionsfaktor_erdreich_boden(
            tiefe=2.55,
            A_FG=56.2,
            P_FG=30.0,
            U_FG0=0.23)
        self.assertAlmostEqual(round(b3, 2), 0.72)

        config.b_GF = (0.72 * 56.2 + 0.75 * 21.8) / (56.2 + 21.8)

        # Temperaturzuschlag Bauzeilheizung K
        config.delta_theta = (3.75 * 21.8 + 0 * 56.2) / (21.8 + 56.2)

        # Fenster horizontal W / (m^2 * K)
        config.U_wH = 1.4

        # Fenster Sued W / (m^2 * K)
        config.U_wS = 1.4

        # Fenster Ost W / (m^2 * K)
        config.U_wE = 1.4

        # Fenster West W / (m^2 * K)
        config.U_wW = 1.4

        config.U_wN = 1.4
        # Fenster Nord W / (m^2 * K)
        config.U_wSW = 0.0
        config.U_wSE = 0.0
        config.U_wNW = 0.0
        config.U_wNE = 0.0

        # Waermebruecke Decke/Wand W / (m * K)
        config.psi_RW = 0.0

        # Waermebruecke Gebaeudesockel W / (m * K)
        config.psi_WG = 0.0

        # Waermebruecke Balkon W / (m * K)
        config.psi_B = 0.0

        # Waermebruecke Fensteranschlag W / (m * K)
        config.psi_W = 0.10

        # Waermebruecke Boden / Keller - Innenwand W / (m * K)
        config.psi_F = 0.0

        # Waermebruecke Stuetzen, Traeger, Konsolen W/ K
        config.chi = 0.0

        # Gesamtenergiedurchlassgrad Fenster (senkrecht)
        config.g_90deg = 0.55

        # Abminderungsfaktor fuer Fensterrahmen -
        config.F_F = 0.7

        # Verschattungsfaktor horizontal -
        config.F_SH = 1.0

        # Verschattungsfaktor Sued -
        config.F_SS = (2.5 * 0.95 + 2.5 * 0.94 + 5.0 * 1.0 + 5.0 * 1.0) / (2.5 + 2.5 + 5.0 + 5.0)

        # Verschattungsfaktor Ost -
        config.F_SE = (1.7 * 0.84 + 1.7 * 0.94 + 2.5 *
                       0.9 + 0.2 * 0.67) / (1.7 + 1.7 + 2.5 + 0.2)

        # Verschattungsfaktor West -
        config.F_SW = (2.5 * 0.84 + 1.7 * 0.84 + 1.0 * 0.94 +
                       6.7 * 0.94 + 0.2 * 0.67) / (2.5 + 1.7 + 1.0 + 6.7 + 0.2)

        # Verschattungsfaktor Nord -
        config.F_SN = 0.97

        config.F_SNE = 0.0
        config.F_SNW = 0.0
        config.F_SSE = 0.0
        config.F_SSW = 0.0

        # Fenster
        # Fenster horizontal m^2
        config.A_wH = 0.0

        # Fenster Sued m^2
        config.A_wS = 2.5 * 2.0 + 5.0 * 2.0

        # Fenster Ost m^2
        config.A_wE = 1.7 * 2.0 + 2.5 + 0.2

        # Fenster West m^2
        config.A_wW = 2.5 + 1.7 + 1.0 + 6.7 + 0.2

        config.A_wNE = 0.0
        config.A_wNW = 0.0
        config.A_wSE = 0.0
        config.A_wSW = 0.0

        # Fenster Nord m^2
        config.A_wN = 1.5

        # Spezielle Engabedaten
        config.C_AE = 0.3
        # Waermespeichergaehigkeit pro Energiebezugsflaeche MJ / (m^2 * K)

        config.a_0 = 1.0
        # numerischer Parameter fuer Ausnutzungsgrad -

        config.tau_0 = 15.0

        # Klimadaten
        # Laenge der Berechnungsperiode d
        config.t_c = days

        # Hoehenlage in Meter ueber Meer m
        config.h = 779.0

        # Aussentemperatur C
        config.theta_e = [-0.3,
                          0.7,
                          4.1,
                          6.9,
                          12.0,
                          14.7,
                          16.9,
                          17.1,
                          12.8,
                          9.0,
                          3.5,
                          1.1]

        # Globale Sonnenstrahlung horizontal MJ / m^2
        config.G_sH = [
            112,
            169,
            308,
            407,
            522,
            550,
            576,
            504,
            334,
            209,
            117,
            86]

        # Raumtemperatur C
        config.theta_o_C = 20.0

        # Regelungszuschlag fuer die Raumteperatur K
        config.delta_theta_o_K = 0.0

        # Personenflaeche m^2 / P
        config.A_P = 60.0

        # Waermeabgabe pro Person W / P
        config.Q_P = 70.0

        # Prasenezzeit pro Tag h / d
        config.t_p = 12.0

        # Elektrizitaetsbedarf pro Jahr MJ/m^2
        config.Q_El = 80.0

        # Reduktionsfaktor Elektrizitaet -
        config.f_El = 0.7

        # fleachenbezogener Aussenluft-Volumenstrom m^3 / (h*m^2)
        config.V_A_Es = [0.7] * 12

        config.add_wall(a="N",
                        F=0.97,
                        G=[51,
                           73,
                           112,
                           127,
                           161,
                           176,
                           174,
                           139,
                           96,
                           64,
                           44,
                           37],
                        A=1.5,
                        U=1.4)

        config.add_wall(a="E",
                        F=0.89,
                        G=[75,
                           119,
                           198,
                           241,
                           292,
                           293,
                           311,
                           279,
                           187,
                           115,
                           70,
                           56],
                        A=6.1,
                        U=1.4)

        config.add_wall(a="S",
                        F=0.98,
                        G=[193,
                           244,
                           319,
                           283,
                           271,
                           251,
                           281,
                           313,
                           285,
                           241,
                           171,
                           145],
                        A=15.0,
                        U=1.4)

        config.add_wall(a="W",
                        F=0.90,
                        G=[86,
                           133,
                           206,
                           236,
                           284,
                           295,
                           319,
                           292,
                           205,
                           137,
                           78,
                           59],
                        A=12.1,
                        U=1.4)

        config.check()

        heat = pyheat.sia380.sia380(config)

        # Transmissionswaermeverluste

        #   Decke gegen aussen
        Q_Re = [6.2, 5.3, 4.8, 3.9, 2.4, 1.6, 0.9, 0.9, 2.1, 3.4, 4.9, 5.8]

        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_Re"], Q_Re[i], places=1)

        #   Wand gegen aussen
        Q_We = [
            13.6,
            11.7,
            10.7,
            8.5,
            5.4,
            3.4,
            2.1,
            1.9,
            4.7,
            7.4,
            10.7,
            12.7]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_We"], Q_We[i], places=1)

        #   Wand gegen Erdreich
        Q_WG = [3.9, 3.4, 3.1, 2.4, 1.5, 1.0, 0.6, 0.6, 1.3, 2.1, 3.1, 3.6]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_WG"], Q_WG[i], places=1)

        #   Fenster S
        QwSS = [6.0, 5.1, 4.7, 3.7, 2.4, 1.5, 0.9, 0.9, 2.1, 3.2, 4.7, 5.6]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["QwS"]['S'], QwSS[i], places=1)

        #   Fenster E
        QwSE = [2.4, 2.1, 1.9, 1.5, 1.0, 0.6, 0.4, 0.3, 0.8, 1.3, 1.9, 2.3]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["QwS"]['E'], QwSE[i], places=1)

        #   Fenster W
        QwSW = [4.8, 4.1, 3.8, 3.0, 1.9, 1.2, 0.7, 0.7, 1.7, 2.6, 3.8, 4.5]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["QwS"]['W'], QwSW[i], places=1)

        #   Fenster N
        QwSN = [0.6, 0.5, 0.5, 0.4, 0.2, 0.2, 0.1, 0.1, 0.2, 0.3, 0.5, 0.6]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["QwS"]['N'], QwSN[i], places=1)

        #   Waermebruecken
        Q_WB = [2.7, 2.3, 2.1, 1.7, 1.1, 0.7, 0.4, 0.4, 0.9, 1.5, 2.1, 2.5]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_WB"], Q_WB[i], places=1)

        #   Transmissionswaermeverlust Qt:
        Q_T = [
            44.2,
            37.9,
            34.6,
            27.6,
            17.5,
            11.3,
            6.9,
            6.5,
            15.3,
            24.0,
            34.8,
            41.1]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_T"], Q_T[i], places=1)

        # Lueftungswaermeverlust QV
        Q_V = [11.7, 10.1, 9.2, 7.3, 4.6, 3.0, 1.8, 1.7, 4.0, 6.4, 9.2, 10.9]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_V"], Q_V[i], places=1)

        # Gesamtwaermeverlust
        Q_ot = [
            55.9,
            48.0,
            43.8,
            35.0,
            22.2,
            14.3,
            8.7,
            8.2,
            19.3,
            30.4,
            44.0,
            52.1]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_ot"], Q_ot[i], places=1)

        # Waermegewinn
        # Solare Waermegewinne S
        QsS = [5.15, 6.5, 8.5, 7.6, 7.2, 6.7, 7.5, 8.4, 7.6, 6.4, 4.6, 3.9]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Qs"]['S'], QsS[i], places=1)

        # Solare Waermegewinne E

        QsE = [0.7, 1.2, 1.95, 2.4, 2.9, 2.9, 3.1, 2.7, 1.8, 1.1, 0.7, 0.6]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Qs"]['E'], QsE[i], places=1)

        # Solare Waermegewinne W
        QsW = [1.7, 2.6, 4.1, 4.7, 5.6, 5.8, 6.3, 5.8, 4.05, 2.7, 1.5, 1.2]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Qs"]['W'], QsW[i], places=1)

        # Solare Waermegewinne N
        QsN = [0.1, 0.2, 0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.2, 0.1, 0.1]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Qs"]['N'], QsN[i], places=1)

        # Ratio gamma
        gamma = [0.3, 0.3, 0.5, 0.6, 1.0, 1.5, 2.7, 2.9, 1.0, 0.6, 0.3, 0.2]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["gamma"], gamma[i], places=1)

        # ratio used heat gains
        phi_g = [
            1.0,
            1.0,
            1.0,
            0.98,
            0.86,
            0.63,
            0.37,
            0.35,
            0.85,
            0.99,
            1.0,
            1.0]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["phi_g"], phi_g[i], places=1)

        # heat demand Q_h
        Q_h = [
            41.9,
            31.8,
            22.8,
            14.3,
            2.9,
            0.3,
            0.0,
            0.0,
            2.4,
            13.8,
            31.0,
            40.1]
        for i in range(12):
            self.assertAlmostEqual(heat[i]["Q_h"], Q_h[i], places=1)
