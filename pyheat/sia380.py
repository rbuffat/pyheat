from collections import defaultdict, OrderedDict
from math import floor, ceil
import numpy as np


class SIABuildingType:
    EFH = "efh"
    MFH = "mfh"
    Verwaltung = "verwaltung"
    Schule = "schule"
    Verkauf = "verkauf"
    Restaurant = "restaurant"
    Versammlungslokale = "versammlungslokale"
    Spital = "spital"
    Industrie = "industrie"
    Lager = "lager"
    Sportbauten = "sport"
    Hallenbad = "hallenbad"


SIAPeopleArea = {SIABuildingType.MFH: 40.0,
                 SIABuildingType.EFH: 60.0,
                 SIABuildingType.Verwaltung: 20.0,
                 SIABuildingType.Schule: 10.0,
                 SIABuildingType.Verkauf: 10.0,
                 SIABuildingType.Restaurant: 5.0,
                 SIABuildingType.Versammlungslokale: 5.0,
                 SIABuildingType.Spital: 30.0,
                 SIABuildingType.Industrie: 20.0,
                 SIABuildingType.Lager: 100.0,
                 SIABuildingType.Sportbauten: 20.0,
                 SIABuildingType.Hallenbad: 20.0}

SIAHeatPersonQp = {SIABuildingType.MFH: 70.0,
                   SIABuildingType.EFH: 70.0,
                   SIABuildingType.Verwaltung: 80.0,
                   SIABuildingType.Schule: 70.0,
                   SIABuildingType.Verkauf: 90.0,
                   SIABuildingType.Restaurant: 100.0,
                   SIABuildingType.Versammlungslokale: 80.0,
                   SIABuildingType.Spital: 80.0,
                   SIABuildingType.Industrie: 100.0,
                   SIABuildingType.Lager: 100.0,
                   SIABuildingType.Sportbauten: 100.0,
                   SIABuildingType.Hallenbad: 60.0}

SIAOccupation_tp = {SIABuildingType.MFH: 12.0,
                    SIABuildingType.EFH: 12.0,
                    SIABuildingType.Verwaltung: 6.0,
                    SIABuildingType.Schule: 4.0,
                    SIABuildingType.Verkauf: 4.0,
                    SIABuildingType.Restaurant: 2.0,
                    SIABuildingType.Versammlungslokale: 2.0,
                    SIABuildingType.Spital: 16.0,
                    SIABuildingType.Industrie: 6.0,
                    SIABuildingType.Lager: 6.0,
                    SIABuildingType.Sportbauten: 6.0,
                    SIABuildingType.Hallenbad: 4.0}

SIAElectricity_Efel = {SIABuildingType.MFH: 100.0,
                       SIABuildingType.EFH: 80.0,
                       SIABuildingType.Verwaltung: 80.0,
                       SIABuildingType.Schule: 40.0,
                       SIABuildingType.Verkauf: 120.0,
                       SIABuildingType.Restaurant: 120.0,
                       SIABuildingType.Versammlungslokale: 60.0,
                       SIABuildingType.Spital: 100.0,
                       SIABuildingType.Industrie: 60.0,
                       SIABuildingType.Lager: 20.0,
                       SIABuildingType.Sportbauten: 20.0,
                       SIABuildingType.Hallenbad: 200.0}

SIAElectricityRed_fel = {SIABuildingType.MFH: 0.7,
                         SIABuildingType.EFH: 0.7,
                         SIABuildingType.Verwaltung: 0.9,
                         SIABuildingType.Schule: 0.9,
                         SIABuildingType.Verkauf: 0.8,
                         SIABuildingType.Restaurant: 0.7,
                         SIABuildingType.Versammlungslokale: 0.8,
                         SIABuildingType.Spital: 0.7,
                         SIABuildingType.Industrie: 0.9,
                         SIABuildingType.Lager: 0.9,
                         SIABuildingType.Sportbauten: 0.9,
                         SIABuildingType.Hallenbad: 0.7}

SIAAussenluftvolumenstrom_VAE = {SIABuildingType.MFH: 0.7,
                                 SIABuildingType.EFH: 0.7,
                                 SIABuildingType.Verwaltung: 0.7,
                                 SIABuildingType.Schule: 0.7,
                                 SIABuildingType.Verkauf: 0.7,
                                 SIABuildingType.Restaurant: 1.2,
                                 SIABuildingType.Versammlungslokale: 1.0,
                                 SIABuildingType.Spital: 1.0,
                                 SIABuildingType.Industrie: 0.7,
                                 SIABuildingType.Lager: 0.3,
                                 SIABuildingType.Sportbauten: 0.7,
                                 SIABuildingType.Hallenbad: 0.7}


