def first_scan(lines):
    for tem in range(len(lines)):
        lines[tem] = lines[tem].replace("\t","").replace("\n","").rstrip()
        # delete all the comments
        if "#" in lines[tem]:
            comment = lines[tem].index("#")
            lines[tem] = lines[tem][:comment]
    while "" in lines:
        lines.remove("")
    #delete the ".data" part 
    for item in lines:
        if '.text' in item:
            q = lines.index(item)
            del lines[:q+1]
            break
    #".data" may locate at bottom of the asm file
    for item in lines:
        if '.data' in item:
            q = lines.index(item)
            del lines[q:]
            break
    #coping with line break
    temp_list = lines
    for line in temp_list:
        if ":" in line:
            del line
    length = len(temp_list)
    position=0
    processed_list=[]
    while position<=length-1:
        if lines[position].endswith(":"):
            merged=lines[position]+lines[position+1]
            processed_list.append(merged)
            position += 2
        else:
            processed_list.append(lines[position])
            position += 1
    labelTable=dict()
    for position in range(len(processed_list)):
        if ":" in processed_list[position]:
            colon_index = processed_list[position].index(":")
            labelTable[processed_list[position][:colon_index]] = position
            processed_list[position]=processed_list[position][colon_index+1:]
    return labelTable,processed_list
  