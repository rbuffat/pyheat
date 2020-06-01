import cython

@cython.cdivision(True)
def sia380_cy(config):
    cdef int i
    cdef double sec_day
    cdef double E1
    cdef double E2
    cdef double E3
    cdef double E4
    cdef double E5
    cdef double E6
    cdef double E7
    cdef double E8
    cdef double E9
    cdef double E10
    cdef double E11
    cdef double E12
    cdef double E17
    cdef double E18
    cdef double E19
    cdef double E20
    cdef double E21
    cdef double E22
    cdef double E23
    cdef double E24
    cdef double E25
    cdef double E26
    cdef double E27
    cdef double E32
    cdef double E33
    cdef double E34
    cdef double E35
    cdef double E36
    cdef double E37
    cdef double E38
    cdef double E39
    cdef double E40
    cdef double E41
    cdef double E42
    cdef double E43
    cdef double E44
    cdef double E45
    cdef double E46
    cdef double E47
    cdef double E48
    cdef double E49
    cdef double E50
    cdef double E51
    cdef double E52
    cdef double E53
    cdef double E54
    cdef double E59
    cdef double E60
    cdef double E61
    cdef double E62
    cdef double E63
    cdef double E64
    cdef double E65
    cdef double E66
    cdef double E67
    cdef double E72
    cdef double E73
    cdef double E74
    cdef double E75
    cdef double E76
    cdef double E77
    cdef double E78
    cdef double E79
    cdef double E80
    cdef double E81
    cdef double E82
    cdef double E83
    cdef double E84
    cdef double E85
    cdef double E86
    cdef double E87
    cdef double E88
    cdef double E89
    cdef double E90
    cdef double E91
    cdef double E92
    cdef double E93
    cdef double E94
    cdef double E95
    cdef double E96
    cdef double E97
    cdef double E98
    cdef double E99
    cdef double E100
    cdef double E101
    cdef double E102
    cdef double E103
    cdef double E104
    cdef double E105
    cdef double E106
    cdef double E107
    cdef double E108
    cdef double E109
    cdef double E110
    cdef double E111
    cdef double E112
    cdef double E113
    cdef double E114
    cdef double E115
    cdef double Q_h
    cdef double f_ug
    cdef double Q_ug
    cdef double Q_T
    cdef double Q_V
    cdef double Q_ot
    cdef double Q_s
    cdef double Q_i
    cdef double Q_g
    cdef double Q_iEl
    cdef double Q_iP
    cdef double a
    cdef double H
    cdef double Q_Re
    cdef double Q_Ru
    cdef double Q_We
    cdef double Q_Wu
    cdef double Q_WG
    cdef double Q_Wn
    cdef double Q_Fe
    cdef double Q_Fu
    cdef double Q_FG
    cdef double Q_wH
    cdef double Q_IRW
    cdef double Q_IWF
    cdef double Q_IB
    cdef double Q_IW
    cdef double Q_IF
    cdef double Q_sH
    cdef double gamma
    cdef double tau
    cdef double phi_g
    cdef double Q_WB
    cdef double QwTot

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
