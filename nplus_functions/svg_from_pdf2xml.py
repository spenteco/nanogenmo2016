#!/usr/bin/python     
## -*- coding: utf-8 -*-

import sys, codecs
from lxml import etree

def svg_from_pdf2xml(input_file, output_folder, url_for_svg_images):
    
    file_name_less_path = input_file.split('/')[-1]
    
    print 'input_file', input_file, 'output_folder', output_folder, 'file_name_less_path', file_name_less_path

    tree = etree.parse(input_file)
    root = tree.getroot()
    
    page_numbers = []
    
    #   IT DOESN'T PRESERVE ITALIC
    
    fonts = {}
    
    for fontspec in root.xpath('//fontspec'):
        fonts[fontspec.get('id')] = fontspec.get('size')
    
    for page in root.xpath('//page'):
        
        page_n = int(page.get('number'))
        w = page.get('width')
        h = page.get('height')
        
        #if page_n > 9:
        #    break

        svg = etree.Element('svg')
        
        image_data = []
        for i in page.xpath('descendant::image'):
            image_data.append({'top': i.get('top'), 'left': i.get('left'), 'width': i.get('width'), 'height': i.get('height')})
            
        text_nodes = page.xpath('descendant::text')
        
        low_x = 999
        high_x = -1
        
        for i, t in enumerate(text_nodes):
            
            if int(t.get('left')) < low_x:
                low_x = int(t.get('left'))
            
            if (int(t.get('left')) + int(t.get('width'))) > high_x:
                high_x = int(t.get('left')) + int(t.get('width'))
        
        for i, t in enumerate(text_nodes):
            
            y = int(t.get('top'))
            
            #if t.get('font') == '1':
            #    y = y + 8
            #if t.get('font') == '5':
            #    y = y + 6
            
            font_family = 'font-family:"Times New Roman", Times, serif;';
            if t.text.find('robineggsky') > -1:
                font_family = 'font-family:"Courier New", Courier, monospace;';
                
            font_variant = ''
            if page_n > 4:
                if i == 0:
                    font_variant = 'font-variant: small-caps;'
                if i == len(text_nodes) - 1:
                    if t.text.find('robineggsky') == -1:
                        try:
                            noop = int(t.text)
                        except:
                            font_variant = 'font-variant: small-caps;'
            
            svg_text_node = etree.Element('text')
            svg_text_node.set('x', t.get('left'))
            svg_text_node.set('y', str(y))
            svg_text_node.set('textLength', t.get('width'))
            svg_text_node.set('style', "fill:#000000;font-size:" + fonts[t.get('font')] + "px;" + font_family + font_variant)
            svg_text_node.text = t.text
            
            svg.append(svg_text_node)
            
            if page_n > 4 and i == 0:
                
                line = etree.Element('line')
                line.set('x1', str(low_x))
                line.set('y1', str(y + 15))
                line.set('x2', str(high_x))
                line.set('y2', str(y + 15))
                line.set('style', "stroke:#000000;stroke-width:0.5")
            
                svg.append(line)
                
            if page_n == 3 and i == 0:
                
                if len(image_data) > 0:
                    
                    print 'adding image'
                
                    image = etree.Element('image')
                    image.set('x', image_data[0]['left'])
                    image.set('y', image_data[0]['top'])
                    image.set('width', image_data[0]['width'])
                    image.set('height', image_data[0]['height'])
                    image.set('href', url_for_svg_images + 'by-nc-sa.png')
                    
                    svg.append(image)
            
        xml = etree.tostring(svg, pretty_print=True).replace('<svg>', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink= "http://www.w3.org/1999/xlink" width="' + w + '" height="' + h + '">').replace(' href=', ' xlink:href=')
        if xml.strip() == '<svg/>':
            print 'FIXING'
            xml = '<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '"></svg>'
        f = codecs.open(output_folder + str(page_n) + '-' + file_name_less_path.replace('.xml', '.svg'), 'w', encoding='utf-8')
        f.write(xml)
        f.close()
        
        page_numbers.append(str(page_n))
        
    return page_numbers


if __name__ == "__main__":

    print svg_from_pdf2xml(sys.argv[1], sys.argv[2])
