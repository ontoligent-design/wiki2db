from wiki2db import Wiki2db


db_file = 'test.db'
w2b = Wiki2db(db_file, verbose=True)

src_file = 'pages-articles-sample.xml'
w2b.add_files([src_file])
w2b.import_xml_files()

# page_n = 0
# def grab_xml(page, src_file_id):
#     global page_n
#     page_n += 1
#     with open('pages/page-{}.xml'.format(page_n), 'w') as out:
#         out.write(page)
# w2b.import_xml('pages-articles-sample.xml', 1, grab_xml)

# file_name = file.split('/')[1]
# file_name2 = re.sub(r'\.bz2$', '', file_name)
# if not os.path.exists(file_name) and not os.path.exists(file_name2):
#     print('Copying', file_name)
#     os.system('cp {} ./{}'.format(file, file_name))
# if not os.path.exists(file_name2):
#     print('Uncompressing', file_name)
#     os.system('bzip2 -d {}'.format(file_name))
#     os.system('rm {}'.format(file_name))
# print('Importing', file_name2)
# import_xml(db_file, file_name2)
# print('Deleting', file_name2)
# os.system('rm {}'.format(file_name2))
# print('Done with', file_name2)
