#!/bin/env python
import subprocess
import shutil
import glob
import argparse
import os
import tarfile

parser = argparse.ArgumentParser(description='Make latex files.')
parser.add_argument('--referee', default=False,
                    action='store_true', help='referee style?')
parser.add_argument('--texpath', default='/usr/texbin/',
                    help='path to pdflatex')
parser.add_argument('--infile', default='OrionGEMS.tex')
parser.add_argument('--outfile', default='auto')
parser.add_argument('--noclean', default=True, action='store_false')
parser.add_argument('--both', default=False, action='store_true')
parser.add_argument('--arxiv', default=False, action='store_true')

args = parser.parse_args()

def do_arxiv():
    filelist = [
        'Orion.bib',
        'OrionGEMS.bbl',
        'OrionGEMS.tex',
        'Orion_figures1.tex',
        'Orion_figures2.tex',
        'Orion_table1.tex',
        'Orion_table2.tex',
        'aa.cls',
        'apj_w_etal.bst',
        'deluxetable.sty',
        'fig10_cartoon.pdf',
        'fig11_Silvia_model_on_GEMS2.pdf',
        'fig12_density_100yrs.png',
        'fig13_x_velocity_100yrs.pdf',
        'fig14_y_velocity_100yrs.pdf',
        'fig15_z_velocity_100yrs.pdf',
        'fig16_temperature_100yrs.png',
        'fig17_jetstar.pdf',
        'fig18_diskshadow.pdf',
        'fig1_H2_FeII_GSAOI.pdf',
        'fig2.pdf',
        'fig3_fingers_on_medianH2.pdf',
        'fig4_H2_FeII_Ks_color.pdf',
        'fig5_H2_2013_1999.pdf',
        'fig6_H2_PMs_fingers.pdf',
        'fig7_FeII_PMs_fingers.pdf',
        'fig8_H2_HVCC.pdf',
        'fig9_FeII_HVCC.pdf',
    ]
    if not os.path.isdir('arxiv'):
        os.mkdir('arxiv')
    tf = tarfile.TarFile("arxiv.tar.gz", mode="w")
    for fn in filelist:
        if 'pdf' in fn:
            os.system('gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=arxiv/{0} {0}'.format(fn))
            tf.add('arxiv/{0}'.format(fn), arcname=fn)
        else:
            tf.add(fn)
    tf.close()
    shutil.rmtree('arxiv')


def do_everything():
    if not args.noclean:
        for globstr in ("OrionGEMS*.aux", "OrionGEMS*.bbl", "OrionGEMS*.blg",
                        "OrionGEMS*.dvi", "OrionGEMS*.log", "OrionGEMS*.lot",
                        "OrionGEMS*.lof"):
            for fn in glob.glob(globstr):
                os.remove(fn)

    PDFLATEX=os.path.join(args.texpath,'pdflatex')
    pdflatex_args = "-halt-on-error -synctex=1 --interaction=nonstopmode".split()

    BIBTEX = os.path.join(args.texpath, 'bibtex')

    with open('OrionGEMS.tex','r') as f:
        preface = ["%"+line if "documentclass" in line else line
                   for line in f.readlines()]

    with open('OrionGEMS.tex','w') as aa:
        if args.referee:
            aa.write('\documentclass[referee]{aa}\n')
            aa.writelines(preface)
        else:
            aa.write('\documentclass{aa}\n')
            aa.writelines(preface)

    pdfcmd = [PDFLATEX] + pdflatex_args + [args.infile]
    bibcmd = [BIBTEX, args.infile.replace(".tex","")]

    subprocess.call(pdfcmd)
    subprocess.call(bibcmd)
    subprocess.call(pdfcmd)
    subprocess.call(bibcmd)
    subprocess.call(pdfcmd)

    if args.outfile == 'auto':
        outprefix = 'OrionGEMS_referee' if args.referee else 'OrionGEMS'
    else:
        outprefix = os.path.splitext(args.outfile)[0]

    # Don't move unnecessarily; messes with Skim.app (maybe?)
    if os.path.split(os.path.basename(outprefix))[0] != 'OrionGEMS':
        shutil.move("OrionGEMS.pdf",outprefix+".pdf")


    gscmd = ["gs",
             "-dSAFER",
             "-dBATCH", 
             "-dNOPAUSE",
             "-sDEVICE=pdfwrite",
             "-sOutputFile={0}_compressed.pdf".format(outprefix),
             "{0}.pdf".format(outprefix)]

    subprocess.call(gscmd)

if args.arxiv:
    do_arxiv()
elif args.both:
    args.referee = True
    do_everything()
    args.referee = False
    do_everything()
else:
    do_everything()
