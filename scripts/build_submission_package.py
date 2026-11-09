from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import shutil, re, html, zipfile, os
import cairosvg
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle, KeepTogether, HRFlowable)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path('/home/user/reasonflux')
PKG = ROOT/'submission_package'
AS = PKG/'assets'
AS.mkdir(parents=True, exist_ok=True)
MANUSCRIPT = ROOT/'arc_claim_evaluation_case_study_draft_v4.md'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_ITAL = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

# ---------- Artwork / submission visuals ----------
art_path = ROOT/'submission_assets/card_art.png'
art = Image.open(art_path).convert('RGB')
# Cover image requires exact Kaggle card ratio (560x280); crop from center, then upscale/downsample cleanly.
w,h=art.size
if w/h > 2:
    nw=int(h*2); left=(w-nw)//2; art=art.crop((left,0,left+nw,h))
else:
    nh=int(w/2); top=(h-nh)//2; art=art.crop((0,top,w,top+nh))
art=art.resize((1120,560), Image.Resampling.LANCZOS).convert('RGBA')
# Layered left-side gradient for legibility; preserve the selected image on the right.
over=Image.new('RGBA', art.size, (0,0,0,0)); pix=over.load()
for x in range(1120):
    alpha=max(0, int(218*(1-x/780))) if x<780 else 0
    for y in range(560): pix[x,y]=(5,15,34,alpha)
art=Image.alpha_composite(art,over)
d=ImageDraw.Draw(art)
font_label=ImageFont.truetype(FONT_BOLD,22)
font_title=ImageFont.truetype(FONT_BOLD,57)
font_sub=ImageFont.truetype(FONT_REG,24)
font_tag=ImageFont.truetype(FONT_BOLD,16)
d.rounded_rectangle((54,46,453,91), radius=18, fill=(12,37,58,220), outline=(57,211,196,200), width=2)
d.text((74,57),'ARC PRIZE 2026  /  PAPER TRACK',font=font_label,fill=(160,244,230,255))
d.text((54,150),'EVALUATING CLAIMS,',font=font_title,fill=(255,255,255,255),stroke_width=1,stroke_fill=(5,15,34,120))
d.text((54,222),'NOT JUST SYSTEMS',font=font_title,fill=(255,255,255,255),stroke_width=1,stroke_fill=(5,15,34,120))
d.rounded_rectangle((57,320,557,324), radius=2, fill=(52,211,196,255))
d.text((57,349),'A longitudinal evidence audit',font=font_sub,fill=(226,239,248,255))
d.text((57,390),'CLAIM  →  EVIDENCE  →  DISPOSITION',font=font_tag,fill=(255,198,110,255))
card=art.convert('RGB').resize((560,280),Image.Resampling.LANCZOS)
card.save(AS/'kaggle_card_560x280.png',optimize=True)
# A large hero image for writeup embeds / gallery.
card.resize((1680,840),Image.Resampling.LANCZOS).save(AS/'hero_banner_1680x840.jpg',quality=94,optimize=True)

# Palette and image drawing helpers
NAVY='#0b1730'; PANEL='#122341'; INK='#10213c'; MUTED='#53647c'; TEAL='#2dd4bf'; AMBER='#f5b942'; BLUE='#5aa7ff'; LAV='#9b8cff'; PALE='#f4f7fb'; WHITE='#ffffff'; GREEN='#4dc58a'; RED='#ef7c6c'
def rgb(hx): return tuple(int(hx[i:i+2],16) for i in (1,3,5))
def font(size,bold=False): return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)
def rr(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)
def textwrap_px(draw, text, f, maxw):
    words=text.split(); lines=[]; cur=''
    for word in words:
        cand=(cur+' '+word).strip()
        if draw.textbbox((0,0),cand,font=f)[2] <= maxw: cur=cand
        else:
            if cur: lines.append(cur)
            cur=word
    if cur: lines.append(cur)
    return lines
def draw_wrapped(draw, xy, text, f, fill, maxw, leading=1.35):
    x,y=xy; lines=textwrap_px(draw,text,f,maxw)
    for line in lines:
        draw.text((x,y),line,font=f,fill=fill); y+=int(f.size*leading)
    return y

def new_canvas(size, title, subtitle):
    im=Image.new('RGB',size,rgb(PALE)); d=ImageDraw.Draw(im)
    d.rectangle((0,0,size[0],170),fill=rgb(NAVY))
    d.text((70,38),title,font=font(42,True),fill=rgb(WHITE))
    d.text((72,104),subtitle,font=font(21),fill=(190,208,229))
    return im,d

