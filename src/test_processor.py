import unittest
from processor import split_nodes_delimiter
from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimeter_none_nodes(self):
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

    def test_split_nodes_delimeter_delimeter(self):
        old_nodes = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes,"**",TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in here", TextType.TEXT),
        ]
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


if __name__ == "__main__":
    unittest.main()
