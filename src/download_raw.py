#!/usr/bin/python3

from announcement import *
from database_mysql import DatabaseMySQL
from multiprocessing import Pool

database = DatabaseMySQL()


def process_announcement(row):

    if row[5] == "":
        announcement = Announcement(row[0], row[1], row[2], row[3], row[4])

        try:
            text = announcement.get_text("html")

            sql = "UPDATE company_announcements SET raw = '" + text + "' " + \
                  "WHERE company_id = " + str(row[0]) + " and " + \
                  "published_at = STR_TO_DATE('" + row[1].strftime('%Y-%m-%d %H:%M:%S') + "','%Y-%m-%d %H:%i:%s')"

            database.set_query(sql)
        except:
            pass

    return


def main():

    # Load all announcements.
    sql = "Select * from company_announcements " + \
          "WHERE published_at > STR_TO_DATE('2012-07-01','%Y-%m-%d') " + \
          "order by company_id, published_at DESC"

    announcements = database.get_query_result(sql)

    pool = Pool(processes=40)
    pool.map(process_announcement, announcements)


# Run Main.
if __name__ == '__main__':
    main()