# Claim ladder — explicitly an organizing lens, not a validated scale.
im,d=new_canvas((1800,1100),'THE CLAIM LADDER','An organizing lens for separating evidence questions — not a validated measurement scale')
steps=[
 ('01','MECHANISM PRESENT','Did the proposed object or operation occur?','Example ceiling: reflection / rotation skill objects appeared in controlled synthetic tasks.',BLUE),
 ('02','TASK-RELEVANT UTILITY','Did it contribute to a relevant outcome in that setting?','Some reuse and simulator-step savings observed; local utility does not prove policy value.',TEAL),
 ('03','INCREMENTAL SUPERIORITY','Did it beat appropriate, sufficiently strong comparators?','Transfer-aware ranking tied simpler controls; skill-creation policies did not clear superiority gates.',AMBER),
 ('04','EXTERNAL GENERALIZATION','Did it hold beyond the development setting?','The ARC-AGI-2 adapter had very low fit coverage and no accepted downstream objects.',LAV),
]
# vertical connectors and numbered nodes
xnode=132; y0=238; gap=194
d.line((xnode,y0+42,xnode,y0+gap*3+42),fill=(175,192,214),width=7)
for i,(num,title,question,example,color) in enumerate(steps):
    y=y0+i*gap
    d.ellipse((xnode-34,y-4,xnode+34,y+64),fill=rgb(color),outline=rgb(WHITE),width=3)
    bb=d.textbbox((0,0),num,font=font(22,True)); d.text((xnode-(bb[2]-bb[0])/2,y+15),num,font=font(22,True),fill=rgb(NAVY))
    rr(d,(215,y-8,1715,y+147),24,rgb(WHITE),outline=rgb(color),width=4)
    d.text((258,y+14),title,font=font(30,True),fill=rgb(INK))
    d.text((258,y+60),question,font=font(22,True),fill=rgb(MUTED))
    draw_wrapped(d,(258,y+97),example,font(20),rgb(MUTED),1370,1.3)
# Bottom strip states that the ladder is not an aggregate grade; placed clear of all four cards.
rr(d,(215,994,1715,1068),20,rgb(NAVY))
d.text((255,1017),'NO OVERALL SCORE',font=font(23,True),fill=rgb(AMBER))
d.text((525,1019),'Each claim can stop at a different evidence ceiling.',font=font(22),fill=rgb(WHITE))
im.save(AS/'claim_ladder.png',optimize=True)

# Disposition dashboard — use only manuscript's five distinct findings.
im,d=new_canvas((1800,1120),'FIVE CLAIMS. FIVE DIFFERENT DISPOSITIONS.','Read the evidence ceiling, not a single program-level pass/fail label')
items=[
 ('PATTERN DISCOVERY','PARTIAL SUPPORT','Recurring operation signatures in controlled synthetic generators.','Generator-bounded; no external validation.',BLUE),
 ('SKILL FORMATION / REUSE','MIXED','Reflection / rotation objects and some reuse; policy superiority gates did not pass.','Local utility ≠ incremental superiority.',TEAL),
 ('CAPABILITY GROWTH','UNVALIDATED CONSTRUCT','Metrics varied across phases; no validated ARC capability group.','Positive values in one cohort are insufficient.',AMBER),
 ('ARC TRANSFER','NOT DEMONSTRATED','Low-coverage adapter; no accepted downstream mechanism objects.','Coverage-limited non-activation, not broad falsification.',LAV),
 ('BL1 BOUNDARY LEARNING','TERMINATED AT P0','Bounded prior-art review stopped work before implementation or experiment.','No experimental efficacy conclusion.',RED),
]
positions=[(70,220),(930,220),(70,500),(930,500),(500,780)]
for (name,status,evidence,ceiling,col),(x,y) in zip(items,positions):
    rr(d,(x,y,x+800,y+228),24,rgb(WHITE),outline=rgb(col),width=4)
    d.rectangle((x,y,x+15,y+228),fill=rgb(col))
    d.text((x+38,y+22),name,font=font(20,True),fill=rgb(MUTED))
    d.text((x+38,y+58),status,font=font(27,True),fill=rgb(col))
    draw_wrapped(d,(x+38,y+105),evidence,font(18),rgb(INK),710,1.28)
    draw_wrapped(d,(x+38,y+174),ceiling,font(16,True),rgb(MUTED),710,1.25)
im.save(AS/'disposition_map.png',optimize=True)

# Scope/provenance infographic
im,d=new_canvas((1800,920),'WHAT IS IN SCOPE — AND WHAT IS NOT','A deliberately bounded retrospective case study; immutable archive preserved')
# included card
rr(d,(90,230,850,735),30,rgb(WHITE),outline=rgb(TEAL),width=5)
d.text((135,270),'INCLUDED IN THIS WRITE-UP',font=font(27,True),fill=rgb(TEAL))
include=[('ASFT','Saved Phase 13–14 evidence synthesis'),('BL1','Bounded P0 prior-art decision; no experiment'),('Cycle closure','Claim dispositions and research-cycle decision')]
y=345
for title,desc in include:
    d.ellipse((140,y+3,165,y+28),fill=rgb(TEAL))
    d.text((190,y),title,font=font(22,True),fill=rgb(INK))
    draw_wrapped(d,(190,y+37),desc,font(18),rgb(MUTED),575,1.25)
    y+=112
