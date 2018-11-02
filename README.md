# wiki2db

A simple library to migrate Wikipedia's XML export files into
a SQLite database. See `test.py` for an example of how to use
it.

## Notes Wikipedia Export Data

Some information about Wikipedia's XML export files.

### Important URLs

* https://dumps.wikimedia.org/enwiki/latest/

### All file types in dump directory

```txt
Filename:<1:LANG_WIKI>-<1:DATE_SLICE>-<+:FILE_TYPE>.<1:DATA_FORMAT>.<?:ARCHIVE_FORMAT>
LANG_WIKI:  e.g. enwiki
DATE_SLICE: e.g. latest, 20110115 (YYYYMMDD)
FILE_TYPE:
abstract                            xml     gz
abstractN                           xml     gz
all-titles                          ---     gz
all-titles-in-ns0                   ---     gz
category                            sql     gz
category-links                      sql     gz
external-links                      sql     gz
flagged-pages                       sql     gz
flagged-revs                        sql     gz
geo-tags                            sql     gz
image                               sql     gz
imagelinks                          sql     gz
iwlinks                             sql     gz
langlinks                           sql     gz
md5sums                             txt     --
page                                sql     gz
page_props                          sql     gz
page_restrictions                   sql     gz
pagelinks                           sql     gz

pages-articles-multistream-index    txt     ---
pages-artciles-multistream          xml     bz2
pages-articles                      xml     bz2
pages-artcilesN                     xml-p*  bz2
pages-logging                       xml     bz2
pages-loggingN                      xml     bz2
pages-meta-current                  xml     bz2
pages-meta-currentN                 xml-p*  bz2
pages-meta-historyN                 xml-p*  bz2

protected_titles                    sql     gz
redirect                            sql     gz
sha1sums                            txt     --
site_stats                          sql     gz
siteinfo_namespaces                 json    gz
sites                               sql     gz
stub-articles                       xml     gz
stub-articlesN                      xml     gz
stub-meta-current                   xml     gz
stub-meta-currentN                  xml     gz
stub-meta-history                   xml     gz
stub-meta-historyN                  xml     gz
templatelinks                       sql     gz
user_groups                         sql     gz
wbc_entity_usage                    sql     gz
```

## Hierarchy of `page` files

```txt
pages
    articles
        DEFAULT
        multistream
            DEFALT
            index
    meta
        current (N)
        history (N)
    logging (N)
```

### Dump Formats

Source: https://meta.wikimedia.org/wiki/Data_dumps/Dump_format

**pages-articles.xml**: Contains current version of all article pages, templates, and other pages
Excludes discussion pages ('Talk:') and user "home" pages ('User:'). Recommended for republishing of content.

**pages-meta-current.xml**: Contains current version of all pages, including discussion and user "home" pages.

**pages-meta-history.xml**: Contains complete text of every revision of every page (can be very large!) Recommended for research and archives.

## Notes for Capstones

* Trust
  * Should focus on pages-meta-history
  * May want to sample non-blocked pages
* Cochrane
  * Should focus on pages-articles
* Both
  * Filter by category
