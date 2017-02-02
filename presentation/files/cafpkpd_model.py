# -*- coding=utf-8 -*-
"""
PKPD model for caffeine clearance.

Free parameters for parameter optimization:
    Ka_caf : caffeine absorption
    HLM_CLint_caf : hepatic clearance caffeine
    fcl_px_caf : hepatic clearance paraxanthine (relative to caffeine)
"""
from libsbml import UNIT_KIND_METRE, UNIT_KIND_SECOND, UNIT_KIND_LITRE, UNIT_KIND_GRAM
from libsbml import XMLNode
from sbmlutils.modelcreator import templates
import sbmlutils.factory as mc

##############################################################
mid = 'caffeine_pkpd'
version = 8
notes = XMLNode.convertStringToXMLNode("""
    <body xmlns='http://www.w3.org/1999/xhtml'>
    <h1>PKPD model for clearance of caffeine</h1>
    <h2>Description</h2>
    <p>
        This model is a physiologically based pharmacokinetic model (PKPD) encoded in <a href="http://sbml.org">SBML</a> format
        for the clearance of caffeine by the human body.
    </p>
    """ + templates.terms_of_use + """
    </body>
    """)

creators = templates.creators
main_units = {
    'time': 'h',
    'extent': 'mg',
    'substance': 'mg',
    'length': 'm',
    'area': 'm2',
    'volume': UNIT_KIND_LITRE,
}

#########################################################################
# Units
##########################################################################
# units (kind, exponent, scale=0, multiplier=1.0)
units = [
    mc.Unit('h', [(UNIT_KIND_SECOND, 1.0, 0, 3600)]),
    mc.Unit('kg', [(UNIT_KIND_GRAM, 1.0, 3, 1.0)]),
    mc.Unit('m', [(UNIT_KIND_METRE, 1.0)]),
    mc.Unit('m2', [(UNIT_KIND_METRE, 2.0)]),
    mc.Unit('per_h', [(UNIT_KIND_SECOND, -1.0, 0, 3600)]),

    mc.Unit('mg', [(UNIT_KIND_GRAM, 1.0, -3, 1.0)]),
    mc.Unit('mg_per_litre', [(UNIT_KIND_GRAM, 1.0, -3, 1.0),
                   (UNIT_KIND_LITRE, -1.0, 0, 1.0)]),
    mc.Unit('mg_per_g', [(UNIT_KIND_GRAM, 1.0, -3, 1.0),
                     (UNIT_KIND_GRAM, -1.0, 0, 1.0)]),
    mc.Unit('mg_per_h', [(UNIT_KIND_GRAM, 1.0, -3, 1.0),
                 (UNIT_KIND_SECOND, -1.0, 0, 3600)]),
    mc.Unit('litre_per_h', [(UNIT_KIND_LITRE, 1.0, 0, 1.0),
                     (UNIT_KIND_SECOND, -1.0, 0, 3600)]),
    mc.Unit('litre_per_kg', [(UNIT_KIND_LITRE, 1.0, 0, 1.0),
                     (UNIT_KIND_GRAM, -1.0, 3, 1.0)]),
    mc.Unit('mulitre_per_min_mg', [(UNIT_KIND_LITRE, 1.0, -6, 1.0),
                           (UNIT_KIND_SECOND, -1.0, 0, 60), (UNIT_KIND_GRAM, -1.0, -3, 1.0)]),

    mc.Unit('ml_per_s', [(UNIT_KIND_LITRE, 1.0, -3, 1.0),
                         (UNIT_KIND_SECOND, -1.0, 0, 1)]),

    mc.Unit('s_per_h', [(UNIT_KIND_SECOND, 1.0, 0, 1.0),
                (UNIT_KIND_SECOND, -1.0, 0, 3600)]),
    mc.Unit('min_per_h', [(UNIT_KIND_SECOND, 1.0, 0, 60),
                  (UNIT_KIND_SECOND, -1.0, 0, 3600)]),

    mc.Unit('ml_per_litre', [(UNIT_KIND_LITRE, 1.0, -3, 1.0),
                     (UNIT_KIND_LITRE, -1.0, 0, 1)]),
    mc.Unit('mulitre_per_g', [(UNIT_KIND_LITRE, 1.0, -6, 1.0),
                      (UNIT_KIND_GRAM, -1.0, 0, 1)]),
]