# excluded card
rr(d,(950,230,1710,735),30,rgb(WHITE),outline=rgb(RED),width=5)
d.text((995,270),'EXCLUDED FROM EVIDENCE',font=font(27,True),fill=rgb(RED))
d.text((1000,350),'T2T / S3',font=font(31,True),fill=rgb(INK))
draw_wrapped(d,(1000,404),'An unresolved timestamp discrepancy prevents use in this submission version.',font(20),rgb(MUTED),625,1.35)
d.line((1000,535,1650,535),fill=(219,226,235),width=2)
draw_wrapped(d,(1000,565),'The immutable archive remains unchanged. No S3 result or disposition is used.',font(20),rgb(INK),625,1.35)
rr(d,(470,790,1330,866),24,rgb(NAVY))
d.text((525,813),'NO NEW EXPERIMENTS  •  NO POST-HOC RESCUE',font=font(22,True),fill=rgb(WHITE))
im.save(AS/'scope_and_provenance.png',optimize=True)

# Rasterize existing source timeline; retain source SVG alongside all assets.
svg=ROOT/'research_cycle_claim_audit_timeline.svg'
shutil.copy2(svg,AS/'research_cycle_claim_audit_timeline.svg')
cairosvg.svg2png(url=str(svg),write_to=str(AS/'research_cycle_claim_audit_timeline.png'),output_width=1600,output_height=650)

# ---------- Copy source / write submission-ready text ----------
shutil.copy2(MANUSCRIPT,PKG/'paper_source_v4.md')

subtitle='A longitudinal evidence audit of one ARC research program'
project_description='''This project is a longitudinal claim-audit case study of one ARC-motivated research cycle. Rather than presenting a new solver or benchmark score, it traces what the project’s archived evidence supports at each step: mechanism occurrence, task-relevant utility, comparator-based superiority, generalization, and final scientific disposition.\n\nThe audit follows two evidence paths. ASFT produced recurring operation-level patterns and reflection/rotation skill objects in controlled synthetic tasks, with some observed reuse and simulator-step savings. Those observations support narrow mechanism occurrence and local utility; they do not establish incremental superiority. Transfer-aware ranking tied simpler controls, skill-creation policies did not clear their primary superiority gates, and capability metrics were mixed across phases. A bounded ARC-AGI-2 adapter had very low fit coverage and produced no accepted downstream objects, so ARC transfer is not demonstrated.\n\nBL1 proposed counterexample-guided applicability-boundary learning. A bounded prior-art review found substantial overlap and stopped the line at P0, before implementation or experiment. This is a novelty/program decision, not an experimental efficacy result.\n\nThe result is not a single success/failure verdict. Pattern discovery receives partial support; skill formation and reuse are mixed; capability growth remains an unvalidated construct; ARC transfer is not demonstrated; and BL1 was terminated at P0. These dispositions have different evidence ceilings and should not be conflated.\n\nScope is intentionally narrow: this is a retrospective account of one research cycle, based on immutable saved records and a purposive literature screen, not a systematic review or field-wide prevalence study. T2T/S3 is excluded because its execution timestamp cannot be reconciled with the manuscript date. The archive remains unchanged; no S3 result or disposition is used here. No new experiment, benchmark run, statistical re-analysis, or post-hoc rescue is claimed.\n\nThe attached paper and visual assets make the evidence path inspectable: a claim ladder, a disposition map, a provenance boundary graphic, and the full longitudinal claim-stage matrix.'''
# Count word count (approximate whitespace token count)
word_count=len(re.findall(r"\b[\w’'-]+\b",project_description))

