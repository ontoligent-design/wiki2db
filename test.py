from wiki2db import Wiki2db

# Specify a target database. Note that SQLite will
# create the file if it does not exist.
db_file = 'test.db'

# Create an instance of the Wiki2db object.
w2b = Wiki2db(db_file)

# Define one or more input files in 
# Wikipedia's XML export format. Open the sample
# file to see how these are structured.
src_file = 'pages-articles-sample.xml'

# Add the file name (provided in a list) to the database.
# The file name is added to keep track of it in the case
# when many files are being added.
w2b.add_files([src_file])

# Import the contents of the file into the database.
# Once done, opent the SQLite database in your favorite
# SQLite viewer, such as DB Browser or from the command line.
w2b.import_xml_files()