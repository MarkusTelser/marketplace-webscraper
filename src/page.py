from genericpath import isfile
from os import listdir
from os.path import join, isdir, dirname
from sys import modules

ROOT_DIR = dirname(dirname(modules['__main__'].__file__))


def gen_html():
    html = '<!DOCTYPE html><html>'
    html += '<head><meta http-equiv="Content-Type" content="text/html;charset=utf-8"><title>New Items</title></head>'
    html += '<link rel="stylesheet" href="style.css">'
    html += '<script src="script.js"></script>'
    html += '<body><h1>New Marketplace Items</h1>'
    if isdir("data"):
        websites = listdir(join(ROOT_DIR, "data", "websites"))
        for i in range(len(websites)):

            with open(join(ROOT_DIR, "data", "websites", websites[i]), "r") as f:
                lines = f.readlines()
                html += '<table class="section">'
                if len(lines) != 0:
                    html += f'<tr class="site"><th colspan="{len(lines[0].split("||")) - 1}">' + websites[i].split('.')[0] + '</th></tr>'
                else:
                    html += f'<tr class="site"><th colspan="4">' + websites[i].split('.')[0] + '</th></tr>'

                html += f'<tr><td class="type">Titel</a></td>'
                html += f'<td class="type">Price</td>'
                if len(lines) != 0 and len(lines[0].split("||")) == 6:
                    html += f'<td class="type">Mileage</td>'
                html += f'<td class="type">Location</td>'
                html += f'<td class="type">Date</td></tr>'
                # add all items
                for line in lines:
                    items = line.split("||")
                    html += f'<tr><td class="items"><a target="_blank" rel="noopener noreferrer" href="{items[4]}">{items[0]}</a></td>'
                    html += f'<td class="items">{items[1]}</td>'
                    if len(items) == 6:
                        html += f'<td class="items">{items[5]}</td>'
                    html += f'<td class="items">{items[2]}</td>'
                    html += f'<td class="items">{items[3]}</td>'
                    html += f'<td class="trash"><button onclick="deleteRow(this)"><img src="{join(ROOT_DIR, "data", "trash.svg")}"></button></td></tr>'
                html += '</table>'
    html += '</body></html>'
    return html


def gen_js():
    js = """
    function deleteRow(btn) {
        var row = btn.parentNode.parentNode;
        var link = row.getElementsByTagName("td")[0].childNodes[0].getAttribute("href");
        
        // remove html column
        row.parentNode.removeChild(row);
    }
    """
    return js

def gen_css():
    css = """
    body{
        background-color: #E1E8ED;
    }
    h1{
        font-size: 30pt;
        font-color: #292F33;
        justify-content: center;
        text-align: center;
    }
    table{
        margin-left: auto;
        margin-right: auto;
        width: 80%;
    }
    th, td{
        border: 2px solid  #66757F;
        font-color: #CCD6DD;
    }
    th{
        font-size: 22pt;
        padding: 5px;
    }
    a {
        color: #66757F;
    }
    td{
        font-size: 16pt;
        width:
    }
    .section{
        margin-top: 40px;
        margin-bottom: 60px;
    }
    .type{
        font-size: 20pt;
        font-weight: bold;
    }
    .items{
        width: 25%;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
    }
    .trash{
        border: none; 
    }
    """
    return css


def gen_website(overwrite=True):
    # write html file
    if overwrite or (not overwrite and not isfile(join(ROOT_DIR, "page", "index.html"))):
        with open(join(ROOT_DIR, "page", "index.html"), "w") as f:
            f.write(gen_html())
    
    # write css file
    if overwrite or (not overwrite and not isfile(join(ROOT_DIR, "page", "style.css"))):
        with open(join(ROOT_DIR, "page", "style.css"), "w") as f:
            f.write(gen_css())

    # write js file
    if overwrite or (not overwrite and not isfile(join(ROOT_DIR, "page", "script.js"))):
        with open(join(ROOT_DIR, "page", "script.js"), "w") as f:
            f.write(gen_js())