from textnode import TextNode, TextType

def main():
    testnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testnode)

main()