class WaermeSpeicherfaehigkeitType:
    Schwer = "schwer"
    Mittel = "mittel"
    Leicht = "leicht"
    SehrLeicht = "sehr_leicht"


# http://www.awel.zh.ch/internet/baudirektion/awel/de/energie_radioaktive_abfaelle/energiepraxis/spezialseminare/kurse_sia_380_1/_jcr_content/contentPar/downloadlist_2/downloaditems/383_1284041696091.spooler.download.1297080458577.pdf/Dokumentation_System.pdf
SIAWaermespeicherfaehigkeit = {WaermeSpeicherfaehigkeitType.Schwer: 0.5, WaermeSpeicherfaehigkeitType.Mittel: 0.3,
                               WaermeSpeicherfaehigkeitType.Leicht: 0.1, WaermeSpeicherfaehigkeitType.SehrLeicht: 0.05}

# bGFs: key: tiefe [m]
# values fuer A/P = 2m,
# A/P = 5m,
# A/P = 10m,
# jeweils fuer U_GF0 [0.2,0.4,0.6,1]'''
bGFs = OrderedDict()
bGFs[0.0] = [[0.82, 0.69, 0.6, 0.49],
             [0.67, 0.52, 0.43, 0.31],
             [0.53, 0.37, 0.29, 0.2]]
bGFs[0.5] = [[0.8, 0.67, 0.57, 0.46],
             [0.66, 0.51, 0.41, 0.3],
             [0.53, 0.36, 0.28, 0.2]]
bGFs[1.0] = [[0.79, 0.65, 0.55, 0.43],
             [0.65, 0.49, 0.4, 0.29],
             [0.52, 0.36, 0.27, 0.19]]
bGFs[2.0] = [[0.76, 0.61, 0.51, 0.39],
             [0.63, 0.47, 0.37, 0.27],
             [0.5, 0.34, 0.26, 0.18]]
bGFs[3.0] = [[0.73, 0.57, 0.47, 0.35],
             [0.61, 0.45, 0.35, 0.25],
             [0.49, 0.33, 0.25, 0.17]]
bGFs[5.0] = [[0.68, 0.51, 0.41, 0.3],
             [0.57, 0.41, 0.32, 0.22],
             [0.47, 0.31, 0.23, 0.16]]
bGFs[10.0] = [[0.58, 0.41, 0.32, 0.22],
              [0.5, 0.33, 0.25, 0.17],
              [0.42, 0.27, 0.2, 0.13]]

_verschattungsfaktor_horizont = defaultdict(dict)
_verschattungsfaktor_horizont[0.0][-90.0] = 1.0
_verschattungsfaktor_horizont[0.0][90.0] = 1.0
_verschattungsfaktor_horizont[0.0][180.0] = 1.0
_verschattungsfaktor_horizont[0.0][-180.0] = 1.0
_verschattungsfaktor_horizont[0.0][0.0] = 1.0

_verschattungsfaktor_horizont[10.0][-90.0] = 0.94
_verschattungsfaktor_horizont[10.0][180.0] = 1.0
_verschattungsfaktor_horizont[10.0][-180.0] = 1.0
_verschattungsfaktor_horizont[10.0][90.0] = 0.94
_verschattungsfaktor_horizont[10.0][0.0] = 0.96

_verschattungsfaktor_horizont[20.0][-90.0] = 0.81
_verschattungsfaktor_horizont[20.0][180.0] = 0.97
_verschattungsfaktor_horizont[20.0][-180.0] = 0.97
_verschattungsfaktor_horizont[20.0][90.0] = 0.81
_verschattungsfaktor_horizont[20.0][0.0] = 0.82

_verschattungsfaktor_horizont[30.0][-90.0] = 0.68
_verschattungsfaktor_horizont[30.0][180.0] = 0.94
_verschattungsfaktor_horizont[30.0][-180.0] = 0.94
_verschattungsfaktor_horizont[30.0][90.0] = 0.68
_verschattungsfaktor_horizont[30.0][0.0] = 0.49