md=f'''# Kaggle Writeup — Ready-to-paste content

## Basic details

- **Title:** Evaluating Claims, Not Just Systems
- **Subtitle:** {subtitle}
- **Writeup URL:** https://www.kaggle.com/competitions/arc-prize-2026-paper-track/writeups/evaluating-claims-not-just-systems
- **Track:** Main Track (auto-selected; leave as-is)
- **DOI:** Enable DOI citation so the writeup receives a DOI after the competition ends.

## Project description (plain-text field)

Paste the text below into the Project Description field. Approximate word count: **{word_count} words**.

---

{project_description}

---

## Rich-media layout suggestion

If Kaggle supports embedded images in the description, place the following assets between the relevant paragraphs; otherwise add them to Media gallery with the captions below:

1. `assets/claim_ladder.png` — **The claim ladder.** Four distinct questions from mechanism occurrence to external generalization. This is an organizing lens, not a validated scale.
2. `assets/disposition_map.png` — **Five evidence ceilings.** The program’s five claim dispositions, kept separate rather than collapsed into one verdict.
3. `assets/research_cycle_claim_audit_timeline.png` — **Research Cycle 1 map.** The retained ASFT, capability, and BL1 paths across hypothesis, mechanism, utility, comparator, generalization, and disposition.
4. `assets/scope_and_provenance.png` — **Scope and provenance.** Included evidence paths and the explicit T2T/S3 exclusion.

The card/thumbnail is `assets/kaggle_card_560x280.png` (exactly 560 × 280 pixels). For a larger visual in the gallery, use `assets/hero_banner_1680x840.jpg`.

## Media gallery captions (copy/paste)

- **Claim ladder:** Mechanism occurrence, local utility, comparator-based superiority, and external generalization are different evidence questions—not a single score.
- **Disposition map:** One research cycle produced different claim-level outcomes: partial support, mixed evidence, an unvalidated construct, transfer not demonstrated, and a pre-experiment P0 termination.
- **Longitudinal map:** Trace each retained claim from hypothesis through evidence to disposition. T2T/S3 is excluded from this version.
- **Scope and provenance:** The case study preserves its immutable archive and excludes T2T/S3 because its recorded timestamp remains unresolved.

## Attachments to upload (all prepared here)

Recommended, in this order:

1. `paper.pdf` — typeset manuscript PDF.
2. `visual_overview.pdf` — short, visual companion for judges/community readers.
3. `paper_editable.docx` — editable Word manuscript.
4. `paper_source_v4.md` — Markdown source version of the submission-facing manuscript.
5. `assets/` images for Media gallery; the card image is a separate exact-size upload.

`submission_files.zip` contains the prepared docs and assets together. Individual files can also be uploaded separately. Total bundle size is documented in `UPLOAD_MANIFEST.md`.

## Project links

Add your project/repository link when ready. No link is invented or prefilled here. Prefer a stable public repository or dataset link that contains only the materials you intend to share; do not point judges at the full internal archive unless you have reviewed its contents and provenance.

## Before clicking Submit

- Verify title and subtitle, and check that the writeup URL remains the intended slug.
- Upload the 560×280 card image; preview crop and legibility.
- Add the four visual assets to Media gallery and paste the captions above.
- Upload `paper.pdf` and `visual_overview.pdf`; optionally include the source Markdown.
- Add your project link when ready.
- Enable DOI citation.
- Preview the complete writeup and confirm that the T2T/S3 exclusion and limitations remain visible.
'''
(PKG/'KAGGLE_WRITEUP_READY_TO_PASTE.md').write_text(md)

(PKG/'PROJECT_DESCRIPTION_PLAIN_TEXT.txt').write_text(f'''TITLE\nEvaluating Claims, Not Just Systems\n\nSUBTITLE\n{subtitle}\n\nPROJECT DESCRIPTION ({word_count} words)\n\n{project_description}\n''')
(PKG/'UPLOAD_MANIFEST.md').write_text('''# Upload manifest\n\nPrepared for the ARC Prize 2026 Paper Track Kaggle writeup. Files are presentation companions to the submission-facing v4 manuscript; they do not add new experiments or revise scientific claims.\n\n- `paper.pdf` — typeset paper, generated from `paper_source_v4.md`.\n- `visual_overview.pdf` — visual companion with the claim ladder, disposition map, longitudinal timeline, and provenance boundary.\n- `paper_editable.docx` — editable Word manuscript in modern OOXML format.\n- `paper_source_v4.md` — copy of the submission-facing manuscript source.\n- `assets/kaggle_card_560x280.png` — exact requested card/thumbnail dimensions.\n- `assets/hero_banner_1680x840.jpg` — large gallery banner.\n- `assets/claim_ladder.png` — claim-evidence progression.\n- `assets/disposition_map.png` — five distinct claim dispositions.\n- `assets/research_cycle_claim_audit_timeline.png` and `.svg` — raster/vector timeline figure.\n- `assets/scope_and_provenance.png` — included/excluded evidence scope graphic.\n\nCurrent ZIP size is approximately 2.4 MB, well below the 100 MB upload limit. The selected card artwork was generated for this submission and then composited with typography; the diagrams are original visual summaries of manuscript content. No official ARC logo or external copyrighted puzzle image is included.\n''')

# ---------- PDF typesetting ----------
pdfmetrics.registerFont(TTFont('DV',FONT_REG)); pdfmetrics.registerFont(TTFont('DV-Bold',FONT_BOLD)); pdfmetrics.registerFont(TTFont('DV-Italic',FONT_ITAL))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyDV',parent=styles['BodyText'],fontName='DV',fontSize=9.1,leading=13.4,textColor=colors.HexColor('#263449'),spaceAfter=7,alignment=TA_LEFT))
styles.add(ParagraphStyle(name='H1DV',parent=styles['Heading1'],fontName='DV-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#10213c'),spaceBefore=12,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='H2DV',parent=styles['Heading2'],fontName='DV-Bold',fontSize=12.5,leading=16,textColor=colors.HexColor('#146b73'),spaceBefore=9,spaceAfter=5,keepWithNext=True))
styles.add(ParagraphStyle(name='H3DV',parent=styles['Heading3'],fontName='DV-Bold',fontSize=10.5,leading=14,textColor=colors.HexColor('#3f5d7d'),spaceBefore=7,spaceAfter=4,keepWithNext=True))
styles.add(ParagraphStyle(name='SmallDV',parent=styles['BodyText'],fontName='DV',fontSize=7.3,leading=9.2,textColor=colors.HexColor('#53647c'),spaceAfter=3))
styles.add(ParagraphStyle(name='CaptionDV',parent=styles['BodyText'],fontName='DV-Italic',fontSize=7.8,leading=10,textColor=colors.HexColor('#53647c'),alignment=TA_CENTER,spaceAfter=7))
styles.add(ParagraphStyle(name='QuoteDV',parent=styles['BodyText'],fontName='DV-Bold',fontSize=10,leading=14,textColor=colors.HexColor('#123c50'),leftIndent=12,rightIndent=12,borderColor=colors.HexColor('#2dd4bf'),borderWidth=2,borderPadding=8,spaceBefore=5,spaceAfter=9))
styles.add(ParagraphStyle(name='BulletDV',parent=styles['BodyText'],fontName='DV',fontSize=8.8,leading=12.2,textColor=colors.HexColor('#263449'),leftIndent=13,firstLineIndent=-8,spaceAfter=3))

