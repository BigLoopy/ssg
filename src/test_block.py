import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType

class TestBlock(unittest.TestCase):

    def test_markdown_to_blocks_none_returns_empty_list(self):
        markdown = None
        expected = list()

        results = markdown_to_blocks(markdown)

        self.assertEqual(results, expected)
                                                        
    def test_markdown_to_blocks_empty_returns_empty_list(self):
        markdown = ""
        expected = list()

        results = markdown_to_blocks(markdown)

        self.assertEqual(results, expected)


    def test_markdown_to_blocks_single_block(self):
        markdown = "# This is a heading"
        expected = ["# This is a heading"]

        results = markdown_to_blocks(markdown)
        self.assertEqual(results, expected)

    def test_markdown_to_blocks_ignore_empties_before(self):
        markdown = """
        
        
        # This is a heading"""
        expected = ["# This is a heading"]

        results = markdown_to_blocks(markdown)
        self.assertEqual(results, expected)

    def test_markdown_to_blocks_ignore_empties_after(self):
        markdown = """# This is a heading
        
        
        """
        expected = ["# This is a heading"]

        results = markdown_to_blocks(markdown)
        self.assertEqual(results, expected)

    def test_markdown_to_blocks_single_multiline_block(self):
        markdown = """
        # This is a heading
        # This is a heading
        # This is a heading
        """ 
        
        expected = ["# This is a heading\n# This is a heading\n# This is a heading"]

        results = markdown_to_blocks(markdown)
        self.assertEqual(results, expected)


    def test_markdown_two_single_line_blocks(self):
        markdown = """# This is a heading
        
        # This is a heading
        """
        expected = ["# This is a heading", "# This is a heading"]

        results = markdown_to_blocks(markdown)
        self.assertEqual(results, expected)

    def test_markdown_to_block_complex(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected = ["# This is a heading", 
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]

        results = markdown_to_blocks(markdown)
        self.assertEqual(results, expected)

    def test_block_to_block_type_paragraph(self):
        input = """This is a paragraph
it can have lots of blocks of text
but it is still a paragraph"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading1(self):
        input = "# This is a heading"
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading2(self):
        input = "## This is a heading"
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading3(self):
        input = "### This is a heading"
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading4(self):
        input = "#### This is a heading"
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading5(self):
        input = "##### This is a heading"
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading6(self):
        input = "###### This is a heading"
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading1_multiline(self):
        input = """# This is a heading
Still heading"""
        expected = BlockType.HEADING.value
        output = block_to_block_type(input)

        self.assertEqual(output, expected)

    def test_block_to_block_type_heading1_invalid_7_returns_paragraph(self):
        input = "####### This is a heading"
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_code(self):
        input = "```This is a code block```"
        expected = BlockType.CODE.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_code_multiline(self):
        input = """```This is a code block
Still a code block
yes all of it```"""
        expected = BlockType.CODE.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)


    def test_block_to_block_type_code_invalid_returns_paragraph(self):
        input = """```This is NOT a code block
Still NOT a code block
yes all of it"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    #Every line in a quote block must start with a > character.
    def test_block_to_block_type_quote_single_line(self):
        input = ">This is a quote"
        expected = BlockType.QUOTE.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_quote_single_line_still_a_quote(self):
        input = ">>This is a quote"
        expected = BlockType.QUOTE.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_quote_single_line_also_still_a_quote(self):
        input = "> This is a quote"
        expected = BlockType.QUOTE.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_quote_multi_line(self):
        input = """>This is still a quote
>with multipl lines"""
        expected = BlockType.QUOTE.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_bad_quote_is_paragraph_case(self):
        input = """>This is not a quote
Because of this line"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)


    def test_block_to_block_type_ul_single_star(self):
        input = "* List Single Item"
        expected = BlockType.UNORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_multi_star(self):
        input = """* list item 1
* list item 2
* list item 3"""
        expected = BlockType.UNORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_single_dash(self):
        input = "- List Single Item"
        expected = BlockType.UNORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_multi_dash(self):
        input = """- list item 1
- list item 2
- list item 3"""
        expected = BlockType.UNORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_multi_mixed(self):
        input = """* list item 1
- list item 2
* list item 3"""
        expected = BlockType.UNORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_start_returns_paragraph(self):
        input = "*This is not a list, there is no space"
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_start_repeats_returns_paragraph(self):
        input = "*** This is also not a list"
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_multi_returns_paragraph(self):
        input = """* list item 1
--list item 2
* list item 3"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)









    def test_block_to_block_type_ol_single(self):
        input = "1. List Single Item"
        expected = BlockType.ORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ol_multi(self):
        input = """1. list item 1
2. list item 2
3. list item 3"""
        expected = BlockType.ORDERED_LIST.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_start_returns_paragraph(self):
        input = "1.This is not a list, there is no space"
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_multi_returns_paragraph(self):
        input = """1. list item 1
2.list item 2
3. list item 3"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_multi_returns_bad_item_space_paragraph(self):
        input = """1. list item 1
2.list item 2
3. list item 3"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_multi_returns_bad_item_type_paragraph(self):
        input = """1. list item 1
- list item 2
2. list item 3"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)

    def test_block_to_block_type_ul_bad_multi_out_of_sequence_returns_paragraph(self):
        input = """1. list item 1
3. list item 2
5. list item 3"""
        expected = BlockType.PARAGRAPH.value
        output = block_to_block_type(input)
        self.assertEqual(output, expected)


#     def test_block_to_block_type_(self):
#         input = ""
#         expected = BlockType.PARAGRAPH.value
#         output = block_to_block_type(input)
#         self.assertEqual(output, expected)

#     #     self.assertEqual(output, expected)

#     # def test_block_to_block_type(self):
#     #     pass

#     # def test_block_to_block_type(self):
#     #     pass

#     # def test_block_to_block_type(self):
#     #     pass    

#     # def test_block_to_block_type(self):
#     #     pass

#     # def test_block_to_block_type(self):
#     #     pass

#     # def test_block_to_block_type(self):
#     #     pass

#     # def test_block_to_block_type(self):
#     #     pass    