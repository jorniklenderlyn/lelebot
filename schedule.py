import fitz
import os
import requests
from PIL import Image


boxOfImages = []


class Schedule:
    def __init__(self, FILENAMEpdf):
        self.FILENAMEpdf = FILENAMEpdf


    def download_pdf(self):
        def check_url(checking_url):
            return checking_url[-1] == "f"


        def get_new_url():
            global html, ind, url_list, flag_url
            new_url = URL
            if ROADFOLDER in html:
                len_html = len(html)
                html = html[html.index(ROADFOLDER):]
                for item in range(len_html):
                    if html[item] != chr(34):
                        new_url += html[item]
                    else:
                        if check_url(new_url):
                            if flag_url:
                                url_list.append(new_url)
                                html = html[item + 1:]
                                get_new_url()
                        else:
                            break


        global html, ind, url_list, flag_url
        flag_url = True
        url_list = list()
        URL = 'http://https.нашашкола27.рф/'
        ROADFOLDER = 'wp-content/uploads/shedule/'
        html = requests.get(URL).text
        ind = html.index(ROADFOLDER)
        html = html[ind:]
        get_new_url()
        request = requests.get(url_list[-1], stream=True)
        with open(self.FILENAMEpdf, 'wb') as file:
            file.write(request.content)


    def delete_pdf_imades(self):
        pass


    def get_classes(self):
        text = self.get_text_pdf()
        box = []
        for i in text.split('\n'):
            if '.' in i:
                iq = i.replace('/', '').replace('.', '').replace(' ', '')
                if any([j.isdigit() for j in (iq)]) and iq.isalnum():
                    if len(i.replace(' ', '')) < 8:
                        if len(i.split('.')) == 2 and len(i.split('.')[0]) == 2 and len(i.split('.')[1]) == 2:
                            pass
                        else:
                            if int(i.split('.')[0]) > 9:
                                box.append(i.strip())
                            else:
                                i = i.split()[0]
                                box.append('.'.join(i.replace('.', ' ').strip().split()))
        return box


    def get_class_groupes(self, clas):
        lst = []
        for i in self.get_classes():
            if i.startswith(clas):
                lst.append(i)
        return lst


    def get_phooto_path(self, clas):
        pass


    def get_num_of_borders(self, text):
        numOfborders = 0
        if 'кабинет' in text.lower() or 'каб.' in text.lower():
            numOfborders += 1
        if 'учитель' in text.lower() or 'уч.' in text.lower():
            numOfborders += 1
        return numOfborders


    def get_text_pdf(self):
        txt = ''
        pdf_document = self.FILENAMEpdf
        doc = fitz.open(pdf_document)
        page1 = doc.loadPage(0)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(1)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(2)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(3)
        txt += '\n' + page1.getText("text")
        return txt


    def get_indent(self, pixMap, width, height):
        box = []
        for i in range(height):
            tok = 0
            for j in range(width):
                if pixMap[j, i] == (0, 0, 0):
                    tok += 1
            if tok > 500:
                box.append(i)
        return (box[0], box[-1])


    def make_lessonslists(self, classes, filePath, pdffile):
        global boxOfImages
        try:
            os.makedirs("data")
        except:
            pass

        doc = None
        file = pdffile
        doc = fitz.open(file)
        for i in range(len(doc)):
            first_page = doc[i]

            image_matrix = fitz.Matrix(fitz.Identity)
            image_matrix.preScale(2, 2)

            pix = first_page.getPixmap(alpha=False, matrix=image_matrix)
            boxOfImages.append(f'{i}.jpg')
            pix.writePNG(f'data/{i}.jpg')

        NUMBEROFCLASS = 0
        for _filename_ in boxOfImages:
            img = Image.open(f"{filePath}{_filename_}")
            pixMap = img.load()
            width, height = img.size

            listTemplates = []
            boxTime2 = [False]
            FIRSTindent, SECONDindent = self.get_indent(pixMap, width, height)
            for i in range(FIRSTindent, SECONDindent):
                boxTime = []
                tok = 0
                for j in range(width):
                    if pixMap[j, i] != (0, 0, 0):
                        boxTime.append(True)
                    else:
                        tok += 1
                        boxTime.append(False)
                # print(boxTime)
                if (not all(boxTime2) and all(boxTime)) or (all(boxTime2) and not all(boxTime)):
                    listTemplates.append(i)
                boxTime2 = boxTime.copy()
            listTemplates.extend([FIRSTindent, SECONDindent])
            listTemplates.sort()

            try:
                os.makedirs("data/data")
            except:
                pass

            def getY(y):
                chek = 0
                border = set()
                variableBorder = None
                for i in range(width):
                    if pixMap[i, y] == (0, 0, 0):
                        variableBorder = i
                    elif variableBorder:
                        border.add(variableBorder)
                return sorted(list(border))

            BORDERNUM = self.get_num_of_borders(self.get_text_pdf())
            for i in range(len(listTemplates) // 2):
                try:
                    if 1:
                        y0 = listTemplates[i * 2]
                        y1 = listTemplates[i * 2 + 1]
                        boxBorder = getY(y0 + 3)
                        im0 = img.crop((boxBorder[0], y0, boxBorder[2], y1))
                        for k in range((len(boxBorder) - 3) // BORDERNUM + 1):

                            # print(boxBorder)
                            x0 = boxBorder[k * (BORDERNUM + 1) + 2]
                            x1 = boxBorder[k * (BORDERNUM + 1) + 3 + BORDERNUM]
                            # print(x0, x1)
                            im1 = img.crop((x0, y0, x1 + 1, y1))
                            new_im = Image.new('RGB', (im0.size[0] + im1.size[0], im0.size[1]))
                            new_im.paste(im0, (0, 0))
                            new_im.paste(im1, (im0.size[0], 0))
                            new_im.save('data/data/' + str(classes[NUMBEROFCLASS]) + '.jpg')
                            NUMBEROFCLASS += 1
                except Exception:
                    pass


if __name__ == '__main__':
    sch = Schedule('q.pdf')
    sch.download_pdf()
    sch.make_lessonslists(sch.get_classes(), 'data/', 'q.pdf')