def md_inline(t):
    t=t.strip()
    # link syntax first
    t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{html.escape(m.group(2),quote=True)}" color="#147e86">{html.escape(m.group(1))}</link>',t)
    t=re.sub(r'(?<!\*)\*\*(.+?)\*\*(?!\*)',r'<b>\1</b>',t)
    t=re.sub(r'(?<!\*)\*(.+?)\*(?!\*)',r'<i>\1</i>',t)
    t=re.sub(r'`([^`]+)`',r'<font name="DV-Bold" color="#334155">\1</font>',t)
    t=t.replace('→','&#8594;').replace('—','&#8212;').replace('–','&#8211;')
    return t

def make_table(lines, avail_w):
    parsed=[]
    for line in lines:
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-{2,}:?',c or '-') for c in cells): continue
        parsed.append(cells)
    if not parsed: return Spacer(1,1)
    n=max(map(len,parsed)); parsed=[r+['']*(n-len(r)) for r in parsed]
    widths=[avail_w*w/sum([1.0]*n) for w in [1]*n]
    if n==4: widths=[avail_w*.19,avail_w*.31,avail_w*.22,avail_w*.28]
    elif n==2: widths=[avail_w*.28,avail_w*.72]
    data=[]
    for ri,row in enumerate(parsed):
        data.append([Paragraph(md_inline(c),ParagraphStyle('cell',fontName='DV-Bold' if ri==0 else 'DV',fontSize=6.5 if n>3 else 7.5,leading=8.2 if n>3 else 9.5,textColor=colors.HexColor('#ffffff' if ri==0 else '#263449'))) for c in row])
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
      ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17304f')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#ccd7e4')),
      ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
      ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f7fb')])]))
    return t

def footer(canvas,doc):
    canvas.saveState(); w,h=letter
    canvas.setStrokeColor(colors.HexColor('#dce5ef')); canvas.line(0.7*inch,0.55*inch,w-0.7*inch,0.55*inch)
    canvas.setFont('DV',7); canvas.setFillColor(colors.HexColor('#607087'))
    canvas.drawString(0.72*inch,0.36*inch,'Evaluating Claims, Not Just Systems  •  ARC Prize 2026 Paper Track')
    canvas.drawRightString(w-0.72*inch,0.36*inch,str(doc.page))
    canvas.restoreState()

src=MANUSCRIPT.read_text().splitlines()
story=[]
# Graphic cover page
cover=Image.open(AS/'hero_banner_1680x840.jpg')
story.append(RLImage(str(AS/'hero_banner_1680x840.jpg'),width=6.35*inch,height=3.175*inch))
story += [Spacer(1,22),Paragraph('A Longitudinal Audit of an ARC Research Program',ParagraphStyle('cover2',fontName='DV-Bold',fontSize=20,leading=25,textColor=colors.HexColor('#10213c'),alignment=TA_LEFT,spaceAfter=9)),Paragraph('Submission-facing case study • Research Cycle 1',ParagraphStyle('coversub',fontName='DV',fontSize=11,leading=15,textColor=colors.HexColor('#517086'),spaceAfter=18))]
story.append(Paragraph('<b>Core contribution</b> &nbsp; An auditable mapping between claim type, evidence type, and scientific disposition across one ARC-motivated research cycle.',styles['QuoteDV']))
story.append(Spacer(1,10))
story.append(Paragraph('<b>Scope note.</b> T2T/S3 is excluded because its immutable execution timestamp remains unreconciled. The archive is unchanged; no S3 result or disposition is used. No new experiment or re-analysis is reported.',styles['BodyDV']))
story.append(Spacer(1,10))
story.append(Paragraph('ABSTRACT',ParagraphStyle('absh',fontName='DV-Bold',fontSize=10,leading=12,textColor=colors.HexColor('#147e86'),spaceAfter=5)))
# find abstract text after ### Abstract, combine until Keywords
abstract=[]; in_abs=False
for line in src:
    if line.strip()=='### Abstract': in_abs=True; continue
    if in_abs and line.startswith('**Keywords:**'): break
    if in_abs and line.strip(): abstract.append(line.strip())
