from astroquery.ned import Ned
result_table = Ned.get_table("m31", table='redshifts')
result_table.show_in_browser(browser = 'chrome',jsviewer = True)
