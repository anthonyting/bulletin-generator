import docx as d
from .. import inputs
from math import ceil

def _deleteParagraph(paragraph: d.text.paragraph.Paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None

def makePage(document: d.Document, I: inputs.Inputs):
    foundFirst = False
    index = 0

    # count number of words to put in
    # textCount = 2*I.num_of_announcements + I.num_of_announcements # start by including ": " and "\n"
    # i = 0
    # while (i < I.num_of_announcements):
        # textCount += len(I.announcements[i]['bold']) + len(I.announcements[i]['text'])
        # i += 1
        
    # a special arbitrary formula to calculate line spacing

    # C = [0.00983392753659840038182871069238899508491158485413,
        # 0.00002112182423746888915161434852052479982376098633,
        # -0.00015938786376083887916244030691359512275084853172,
        # -0.08095023980842638855470738690200960263609886169434,
        # -0.02451201689433830585573836913226841716095805168152,
        # 9.16630170781075825914285815088078379631042480468750]
    # x = I.num_of_announcements
    # y = textCount

    # lineSpacing = C[0]*x**2 + C[1]*y**2 + C[2]*x*y + C[3]*x + C[4]*y + C[5]

    totalNumOfTextCounts = []
    for i in range(I.num_of_announcements):
        newLines = I.announcements[i]['text'].count('\n')
        thisNumOfLines = (len(I.announcements[i]['bold']) + len(I.announcements[i]['text']) + 2 - newLines)/30 # max line length ~= 30
        totalNumOfTextCounts.append(ceil(thisNumOfLines) + newLines) # a partially filled line counts as a full line

    constant = 0.028 * I.num_of_announcements # the paragraph spacing in between each announcement -> can be made into a proportion eventually

    maxLines = 36 # max number of lines in a page if lineSpacing = 1
    lineSpacing = (maxLines / (sum(totalNumOfTextCounts))) - constant

    # apply text
    for paragraph in document.paragraphs:
        if (not foundFirst and paragraph.text == "*ANN_START*"):
            foundFirst = True

        if (paragraph.text == "*ANN_START*"):
            _deleteParagraph(paragraph)
        elif (paragraph.text == "*ANN_END*"):
            _deleteParagraph(paragraph)
            return  
        elif (foundFirst):
            if (index < I.num_of_announcements):
                # each paragraph is set to have two runs
                paragraph.runs[0].text = f"{I.announcements[index]['bold']}: "
                paragraph.runs[1].text = I.announcements[index]["text"]
                paragraph.runs[1].font.name = "Times New Roman"
                # this line relies on the fact that chinese text font does not change in the api.
                paragraph.paragraph_format.line_spacing = lineSpacing
            else:
                _deleteParagraph(paragraph)
            index += 1