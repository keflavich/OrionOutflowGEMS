#!/bin/env python
import subprocess
import shutil
import glob
import argparse
import os

parser = argparse.ArgumentParser(description='Make latex files.')
parser.add_argument('--referee', default=False,
                    action='store_true', help='referee style?')
parser.add_argument('--texpath', default='/usr/texbin/',
                    help='path to pdflatex')
parser.add_argument('--infile', default='OrionGEMS.tex')
parser.add_argument('--outfile', default='auto')
parser.add_argument('--noclean', default=True, action='store_false')
parser.add_argument('--both', default=False, action='store_true')

args = parser.parse_args()


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

if args.both:
    args.referee = True
    do_everything()
    args.referee = False
    do_everything()
else:
    do_everything()
