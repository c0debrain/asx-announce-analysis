#!/usr/bin/python3

from announcement import *
from database_mysql import DatabaseMySQL
from multiprocessing import Pool


def process_announcement(row):

    database = DatabaseMySQL()

    announcement = Announcement(row[0], row[1], row[2], row[3], row[4])

    try:
        text = announcement.get_text("html")

        sql = "UPDATE company_announcements SET raw = '" + text + "' " + \
              "WHERE company_id = " + str(row[0]) + " and " + \
              "published_at = STR_TO_DATE('" + row[1].strftime('%Y-%m-%d %H:%M:%S') + "','%Y-%m-%d %H:%i:%s')"

        print(row[0], row[1])

        database.set_query(sql)
    except:
        pass

    return


def main():

    # Load list of asx stocks.
    database = DatabaseMySQL()

    # Load all announcements for this stock.
    sql = "Select * from company_announcements " + \
          "order by company_id, published_at DESC LIMIT 4"
    announcements = database.get_query_result(sql)

    pool = Pool(processes=7)  # how much parallelism?
    pool.map(process_announcement, announcements)


# Run Main.
if __name__ == '__main__':
    main()