##############################################################
# Compartments
##############################################################
compartments = [
    mc.Compartment('Vre', value=1, unit=UNIT_KIND_LITRE, constant=False, name='rest of body'),

    mc.Compartment('Vgu', value=1, unit=UNIT_KIND_LITRE, constant=False, name='gut'),
    mc.Compartment('Vki', value=1, unit=UNIT_KIND_LITRE, constant=False, name='kidney'),
    mc.Compartment('Vli', value=1, unit=UNIT_KIND_LITRE, constant=False, name='liver'),
    mc.Compartment('Vlu', value=1, unit=UNIT_KIND_LITRE, constant=False, name='lung'),
    mc.Compartment('Vsp', value=1, unit=UNIT_KIND_LITRE, constant=False, name='spleen'),

    mc.Compartment('Vve', value=1, unit=UNIT_KIND_LITRE, constant=False, name='venous blood'),
    mc.Compartment('Var', value=1, unit=UNIT_KIND_LITRE, constant=False, name='arterial blood'),
    mc.Compartment('Vpl', value=1, unit=UNIT_KIND_LITRE, constant=False, name='plasma'),
    mc.Compartment('Vplas_ven', value=1, unit=UNIT_KIND_LITRE, constant=False, name='venous plasma'),
    mc.Compartment('Vplas_art', value=1, unit=UNIT_KIND_LITRE, constant=False, name='arterial plasma'),
]

