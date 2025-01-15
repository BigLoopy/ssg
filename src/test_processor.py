import unittest
from processor import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes
from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_split_nodes_image_none_nodes(self):
        old_nodes = None
        new_nodes = split_nodes_delimiter(old_nodes,"*",TextType.BOLD)
        self.assertEqual(new_nodes, list())

    def test_split_nodes_delimeter_valueerror_bad_type(self):
        old_nodes = TextType.TEXT
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes,"*",TextType.BOLD)

    def test_split_nodes_delimeter_valueerror_list_of_bad_type(self):
        old_nodes = [TextType.TEXT]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes,"*",TextType.BOLD)

    def test_split_nodes_delimeter_single_node_none_delimeter(self):
        singleNode = TextNode("This is **bolded phrase** in here",TextType.TEXT)
        new_nodes = split_nodes_delimiter(singleNode,None,TextType.BOLD)
        expected = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        # print(f"->{singleNode}")
        # print(f"-->{new_nodes}")
        # print(f"--->{expected}")
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_none_delimeter(self):
        old_nodes = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,None,TextType.BOLD)
        expected = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_only_delimeted(self):
        old_nodes = [TextNode("**bolded phrase**",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("bolded phrase", TextType.BOLD),
        ]
        # print(f"!!->{old_nodes}")
        # print(f"!!-->{new_nodes}")
        # print(f"!!--->{expected}")
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_already_split_doesnt_change(self):
        old_nodes = [TextNode("bolded phrase",TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("bolded phrase", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)
        

    def test_split_nodes_delimeter_only_delimeted_multiple_nodes(self):
        old_nodes = [TextNode("**bolded phrase**",TextType.TEXT),TextNode("**bolded phrase**",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("bolded phrase", TextType.BOLD),
            TextNode("bolded phrase", TextType.BOLD),
        ]
        # print(f"!!->{old_nodes}")
        # print(f"!!-->{new_nodes}")
        # print(f"!!--->{expected}")
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_only_delimeted_double_process(self):
        old_nodes = [TextNode("**bolded phrase**",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("bolded phrase", TextType.BOLD),
        ]
        # print(f"!!->{old_nodes}")
        # print(f"!!-->{new_nodes}")
        # print(f"!!--->{expected}")
        self.assertEqual(new_nodes, expected)
        
        newer_nodes = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
        self.assertEqual(new_nodes, newer_nodes)

    def test_split_nodes_delimeter_bold_delimeter(self):
        old_nodes = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in here", TextType.TEXT),
        ]
        # print(f"!!->{old_nodes}")
        # print(f"!!-->{new_nodes}")
        # print(f"!!--->{expected}")
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_delimeter_not_in(self):
        old_nodes = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"-",TextType.ITALIC)
        expected = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_delimeter_start(self):
            old_nodes = [TextNode("**bolded phrase** at start",TextType.TEXT)]
            new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
            expected = [
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" at start", TextType.TEXT),
            ]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_delimeter_end(self):
            old_nodes = [TextNode("Ends with **bolded phrase**",TextType.TEXT)]
            new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
            expected = [
                TextNode("Ends with ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
            ]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_unmatche_delim_exception(self):
        old_nodes = [TextNode("**bolded phrase with no closing",TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        

    def test_split_nodes_delimeter_bold_delimeter_multiples(self):
        old_nodes = [TextNode("This is **bolded phrase** in here **and another one**",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in here ", TextType.TEXT),
            TextNode("and another one", TextType.BOLD),
        ]
        # print(f"!!->{old_nodes}")
        # print(f"!!-->{new_nodes}")
        # print(f"!!--->{expected}")
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_bold_delimeter_only_split_bold(self):
        old_nodes = [TextNode("This is **bolded phrase** in here `don't split the code`",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in here `don't split the code`", TextType.TEXT),
        ]
        # print(f"!!->{old_nodes}")
        # print(f"!!-->{new_nodes}")
        # print(f"!!--->{expected}")

        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimeter_chained_different_delimeters(self):
        old_nodes = [TextNode("This is **bolded phrase** in here `don't split the code`",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in here `don't split the code`", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        

        newer_nodes = split_nodes_delimiter(new_nodes,"`", TextType.CODE)
        expecteder = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in here ", TextType.TEXT),
            TextNode("don't split the code", TextType.CODE),
        ]
        self.assertEqual(newer_nodes, expecteder)



    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(matches, expected)
    
    def test_extract_markdown_images_complex(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(matches, expected)


    def test_extract_markdown_images_empty_text(self):
        text = ""
        matches = extract_markdown_images(text)
        expected = list()
        self.assertEqual(matches, expected)


    def test_extract_markdown_images_nothing_to_extract(self):
        text = ""
        matches = extract_markdown_images(text)
        expected = list()
        self.assertEqual(matches, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        result = text_to_textnodes(text)
        self.assertEqual(result, expected)




if __name__ == "__main__":
    unittest.main()
