from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type, debug = False):
    if debug == True: print(f"--CALL-->split_nodes_delimiter({old_nodes}, {delimiter}, {text_type}):")
    
    if isinstance(old_nodes,list) == False and old_nodes != None and isinstance(old_nodes,TextNode) == False:
        raise ValueError("old_nodes must be a list of TextNode, or a single TextNode")
    if isinstance(old_nodes, list):
        for node in old_nodes:
            if isinstance(node,TextNode) != True:
                raise ValueError("All nodes must be TextNode")
    if old_nodes == None:
        return list()
    elif isinstance(old_nodes,list) == False:
        nodes_to_process = [old_nodes]
    else:
        nodes_to_process = old_nodes.copy()

    if delimiter == "" or delimiter == None:
        return nodes_to_process
    
    new_nodes = list()
    # print(f"----->processing {len(nodes_to_process)} items")
    
    for node in nodes_to_process:
        if debug == True: print(f"--->processing node: {node}")
        text = node.text
        firstdelim = text.find(delimiter)
        lastdelim = text.find(delimiter,firstdelim+len(delimiter))

        if debug == True: print(f"firstdelim->{firstdelim}")
        if debug == True: print(f"lastdelim->{lastdelim}")


        if firstdelim >=0 and lastdelim == -1:
            raise ValueError(f"delimeter {delimiter} was not closed in {node.text}")

        type_override = TextType.TEXT
        if firstdelim == -1 and lastdelim == -1:
            part1 = text
            part2 = ""
            part3 = ""
            if debug == True: print(f"-------> Forcing node type to {node.text_type}")
            type_override = node.text_type
            
        else:        
            if debug == True: print(f"--- delims ->{firstdelim}->{lastdelim}")
            part1 = text[:firstdelim]
            part2 = text[firstdelim + len(delimiter):lastdelim]
            part3 = text[lastdelim + len(delimiter):]
            

        if debug == True:  print(f"part1->{part1}")
        if debug == True:  print(f"part2->{part2}")
        if debug == True: print(f"part3->{part3}")

        if part1 != "":
            new_nodes.append(TextNode(part1,type_override, node.url))
        if (part2 != ""):
            new_nodes.append(TextNode(part2,text_type))
        if part3 != "":
            #if delimiter in part3:
            new_nodes.extend(split_nodes_delimiter([TextNode(part3,TextType.TEXT)],delimiter,text_type))
            #new_nodes.append(TextNode(part3,TextType.TEXT))

    return new_nodes
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
    if isinstance(old_nodes,list) == False and old_nodes != None and isinstance(old_nodes,TextNode) == False:
        raise ValueError("old_nodes must be a list of TextNode, or a single TextNode")
    
    if isinstance(old_nodes, list):
        for node in old_nodes:
            if isinstance(node,TextNode) != True:
                raise ValueError("All nodes must be TextNode")

    if old_nodes == None:
        return list()
    elif isinstance(old_nodes,list) == False:
        nodes_to_process = [old_nodes]
    else:
        nodes_to_process = old_nodes.copy()
        
    new_nodes = list()
    # print(f"----->processing {len(nodes_to_process)} items")
    
    for node in nodes_to_process:
        # print(f"--->processing node: {node}")
        text = node.text
        matches = extract_markdown_images(text)

        if matches == list():
            # print("---->BOOYAH TRIVIAL CASE")
            new_nodes.append(node)
            continue

        
        image_alt = matches[0][0]
        image_link = matches[0][1]
        image_markdown = f"![{image_alt}]({image_link})"
        image_textnode = TextNode(image_alt,TextType.IMAGE,image_link)
        sections = text.split(image_markdown, 1)
        # print(f"\n--->Sections: {sections}")

        starts_with = text.startswith(image_markdown)
        ends_with = text.endswith(image_markdown) 
        
        if (starts_with and ends_with and len(text) != len(image_markdown)):
            ends_with = False
        
        # print(f"--->text = {text}")
        # print(f"--->text = {len(text)}")
        # print(f"--->image_markdown = {image_markdown}")
        # print(f"--->image_markdown = {len(image_markdown)}")
        # print(f"--->starts_with = {starts_with}")
        # print(f"--->ends_with = {ends_with}")

        part1 = None
        part2 = None
        part3 = None

        if starts_with and ends_with:
            part1 = None
            part2 = image_textnode
            part3 = None
        
        elif starts_with:
            part1 = None
            part2 = image_textnode
            part3 = sections[1]

        elif ends_with:
            part1 = sections[0]
            part2 = image_textnode
            part3 = None

        else:
            part1 = sections[0]
            part2 = image_textnode
            part3 = sections[1]


        # print(f"part1->{part1}")
        # print(f"part2->{part2}")
        # print(f"part3->{part3}")

        if part1 != None:
            new_nodes.append(TextNode(part1,TextType.TEXT))
        if (part2 != None):
            new_nodes.append(image_textnode)
        if part3 != None:
            #if delimiter in part3:
            new_nodes.extend(split_nodes_image([TextNode(part3,TextType.TEXT)]))
            #new_nodes.append(TextNode(part3,TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    # print(f"--->split_nodes_link(old_nodes)")
    if isinstance(old_nodes,list) == False and old_nodes != None and isinstance(old_nodes,TextNode) == False:
        raise ValueError("old_nodes must be a list of TextNode, or a single TextNode")
    
    if isinstance(old_nodes, list):
        for node in old_nodes:
            if isinstance(node,TextNode) != True:
                raise ValueError("All nodes must be TextNode")

    if old_nodes == None:
        return list()
    elif isinstance(old_nodes,list) == False:
        nodes_to_process = [old_nodes]
    else:
        nodes_to_process = old_nodes.copy()
        
    new_nodes = list()
    # print(f"----->processing {len(nodes_to_process)} items")
    
    for node in nodes_to_process:
        # print(f"----->processing node: {node}")
        text = node.text
        matches = extract_markdown_links(text)

        if matches == list():
            # print("------->BOOYAH TRIVIAL CASE")
            new_nodes.append(node)
            continue

        
        image_alt = matches[0][0]
        image_link = matches[0][1]
        # print(f"----->matches[0][0]{matches[0][0]}")
        # print(f"----->matches[0][1]{matches[0][1]}")
        
        image_markdown = f"[{image_alt}]({image_link})"
        image_textnode = TextNode(image_alt,TextType.LINK,image_link)
        sections = text.split(image_markdown, 1)
        # print(f"\n--->Sections: {sections}")

        starts_with = text.startswith(image_markdown)
        ends_with = text.endswith(image_markdown) 
        
        if (starts_with and ends_with and len(text) != len(image_markdown)):
            ends_with = False
        
        # print(f"----->text = {text}")
        # print(f"----->text = {len(text)}")
        # print(f"----->image_markdown = {image_markdown}")
        # print(f"----->image_markdown = {len(image_markdown)}")
        # print(f"----->starts_with = {starts_with}")
        # print(f"----->ends_with = {ends_with}")

        part1 = None
        part2 = None
        part3 = None

        if starts_with and ends_with:
            part1 = None
            part2 = image_textnode
            part3 = None
        
        elif starts_with:
            part1 = None
            part2 = image_textnode
            part3 = sections[1]

        elif ends_with:
            part1 = sections[0]
            part2 = image_textnode
            part3 = None

        else:
            part1 = sections[0]
            part2 = image_textnode
            part3 = sections[1]

        # print(f"-----part1->{part1}")
        # print(f"-----part2->{part2}")
        # print(f"-----part3->{part3}")

        if part1 != None:
            new_nodes.append(TextNode(part1,TextType.TEXT))
        if (part2 != None):
            new_nodes.append(image_textnode)
        if part3 != None:
            #if delimiter in part3:
            new_nodes.extend(split_nodes_link([TextNode(part3,TextType.TEXT)]))
            #new_nodes.append(TextNode(part3,TextType.TEXT))

    return new_nodes

def text_to_textnodes(text, debug = False):
    new_nodes = [TextNode(text,TextType.TEXT)]
    if debug == True: print(f"-----1>\n{new_nodes}")
    new_nodes = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
    if debug == True: print(f"-----2>\n{new_nodes}")
    new_nodes = split_nodes_delimiter(new_nodes,"*",TextType.ITALIC)
    if debug == True: print(f"-----3>\n{new_nodes}")
    new_nodes = split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    if debug == True: print(f"-----4>\n{new_nodes}")
    new_nodes = split_nodes_link(new_nodes)
    if debug == True: print(f"-----5>\n{new_nodes}")
    new_nodes = split_nodes_image(new_nodes)
    if debug == True: print(f"-----6>\n{new_nodes}")

    return new_nodes