story.append(Paragraph(md_inline(' '.join(abstract)),styles['BodyDV']))
story.append(Spacer(1,8)); story.append(Paragraph('<b>Keywords:</b> ARC-AGI; evaluation methodology; claim-evidence mapping; comparator design; generalization; retrospective case study',styles['SmallDV']))
story.append(PageBreak())
# Body starting at Introduction (skip cover notes/abstract)
body_start=next(i for i,l in enumerate(src) if l.strip()=='## 1. Introduction')
i=body_start
while i<len(src):
    line=src[i]
    if not line.strip(): i+=1; continue
    # Markdown image block (use local timeline)
    m=re.match(r'!\[([^]]*)\]\(([^)]+)\)',line.strip())
    if m:
        imgpath=ROOT/m.group(2)
        if imgpath.exists():
            story.append(Spacer(1,4)); story.append(RLImage(str(AS/'research_cycle_claim_audit_timeline.png'),width=7.15*inch,height=7.15*inch*650/1600)); story.append(Spacer(1,3))
        i+=1; continue
    if line.startswith('|'):
        block=[]
        while i<len(src) and src[i].strip().startswith('|'):
            block.append(src[i]); i+=1
        story.append(Spacer(1,4)); story.append(make_table(block,7.1*inch)); story.append(Spacer(1,8)); continue
    if line.startswith('---'):
        i+=1; continue
    if line.startswith('#'):
        lev=len(line)-len(line.lstrip('#')); text=line[lev:].strip()
        style=styles['H1DV'] if lev==2 else styles['H2DV'] if lev==3 else styles['H3DV']
        story.append(Paragraph(md_inline(text),style)); i+=1; continue
    if line.startswith('>'):
        q=[]
        while i<len(src) and src[i].startswith('>'):
            q.append(src[i].lstrip('> ').strip()); i+=1
        story.append(Paragraph(md_inline(' '.join(q)),styles['QuoteDV'])); continue
    if re.match(r'^\s*[-*] ',line):
        content=line.strip()[2:]
        story.append(Paragraph('• '+md_inline(content),styles['BulletDV'])); i+=1; continue
    # collect normal paragraph until blank, heading, table, list, quote, image
    para=[line.strip()]; i+=1
    while i<len(src) and src[i].strip() and not src[i].startswith(('#','|','>','- ','* ','![','---')):
        para.append(src[i].strip()); i+=1
    txt=' '.join(para).replace('  ',' ')
    # editorial note at end visually mark as appendix-ish note, keep as source
    story.append(KeepTogether([Paragraph(md_inline(txt),styles['BodyDV'])]))

pdf_path=PKG/'paper.pdf'
doc=SimpleDocTemplate(str(pdf_path),pagesize=letter,rightMargin=.7*inch,leftMargin=.7*inch,topMargin=.68*inch,bottomMargin=.74*inch,title='Evaluating Claims, Not Just Systems',subject='Longitudinal claim-audit case study for ARC evaluation')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

