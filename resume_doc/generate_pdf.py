import numpy as np
import pdfkit
from PIL import Image, ImageDraw
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


def make_circle(file_path):
    # Open the input image as numpy array, convert to RGB
    img = Image.open(file_path).convert("RGB")
    npImage = np.array(img)
    h, w = img.size

    # Image.new form lib pil
    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    # draw circle (size, start angle > end angle, transparency
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    # split file with photo path without format
    new_file_path = file_path.split('.')[0]+'.png'
    Image.fromarray(npImage).save(new_file_path)
    return new_file_path


def make_paragraph(string,length, delimiter = ' '):
    words = string.split(delimiter)
    new_string = ''
    string_length = 0
    for word in words:
        if string_length+len(word)>length:
            new_string+=delimiter+'</br>'
            string_length = len(word)
        elif len(new_string)>0:
            new_string+=delimiter
            string_length+= len(word)+1
        new_string+=word
    return new_string


def make_new_lines(string_list,length):
    new_string = ''
    for string in string_list:
        new_string+=make_paragraph(string,length)
        new_string+='</br></br>'
    return new_string


def make_specialized_new_lines(nums_of_delimiters,delimiters,len_of_paragraph,collection):
    new_string = ''
    for dictionary in collection:
        counter = 0
        for value in dictionary.values():
            new_string += make_paragraph(value, len_of_paragraph)
            new_string += delimiters[counter]*nums_of_delimiters[counter]
            counter += 1
    return new_string


def create_pdf(first_name='',
                  last_name='',
                  phone_number='',
                  vacantion='',
                  last_jobs=[],
                  mail='',
                  educations=[],
                  photo_path = '',
                  final_file_path = 'demo.pdf'):

    if(photo_path!=''):
        new_photo_path = make_circle(photo_path)

    html_string = '''
    <!DOCTYPE html>
    <html>
    <head>
    <title></title>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
     <br/>
    <style type="text/css">
    <!--
        p {margin: 0; padding: 0;}	.ft10{font-size:40px;font-family:Times;color:#1f1d1d;}
        .ft11{font-size:22px;font-family:Times;color:#1f1d1d;}
        .ft12{font-size:23px;font-family:Times;color:#1f1d1d;}
        .ft13{font-size:11px;font-family:Times;color:#1f1d1d;}
        .ft14{font-size:17px;font-family:Times;color:#ffffff;}
        .ft15{font-size:13px;font-family:Times;color:#1f1d1d;}
        .ft16{font-size:15px;font-family:Times;color:#ffffff;}
        .ft17{font-size:12px;font-family:Times;color:#ffffff;}
        .ft18{font-size:14px;font-family:Times;color:#ffffff;}
        .ft19{font-size:11px;line-height:22px;font-family:Times;color:#1f1d1d;}
    -->
    </style>
    </head>
    <body bgcolor="#A0A0A0" vlink="blue" link="blue">
    <div id="page1-div" style="position:relative;width:893px;height:1263px;">
    <img width="893" height="1263" src="C:/Users/danyl/GitHub/python_bot_project_v_1/resume_doc/target001.png" alt="background image"/>'''+(
    '<img style="position:absolute;top:45px;left:33px;white-space:nowrap" width="251" height="251" src="'+new_photo_path+'''"
     alt="Your photo"/>''' if len(photo_path)>0 else '') + '''
    <p style="position:absolute;top:99px;left:367px;white-space:nowrap" class="ft10"><b>'''+first_name.upper()+' '+last_name.upper()+'''</b></p>
    <p style="position:absolute;top:170px;left:367px;white-space:nowrap" class="ft11">'''+vacantion.upper()+'''</p>
    <p style="position:absolute;top:429px;left:367px;white-space:nowrap" class="ft12"><b>ДОСВІД РОБОТИ</b></p>
    <p style="position:absolute;top:342px;left:35px;white-space:nowrap" class="ft14"><b>КОНТАКТНІ ДАННІ</b></p>
    <p style="position:absolute;top:498px;left:367px;white-space:nowrap" class="ft19">'''+make_specialized_new_lines([1,1,2],['</br>','</br>','</br>'],70,last_jobs)+'''</p>
    <p style="position:absolute;top:1004px;left:367px;white-space:nowrap" class="ft12"><b>ОСВІТА</b></p>
    <p style="position:absolute;top:1066px;left:367px;white-space:nowrap" class="ft19">'''+make_specialized_new_lines([1,1,2],[', ','</br>','</br>'],70,educations)+'''</p>
    <p style="position:absolute;top:412px;left:84px;white-space:nowrap" class="ft16">'''+phone_number+'''</p>
    <p style="position:absolute;top:464px;left:83px;white-space:nowrap" class="ft17">'''+mail+'''</p>
    </div>
    </body>
    </html>

    '''
    pdfkit.from_string(html_string, final_file_path, configuration=config, options={"enable-local-file-access": ""})

