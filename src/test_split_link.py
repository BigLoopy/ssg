import unittest
from processor import split_nodes_link
from textnode import TextType, TextNode

class TestLinks(unittest.TestCase):


    def test_split_nodes_link_none_nodes_returns_empty_list(self):
        old_nodes = None
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, list())

    def test_split_nodes_link_bad_type_raises_valueerror(self):
        old_nodes = TextType.TEXT
        with self.assertRaises(ValueError):
            split_nodes_link(old_nodes)

    def test_split_nodes_link_valueerror_list_of_bad_type(self):
        old_nodes = [TextType.TEXT]
        with self.assertRaises(ValueError):
            split_nodes_link(old_nodes)

    def test_split_nodes_link_delimeter_only_the_thing(self):
            old_nodes = [TextNode("[to boot dev](https://www.boot.dev)",TextType.TEXT)]
            new_nodes = split_nodes_link(old_nodes)
            expected = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_delimeter_only_the_thing_multiple(self):
        #print("test_split_nodes_link_delimeter_only_the_thing_multiple")
        old_nodes = [TextNode("[to boot dev](https://www.boot.dev)[to boot dev](https://www.boot.dev)",TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_delimeter_only_the_thing_multiple_with_space(self):
            old_nodes = [TextNode("[to boot dev](https://www.boot.dev) [to boot dev](https://www.boot.dev)",TextType.TEXT)]
            new_nodes = split_nodes_link(old_nodes)
            expected = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                        TextNode(" ", TextType.TEXT),
                        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_delimeter_start(self):
            old_nodes = [TextNode("[to boot dev](https://www.boot.dev) some additional **stuff**",TextType.TEXT)]
            new_nodes = split_nodes_link(old_nodes)
            expected = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                        TextNode(" some additional **stuff**", TextType.TEXT),
            ]
            self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_before_and_after_text(self):
        singleNode = TextNode("This is text with a [to boot dev](https://www.boot.dev).",TextType.TEXT)
        new_nodes = split_nodes_link(singleNode)
        expected =  [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(".", TextType.TEXT),
                    ]
        self.assertEqual(new_nodes, expected)


    def test_split_nodes_link_delimeter_not_in_text(self):
        old_nodes = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        expected = [TextNode("This is **bolded phrase** in here",TextType.TEXT)]
        self.assertEqual(new_nodes, expected)


    def test_split_nodes_link_delimeter_end(self):
            old_nodes = [TextNode("some additional **stuff** [to boot dev](https://www.boot.dev)",TextType.TEXT)]
            new_nodes = split_nodes_link(old_nodes)
            expected = [TextNode("some additional **stuff** ", TextType.TEXT),
                        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                        
            ]
            self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()
