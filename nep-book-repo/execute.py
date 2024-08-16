from thuprai import ThupraiScrapper, BooksDetails

execute_ThupraiScrapper = False

if execute_ThupraiScrapper:
    ts = ThupraiScrapper()
    ts.get_title_and_links(iter_range=136)

bd = BooksDetails()
bd.execute()


