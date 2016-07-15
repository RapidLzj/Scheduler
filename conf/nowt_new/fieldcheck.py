"""
    NOWT field check, compare with SDSS DR12 catalog
"""

import MySQLdb
#from matplotlib import pyplot as plt
#%matplotlib inline
import math
import time


if __name__ == "__main__" :
    conn = MySQLdb.connect("localhost", "uvbys", "uvbySurvey", "surveylog")
    cur = conn.cursor()

    sql_f = "select field_id, ra_deg, dec_deg from nowt_field"
    n_f = cur.execute(sql_f)
    tb_f = cur.fetchall()

    sql_s0 = "select count(*) as cnt, avg(radeg) as raavg, avg(decdeg) as decavg from dr12.sdssdr12 " +\
        "where radeg between %f and %f and decdeg between %f and %f"
    fov = 1.2
    fov2 = fov / 2.0
    fov_limit = 0.4
    sql_u0 = "update nowt_field set sdss_cnt = %d, sdss_ra_avg = %f, sdss_dec_avg = %f, tag = %d where field_id = %d"

    for f in tb_f :
        t0 = time.time()
        ra_f, dec_f = f[1], f[2]
        ra_scale = math.cos(dec_f / 180.0 * math.pi)
        sql_s = sql_s0 % (ra_f - fov2 / ra_scale, ra_f + fov2 / ra_scale, dec_f - fov2, dec_f + fov2)
        cur.execute(sql_s)
        tb_s = cur.fetchall()
        sdss_cnt, ra_avg, dec_avg = tb_s[0]
        if sdss_cnt < 100 :
            tag = 127
        elif abs(ra_avg - ra_f) > fov_limit / ra_scale or abs(dec_avg - dec_f) > fov_limit :
            tag = 63
        else :
            tag = 0
        sql_u = sql_u0 % (sdss_cnt, ra_avg, dec_avg, tag, f[0])
        cur.execute(sql_u)
        conn.commit()
        t1 = time.time()
        print ("Field %5d | %7d | %3d | %7.2f" % (f[0], sdss_cnt, tag, t1 - t0))


    print ('DONE')
    cur.close()
    conn.close()