_verschattungsfaktor_horizont[40.0][-90.0] = 0.60
_verschattungsfaktor_horizont[40.0][180.0] = 0.90
_verschattungsfaktor_horizont[40.0][-180.0] = 0.90
_verschattungsfaktor_horizont[40.0][90.0] = 0.60
_verschattungsfaktor_horizont[40.0][0.0] = 0.45


def get_verschattungsfaktor_horizont(hor_deg, az_deg):
    """ Calculate Verschattungsfaktor for horizontal solar irradiation

    Args:
        hor_deg: Horizon angle [degree]
        az_deg: azimuth direction degree [degree] (0 south, -90 east, 90 west)

    Returns:
        Verschattungsfaktor

    """
    hor = min(hor_deg, 40.0)
    min_hor = floor(hor / 10.0) * 10.0
    max_hor = ceil(hor / 10.0) * 10.0

    if min_hor == max_hor:
        w_min_hor = w_max_hor = 0.5
    else:
        w_min_hor = (hor - min_hor) / 10.0
        w_max_hor = (max_hor - hor) / 10.0

    az1 = floor(az_deg / 90.0) * 90.0
    az2 = ceil(az_deg / 90.0) * 90.0

    if az1 == az2:
        w_az1 = w_az2 = 0.5
    else:
        w_az1 = (az_deg - az1) / 90.0
        w_az2 = (az2 - az_deg) / 90.0

    f1 = (w_min_hor * _verschattungsfaktor_horizont[min_hor][az1]
          + w_max_hor * _verschattungsfaktor_horizont[max_hor][az1])

    f2 = (w_min_hor * _verschattungsfaktor_horizont[min_hor][az2]
          + w_max_hor * _verschattungsfaktor_horizont[max_hor][az2])

    return f1 * w_az1 + f2 * w_az2


def reduktionsfaktor_erdreich_boden(tiefe, A_FG, P_FG, U_FG0):
    """ Calculate Reduktionsfaktoren fuer Waermeverluste von Boden gegen Erdreich

    Args:
        tiefe: Tiefe UK Bodenplatte unter OK Erdreich [m]
        A_FG: Flaeche der thermischen Gebaeudehuelle, die auf dem Erdreich aufliegt (m^2)
        P_FG: Umfang von A FG an der Gebaeudeaussenkante oder gegen unbeheizte Raeume ausserhalb der
        thermischen Gebaeudehuelle. Kanten gegen benachbarte beheizte Raeume werden nicht mitgezaehlt.
        U_FG0: Reduktionsfaktor des Bauteils

    Returns:
    """
    ap = A_FG / P_FG
    APs = [2.0, 5.0, 10.0]
    depths = list(bGFs.keys())
    bgfs_APs_Us = []
    for d in depths:
        bgfs_APs = []
        for i in range(len(APs)):
            us = [0.2, 0.4, 0.6, 1.0]
            bgfs = bGFs[d][i]
            z = np.polyfit(us, bgfs, 2)
            p = np.poly1d(z)
            bGF_AP = p(U_FG0)
            bgfs_APs.append(bGF_AP)
        z = np.polyfit(APs, bgfs_APs, 2)
        p = np.poly1d(z)
        bGF_AP = p(ap)
        bgfs_APs_Us.append(bGF_AP)
    z = np.polyfit(depths, bgfs_APs_Us, 2)
    p = np.poly1d(z)
    bGF = p(tiefe)
    return bGF


# key: tiefe [m], jeweils fuer U_GW0 [0.2,0.4,0.6,1]
ugw0S = OrderedDict()
ugw0S[0.0] = [1.0, 1.0, 1.0, 1.0]
ugw0S[0.5] = [0.92, 0.88, 0.85, 0.8]
ugw0S[1.0] = [0.88, 0.83, 0.78, 0.7]
ugw0S[2.0] = [0.82, 0.73, 0.66, 0.56]
ugw0S[3.0] = [0.77, 0.66, 0.58, 0.48]
ugw0S[5.0] = [0.69, 0.56, 0.47, 0.37]
ugw0S[10.0] = [0.55, 0.41, 0.33, 0.25]


