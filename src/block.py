import re
from enum import Enum

class BlockType(Enum):
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered List"
    ORDERED_LIST = "Ordered List"
    PARAGRAPH = "Paragraph"


def markdown_to_blocks(markdown, debug = False):
    if debug == True: print("--CALL-->markdown_to_blocks(markdown)")
    if debug == True: print(f"markdown:\n{markdown}")
    
    results = list()

    if markdown == None or markdown == "":
        return results
    
    new_block = True
    accumulator = list()
    for block in markdown.split("\n"):
        if debug == True: print(f"----->working on: {block}")
        
        # detect trivial blocks
        if (block.strip() == ""):
            if debug == True: print("------->Trivial Block (all whitespace)")
            new_block = True
            if accumulator != list(): 
                if debug == True: print(f"------->Trivial Block accumulator->results{accumulator}")
                results.append("\n".join(accumulator))
            accumulator = list()
            continue

        accumulator.append(block.strip())
        #if debug == True: print(f"------->{accumulator}")
        new_block = False
        
    if accumulator != list(): 
        if debug == True: print(f"------->accumulator->results{accumulator.strip()}")
        results.append("\n".join(accumulator))

    if debug == True: print(f"--->Returning: {results}")
    return results

def block_to_block_type(markdown_block, debug = False):
    if debug == True: print(f"---markdown_block>{markdown_block}")

    if (markdown_block.startswith("# ")): return BlockType.HEADING.value
    if (markdown_block.startswith("## ")): return BlockType.HEADING.value
    if (markdown_block.startswith("### ")): return BlockType.HEADING.value
    if (markdown_block.startswith("#### ")): return BlockType.HEADING.value
    if (markdown_block.startswith("##### ")): return BlockType.HEADING.value
    if (markdown_block.startswith("###### ")): return BlockType.HEADING.value
    if (markdown_block.startswith("```") and markdown_block.endswith("```")): return BlockType.CODE.value
    if (markdown_block.startswith(">")): 
        #Every line in a quote block must start with a > character.
        lines = markdown_block.splitlines()
        for line in lines:
            if line.startswith(">") == False:
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if (markdown_block.startswith("* ")) or (markdown_block.startswith("- ")): 
        lines = markdown_block.splitlines()
        for line in lines:
            if debug == True: print(f"----Line>{line}")
            if line.startswith("* ") == False and line.startswith("- ") == False:
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED_LIST.value

    if re.search(r"^[0-9]+\.\s", markdown_block) != None:
        lines = markdown_block.splitlines()
        accumulator = 1
        for line in lines:
            if debug == True: print(f"---->Line:{line}")
            if debug == True: print(f"---->accumulator:{accumulator}")
            search = re.search(r"^[0-9]+\.\s", line)
            if debug == True: print(f"---->Search:{search.group()}")
            if re.search(r"(^[0-9]+\.)\s", line) == None:
                return BlockType.PARAGRAPH.value
            if search.group().strip() != f"{accumulator}.":
                if debug == True: print(f"------->Accumulator Mismatch: {search.group()} != {accumulator}.")
                return BlockType.PARAGRAPH.value
            accumulator += 1
        return BlockType.ORDERED_LIST.value


    return BlockType.PARAGRAPH.value
