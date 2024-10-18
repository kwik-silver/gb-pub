# gb-pub

This tool is a work in progress that will eventually allow a Game Boy to be used as an e-book reader. 

This python script consumes a text file and outputs a series of numbered PNG files that can be used as backgrounds in GB Studio. Currently only supports a monospace font.

Experimentally, it also edits a GB Studio project file, intended to include the navigation functionality through the ebook. This is a work in progress as of last commit. 

##Arguments:

-i INPUT, --input INPUT The input .txt file to be converted. Default is to convert a test string.

-r ROWS, --rows ROWS  The height of a page of text, in rows of 8-pixel tall text. The minimum is 18. The maximum is
                        800. Default is 100. If you are adding a page number consider each page to have one
                        additional row than what you enter here.

-t TITLE, --title TITLE
                        The title of the book. Default blank.

-a AUTHOR, --author AUTHOR
                        The author of the book. Default blank.

-f, --frontmatter     Include a first page consisting of the title and author of the work. Default false.

-c COPYRIGHT, --copyright COPYRIGHT
                        Text of the copywrite statement on the frontmatter page. Default is none.

-p SHOWPAGENUMBER, --showPageNumber SHOWPAGENUMBER
                        Show a page number on the page. Default is none. Options: top, bottom.
