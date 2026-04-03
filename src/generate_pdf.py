# ============================================================
# Partie I - Recommandation executive — PDF
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime

OUTPUT = 'reports/recommandation_executive.pdf'

# ── Couleurs ─────────────────────────────────────────────
BLUE_DARK  = colors.HexColor('#1a2a7a')
BLUE_MID   = colors.HexColor('#4f6ef7')
BLUE_LIGHT = colors.HexColor('#dce6ff')
GREEN      = colors.HexColor('#2ecc71')
RED        = colors.HexColor('#e74c3c')
AMBER      = colors.HexColor('#f39c12')
GRAY_LIGHT = colors.HexColor('#f5f5f5')
GRAY_MID   = colors.HexColor('#888888')
WHITE      = colors.white
BLACK      = colors.black

# ── Document ─────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title='Recommandation Executive — Marketing Campaign ML',
    author='Equipe Data Science'
)

styles = getSampleStyleSheet()
story  = []

# ── Styles custom ─────────────────────────────────────────
def S(name, **kwargs):
    return ParagraphStyle(name, **kwargs)

s_title = S('s_title', fontSize=26, textColor=WHITE,
            fontName='Helvetica-Bold', alignment=TA_CENTER,
            spaceAfter=6, leading=32)
s_subtitle = S('s_subtitle', fontSize=13, textColor=BLUE_LIGHT,
               fontName='Helvetica', alignment=TA_CENTER,
               spaceAfter=4)
s_date = S('s_date', fontSize=10, textColor=BLUE_LIGHT,
           fontName='Helvetica', alignment=TA_CENTER)
s_h1 = S('s_h1', fontSize=15, textColor=WHITE,
         fontName='Helvetica-Bold', alignment=TA_LEFT,
         spaceAfter=4, leading=18)
s_h2 = S('s_h2', fontSize=12, textColor=BLUE_DARK,
         fontName='Helvetica-Bold', spaceAfter=4,
         spaceBefore=8, leading=15)
s_body = S('s_body', fontSize=10, textColor=BLACK,
           fontName='Helvetica', spaceAfter=4,
           leading=14)
s_bullet = S('s_bullet', fontSize=10, textColor=BLACK,
             fontName='Helvetica', leftIndent=16,
             spaceAfter=3, leading=14)
s_kpi_val = S('s_kpi_val', fontSize=22, textColor=BLUE_MID,
              fontName='Helvetica-Bold', alignment=TA_CENTER,
              leading=26)
s_kpi_lbl = S('s_kpi_lbl', fontSize=9, textColor=GRAY_MID,
              fontName='Helvetica', alignment=TA_CENTER,
              leading=11)
s_footer = S('s_footer', fontSize=8, textColor=GRAY_MID,
             fontName='Helvetica', alignment=TA_CENTER)

def section_header(title):
    tbl = Table([[Paragraph(title, s_h1)]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
        ('ROWPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(Spacer(1, 0.3*cm))
    story.append(tbl)
    story.append(Spacer(1, 0.3*cm))

def kpi_row(kpis):
    cells = []
    for val, lbl, color in kpis:
        cell = [Paragraph(val, s_kpi_val), Paragraph(lbl, s_kpi_lbl)]
        cells.append(cell)
    tbl = Table([cells], colWidths=[17/len(kpis)*cm]*len(kpis))
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GRAY_LIGHT),
        ('ROWPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.3*cm))

def bullet(text):
    story.append(Paragraph(f"  -  {text}", s_bullet))

def body(text):
    story.append(Paragraph(text, s_body))

def spacer(h=0.2):
    story.append(Spacer(1, h*cm))

def hr():
    story.append(HRFlowable(width='100%', thickness=0.5,
                            color=BLUE_LIGHT, spaceAfter=6))

# ============================================================
# PAGE DE COUVERTURE
# ============================================================
cover = Table([['']], colWidths=[17*cm], rowHeights=[4*cm])
cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
    ('ROUNDEDCORNERS', [8]),
]))
story.append(Spacer(1, 1*cm))
story.append(cover)

title_block = Table([
    [Paragraph('Recommandation Executive', s_title)],
    [Paragraph('Marketing Campaign — Intelligence Decisionnelle ML', s_subtitle)],
    [Spacer(1, 0.2*cm)],
    [Paragraph(f'Date : {datetime.now().strftime("%d %B %Y")}  |  Equipe Data Science', s_date)],
], colWidths=[17*cm])
title_block.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), BLUE_DARK),
    ('ROWPADDING', (0,0), (-1,-1), 6),
    ('ROUNDEDCORNERS', [8]),
]))
story.append(title_block)
story.append(Spacer(1, 1*cm))

