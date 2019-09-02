# files-finder
Map files in your PC in a big table, filter from it by size, date, substring in filename, tags

This project is in constant change, but its purpose is to produce a table containing files important info, with fields you can complete yourself

The current table layout has:

- ID
- Path
- Filename
- Extension
- Date
- Bytes
- Tag List
- Status
- Comment

The code is run in 3 modes:

Mapping Mode - it will take a list of parent folders and return all the files on folder and subfolders contained on those parent folders, organized according to the table described above.

Filtering Mode - given the main table with all files necessary, this mode will ask for filters on Parent Folder, Extension, Tags and (if activated) a Regular Expression over the filename. It will then return another table, containing just then filtered files.

Merge Mode - if you make alteration on the filtered table, they can then be merged to the main folder. The code will use filename and path to find the files from filtered table on main table.

The project can be used for many uses, for example:

Produce headers for experiments. In this case, you can map the data parent folder, then filter for anything related to this experiment.
Do a state-of-art review on a topic. Find all papers with certain tags and produce a table where you can add your comments as you read the papers
Find copies of a file inside any of the mapped folders or subfolders
OBS.: Tags, Status and Comments are completed manually. But external codes or modifications to the project can be done, such data those fields can be completed automatically, or semi-automatically