# Visual overview PDF: concise, visual, judges-first companion.
vis_story=[]
vis_story += [RLImage(str(AS/'hero_banner_1680x840.jpg'),width=7.15*inch,height=3.575*inch),Spacer(1,18)]
vis_story += [Paragraph('EVALUATING CLAIMS, NOT JUST SYSTEMS',ParagraphStyle('visTitle',fontName='DV-Bold',fontSize=21,leading=25,textColor=colors.HexColor('#10213c'),spaceAfter=8)),Paragraph('A one-cycle audit of what the evidence does—and does not—support',ParagraphStyle('visSub',fontName='DV',fontSize=11,leading=15,textColor=colors.HexColor('#53647c'),spaceAfter=13)),Paragraph('The project contributes a traceable claim-level map, not a new ARC solver, benchmark score, or validated universal methodology. Its central lesson: mechanism occurrence, local utility, comparator superiority, and external generalization are separate questions.',styles['BodyDV']),Spacer(1,12),RLImage(str(AS/'claim_ladder.png'),width=7.1*inch,height=7.1*inch*1100/1800),PageBreak()]
vis_story += [Paragraph('THE DISPOSITION MAP',styles['H1DV']),Paragraph('Each conclusion is reported at its own evidence ceiling; dispositions should not be collapsed into one success/failure grade.',styles['BodyDV']),RLImage(str(AS/'disposition_map.png'),width=7.1*inch,height=7.1*inch*1120/1800),PageBreak()]
vis_story += [Paragraph('THE RESEARCH-CYCLE MAP',styles['H1DV']),Paragraph('Read each row across the six stages. Synthetic evidence, capability metrics, bounded ARC adaptation, and the BL1 prior-art stop are kept distinct.',styles['BodyDV']),RLImage(str(AS/'research_cycle_claim_audit_timeline.png'),width=7.1*inch,height=7.1*inch*650/1600),Spacer(1,8),Paragraph('SCOPE & PROVENANCE',styles['H1DV']),RLImage(str(AS/'scope_and_provenance.png'),width=7.1*inch,height=7.1*inch*920/1800),Spacer(1,10),Paragraph('<b>Important exclusion:</b> T2T/S3 is excluded because its immutable execution timestamp cannot be reconciled with the manuscript date. The archive is unchanged; no S3 result or disposition is used. The literature screen is purposive, not systematic; the case supports no field-wide prevalence claim.',styles['BodyDV']),PageBreak()]
vis_story += [Paragraph('WHAT THE CASE SUPPORTS',styles['H1DV'])]
summary_rows=[['Claim','Disposition','Boundary'],['Pattern discovery','Partial support','Synthetic generators; no external validation'],['Skill formation / reuse','Mixed','Some local utility; superiority not established'],['Capability growth','Unvalidated construct','Mixed phases; no validated ARC capability group'],['ARC transfer','Not demonstrated','Low-coverage adapter; non-activation, not falsification'],['BL1 boundary learning','Terminated at P0','Prior-art stop before implementation or experiment']]
table_data=[[Paragraph(md_inline(c),styles['SmallDV']) for c in row] for row in summary_rows]
t=Table(table_data,colWidths=[1.45*inch,1.5*inch,4.15*inch],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17304f')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.5,colors.HexColor('#ccd7e4')),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f7fb')]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
vis_story += [t,Spacer(1,18),Paragraph('READ THE FULL PAPER',styles['H1DV']),Paragraph('The attached manuscript documents scope, source records, the claim ladder, comparative results, limitations, citations, and the exact provenance boundary. It reports no new experimental data or post-hoc rescue. The accompanying visual assets are explanatory summaries of that manuscript.',styles['BodyDV']),HRFlowable(width='100%',thickness=1,color=colors.HexColor('#dce5ef')),Spacer(1,8),Paragraph('Title: Evaluating Claims, Not Just Systems — A Longitudinal Audit of an ARC Research Program',styles['SmallDV'])]
vis_path=PKG/'visual_overview.pdf'
vd=SimpleDocTemplate(str(vis_path),pagesize=letter,rightMargin=.7*inch,leftMargin=.7*inch,topMargin=.68*inch,bottomMargin=.74*inch,title='Visual Overview — Evaluating Claims, Not Just Systems')
vd.build(vis_story,onFirstPage=footer,onLaterPages=footer)

# Editable OOXML manuscript companion (.docx).
def add_docx_runs(paragraph, text):
    # Preserve bold/italic/code and links sufficiently for editing; markdown is not emitted literally.
    pat=re.compile(r'(\*\*.+?\*\*|\*[^*]+\*|`[^`]+`|\[[^]]+\]\(https?://[^)]+\))')
    pos=0
    for m in pat.finditer(text):
        if m.start()>pos: paragraph.add_run(text[pos:m.start()].replace('  ',' '))
        tok=m.group(0)
        if tok.startswith('**'):
            r=paragraph.add_run(tok[2:-2]); r.bold=True
        elif tok.startswith('*'):
            r=paragraph.add_run(tok[1:-1]); r.italic=True
        elif tok.startswith('`'):
            r=paragraph.add_run(tok[1:-1]); r.font.name='Consolas'; r.font.size=Pt(8)
        else:
            mm=re.match(r'\[([^]]+)\]\((https?://[^)]+)\)',tok)
            paragraph.add_run(f'{mm.group(1)} ({mm.group(2)})' if mm else tok)
        pos=m.end()
    if pos<len(text): paragraph.add_run(text[pos:].replace('  ',' '))
    return paragraph

def shade_cell(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)

docx=Document()
docx.core_properties.title='Evaluating Claims, Not Just Systems'
docx.core_properties.author=''
sec=docx.sections[0]
sec.top_margin=Inches(.72); sec.bottom_margin=Inches(.72); sec.left_margin=Inches(.78); sec.right_margin=Inches(.78)
normal=docx.styles['Normal']; normal.font.name='Aptos'; normal.font.size=Pt(10); normal.font.color.rgb=RGBColor(38,52,73)
normal.paragraph_format.space_after=Pt(6); normal.paragraph_format.line_spacing=1.12
for stylename,size,color in [('Heading 1',17,'10213C'),('Heading 2',13,'146B73'),('Heading 3',11,'3F5D7D')]:
    st=docx.styles[stylename]; st.font.name='Aptos Display'; st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor.from_string(color)
header=sec.header.paragraphs[0]; header.alignment=WD_ALIGN_PARAGRAPH.RIGHT; r=header.add_run('ARC PRIZE 2026 PAPER TRACK  •  SUBMISSION MANUSCRIPT'); r.font.size=Pt(8); r.font.color.rgb=RGBColor(96,112,135)
footerp=sec.footer.paragraphs[0]; footerp.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=footerp.add_run('Evaluating Claims, Not Just Systems  •  '); r.font.size=Pt(8); r.font.color.rgb=RGBColor(96,112,135)
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footerp._p.append(fld)
pic=docx.add_paragraph(); pic.alignment=WD_ALIGN_PARAGRAPH.CENTER; pic.add_run().add_picture(str(AS/'hero_banner_1680x840.jpg'),width=Inches(6.55))
p=docx.add_paragraph(); p.paragraph_format.space_before=Pt(12); p.paragraph_format.space_after=Pt(5)
r=p.add_run('Evaluating Claims, Not Just Systems'); r.bold=True; r.font.size=Pt(25); r.font.color.rgb=RGBColor(16,33,60)
p=docx.add_paragraph(); r=p.add_run('A Longitudinal Audit of an ARC Research Program'); r.font.size=Pt(17); r.font.color.rgb=RGBColor(20,107,115)
p=docx.add_paragraph('Submission-facing case study • Research Cycle 1'); p.runs[0].italic=True; p.runs[0].font.color.rgb=RGBColor(83,100,124)
p=docx.add_paragraph(); p.paragraph_format.left_indent=Inches(.12); p.paragraph_format.right_indent=Inches(.12)
r=p.add_run('Core contribution — '); r.bold=True; r.font.color.rgb=RGBColor(20,107,115); p.add_run('An auditable mapping between claim type, evidence type, and scientific disposition across one ARC-motivated research cycle.')
p=docx.add_paragraph(); r=p.add_run('Scope note. '); r.bold=True; p.add_run('T2T/S3 is excluded because its immutable execution timestamp remains unreconciled. The archive remains unchanged; no S3 result or disposition is used.')
p=docx.add_paragraph('ABSTRACT'); p.runs[0].bold=True; p.runs[0].font.color.rgb=RGBColor(20,126,134)
for paragraph in abstract:
    p=docx.add_paragraph(); add_docx_runs(p,paragraph)
p=docx.add_paragraph(); r=p.add_run('Keywords: '); r.bold=True; p.add_run('ARC-AGI; evaluation methodology; claim-evidence mapping; comparator design; generalization; retrospective case study')
docx.add_page_break()
# Body from Introduction onward.
i=body_start
while i<len(src):
    line=src[i]
    if not line.strip(): i+=1; continue
    m=re.match(r'!\[([^]]*)\]\(([^)]+)\)',line.strip())
    if m:
        p=docx.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(AS/'research_cycle_claim_audit_timeline.png'),width=Inches(6.65))
        p=docx.add_paragraph('Figure 1. Each retained claim is traced across hypothesis, mechanism, utility, comparator, generalization, and disposition. T2T/S3 is excluded from this submission version pending provenance reconciliation.')
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs: run.italic=True; run.font.size=Pt(8); run.font.color.rgb=RGBColor(83,100,124)
        i+=1; continue
    if line.startswith('|'):
        block=[]
        while i<len(src) and src[i].strip().startswith('|'):
            cells=[c.strip() for c in src[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{2,}:?',c or '-') for c in cells): block.append(cells)
            i+=1
        if block:
            n=max(map(len,block)); t=docx.add_table(rows=len(block),cols=n); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Light Shading Accent 1'
            for ri,row in enumerate(block):
                for ci,val in enumerate(row):
                    cell=t.cell(ri,ci); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP
                    p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(2); add_docx_runs(p,val)
                    for rr in p.runs:
                        rr.font.size=Pt(8)
                        if ri==0: rr.bold=True; rr.font.color.rgb=RGBColor(255,255,255)
                    if ri==0: shade_cell(cell,'17304F')
        continue
    if line.startswith('---'): i+=1; continue
    if line.startswith('#'):
        lev=len(line)-len(line.lstrip('#')); title=line[lev:].strip()
        docx.add_heading(title,level=min(3,max(1,lev-1))); i+=1; continue
    if line.startswith('>'):
        q=[]
        while i<len(src) and src[i].startswith('>'):
            q.append(src[i].lstrip('> ').strip()); i+=1
        p=docx.add_paragraph(); p.paragraph_format.left_indent=Inches(.18); p.paragraph_format.right_indent=Inches(.18); add_docx_runs(p,' '.join(q))
        for rr in p.runs: rr.bold=True; rr.font.color.rgb=RGBColor(18,60,80)
        continue
    if re.match(r'^\s*[-*] ',line):
        p=docx.add_paragraph(style='List Bullet'); add_docx_runs(p,line.strip()[2:]); i+=1; continue
    para=[line.strip()]; i+=1
    while i<len(src) and src[i].strip() and not src[i].startswith(('#','|','>','- ','* ','![','---')):
        para.append(src[i].strip()); i+=1
    p=docx.add_paragraph(); add_docx_runs(p,' '.join(para))

docx_path=PKG/'paper_editable.docx'
docx.save(docx_path)

# Bundle: only prepared submission files and generated assets; not the research archive.
zip_path=PKG/'submission_files.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(PKG.rglob('*')):
        if p.is_file() and p!=zip_path:
            z.write(p,p.relative_to(PKG.parent))
# print concise build manifest
for p in [PKG/'paper.pdf',vis_path,AS/'kaggle_card_560x280.png',AS/'hero_banner_1680x840.jpg',AS/'claim_ladder.png',AS/'disposition_map.png',AS/'research_cycle_claim_audit_timeline.png',AS/'scope_and_provenance.png',zip_path]:
    print(f'{p.relative_to(ROOT)}\t{p.stat().st_size:,} bytes')
print('Description words:',word_count)
