from PIL import Image
import json
import argparse
import random
import math

# to do: allow custom font files. Font width may be dynamic if they use 
letter_width = 8
font_tilesheet = 'gbs-mono.png'
title = ''
author = ''
frontmatter = False
copyright = ''
showPageNumber = ''

gb_char_cols = 20
# to do: allow the user to change the height of a "page". 
# this 18 is a minimum
# maximum would be 819 given GB studio's limitations. This is still quite generous. 
# that would be about 16 kb of text on a screen. 
# maybe default should be 102 rows, or just shy of 2 kb of text per screen, a normal "page"
gb_char_rows = 100
# height of GB screen in 8 pixel rows
min_rows = 18

#to do: allow input by a text file or cli parameter
test_string='All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood. \n\n Everyone is entitled to all the rights and freedoms set forth in this Declaration, without distinction of any kind, such as race, colour, sex, language, religion, political or other opinion, national or social origin, property, birth or other status. Furthermore, no distinction shall be made on the basis of the political, jurisdictional or international status of the country or territory to which a person belongs, whether it be independent, trust, non-self-governing or under any other limitation of sovereignty.'

# to do: add the non-ASCII characters from the font sheet
character_map = {
    ' ': (0, 0),
    '!': (1, 0),
    '"': (2, 0),
    '#': (3, 0),
    '$': (4, 0),
    '%': (5, 0),
    '&': (6, 0),
    '\'': (7, 0),
    '(': (8, 0),
    ')': (9, 0),
    '*': (10, 0),
    '+': (11, 0),
    ',': (12, 0),
    '-': (13, 0),
    '.': (14, 0),
    '/': (15, 0),

    '0': (0, 1),
    '1': (1, 1),
    '2': (2, 1),
    '3': (3, 1),
    '4': (4, 1),
    '5': (5, 1),
    '6': (6, 1),
    '7': (7,1),
    '8': (8, 1),
    '9': (9, 1),
    ':': (10,1),
    ';': (11, 1),
    '<': (12, 1),
    '=': (13, 1),
    '>': (14, 1),
    '?': (15, 1),

    '@': (0, 2),
    'A': (1, 2),
    'B': (2, 2),
    'C': (3, 2),
    'D': (4, 2),
    'E': (5, 2),
    'F': (6, 2),
    'G': (7,2),
    'H': (8, 2),
    'I': (9, 2),
    'J': (10,2),
    'K': (11, 2),
    'L': (12, 2),
    'M': (13, 2),
    'N': (14, 2),
    'O': (15, 2),

    'P': (0, 3),
    'Q': (1, 3),
    'R': (2, 3),
    'S': (3, 3),
    'T': (4, 3),
    'U': (5, 3),
    'V': (6, 3),
    'W': (7,3),
    'X': (8, 3),
    'Y': (9, 3),
    'Z': (10,3),
    '[': (11, 3),
    '\\': (12, 3),
    ']': (13, 3),
    '^': (14, 3),
    '_': (15, 3),

    '`': (0, 4),
    'a': (1, 4),
    'b': (2, 4),
    'c': (3, 4),
    'd': (4, 4),
    'e': (5, 4),
    'f': (6, 4),
    'g': (7,4),
    'h': (8, 4),
    'i': (9, 4),
    'j': (10,4),
    'k': (11, 4),
    'l': (12, 4),
    'm': (13, 4),
    'n': (14, 4),
    'o': (15, 4),

    'p': (0, 5),
    'q': (1, 5),
    'r': (2, 5),
    's': (3, 5),
    't': (4, 5),
    'u': (5, 5),
    'v': (6, 5),
    'w': (7,5),
    'x': (8, 5),
    'y': (9, 5),
    'z': (10,5),
    '{': (11, 5),
    '|': (12, 5),
    '}': (13, 5),
    '~': (14, 5),

    '©': (9, 8)
    # Define coordinates for other characters here
}
# to do: consider adding variable width font, which may require a lot of extra code to handle

