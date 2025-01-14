from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
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
        # print(f"--->processing node: {node}")
        text = node.text
        firstdelim = text.find(delimiter)
        lastdelim = text.find(delimiter,firstdelim+len(delimiter))

        if firstdelim >=0 and lastdelim == -1:
            raise ValueError(f"delimeter {delimiter} was not closed in {node.text}")

        if firstdelim == -1 and lastdelim == -1:
            part1 = text
            part2 = ""
            part3 = ""
        else:        
            # print(f"{firstdelim}->{lastdelim}")
            part1 = text[:firstdelim]
            part2 = text[firstdelim + len(delimiter):lastdelim]
            part3 = text[lastdelim + len(delimiter):]

        # print(f"part1->{part1}")
        # print(f"part2->{part2}")
        # print(f"part3->{part3}")

        if part1 != "":
            new_nodes.append(TextNode(part1,TextType.TEXT))
        if (part2 != ""):
            new_nodes.append(TextNode(part2,text_type))
        if part3 != "":
            #if delimiter in part3:
            new_nodes.extend(split_nodes_delimiter([TextNode(part3,text_type)],delimiter,text_type))
            #new_nodes.append(TextNode(part3,TextType.TEXT))

    return new_nodes
    
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