##############################################################
# Parameters
##############################################################
parameters = [
    # whole body data
    mc.Parameter('BW', 70, 'kg', constant=True, name='body weight'),
    mc.Parameter('CO', 108.33, 'ml_per_s', constant=True, name='cardiac output [ml/s]'),
    mc.Parameter('QC', 108.33*1000*60*60, 'litre_per_h', constant=False, name='cardiac output [L/hr]'),

    # fractional tissue volumes
    mc.Parameter('FVre', 0.9049, 'litre_per_kg', constant=True, name='rest of body fractional tissue volume'),
    mc.Parameter('FVgu', 0.0171, 'litre_per_kg', constant=True, name='gut fractional tissue volume'),
    mc.Parameter('FVki', 0.0044, 'litre_per_kg', constant=True, name='kidney fractional tissue volume'),
    mc.Parameter('FVli', 0.021, 'litre_per_kg', constant=True, name='liver fractional tissue volume'),
    mc.Parameter('FVlu', 0.0076, 'litre_per_kg', constant=True, name='lung fractional tissue volume'),
    mc.Parameter('FVsp', 0.0026, 'litre_per_kg', constant=True, name='spleen fractional tissue volume'),
    mc.Parameter('FVve', 0.0514, 'litre_per_kg', constant=True, name='venous fractional tissue volume'),
    mc.Parameter('FVar', 0.0257, 'litre_per_kg', constant=True, name='arterial fractional tissue volume'),
    mc.Parameter('FVpl', 0.0424, 'litre_per_kg', constant=True, name='plasma fractional tissue volume'),

    # fractional tissue blood flows
    mc.Parameter('FQgu', 0.146462, '-', constant=True, name='gut fractional tissue blood flow'),
    mc.Parameter('FQki', 0.19, '-', constant=True, name='kidney fractional tissue blood flow'),
    mc.Parameter('FQh', 0.215385, '-', constant=True, name='hepatic (venous side) fractional tissue blood flow'),
    mc.Parameter('FQlu', 1, '-', constant=True, name='lung fractional tissue blood flow'),
    mc.Parameter('FQsp', 0.017231, '-', constant=True, name='spleen fractional tissue blood flow'),
    mc.Parameter('FQre', 0.594615, '-', constant=True, name='rest of body fractional tissue blood flow'),

    # liver data
    mc.Parameter('MPPGL', 45, 'mg_per_g', constant=True, name='mg microsomal protein per g liver'),

    # <Substance specific data>
    # tissue to plasma partition coefficients
    mc.Parameter('Kpgu_caf', 1, '-', constant=True, name='gut plasma partition coefficient caffeine'),
    mc.Parameter('Kpki_caf', 1, '-', constant=True, name='kidney plasma partition coefficient caffeine'),
    mc.Parameter('Kpli_caf', 1, '-', constant=True, name='liver plasma partition coefficient caffeine'),
    mc.Parameter('Kplu_caf', 1, '-', constant=True, name='lung plasma partition coefficient caffeine'),
    mc.Parameter('Kpsp_caf', 1, '-', constant=True, name='spleen plasma partition coefficient caffeine'),
    mc.Parameter('Kpre_caf', 0.5, '-', constant=True, name='rest plasma partition coefficient caffeine'),

    mc.Parameter('Kpgu_px', 1, '-', constant=True, name='gut plasma partition coefficient paraxanthine'),
    mc.Parameter('Kpki_px', 1, '-', constant=True, name='kidney plasma partition coefficient paraxanthine'),
    mc.Parameter('Kpli_px', 1, '-', constant=True, name='liver plasma partition coefficient paraxanthine'),
    mc.Parameter('Kplu_px', 1, '-', constant=True, name='lung plasma partition coefficient paraxanthine'),
    mc.Parameter('Kpsp_px', 1, '-', constant=True, name='spleen plasma partition coefficient paraxanthine'),
    mc.Parameter('Kpre_px', 0.5, '-', constant=True, name='rest plasma partition coefficient paraxanthine'),

    # amounts
    mc.Parameter('Agu_caf', 0, 'mg', name="A [mg] amount gut caffeine", constant=False),
    mc.Parameter('Aki_caf', 0, 'mg', name="A [mg] amount kidney caffeine", constant=False),
    mc.Parameter('Ali_caf', 0, 'mg', name="A [mg] amount liver caffeine", constant=False),
    mc.Parameter('Alu_caf', 0, 'mg', name="A [mg] amount lung caffeine", constant=False),
    mc.Parameter('Asp_caf', 0, 'mg', name="A [mg] amount spleen caffeine", constant=False),
    mc.Parameter('Are_caf', 0, 'mg', name="A [mg] amount rest caffeine", constant=False),
    mc.Parameter('Aar_caf', 0, 'mg', name="A [mg] amount arterial blood caffeine", constant=False),

    mc.Parameter('Agu_px', 0, 'mg', name="A [mg] amount gut paraxanthine", constant=False),
    mc.Parameter('Aki_px', 0, 'mg', name="A [mg] amount kidney paraxanthine", constant=False),
    mc.Parameter('Ali_px', 0, 'mg', name="A [mg] amount liver paraxanthine", constant=False),
    mc.Parameter('Alu_px', 0, 'mg', name="A [mg] amount lung paraxanthine", constant=False),
    mc.Parameter('Asp_px', 0, 'mg', name="A [mg] amount spleen paraxanthine", constant=False),
    mc.Parameter('Are_px', 0, 'mg', name="A [mg] amount rest paraxanthine", constant=False),
    mc.Parameter('Aar_px', 0, 'mg', name="A [mg] amount arterial blood paraxanthine", constant=False),

    # dosing
    mc.Parameter('Ave_caf', 0, 'mg', constant=False, name="A [mg] amount venous blood caffeine", ),
    mc.Parameter('D_caf', 0, 'mg', constant=False, name='oral dose caffeine [mg]'),
    mc.Parameter('DCL_caf', 0, 'mg', constant=False),
    mc.Parameter('IVDOSE_caf', 0, 'mg', constant=True, name='IV bolus dose caffeine [mg]'),
    mc.Parameter('PODOSE_caf', 100, 'mg', constant=True, name='oral bolus dose caffeine [mg]'),

    mc.Parameter('Ave_px', 0, 'mg', constant=False, name="A [mg] amount venous blood paraxanthine", ),
    mc.Parameter('D_px', 0, 'mg', constant=False, name='oral dose paraxanthine [mg]'),
    mc.Parameter('DCL_px', 0, 'mg', constant=False),
    mc.Parameter('IVDOSE_px', 0, 'mg', constant=True, name='IV bolus dose paraxanthine [mg]'),
    mc.Parameter('PODOSE_px', 0, 'mg', constant=True, name='oral bolus dose paraxanthine [mg]'),

    # absorption
    mc.Parameter('Ka_caf', 2.5, 'per_h', constant=True, name='Ka [1/hr] absorption caffeine'),
    mc.Parameter('F_caf', 1, '-', constant=True, name='fraction absorbed caffeine'),
    mc.Parameter('Ka_px', 2.5, 'per_h', constant=True, name='Ka [1/hr] absorption paraxanthine'),
    mc.Parameter('F_px', 1, '-', constant=True, name='fraction absorbed paraxanthine'),

    # in vitro binding data
    mc.Parameter('fup_caf', 1, '-', constant=True, name='fraction unbound in plasma caffeine'),
    mc.Parameter('BP_caf', 1, '-', constant=True, name='blood to plasma ratio caffeine'),
    mc.Parameter('fumic_caf', 1, '-', constant=True, name='fraction unbound in microsomes caffeine'),

    mc.Parameter('fup_px', 1, '-', constant=True, name='fraction unbound in plasma paraxanthine'),
    mc.Parameter('BP_px', 1, '-', constant=True, name='blood to plasma ratio paraxanthine'),
    mc.Parameter('fumic_px', 1, '-', constant=True, name='fraction unbound in microsomes paraxanthine'),

    # clearances
    mc.Parameter('HLM_CLint_caf', 2.0, 'mulitre_per_min_mg', constant=True,
                 name='HLM apparent clearance caffeine by hepatic microsomes [mul/min/mg]'),
    mc.Parameter('fcl_px_caf', 1.5, '-', constant=True,
                 name='relative clearance of px to caf'),
    mc.Parameter('HLM_CLint_px', 3.0, 'mulitre_per_min_mg', constant=True,
                 name='HLM apparent clearance paraxanthine by hepatic microsomes [mul/min/mg]'),

    # renal clearances in the range of 1-2 % (in simplified model set to 0)
    mc.Parameter('CLrenal_caf', 0, 'litre_per_h', constant=True, name='renal clearance [L/hr] caffeine'),
    mc.Parameter('CLrenal_px', 0, 'litre_per_h', constant=True, name='renal clearance [L/hr] paraxanthine'),
]


