# LRMS IEEE Paper - Build and Submission Checklist

## How to Compile (Windows PowerShell)

1. Install a LaTeX distribution (MiKTeX or TeX Live) and ensure `pdflatex` and `bibtex` are in PATH.
2. From the `paper/` folder run:
   ```powershell
   pdflatex lrms_ieee.tex
   bibtex lrms_ieee
   pdflatex lrms_ieee.tex
   pdflatex lrms_ieee.tex
   ```
3. Output: `lrms_ieee.pdf`

If you see missing package prompts (MiKTeX), allow on-the-fly install or preinstall packages: `graphics`, `hyperref`, `tikz`, `booktabs`, `cite`, `listings`.

## Where to Edit
- Author/affiliation/email: in `\author{...}` of `lrms_ieee.tex`.
- Abstract and keywords: `\begin{abstract}...` and `\begin{IEEEkeywords}...`.
- References: add to `refs.bib` and cite with `\cite{key}`.
- Figures/Tables: edit TikZ diagrams and tables in the .tex file.

## Submission Checklist (IEEE conference style)
- [ ] Title, author names, affiliations correct
- [ ] Abstract (150–250 words)
- [ ] Index Terms (3–6 keywords)
- [ ] Sections: Intro, Related Work, Method/Architecture, Implementation/DB Design, Results/Evaluation, Discussion, Conclusion
- [ ] At least 1 architecture figure and 1 ER diagram
- [ ] Tables have captions above; figures have captions below
- [ ] All figures/tables referenced from text (Fig. 1, Table I)
- [ ] References compiled (no `?` marks); all URLs accessible
- [ ] No overfull hboxes (LaTeX warnings minimized)
- [ ] Acknowledgment and Ethics/Data Availability statements (if required)
- [ ] Spell-check and grammar pass

## Common Edits for Your Project
- Update sample dataset size and metrics in Table “Summary of database objects” if you change DB objects.
- Add performance numbers (query timing, page load) in Evaluation, if available.
- Add any screenshots as figures (convert to PDF/PNG and include with `\includegraphics`).

## Troubleshooting
- BibTeX shows `?` for citations: ensure you ran `bibtex lrms_ieee` and keys in `refs.bib` match `\cite{...}`.
- Missing package errors: install via MiKTeX console or `tlmgr` (TeX Live).
- TikZ errors: ensure `tikz` is installed; comment out TikZ figures if needed to compile quickly.