# Résumé exécutif cover
exec_summ = Table([[
    Paragraph(
        'Ce document presente les resultats d\'une mission d\'analyse ML '
        'appliquee a 2212 clients. Il repond aux questions : qui cibler, '
        'comment decider, quel ROI attendre et comment industrialiser '
        'cette approche.',
        s_body)
]], colWidths=[17*cm])
exec_summ.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), BLUE_LIGHT),
    ('ROWPADDING', (0,0), (-1,-1), 12),
    ('ROUNDEDCORNERS', [4]),
]))
story.append(exec_summ)
story.append(PageBreak())

# ============================================================
# PAGE 2 — KPIs CLES
# ============================================================
section_header('1. Chiffres Cles du Projet')

kpi_row([
    ('2 212', 'Clients analyses', BLUE_MID),
    ('15.1%', 'Taux reponse global', AMBER),
    ('4', 'Segments identifies', GREEN),
    ('0.91', 'AUC-ROC meilleur modele', GREEN),
])
kpi_row([
    ('4 720 eur', 'Profit net test set', GREEN),
    ('299%', 'ROI strategie optimale', GREEN),
    ('158', 'Clients a cibler (test)', BLUE_MID),
    ('23 568 eur', 'Profit extrapole (base complete)', GREEN),
])

spacer(0.3)
story.append(Paragraph('Resume de la mission', s_h2))
body('La mission consistait a construire un systeme d\'aide a la decision '
     'marketing base sur le machine learning, applique a un dataset de '
     '2212 clients avec 29 variables socio-demographiques, transactionnelles '
     'et marketing.')
body('Le pipeline complet couvre : audit des donnees, preparation, '
     'exploration, segmentation par clustering, modelisation predictive, '
     'optimisation du seuil de decision et vision de deploiement industriel.')

# ============================================================
# PAGE 3 — COMPORTEMENTS ET SEGMENTS
# ============================================================
spacer()
section_header('2. Comportements Observes et Segments Clients')

story.append(Paragraph('Insights comportementaux cles', s_h2))
bullet('Correlation Income / TotalSpend : 0.793 — le revenu est le premier determinant des depenses')
bullet('Les repondants depensent 82% de plus que les non-repondants (985 vs 540 euros)')
bullet('Les repondants ont un revenu superieur de 19% (60 209 vs 50 496 euros)')
bullet('Recency plus faible chez les repondants : -31% — ils sont plus recemment actifs')
bullet('CmpAccepted_Total : correlation 0.43 — variable la plus predictive de la reponse')
bullet('Moins d\'enfants = plus de budget disponible : -35% chez les repondants')
spacer(0.3)

story.append(Paragraph('Les 4 segments identifies (K-Means)', s_h2))

seg_data = [
    ['Segment', 'Taille', 'Income moy.', 'Depenses moy.', 'Taux reponse', 'Priorite'],
    ['Premium Engages',  '196 (9%)',  '81 358 eur', '1 655 eur', '53.6%', 'PRIORITAIRE'],
    ['Aises Passifs',    '425 (19%)', '72 173 eur', '1 261 eur', '16.7%', 'A ACTIVER'],
    ['Actifs Moyens',    '553 (25%)', '57 594 eur', '690 eur',   '11.4%', 'NURTURING'],
    ['Petits Budgets',   '1038 (47%)','35 128 eur', '97 eur',    '9.1%',  'FAIBLE PRIO'],
]

seg_tbl = Table(seg_data, colWidths=[3.8*cm, 2.2*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
seg_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
    ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 9),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [WHITE, GRAY_LIGHT]),
    ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',   (0,0), (-1,-1), 6),
    ('TEXTCOLOR',    (5,1), (5,1),   RED),
    ('FONTNAME',     (5,1), (5,1),   'Helvetica-Bold'),
    ('TEXTCOLOR',    (5,2), (5,2),   AMBER),
    ('TEXTCOLOR',    (5,3), (5,3),   BLUE_MID),
    ('TEXTCOLOR',    (5,4), (5,4),   GRAY_MID),
]))
story.append(seg_tbl)
story.append(PageBreak())

# ============================================================
# PAGE 4 — MODELE ET PERFORMANCE
# ============================================================
section_header('3. Modele Recommande et Performance')

story.append(Paragraph('Comparaison des modeles', s_h2))

mod_data = [
    ['Modele', 'AUC-ROC', 'Recall Repondants', 'F1', 'Recommandation'],
    ['Logistic Regression',      '0.9109', '0.82', '0.60', 'RETENU'],
    ['Gradient Boosting optim.', '0.9019', '0.42', '0.54', 'Reference'],
    ['Random Forest',            '0.8586', '0.25', '0.38', 'Ecarte'],
    ['KNN',                      '0.7517', '0.31', '0.42', 'Ecarte'],
]