def run():
    global font_tilesheet
    global letter_width
    global test_string
    global gb_char_rows
    global title
    global author
    global frontmatter
    global showPageNumber

    inputTXT = ''
    text_tilesheet = Image.open(font_tilesheet)

    parser = argparse.ArgumentParser(description='This tool is part of a whole that allows a Game Boy to be used as an e-book reader. This python script consumes a text file and outputs a series of numbered PNG files that can be used as backgrounds in GB Studio. See the readme for the whole project for details.')
    parser.add_argument("-i","--input",  type=str, help="The input .txt file to be converted. Default is to convert a test string.", action="store")
    parser.add_argument("-r","--rows",  type=int, help="The height of a page of text, in rows of 8-pixel tall text. The minimum is 18. The maximum is 800. Default is 100. If you are adding a page number consider each page to have one additional row than what you enter here.", action="store")
    parser.add_argument("-t","--title",  type=str, help="The title of the book. Default blank.", action="store")
    parser.add_argument("-a","--author",  type=str, help="The author of the book. Default blank.", action="store")
    parser.add_argument("-f","--frontmatter", help="Include a first page consisting of the title and author of the work. Default false.", action="store_true")
    parser.add_argument("-c","--copyright",  type=str, help="Text of the copywrite statement on the frontmatter page. Default is none.", action="store")
    parser.add_argument("-p","--showPageNumber",  type=str, help="Show a page number on the page. Default is none. Options: top, bottom.", action="store")

    args = parser.parse_args()
    if args.input is not None:
        inputTXT = open(args.input, "r").read()
    else: 
        inputTXT = open('example_input.txt', "r").read()
    if args.rows is not None:
        gb_char_rows = args.rows
    if args.title is not None:
        title = args.title
    if args.author is not None:
        author = args.author
    if args.frontmatter is not None:
        frontmatter = True
    if args.copyright is not None:
        copyright = args.copyright
    if args.copyright is not None:
        showPageNumber = args.showPageNumber

    #pages = convert_to_pages(test_string)
    # right here, we take the input text and generate our list of lists, the pages. 
    pages = convert_to_pages_w_words(inputTXT)
    
    
    proj = json.loads(open('gb-json.gbsproj', "r").read())
    if title != '':
        proj["name"] = title
    else:
        proj["name"] = 'New Book'
    if author != '':
        proj["author"] = author
    # Create a background and scene template
    backgroundTemplate = proj["backgrounds"][0]
    backgroundTemplate["width"] = gb_char_cols
    backgroundTemplate["height"] = gb_char_rows
    backgroundTemplate["imageWidth"] = gb_char_cols * letter_width
    backgroundTemplate["imageHeight"] = gb_char_rows * letter_width

    sceneTemplate = proj["scenes"][0]
    sceneTemplate["width"] = gb_char_cols
    sceneTemplate["height"] = gb_char_rows
    
    pageIdList = []

    startScenes = len(proj["scenes"])

    # if a front page is to be generated, make it and add it to the 
    # first location in pages
    totalPages = len(pages)
    pageNumber = 0
    if frontmatter:
        pages = generateFrontMatter(pages,author,title,copyright)

    # loop through the "pages" and convert them to images. Then add those images as 
    # backgrouns to the gb studio project
    for page in pages:
        pageNumber = pageNumber + 1
        if showPageNumber != '':
            if pageNumber == 1 and frontmatter:
                pageNumber = 0
                frontmatter = False
                # don't add a page number to the frontmatter
                # setting frontmatter to false means we won't end up in a death loop
            else:
                pageNumberString = str(pageNumber)+' / '+str(totalPages)
                if showPageNumber == 'top':
                    page.insert(0,addStringToRow(centerString(pageNumberString)))
                elif showPageNumber == 'bottom':
                    page.append(addStringToRow(centerString(pageNumberString)))
        
        txt_img_array = build_image_array(text_tilesheet,page)
        output = stitch_images(txt_img_array, letter_width)
        fileName = 'page'+str(pageNumber)
        output.save(fileName+'.png')
        # add the file output to a background
        newBackground = backgroundTemplate
        newBackground["filename"] = fileName+'.png'
        newBackground["name"] = fileName
        newBackground["symbol"] = 'bg_'+fileName
        newBackground["id"] = generateGBstudioId()
        #now add a scene
        newScene = sceneTemplate
        newScene["backgroundId"] = newBackground["id"]
        newScene["id"] = generateGBstudioId()
        newScene["name"] = title
        newScene["x"] = newScene["x"] * pageNumber * 100
        pageIdList.insert(pageNumber,newScene["id"])
        newScene["symbol"] = 'scene_'+str(startScenes+pageNumber)# set the scene symbol, don't duplicate what is in there
        # add the background and scene to the list
        proj["backgrounds"].append(newBackground)
        proj["scenes"].append(newScene)
    with open(proj["name"]+'.gbsproj', 'w', encoding='utf-8') as f:
        json.dump(proj, f, ensure_ascii=False, indent=4)