def reduktionsfaktor_erdreich_wand(tiefe, U_GW0):
    """ Reduktionsfaktoren fuer Waermeverluste von Wand gegen Erdreich
    Args:
        tiefe: Tiefe UK Bodenplatte unter OK Erdreich [m]
        U_GW0: Reduktionsfaktor des Bauteils

    Returns:

    """
    depths = bGFs.keys()
    bGW_Us = []
    for d in depths:
        us = [0.2, 0.4, 0.6, 1.0]
        bgws = ugw0S[d]
        z = np.polyfit(us, bgws, 2)
        p = np.poly1d(z)
        bGW_U = p(U_GW0)
        bGW_Us.append(bGW_U)

    z = np.polyfit(list(depths), bGW_Us, 3)
    p = np.poly1d(z)
    bGW = p(tiefe)
    return bGW


class SIAConf:

    def __init__(self):
        # Ferschattungsfaktoren
        self.Fs = []

        # Globalstrahlung Fassaden
        self.Gs = []

        # Flache Fenster
        self.As = []

        # Fenster Uwerte
        self.Us = []

        # Azimuth Fassade
        self.azimuths = []

        self.theta_o_C = None
        # Raumtemperatur C

        # Regelungszuschlag fuer die Raumteperatur K
        self.delta_theta_o_K = None

        # Personenflaeche m^2 / P
        self.A_P = None

        # Waermeabgabe pro Person W / P
        self.Q_P = None

        # Prasenezzeit pro Tag h / d
        self.t_p = None

        # Elektrizitaetsbedarf pro Jahr MJ/m^2
        self.Q_El = None

        # Reduktionsfaktor Elektrizitaet -
        self.f_El = None

        # fleachenbezogener Aussenluft-Volumenstrom m^3 / (h*m^2)
        self.V_A_Es = []

        # Klimadaten
        # Laenge der Berechnungsperiode d
        self.t_c = None

        # Hoehenlage in Meter ueber Meer m
        self.h = None

        # Aussentemperatur C
        self.theta_e = None

        # Globale Sonnenstrahlung horizontal MJ / m^2
        self.G_sH = None

        # Flachen, Laengen, Anzahl

        # Energiebezugsflache m^2
        self.A_E = None

        # Dach gegen Aussenluft m^2
        self.A_Re = None

        # Decke gegen unbeheizte Raeume m^2
        self.A_Ru = None

        # Wand gegen Aussenluft m^2
        self.A_We = None

        # Wand gegen unbeheizte Raueme m^2
        self.A_Wu = None

        # Wand gegen Erdreich m^2
        self.A_WG = None

        # Wand gegen benachbarten beheitzen Raum
        self.A_Wn = None

        # Boden gegen Aussenluft m^2
        self.A_Fe = None

        # Boden gegen unbehizte Raume m^2
        self.A_Fu = None

        # Boden gegen Erdreich mit Bauteilheizung m^2
        self.A_FG = None

        # Fenster horizontal m^2
        self.A_wH = None

        # Waermebruecke Decke/Wand m
        self.l_RW = None

        # Waermebruecke Gebaudesockel m
        self.l_WF = None

        # Waermebruecke Balkon m
        self.l_B = None

        # Waermebruecke Fensteranschlag m
        self.l_w = None

        # Waermebruecke Boden / Keller-Innenwand m
        self.l_F = None

        # Waermebruecke Stuetzen, Traeger, Konsolen
        self.z = None

        # Diverses
        self.U_Re = None
        # Dach gegen Aussenluft W / (m^2 * K)

        self.U_Ru = None
        # Decke gegen unbeheizte Raeume W / (m^2 * K)

        self.b_uR = None
        # Reduktionsfaktor Decke gegen unbeheizte Raeume -

        self.U_We = None
        # Wand gegen Aussenluft W / (m^2 * K)

        self.U_Wu = None
        # Wand gegen unbehizte Raume W / (m^2 * K)

        self.b_uW = None
        # Reduktionsfaktor Wand gegen unbehizte Raume

        self.U_WG0 = None
        # Wand gegen Erdreich W / (m^2 * K)

        self.b_GW = None
        # Reduktionsfaktor Wand gegen Erdreich -

        self.U_Wh = None
        # Wand gegen benachbarten beheizten Raum W / (m^2 * K)

        self.theta_on = None
        # Raumteperatur des benachbarten beheizten Raumes C

        self.U_Fe = None
        # Boden gegen Aussenluft W / (m^2 * K)

        self.U_Fu = None
        # Boden gegen unbeheizte Raeume W / (m^2 * K)

        self.b_uF = None
        # Reduktionsfaktor Boden gegen unbeheizte Raume -

        self.U_FG0 = None
        # Boden gegen Erdreich mit Bauteilheizung W / (m^2 * K)

        self.b_GF = None
        # Reduktionsfaktor Boden gegen Erdreich -

        self.delta_theta = None
        # Temperaturzuschlag Bauzeilheizung K

        self.U_wH = None
        # Fenster horizontal W / (m^2 * K)

        self.U_wS = None
        # Fenster Sued W / (m^2 * K)

        self.psi_RW = None
        # Waermebruecke Decke/Wand W / (m * K)

        self.psi_WG = None
        # Waermebruecke Gebaeudesockel W / (m * K)

        self.psi_B = None
        # Waermebruecke Balkon W / (m * K)

        self.psi_W = None
        # Waermebruecke Fensteranschlag W / (m * K)

        self.psi_F = None
        # Waermebruecke Boden / Keller - Innenwand W / (m * K)

        self.chi = None
        # Waermebruecke Stuetzen, Traeger, Konsolen W/ K

        self.g_90deg = None
        # Gesamtenergiedurchlassgrad Fenster (senkrecht) -

        self.F_F = None
        # Abminderungsfaktor fuer Fensterrahmen -

        self.F_SH = None
        # Verschattungsfaktor horizontal -

        # Spezielle Engabedaten

        self.C_AE = None
        # Waermespeichergaehigkeit pro Energiebezugsflaeche MJ / (m^2 * K)

        self.a_0 = None
        # numerischer Parameter fuer Ausnutzungsgrad -

        self.tau_0 = None

    def add_wall(self, a, F, G, A, U):
        """ Add wall configuration

        Args:
            a: Azimuth angel (needs to be unique!)
            F: Verschattungsfaktor Fassade
            G: Globalstrahlung Fassade fuer Azimuth
            A: Fensterflaeche
            U: U-Wert des Fensters

        """

        assert a not in self.azimuths
        self.azimuths.append(a)

        # Ferschattungsfaktoren
        self.Fs.append(float(F))

        # Globalstrahlung Fassaden
        self.Gs.append(list(map(float, G)))

        # Flache Fenster
        self.As.append(float(A))

        # Fenster Uwerte
        self.Us.append(float(U))

    def check(self):
        assert len(self.theta_e) == len(self.t_c), "Ambient temperature do not equal time intervals"
        assert len(self.G_sH) == len(self.t_c), "Global horizontal radiation do not equal time intervals"
        assert len(self.azimuths) == len(self.As), "Window areas do not equal azimuths"
        assert len(self.azimuths) == len(self.Fs), "Verschattungsfaktoren do not equal azimuths"
        assert len(self.azimuths) == len(self.Gs), "Global radiation do not equal azimuths"
        assert len(self.azimuths) == len(self.Us), "U values do not equal azimuths"
        assert len(self.azimuths) == len(set(self.azimuths)), "Azimuth ids not unique"
        for a in range(len(self.azimuths)):
            assert len(self.Gs[a]) == len(self.t_c), "Global radiation do not equal time intervals"


