from datetime import datetime

def bookmarks_to_csv ():
    html_file = open('bookmarks.html', 'r', encoding='utf-8')
    csv_file = open('bookmarks.csv', 'w', encoding='utf-8')
    
    # write header
    csv_file.write(',link+label,path,label,href,add date,icon_iri\n')
    path = []
    for line in html_file:
        # if line has H3, it's a folder (add to path)
        if '<H3 ' in line:
            folder_name = line.split('>')[-2].split('<')[0]
            path.append(folder_name)
            continue
        # if line has /DL, it's going up a folder (pop last from path)
        if '</DL>' in line and len(path) > 0:
            path.pop()
            continue
        # if line has HREF, it's a bookmark
        if ' HREF=' in line:
            # parse string using XML element tree
            split_line_list = line.strip().split(' ')
            href = add_date = icon_uri = label = ''
            for string in split_line_list:
                match contains_which_element(string):
                    case 0:
                        href = string.split('"')[1]
                    case 1:
                        add_date = str(datetime.fromtimestamp(int(string.split('"')[1])))
                    case 2:
                        icon_uri = string.split('"')[1]
            label = line.split('>')[-2].split('<')[0]
            # create string to add to .csv
            csv_line = ',,' # first columns empty for manual additions later
            path_str = ''
            for i in range(0, len(path)):
                path_str += path[i]
                if i is not len(path) - 1:
                    path_str += '→'
            # add padding to ensure links/labels containing commas are safe
            csv_line += '"' + path_str + '",'
            csv_line += '"' + label + '",'
            csv_line += '"' + href + '",'
            csv_line += '"' + add_date + '",'
            csv_line += '"' + icon_uri + '"'
            # add to .csv file 
            csv_file.write(csv_line + '\n')
    html_file.close()
    csv_file.close()

# have to do this because variable number of elements, some can be missing
def contains_which_element(str):
    if 'HREF' in str:
        return 0
    if 'ADD_DATE' in str:
        return 1
    if 'ICON_URI' in str and 'fake-favicon' not in str:
        return 2

if __name__ == '__main__':
    bookmarks_to_csv()