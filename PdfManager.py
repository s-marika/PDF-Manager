import PyPDF2


def pdf_merger(filelist, savepath):
    merger = PyPDF2.PdfFileMerger()
    for f in filelist:
        merger.append(f)
    merger.write(savepath)
    merger.close()


def pdf_spliter(filename, start_page2, savepath):
    merger = PyPDF2.PdfFileMerger()
    merger.append(filename,
                  pages=PyPDF2.pagerange.PageRange(':{}'.format(start_page2 - 1)))
    merger.write(savepath)
    merger.close()

    merger = PyPDF2.PdfFileMerger()
    merger.append(filename,
                  pages=PyPDF2.pagerange.PageRange('{}:'.format(start_page2 - 1)))
    merger.write(savepath)
    merger.close()


def pdf_extractor(filename, start, stop, savepath):
    merger = PyPDF2.PdfFileMerger()
    merger.append(filename,
                  pages=PyPDF2.pagerange.PageRange('{}:{}:'.format(start - 1, stop)))
    merger.write(savepath)
    merger.close()