def sia380_py(config):
    config.check()

    sec_day = 86400.0

    res = []
    for i in range(len(config.t_c)):

        # Nutzung
        E1 = config.theta_o_C

        # Raumtemperatur C
        E2 = config.delta_theta_o_K
        # Regelungszuschlag fuer die Raumteperatur K

        E3 = config.A_P
        # Personenflaeche m^2 / P

        E4 = config.Q_P
        # Waermeabgabe pro Person W / P

        E5 = config.t_p
        # Prasenezzeit pro Tag h / d

        E6 = config.Q_El
        # Elektrizitaetsbedarf pro Jahr MJ/m^2

        E7 = config.f_El
        # Reduktionsfaktor Elektrizitaet -

        E8 = config.V_A_Es[i]
        # fleachenbezogener Aussenluft-Volumenstrom m^3 / (h*m^2)

        # Klimadaten

        E9 = config.t_c[i]
        # Laenge der Berechnungsperiode d

        E10 = config.h
        # Hoehenlage in Meter ueber Meer m

        E11 = config.theta_e[i]
        # Aussentemperatur C

        E12 = config.G_sH[i]
        # Globale Sonnenstrahlung horizontal MJ / m^2

        # Flachen, Laengen, Anzahl

        E17 = config.A_E
        # Energiebezugsflache m^2

        E18 = config.A_Re
        # Dach gegen Aussenluft m^2

        E19 = config.A_Ru
        # Decke gegen unbeheizte Raeume m^2

        E20 = config.A_We
        # Wand gegen Aussenluft m^2

        E21 = config.A_Wu
        # Wand gegen unbeheizte Raueme m^2

        E22 = config.A_WG
        # Wand gegen Erdreich m^2

        # Wand gegen benachbarten beheitzen Raum
        E23 = config.A_Wn

        E24 = config.A_Fe
        # Boden gegen Aussenluft m^2

        E25 = config.A_Fu
        # Boden gegen unbehizte Raume m^2

        E26 = config.A_FG
        # Boden gegen Erdreich mit Bauteilheizung m^2

        E27 = config.A_wH
        # Fenster horizontal m^2

        E32 = config.l_RW
        # Waermebruecke Decke/Wand m

        E33 = config.l_WF
        # Waermebruecke Gebaudesockel m

        E34 = config.l_B
        # Waermebruecke Balkon m

        E35 = config.l_w
        # Waermebruecke Fensteranschlag m

        E36 = config.l_F
        # Waermebruecke Boden / Keller-Innenwand m

        E37 = config.z
        # Waermebruecke Stuetzen, Traeger, Konsolen

        # Diverses
        E38 = config.U_Re
        # Dach gegen Aussenluft W / (m^2 * K)

        E39 = config.U_Ru
        # Decke gegen unbeheizte Raeume W / (m^2 * K)

        E40 = config.b_uR
        # Reduktionsfaktor Decke gegen unbeheizte Raeume -

        E41 = config.U_We
        # Wand gegen Aussenluft W / (m^2 * K)

        E42 = config.U_Wu
        # Wand gegen unbehizte Raume W / (m^2 * K)

        E43 = config.b_uW
        # Reduktionsfaktor Wand gegen unbehizte Raume

        E44 = config.U_WG0
        # Wand gegen Erdreich W / (m^2 * K)

        E45 = config.b_GW
        # Reduktionsfaktor Wand gegen Erdreich -

        E46 = config.U_Wh
        # Wand gegen benachbarten beheizten Raum W / (m^2 * K)

        E47 = config.theta_on
        # Raumteperatur des benachbarten beheizten Raumes C

        E48 = config.U_Fe
        # Boden gegen Aussenluft W / (m^2 * K)

        E49 = config.U_Fu
        # Boden gegen unbeheizte Raeume W / (m^2 * K)

        E50 = config.b_uF
        # Reduktionsfaktor Boden gegen unbeheizte Raume -

        E51 = config.U_FG0
        # Boden gegen Erdreich mit Bauteilheizung W / (m^2 * K)

        E52 = config.b_GF
        # Reduktionsfaktor Boden gegen Erdreich -

        E53 = config.delta_theta
        # Temperaturzuschlag Bauzeilheizung K

        E54 = config.U_wH
        # Fenster horizontal W / (m^2 * K)

        E59 = config.psi_RW
        # Waermebruecke Decke/Wand W / (m * K)

        E60 = config.psi_WG
        # Waermebruecke Gebaeudesockel W / (m * K)

        E61 = config.psi_B
        # Waermebruecke Balkon W / (m * K)

        E62 = config.psi_W
        # Waermebruecke Fensteranschlag W / (m * K)

        E63 = config.psi_F
        # Waermebruecke Boden / Keller - Innenwand W / (m * K)

        E64 = config.chi
        # Waermebruecke Stuetzen, Traeger, Konsolen W/ K

        E65 = config.g_90deg
        # Gesamtenergiedurchlassgrad Fenster (senkrecht) -

        E66 = config.F_F
        # Abminderungsfaktor fuer Fensterrahmen -

        azimuths = config.azimuths
        Fs = config.Fs
        Gs = config.Gs
        As = config.As
        Us = config.Us

        # Verschattungsfaktor horizontal -
        E67 = config.F_SH

        # Spezielle Engabedaten
        E72 = config.C_AE

        # Waermespeichergaehigkeit pro Energiebezugsflaeche MJ / (m^2 * K)

        E73 = config.a_0
        # numerischer Parameter fuer Ausnutzungsgrad -

        E74 = config.tau_0

        # Referenzteitkonstante fuer Ausnutzungsgrad h

        # Datenblatt Resutate
        E75 = theta_OC = E1 + E2
        # Raumtemperatur mit Regelungszuschlag C

        E76 = Q_Re = (E75 - E11) * E9 * E18 * E38 * sec_day / (E17 * 10.0 ** 6)
        # Dach gegen Aussenluft

        E77 = Q_Ru = (E75 - E11) * E9 * E19 * E39 * \
                     E40 * sec_day / (E17 * 10.0 ** 6)
        # Decke gegen unbeheizte Raeume

        E78 = Q_We = (E75 - E11) * E9 * E20 * E41 * sec_day / (E17 * 10.0 ** 6)
        # Wand gegen Aussenluft

        E79 = Q_Wu = (E75 - E11) * E9 * E21 * E42 * \
                     E43 * sec_day / (E17 * 10.0 ** 6)
        # Wand gegen unbeheizte Raeume

        E80 = Q_WG = (E75 - E11) * E9 * E22 * E44 * \
                     E45 * sec_day / (E17 * 10.0 ** 6)
        # Wand gegen Erdreich

        E81 = Q_Wn = (E75 - E47) * E9 * E23 * E46 * sec_day / (E17 * 10.0 ** 6)
        # Wand gegen benachbarten Raum

        E82 = Q_Fe = (E75 - E11) * E9 * E24 * E48 * sec_day / (E17 * 10.0 ** 6)
        # Boden gegen Aussenluft

        E83 = Q_Fu = (E75 - E11) * E9 * E25 * E49 * \
                     E50 * sec_day / (E17 * 10.0 ** 6)
        # Boden gegen unbeheizte Raeume

        E84 = Q_FG = (E75 - E11 + E53) * E9 * E26 * E51 * \
                     E52 * sec_day / (E17 * 10.0 ** 6)
        # Boden gegen Erdreich mit Bauteilheizung

        Q_wH = (E75 - E11) * E9 * E27 * E54 * sec_day / (E17 * 10.0 ** 6)
        # Fenster horizontal

        QwS = {}
        for az in range(len(azimuths)):
            QwS[azimuths[az]] = (E75 - E11) * E9 * As[az] * Us[az] * sec_day / (E17 * 10.0 ** 6)

        QwTot = Q_wH + sum(QwS.values())

        E90 = Q_IRW = (E75 - E11) * E9 * E32 * E59 * \
                      sec_day / (E17 * 10.0 ** 6)
        # Waermebruecke Decke / Wand

        E91 = Q_IWF = (E75 - E11) * E9 * E33 * E60 * \
                      sec_day / (E17 * 10.0 ** 6)
        # Waermebruecke Gebaeudesockel

        E92 = Q_IB = (E75 - E11) * E9 * E34 * E61 * sec_day / (E17 * 10.0 ** 6)
        # Waermebruecke Balkon

        E93 = Q_IW = (E75 - E11) * E9 * E35 * E62 * sec_day / (E17 * 10.0 ** 6)
        # Waermebruecke Fensteranschlag

        E94 = Q_IF = (E75 - E11) * E9 * E36 * E50 * \
                     E63 * sec_day / (E17 * 10.0 ** 6)
        # Waermebruecke Boden / Keller-Innenwand

        E95 = Q_P = (E75 - E11) * E9 * E37 * E64 * sec_day / (E17 * 10.0 ** 6)
        # Waermebrueche Stuetzen, Traeger, Konsolen

        Q_WB = Q_IB + Q_IW + Q_IF + Q_IRW + Q_P
        # Total Waermebruecken

        E96 = Q_T = E76 + E77 + E78 + E79 + E80 + E81 + E82 + E83 + E84 + QwTot + E90 + E91 + E92 + E93 + E94 + E95
        # Transmissionswaermeverluste

        # Lueftungswaermeverlust

        E97 = p_a_C_a = 1220.0 - 0.14 * E10
        # spez. Waermespeciherfaehigkeit Luft

        E98 = Q_V = (E75 - E11) * E8 * E9 * E97 * 24.0 / 10.0 ** 6
        # Lueftungswaermeverlust

        if Q_T + Q_V < 0:
            E96 = Q_T = 0.0
            E98 = Q_V = 0.0

        # Aussenluftvolumenstrom 22-36m^3 pro Person
        # http://www.raumlufthygiene.ch/download/LIWOTEV-Schlussbericht.pdf

        # Gesamtwaermeverlust
        E99 = Q_ot = E96 + E98

        # spezifischer Waermetransferkoeffizient
        E100 = H = E18 * E38 + \
                   E19 * E39 * E40 + \
                   E20 * E41 + \
                   E21 * E42 * E43 + \
                   E22 * E44 * E45 + \
                   E24 * E48 + \
                   E25 * E49 * E50 + \
                   E26 * E51 * E52 + \
                   E27 * E54 + \
                   (sum([As[az] * Us[az] for az in range(len(azimuths))])) + \
                   E32 * E59 + \
                   E33 * E60 + \
                   E34 * E61 + \
                   E35 * E62 + \
                   E36 * E63 + \
                   E37 * E64 + \
                   E8 * E17 * E97 / 3600.0

        # Waermegewinne
        # Waermegewinne Elektrizitaet
        E101 = Q_iEl = E6 * E7 * E9 / 365.0

        # Waermegewinne Personen
        E102 = Q_iP = E4 * E5 * E9 * 3600.0 / (E3 * 10.0 ** 6)

        # Interne Waermegewinne
        E103 = Q_i = E101 + E102

        # solarer Waermegewinn horizontal
        E104 = Q_sH = E12 * E27 * 0.9 * E65 * E66 * E67 / E17

        Qs = {}
        for az in range(len(azimuths)):
            Qs[azimuths[az]] = Gs[az][i] * As[az] * 0.9 * E65 * E66 * Fs[az] / E17

        # solarer Waermegewinn total
        E109 = Q_s = sum(Qs.values()) + Q_sH

        # Waermegewinne total
        E110 = Q_g = E103 + E109

        # Waermegewinn/ verlust / verhaeltnis
        if E99 == 0.0:
            E111 = gamma = 1.0
        else:
            E111 = gamma = E110 / E99

        # Zeitkonstante
        E112 = tau = E72 * E17 * 10.0 ** 6 / (E100 * 3600.0)

        # Parameter fuer Ausnutzungsgrad
        E113 = a = E73 + E112 / E74

        # Ausnutzungsgrad fuer Waermegewinne
        if E111 == 1.0:
            E114 = phi_g = E113 / (E113 + 1.0)
        elif E99 <= 0.0:
            E114 = phi_g = 0.0
        else:
            E114 = phi_g = (1.0 - E111 ** E113) / (1.0 - E111 ** (E113 + 1.0))

        # genutzte Waermegewinne
        E115 = Q_ug = E110 * E114

        # Deckungsgrad durch Waermegewinne
        if E99 == 0.0:
            E116 = f_ug = 1.0
        else:
            E116 = f_ug = E115 / E99

        # Heizwaermebedarf
        E117 = Q_h = E99 - E115

        cur_res = {'i': i,
                   'Q_h': Q_h,
                   'f_ug': f_ug,
                   'Q_ug': Q_ug,
                   'Q_T': Q_T,
                   'Q_V': Q_V,
                   'Q_ot': Q_ot,
                   'Q_s': Q_s,
                   'Q_i': Q_i,
                   'Q_g': Q_g,
                   'Q_iEl': Q_iEl,
                   'Q_iP': Q_iP,
                   'a': a,
                   'H': H,
                   'Q_Re': Q_Re,
                   'Q_Ru': Q_Ru,
                   'Q_RTOT': Q_Ru + Q_Re,
                   'Q_We': Q_We,
                   'Q_Wu': Q_Wu,
                   'Q_WG': Q_WG,
                   'Q_Wn': Q_Wn,
                   'QwS': QwS,
                   'Q_WTOT': Q_Wn + Q_WG + Q_Wu + Q_We,
                   'Q_Fe': Q_Fe,
                   'Q_Fu': Q_Fu,
                   'Q_FG': Q_FG,
                   'Q_FTOT': Q_Fe + Q_Fu + Q_FG,
                   'Q_wH': Q_wH,
                   'Q_wTOT': QwTot,
                   'Q_IRW': Q_IRW,
                   'Q_IWF': Q_IWF,
                   'Q_IB': Q_IB,
                   'Q_IW': Q_IW,
                   'Q_IF': Q_IF,
                   'Q_sH': Q_sH,
                   'Qs': Qs,
                   'gamma': gamma,
                   'tau': tau,
                   'a': a,
                   'phi_g': phi_g,
                   'Q_WB': Q_WB,
                   'Q_nug': Q_g - Q_ug
                   }

        res.append(cur_res)

    return res


def sia380(config):
    try:
        from pyheat.sia380cy import sia380_cy
        return sia380_cy(config)
    except:
        return sia380_py(config)