mod_tbl = Table(mod_data, colWidths=[4.5*cm, 2.8*cm, 3.5*cm, 2*cm, 3.2*cm])
mod_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [BLUE_LIGHT, WHITE, GRAY_LIGHT, GRAY_LIGHT]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 6),
    ('FONTNAME',      (0,1), (-1,1),  'Helvetica-Bold'),
    ('TEXTCOLOR',     (4,1), (4,1),   GREEN),
    ('FONTNAME',      (4,1), (4,1),   'Helvetica-Bold'),
]))
story.append(mod_tbl)
spacer(0.3)

story.append(Paragraph('Justification du choix — Logistic Regression', s_h2))
bullet('Meilleur AUC-ROC : 0.9109 — capacite discriminante superieure')
bullet('Recall repondants : 0.82 — detecte 82% des vrais repondants')
bullet('En marketing, rater un repondant coute plus cher que contacter un non-repondant par erreur')
bullet('Modele interpretable : coefficients lisibles par les equipes metier')
bullet('Rapide a scorer : adapte a des volumes importants')
spacer(0.3)

story.append(Paragraph('Top 5 variables influentes (SHAP)', s_h2))
shap_data = [
    ['Variable', 'Importance SHAP', 'Interpretation metier'],
    ['Recency',            '0.636', 'Plus le client est recent, plus il repond'],
    ['Seniority_Days',     '0.580', 'Anciennete client : les fideles repondent plus'],
    ['CmpAccepted_Total',  '0.471', 'Historique campagnes : signal le plus fort'],
    ['Is_Couple',          '0.352', 'Situation familiale influence la reponse'],
    ['MntMeatProducts',    '0.307', 'Profil de depenses : viande = client premium'],
]
shap_tbl = Table(shap_data, colWidths=[4*cm, 3.5*cm, 9.5*cm])
shap_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ALIGN',         (1,0), (1,-1),  'CENTER'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, GRAY_LIGHT]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 6),
]))
story.append(shap_tbl)
story.append(PageBreak())

# ============================================================
# PAGE 5 — STRATEGIE DE CIBLAGE
# ============================================================
section_header('4. Strategie de Ciblage et ROI')

story.append(Paragraph('Comparaison des strategies', s_h2))
strat_data = [
    ['Strategie', 'Contactes', 'Convertis', 'Profit', 'ROI', 'Recommandation'],
    ['Tous les clients',         '443', '67', '2 270 eur',  '51%',  ''],
    ['Seuil defaut (0.50)',       '37',  '28', '2 430 eur',  '657%', ''],
    ['Seuil optimal (0.07)',      '158', '63', '4 720 eur',  '299%', 'RECOMMANDE'],
    ['Top 20% scores',            '89',  '44', '3 510 eur',  '394%', ''],
    ['Premium Engages seul',      '38',  '21', '1 720 eur',  '453%', ''],
]
strat_tbl = Table(strat_data,
                  colWidths=[4.5*cm, 2.2*cm, 2.2*cm, 2.5*cm, 2*cm, 3*cm])
strat_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ALIGN',         (1,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, GRAY_LIGHT,
                                       BLUE_LIGHT, GRAY_LIGHT, WHITE]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 6),
    ('FONTNAME',      (0,3), (-1,3),  'Helvetica-Bold'),
    ('TEXTCOLOR',     (5,3), (5,3),   GREEN),
    ('FONTNAME',      (5,3), (5,3),   'Helvetica-Bold'),
]))
story.append(strat_tbl)
spacer(0.3)

story.append(Paragraph('Regles de ciblage recommandees', s_h2))
bullet('Contacter les clients avec score de probabilite >= 0.07')
bullet('Prioriser le segment Premium Engages (53.6% taux reponse)')
bullet('Exclure les clients avec Recency > 70 jours (inactifs)')
bullet('Exclure le segment Petits Budgets (profit negatif : -850 eur)')
bullet('Budget campagne estime : 1 580 euros pour 158 contacts')
spacer(0.3)

story.append(Paragraph('Extrapolation sur la base complete', s_h2))
extrap_data = [
    ['Indicateur', 'Test set (443)', 'Base complete (2212)'],
    ['Clients a cibler',     '158',        '788'],
    ['Conversions attendues','63',          '314'],
    ['Budget campagne',      '1 580 eur',  '7 880 eur'],
    ['Profit net attendu',   '4 720 eur',  '23 568 eur'],
    ['ROI',                  '299%',       '299%'],
]
ext_tbl = Table(extrap_data, colWidths=[6*cm, 4.5*cm, 5.5*cm])
ext_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ALIGN',         (1,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, GRAY_LIGHT]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 7),
    ('FONTNAME',      (0,-1),(-1,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR',     (1,-1),(-1,-1), GREEN),
]))
story.append(ext_tbl)
story.append(PageBreak())

