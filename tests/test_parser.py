from config.parser import ConfigParser

parser = ConfigParser("config.txt")

text = parser.parse()

print(text)
