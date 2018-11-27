"""
Read images from /img/ folder and generate LaTex code.
"""
import os

def str2dict(s):
    s = s.split('_')
    d = {}
    for i in s:
        param = i.split('=')
        d[param[0]] = param[1]
    return d

def process():
    imgs = os.listdir('./img/')
    if len(imgs) == 0:
        return
    imgs = filter(lambda x: x.find('eps') > 0 and x.find('round') > 0, imgs)
    imgs = list(imgs)
    imgs.sort()

    img_groups = {}
    for f in imgs:
        params = f.split('_round')[0]
        if params in img_groups:
            img_groups[params].append(f)
        else:
            img_groups[params]= [f]
    figs = []
    index = 0
    for g in img_groups.keys():
        index += 1
        subfigs = []
        for f in img_groups[g]:
            param_str = f.rsplit('.', 1)[0]
            params = str2dict(param_str)
            subfigure = '\n'.join([
                '\\subfigure[$round=%s$] {' % (params['round']),
                '    \\centering',
                '    \\includegraphics[width=3.4cm]{../code/img/%s}' % f,
                '}'
            ])
            subfigs.append(subfigure)
        figs.append('\n'.join([
            '\\begin{figure}\centering',
            '\n'.join(subfigs),
            '\caption{$%s$}' % (g.replace('_', ', ')),
            '\label{bigfig_%d}' % index,
            '\\end{figure}'
        ]))
    index = 0
    for fig in figs:
        index += 1
        with open('../doc/img%d.tex' % index, 'w') as f:
            f.write(fig)

def format_line(line):
    """
    Format the line that it's length larger than 80.
    """
    formatted_lines = []
    tabs = ''
    letters = list(line)
    # get the length of tabs
    for letter in letters:
        if letter == ' ':
            tabs += ' '
        else:
            break
    # break the line into pieces, each piece contains no more than 80 words
    formatted_lines.append(tabs + ''.join(letters[0:len(tabs) + 81]))
    letters = letters[len(tabs) + 81:]
    while len(letters) > 80:
        tabs += '  '
        formatted_line = ''.join(letters[0:81])
        formatted_lines.append(tabs + formatted_line)
        letters = letters[81:]
    return '\n'.join(formatted_lines)

def auto_code_text():
    filename = ['Prisoner_s_Dilemma.py', 'Divide_the_Cake.py']
    tex_content = []
    for f in filename:
        with open('./%s' % f) as fp:
            content = fp.readlines()
            # content = [format_line(line) for line in content]
            tex_content.extend([
                '\n',
                '\\begin{lstlisting}[language=Python]\n',
                ''.join(content),
                '\\end{lstlisting}',
                '\\pagebreak'
            ])
    with open('../doc/code.tex', 'w') as f:
        f.writelines(tex_content)

if __name__ == "__main__":
    process()
    auto_code_text()