# ============================================================
# PAGE 6 — RISQUES ET FEUILLE DE ROUTE
# ============================================================
section_header('5. Risques Analytiques')

risques = [
    ['Risque', 'Niveau', 'Mitigation'],
    ['Dataset limite (2212 obs)',
     'MOYEN',
     'Regularisation L2, cross-validation stratifiee'],
    ['Desequilibre classes (85/15)',
     'MOYEN',
     'class_weight balanced, seuil optimise'],
    ['Surapprentissage potentiel',
     'FAIBLE',
     'Validation croisee 5 folds, AUC stable'],
    ['Derive des donnees (drift)',
     'MOYEN',
     'Monitoring mensuel, reapprentissage si AUC < 0.88'],
    ['Biais selection campagnes passees',
     'ELEVE',
     'Donnees non representatives des non-contactes'],
    ['Absence variable geographique',
     'FAIBLE',
     'Segmentation compensee par comportement achat'],
]
risk_tbl = Table(risques, colWidths=[5*cm, 2.5*cm, 9*cm])
risk_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ALIGN',         (1,1), (1,-1),  'CENTER'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, GRAY_LIGHT]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 6),
    ('TEXTCOLOR',     (1,5), (1,5),   RED),
    ('FONTNAME',      (1,5), (1,5),   'Helvetica-Bold'),
    ('TEXTCOLOR',     (1,1), (1,4),   AMBER),
    ('TEXTCOLOR',     (1,3), (1,3),   AMBER),
    ('TEXTCOLOR',     (1,6), (1,6),   GREEN),
]))
story.append(risk_tbl)
spacer(0.5)

section_header('6. Feuille de Route — Prochains Mois')

roadmap_data = [
    ['Phase', 'Actions', 'Echeance'],
    ['Court terme',
     'API REST scoring (FastAPI) | Dockerisation | MLflow versioning',
     '1-3 mois'],
    ['Moyen terme',
     'Connexion CRM temps reel | Reapprentissage auto (Airflow) | A/B testing',
     '3-6 mois'],
    ['Long terme',
     'Feature store | Scoring temps reel | Personnalisation individuelle',
     '6-12 mois'],
]
road_tbl = Table(roadmap_data, colWidths=[3*cm, 10*cm, 3*cm])
road_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ALIGN',         (2,0), (2,-1),  'CENTER'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [BLUE_LIGHT, WHITE, GRAY_LIGHT]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 8),
]))
story.append(road_tbl)
story.append(PageBreak())

# ============================================================
# PAGE 7 — CONCLUSION
# ============================================================
section_header('7. Conclusion et Recommandation Finale')

spacer(0.3)
concl = Table([[
    Paragraph(
        'Recommandation : Deployer le pipeline ML avec la Logistic Regression '
        '(AUC 0.91), un seuil de decision a 0.07, en ciblant 788 clients sur '
        '2212 pour un profit net attendu de 23 568 euros par campagne (ROI 299%). '
        'Prioriser le segment Premium Engages et exclure les Petits Budgets.',
        s_body)
]], colWidths=[17*cm])
concl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), BLUE_LIGHT),
    ('ROWPADDING', (0,0), (-1,-1), 14),
    ('ROUNDEDCORNERS', [4]),
    ('BOX', (0,0), (-1,-1), 2, BLUE_MID),
]))
story.append(concl)
spacer(0.4)

story.append(Paragraph('Synthese des decisions', s_h2))
decisions = [
    ['Decision', 'Choix retenu', 'Justification'],
    ['Segmentation',     'K-Means k=4',           '4 segments metier actionnables'],
    ['Modele',           'Logistic Regression',    'Meilleur AUC (0.91) + Recall 0.82'],
    ['Seuil',            '0.07',                  'Maximise le profit net (4 720 eur)'],
    ['Strategie',        'Seuil optimal',          'Meilleur profit absolu (299% ROI)'],
    ['Priorite segment', 'Premium Engages',        '53.6% taux reponse, ROI maximal'],
    ['MLOps',            'API + MLflow + Airflow', 'Industrialisation 1-6 mois'],
]
dec_tbl = Table(decisions, colWidths=[4*cm, 4.5*cm, 8.5*cm])
dec_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  BLUE_DARK),
    ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
    ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, GRAY_LIGHT]),
    ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
    ('ROWPADDING',    (0,0), (-1,-1), 7),
]))
story.append(dec_tbl)
spacer(0.5)
hr()
spacer(0.2)

story.append(Paragraph(
    f'Document genere le {datetime.now().strftime("%d/%m/%Y")} | '
    f'Equipe Data Science | marketing_campaign_ML_dm2',
    s_footer))

# ── Build ─────────────────────────────────────────────────
doc.build(story)
print(f"PDF genere -> {OUTPUT}")