##############################################################
# Assignments
##############################################################
assignments = [
    mc.InitialAssignment('Ave_caf', 'IVDOSE_caf', 'mg'),
    mc.InitialAssignment('D_caf', 'PODOSE_caf', 'mg'),

    mc.InitialAssignment('Ave_px', 'IVDOSE_px', 'mg'),
    mc.InitialAssignment('D_px', 'PODOSE_px', 'mg'),
]

##############################################################
# Rules
##############################################################
rules = [
    # absorption px identical to caf
    mc.AssignmentRule('Ka_px', 'Ka_caf', 'per_h'),

    # clearance of px relative to caf (both via Cyp1a2)
    mc.AssignmentRule('HLM_CLint_px', 'fcl_px_caf*HLM_CLint_caf', 'mulitre_per_min_mg'),


    # volumes
    mc.AssignmentRule('Vgu', 'BW*FVgu', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vki', 'BW*FVki', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vli', 'BW*FVli', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vlu', 'BW*FVlu', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vsp', 'BW*FVsp', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vve', 'BW*FVve', UNIT_KIND_LITRE),
    mc.AssignmentRule('Var', 'BW*FVar', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vpl', 'BW*FVpl', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vre', 'BW*FVre', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vplas_ven', 'Vpl*Vve/(Vve + Var)', UNIT_KIND_LITRE),
    mc.AssignmentRule('Vplas_art', 'Vpl*Var/(Vve + Var)', UNIT_KIND_LITRE),

    # blood flows
    mc.AssignmentRule('QC', 'CO/1000 ml_per_litre * 3600 s_per_h', 'litre_per_h'),
    mc.AssignmentRule('Qgu', 'QC*FQgu', 'litre_per_h', name='gut blood flow'),
    mc.AssignmentRule('Qki', 'QC*FQki', 'litre_per_h', name='kidney blood flow'),
    mc.AssignmentRule('Qh', 'QC*FQh', 'litre_per_h', name='hepatic (venous side) blood flow'),
    mc.AssignmentRule('Qha', 'Qh - Qgu - Qsp', 'litre_per_h', name='hepatic artery blood flow'),
    mc.AssignmentRule('Qlu', 'QC*FQlu', 'litre_per_h', name='lung blood flow'),
    mc.AssignmentRule('Qsp', 'QC*FQsp', 'litre_per_h', name='spleen blood flow'),
    mc.AssignmentRule('Qre', 'QC*FQre', 'litre_per_h', name='rest of body blood flow'),

    # concentrations
    mc.AssignmentRule('Cgu_caf', 'Agu_caf/Vgu', 'mg_per_litre', name='C caffeine [mg/l] gut'),
    mc.AssignmentRule('Cki_caf', 'Aki_caf/Vki', 'mg_per_litre', name='C caffeine [mg/l] kidney'),
    mc.AssignmentRule('Cli_caf', 'Ali_caf/Vli', 'mg_per_litre', name='C caffeine [mg/l] liver'),
    mc.AssignmentRule('Clu_caf', 'Alu_caf/Vlu', 'mg_per_litre', name='C caffeine [mg/l] lung'),
    mc.AssignmentRule('Csp_caf', 'Asp_caf/Vsp', 'mg_per_litre', name='C caffeine [mg/l] spleen'),
    mc.AssignmentRule('Cre_caf', 'Are_caf/Vre', 'mg_per_litre', name='C caffeine [mg/l] rest of body'),
    mc.AssignmentRule('Cve_caf', 'Ave_caf/Vve', 'mg_per_litre', name='C caffeine [mg/l] venous blood'),
    mc.AssignmentRule('Car_caf', 'Aar_caf/Var', 'mg_per_litre', name='C caffeine [mg/l] arterial blood'),

    mc.AssignmentRule('Cgu_px', 'Agu_px/Vgu', 'mg_per_litre', name='C paraxanthine [mg/l] gut'),
    mc.AssignmentRule('Cki_px', 'Aki_px/Vki', 'mg_per_litre', name='C paraxanthine [mg/l] kidney'),
    mc.AssignmentRule('Cli_px', 'Ali_px/Vli', 'mg_per_litre', name='C paraxanthine [mg/l] liver'),
    mc.AssignmentRule('Clu_px', 'Alu_px/Vlu', 'mg_per_litre', name='C paraxanthine [mg/l] lung'),
    mc.AssignmentRule('Csp_px', 'Asp_px/Vsp', 'mg_per_litre', name='C paraxanthine [mg/l] spleen'),
    mc.AssignmentRule('Cre_px', 'Are_px/Vre', 'mg_per_litre', name='C paraxanthine [mg/l] rest of body'),
    mc.AssignmentRule('Cve_px', 'Ave_px/Vve', 'mg_per_litre', name='C paraxanthine [mg/l] venous blood'),
    mc.AssignmentRule('Car_px', 'Aar_px/Var', 'mg_per_litre', name='C paraxanthine [mg/l] arterial blood'),


    # free concentrations & clearance
    mc.AssignmentRule('Cpl_ve_caf', 'Cve_caf/BP_caf', 'mg_per_litre', name='venous plasma concentration caffeine'),
    mc.AssignmentRule('Cli_free_caf', 'Cli_caf*fup_caf', 'mg_per_litre', name='free liver concentration caffeine'),
    mc.AssignmentRule('Cki_free_caf', 'Cki_caf*fup_caf', 'mg_per_litre', name='free kidney concentration caffeine'),

    mc.AssignmentRule('CLliv_caf', '(HLM_CLint_caf/fumic_caf) * MPPGL * Vli * 60 min_per_h / 1000 mulitre_per_g', 'litre_per_h',
                      name='liver clearance caffeine [l/hr]'),
    mc.AssignmentRule('vliv_caf', 'Cli_free_caf*CLliv_caf', 'mg_per_h',
                      name='rate of caffeine change [l/hr]'),

    mc.AssignmentRule('Cpl_ve_px', 'Cve_px/BP_px', 'mg_per_litre', name='venous plasma concentration paraxanthine'),
    mc.AssignmentRule('Cli_free_px', 'Cli_px*fup_px', 'mg_per_litre', name='free liver concentration paraxanthine'),
    mc.AssignmentRule('Cki_free_px', 'Cki_px*fup_px', 'mg_per_litre', name='free kidney concentration paraxanthine'),

    mc.AssignmentRule('CLliv_px', '(HLM_CLint_px/fumic_px) * MPPGL * Vli * 60 min_per_h / 1000 mulitre_per_g', 'litre_per_h',
                      name='liver clearance paraxanthine [l/hr]'),

    mc.AssignmentRule('vliv_px', 'Cli_free_px*CLliv_px', 'mg_per_h',
                      name='rate of paraxanthine change [l/hr]'),


    # rates
    mc.AssignmentRule('Absorption_caf', 'Ka_caf*D_caf*F_caf', 'mg_per_h', name="caffeine absorption"),
    mc.AssignmentRule('Venous_caf', 'Qki*(Cki_caf/Kpki_caf*BP_caf) + Qh*(Cli_caf/Kpli_caf*BP_caf) + Qre*(Cre_caf/Kpre_caf*BP_caf)', 'mg_per_h'),

    mc.AssignmentRule('Absorption_px', 'Ka_px*D_px*F_px', 'mg_per_h', name="paraxanthine absorption"),
    mc.AssignmentRule('Venous_px', 'Qki*(Cki_px/Kpki_px*BP_px) + Qh*(Cli_px/Kpli_px*BP_px) + Qre*(Cre_px/Kpre_px*BP_px)', 'mg_per_h'),

    # total substance
    mc.AssignmentRule('Abody_caf', 'Aar_caf + Agu_caf + Aki_caf + Ali_caf + Alu_caf + Asp_caf + Are_caf + Ave_caf', 'mg'),
    mc.AssignmentRule('Abody_px', 'Aar_px + Agu_px + Aki_px + Ali_px + Alu_px + Asp_px + Are_px + Ave_px', 'mg')
]

rate_rules = [
    mc.RateRule('Agu_caf', 'Absorption_caf + Qgu*(Car_caf - Cgu_caf/Kpgu_caf*BP_caf)', 'mg_per_h'),
    mc.RateRule('Aki_caf', 'Qki*(Car_caf - Cki_caf/Kpki_caf*BP_caf) - CLrenal_caf*Cki_free_caf', 'mg_per_h'),
    mc.RateRule('Ali_caf', 'Qha*Car_caf + Qgu*(Cgu_caf/Kpgu_caf*BP_caf) + Qsp*(Csp_caf/Kpsp_caf*BP_caf) - Qh*(Cli_caf/Kpli_caf*BP_caf) - vliv_caf', 'mg_per_h'),
    mc.RateRule('Alu_caf', 'Qlu*Cve_caf - Qlu*(Clu_caf/Kplu_caf*BP_caf)', 'mg_per_h'),
    mc.RateRule('Asp_caf', 'Qsp*(Car_caf - Csp_caf/Kpsp_caf*BP_caf)', 'mg_per_h'),
    mc.RateRule('Ave_caf', 'Venous_caf - Qlu*Cve_caf', 'mg_per_h'),
    mc.RateRule('Aar_caf', 'Qlu*(Clu_caf/Kplu_caf*BP_caf) - Qlu*Car_caf', 'mg_per_h'),
    mc.RateRule('Are_caf', 'Qre*(Car_caf - Cre_caf/Kpre_caf*BP_caf)', 'mg_per_h'),
    mc.RateRule('D_caf', '-Absorption_caf', 'mg_per_h'),
    mc.RateRule('DCL_caf', 'CLrenal_caf*Cki_free_caf + Cli_free_caf*CLliv_caf', 'mg_per_h'),

    mc.RateRule('Agu_px', 'Absorption_px + Qgu*(Car_px - Cgu_px/Kpgu_px*BP_px)', 'mg_per_h'),
    mc.RateRule('Aki_px', 'Qki*(Car_px - Cki_px/Kpki_px*BP_px) - CLrenal_px*Cki_free_px', 'mg_per_h'),
    mc.RateRule('Ali_px', 'Qha*Car_px + Qgu*(Cgu_px/Kpgu_px*BP_px) + Qsp*(Csp_px/Kpsp_px*BP_px) - Qh*(Cli_px/Kpli_px*BP_px) + vliv_caf - vliv_px', 'mg_per_h'),
    mc.RateRule('Alu_px', 'Qlu*Cve_px - Qlu*(Clu_px/Kplu_px*BP_px)', 'mg_per_h'),
    mc.RateRule('Asp_px', 'Qsp*(Car_px - Csp_px/Kpsp_px*BP_px)', 'mg_per_h'),
    mc.RateRule('Ave_px', 'Venous_px - Qlu*Cve_px', 'mg_per_h'),
    mc.RateRule('Aar_px', 'Qlu*(Clu_px/Kplu_px*BP_px) - Qlu*Car_px', 'mg_per_h'),
    mc.RateRule('Are_px', 'Qre*(Car_px - Cre_px/Kpre_px*BP_px)', 'mg_per_h'),
    mc.RateRule('D_px', '-Absorption_px', 'mg_per_h'),
    mc.RateRule('DCL_px', 'CLrenal_px*Cki_free_px -vliv_px', 'mg_per_h'),
]
