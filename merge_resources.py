import os
from io import TextIOWrapper

path = os.path.dirname(__file__)

output_file = 'test_output.txt'
text_resources_file = 'test_TextResources.txt'
text_resources_with_gr_file = 'test_TextResourcesWithGR.txt'

lines_tr_gr_index = 0

gr_text = str()


def get_text_resource_id(begin_text_resource_line:str) -> int:
    if begin_text_resource_line.find("Begin TextResource ") != -1:
        splited_text = begin_text_resource_line.split("Begin TextResource ")
        return int(splited_text[len(splited_text)-1])
    else:
        return -1


def find_gr_text_index(lines_tr_gr:list[str]) -> None:
    global lines_tr_gr_index

    while True:
        try:
            if lines_tr_gr[lines_tr_gr_index].find("GR") != -1:
                break
        except:
            break

        lines_tr_gr_index+=1


def arrange_index_by_id(lines_tr_gr:list[str], tr_id:int, tr_gr_id:int) -> None:
    global lines_tr_gr_index
    
    if tr_id > tr_gr_id:
        lines_tr_gr_index+=1
        while True:
            try:
                line_tr_gr = lines_tr_gr[lines_tr_gr_index]
                if line_tr_gr.find("Begin TextResource ") != -1:
                    new_tr_gr_id = get_text_resource_id(line_tr_gr)
                    if tr_id == new_tr_gr_id:
                        break
            except:
                break
            
            lines_tr_gr_index+=1
    
    elif tr_id < tr_gr_id:
        lines_tr_gr_index-=1
        while True:
            try:
                line_tr_gr = lines_tr_gr[lines_tr_gr_index]
                if line_tr_gr.find("Begin TextResource ") != -1:
                    new_tr_gr_id = get_text_resource_id(line_tr_gr)
                    if tr_id == new_tr_gr_id:
                        break
            except:
                break

            lines_tr_gr_index-=1


def get_gr_text(lines_tr_gr:list[str], line:str) -> str:
    global lines_tr_gr_index

    result = str()

    tr_id = get_text_resource_id(line)
    print(f"id: {tr_id}")
    
    if lines_tr_gr_index == len(lines_tr_gr)-1:
        return result
    
    while True:
        try:
            line_tr_gr = lines_tr_gr[lines_tr_gr_index]
            if line_tr_gr.find("Begin TextResource ") != -1:
                tr_gr_id = get_text_resource_id(line_tr_gr)
                if tr_gr_id == tr_id:
                    find_gr_text_index(lines_tr_gr)
                    result = lines_tr_gr[lines_tr_gr_index]
                    break
                else:
                    arrange_index_by_id(lines_tr_gr, tr_id, tr_gr_id)
                    find_gr_text_index(lines_tr_gr)
                    break
        except:
            break

        lines_tr_gr_index+=1
         
    
    return result


def merge_text_resources(file:TextIOWrapper, lines_tr_gr:list[str], line:str) -> TextIOWrapper:
    global gr_text

    if line.find("Begin TextResource ") != -1:
        gr_text = get_gr_text(lines_tr_gr, line)
        file.write(line)
    elif line.find("TR") != -1:
        file.write(line)
    elif line.find("EN") != -1:
        file.write(line)
    elif line.find("End") != -1:
        if gr_text != str():
            file.write(gr_text)
            gr_text = str()
            
        file.write(line)

    return file


def write_output_file(lines_tr:list[str], lines_tr_gr:list[str]) -> None:
    start_merge = False
    print(10 * "-" + "Write Begin" + 10 * "-")
    with open(os.path.join(path, './' + output_file), 'w', encoding='cp1254') as f:
        for line in lines_tr:
            if line.find("Begin TextResources") != -1:
                f.write(line)
                start_merge = True

            if start_merge:
                f = merge_text_resources(f, lines_tr_gr, line)
            else:
                f.write(line)
    print(10 * "-" + "Write End" + 10 * "-")                
            

def main() -> None:
    lines_tr = list[str]
    lines_tr_gr = list[str]

    with open(os.path.join(path, './' + text_resources_file), 'r', encoding='cp1254') as f_tr:
        lines_tr = f_tr.readlines()

    with open(os.path.join(path, './' + text_resources_with_gr_file), 'r', encoding='cp1254') as f_tr_gr:
        lines_tr_gr = f_tr_gr.readlines()    

    write_output_file(lines_tr, lines_tr_gr)


if __name__ == "__main__":
    main()