### STILL TO DO
    # we need to modify a script that has a switch statement that lets us "change scene" to each page
    # Also to do in the demo file, create an interface to let readers put in a number and go to that page. Should default to the current page. 


### TEXT Functions

# takes a text string and converts it to a 3d array of pages, rows, and characters
# This is not actually used in the final program
def convert_to_pages(input):
    result = []
    page = []
    row = []
    col_count = 0
    row_count = 1
    
    for char in input:
        skip_char=False
        col_count = col_count + 1
        # \r and \n make new lines, as does running out of characters on the row
        if char == '\n' or char == '\r':
            skip_char=True
            while col_count < gb_char_cols-1:
                row.append(' ')
                col_count = col_count + 1
        if col_count >= gb_char_cols:
            col_count = 1
            row_count = row_count + 1
            if row_count >= gb_char_rows:
                row_count = 1
                result.append(page)
                page=[]
            print(row)
            page.append(row)
            row = []
        if skip_char==False:
            row.append(char)
        else:
            row.append(' ')
    if col_count < gb_char_cols:
        while col_count < gb_char_cols-1:
            col_count = col_count + 1
            row.append(' ')
            
    #print(row)
    page.append(row)
    # here, we need to fill out the last page to a full height
    result.append(page)

    return result



# This does its best to split the string more efficiently, breaking up long words onto multiple lines
def convert_to_pages_w_words(input):
    global gb_char_rows
    global gb_char_cols
    global showPageNumber
    result = []
    page = []
    row = []
    words = input.split(' ')
    
    def addWordToRow(word):
        nonlocal row
        global gb_char_cols
        for char in word:
            if char == '\n' or char == '\r':
                newLine()
            else:
                row.append(char)
        if len(row) < gb_char_cols:
            row.append(' ')

    def newLine():
        nonlocal row
        nonlocal page
        nonlocal result
        global gb_char_rows
        global gb_char_cols

        while len(row) < gb_char_cols:
            row.append(' ')
        print(row)
        page.append(row)
        row=[]
        if len(page) >= gb_char_rows:
            result.append(page)
            page = []
    
    for word in words:
        #how many more spots in the row?
        spots = gb_char_cols - len(row)
        # if the word is longer than spots remaining then we have to break it up or something
        if len(word) > spots:
            if (word.find('\n')>=0 and word.find('\n') < spots) or (word.find('\r')>=0 and word.find('\r') < spots):
                # the word has a new line, so we just add it
                addWordToRow(word)
            elif len(word) <= 5:
                #it's short so just go to a new line
                newLine()
                addWordToRow(word)
            else:
                #long ass word
                first_half = left(word, spots-1)
                last_half = right(word, len(word)-spots+1 )
                # don't leave a tiny snippet on the next line. Always make it at least 3 characters
                while len(last_half) < 3:
                    last_half = right(first_half,1) + last_half
                    first_half = left(first_half,len(first_half)-1)
                if len(first_half) < 3:
                    # first half is too short, just go to the next line
                    newLine()
                    last_half = word
                else:
                    #if first_half.find('-')>=0:
                        #it already has a hyphen, make this the split point, undoing what we already did
                    #    first_half = left(word,word.index('-'))
                    #    last_half = right(word,len(first_half))
                    #else:
                    #    #add hyphen and the word
                    #    first_half = first_half+'-'
                    first_half = first_half+'-'
                    addWordToRow(first_half)
                    newLine()
                # add the last half of the word to the next line, dealing with extremely long words appropriately
                if len(last_half) > gb_char_cols:
                    #wow this is a long word
                    while len(last_half) > gb_char_cols:
                        mid_bit = left(last_half,gb_char_cols-1)
                        last_half = right(last_half,len(last_half)-gb_char_cols+1)
                        addWordToRow(mid_bit)
                        newLine()
                else:
                    addWordToRow(last_half)
        else:
            #there is room and we don't have to do anything fancy
            addWordToRow(word)
        #have we run out of room on this row?
        if gb_char_cols - len(row) == 0:
            newLine()
    while len(row) < gb_char_cols:
        row.append(' ')

    print(row)
    page.append(row)
    while len(page) < min_rows:
        page.append(emptyRow())
    result.append(page)

    return result

def get_character_coords(char):
    if char in character_map:
        x , y = character_map[char]
        x = x * letter_width
        y = y * letter_width
        return (x,y)
    else:
        return None

def generateFrontMatter(pages,author,title,copyright):
    global gb_char_cols
    global min_rows

    titleRows = splitLongStringBetweenRows(title)
    authorRows = splitLongStringBetweenRows('by '+author)
    copyRows = splitLongStringBetweenRows('© '+copyright)
    page = []
    availableBuffer = min_rows - (len(titleRows) + len(authorRows) + len(copyRows))
    buffer = 0
    if math.floor(availableBuffer/2) > buffer:
        buffer = math.floor(availableBuffer/2)
    page.extend(titleRows)
    if buffer > 0: page.extend(genBufferRows(buffer))
    page.extend(authorRows)
    if buffer > 0: page.extend(genBufferRows(buffer))
    page.extend(copyRows)
    for row in page:
        print(row)
    pages.insert(0, page)
    return pages

def splitLongStringBetweenRows(string):
    global gb_char_cols

    output = []
    row = []

    if len(string) <= gb_char_cols:
        row = addStringToRow(centerString(string))
        output.append(row)
        return output
    else:
        words = string.split(' ')
        line = ''
        for word in words:
            temp_line = line+' '+word
            if len(temp_line) > gb_char_cols:
                row = addStringToRow(centerString(line))
                output.append(row)
                row = []
                line = word
            else:
                line = temp_line
        row = addStringToRow(centerString(line))
        output.append(row)
        return output
    
def genBufferRows(buffer):
    output = []
    i = 0
    while i < buffer:
        output.append(emptyRow())
        i += 1
    return output

def addStringToRow(string):
    row = []
    for char in string:
        row.append(char)
    return row

def emptyRow():
    global gb_char_cols
    row = []
    i = 0
    while i < gb_char_cols:
        row.append(' ')
        i += 1
    return row;

def centerString(string):
    global gb_char_cols
    # this fails if the string is longer than gb_char_cols
    padding = gb_char_cols - len(string)
    front = 0
    back = 0
    backOffset = 0
    if padding % 2 != 0: # is even number
        padding = padding - 1
        backOffset = 1
    front = padding/2
    back = (padding/2) + backOffset
    i = 0
    output = ''
    while i < front:
        output = output+' '
        i += 1
    output = output+string
    i = 0
    while i < back:
        output = output+' '
        i += 1
    return output
        
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def generateGBstudioId():
    hex_chars = '0123456789abcdef'
    hex_id = ''
    lengths = [8, 4, 4, 4, 12]
    
    for length in lengths:
        hex_id += ''.join(random.choices(hex_chars, k=length))
        hex_id += '-' if length != 12 else ''
    
    return hex_id

### IMAGE FUNCTIONS

# consume a "page" of text and convert it to an array of png images.
def build_image_array(text_tilesheet, page_array):
    global letter_width
    output = []
    for row in page_array:
        output_row = []
        for char in row:
            coords = get_character_coords(char)
            letter_img = getLetter(text_tilesheet, coords, letter_width)
            output_row.append(letter_img)
        output.append(output_row)
    return output

#get the png of a character
def getLetter(tilesheet, letter_coords, width):
    # Open the PNG file
    #image = Image.open(png_file)
    tilesheet
    
    # Extracting coordinates
    left, top = letter_coords
    right = left + width
    bottom = top + width
    
    # Crop the rectangle
    letter = tilesheet.crop((left, top, right, bottom))
    
    return letter

# Stitch a 2d array of images into one png image
def stitch_images(image_array, width):
    # Get the dimensions of the image array
    rows = len(image_array)
    cols = len(image_array[0])
    
    # Calculate the dimensions of the stitched image
    stitched_width = cols * width
    stitched_height = rows * width
    
    # Create a new blank image to stitch the images onto
    stitched_image = Image.new('RGB', (stitched_width, stitched_height))
    
    # Iterate over the image array and paste each image onto the stitched image
    for i in range(rows):
        for j in range(cols):
            # Calculate the position to paste the current image
            x_offset = j * width
            y_offset = i * width
            # Paste the current image onto the stitched image
            stitched_image.paste(image_array[i][j], (x_offset, y_offset))
    
    return stitched_image

# Defining main function 
def main(): 
    run()
  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 