class FontGenerator:
    def __init__(self, leds, headerFile, sourceFile):
        self.leds = leds
        self.headerFile = headerFile
        self.sourceFile = sourceFile

    def generateFontSource(self):
        f = open(self.sourceFile, "w")
        f.write("#include \"" + self.headerFile + "\"\n")
        f.write("""
namespace hpasteur {
""")
        str_size_list = []
        str_font_list = []
        for id_list, leds in self.leds.items():
            f.write("\n\tconst uint8_t PROGMEM Font::font_" + str(leds[0]) + "[" + str(len(leds[1])) + "] = {" + str(leds[1])[1:-1] + "};")
            str_size_list.append("Font::size_" + str(leds[0]))
            str_font_list.append("Font::font_" + str(leds[0]))
        f.write("\n\n\tconst uint8_t * const Font::characters[" + str(len(self.leds)) + "] = {" + (', '.join(str_font_list)) + "};")
        f.write("\n\tconst size_t    Font::characters_size[" + str(len(self.leds)) + "] = {" + (', '.join(str_size_list)) + "};")
        f.write("\n}\n")
        f.close()

    def generateFontHeader(self):
        f = open(self.headerFile, "w")
        f.write("""#ifndef FONT_H
#define FONT_H
#include <stdlib.h>
#include <avr/pgmspace.h>
typedef unsigned char uint8_t;

namespace hpasteur {
  class Font
  {
  public:

""")

        str_size = ""
        str_font = ""
        for id_list, leds in self.leds.items():
            str_size += "\tstatic const size_t size_" + str(leds[0]) + " = " + str(len(leds[1])) + ";\n"
            str_font += "\tstatic const uint8_t font_" + str(leds[0]) + "[" + str(len(leds[1])) + "];\n"
        f.write(str_size)
        f.write("\n")
        f.write(str_font)
        f.write("\n")

        f.write("\tstatic const uint8_t * const characters[" + str(len(self.leds)) + "];\n")
        f.write("\tstatic const size_t    characters_size[" + str(len(self.leds)) + "];\n")

        f.write("""\n\tuint8_t maxIndex = 0;
    
  public:

    /* Constructor */
    Font(/* args */) {
      maxIndex = ('Z' - 'A' + 1) + ('9' - '0' + 1); // All the capital letters + all the digits
    }

    ~Font() {}

    bool getCharacterByIndex(size_t index, const uint8_t * &char_ptr, size_t & char_size) {
      if (index > maxIndex) return false;
      char_ptr = characters[index];
      char_size = characters_size[index];
      return true;
    }

    bool getCharacterByChar(char chr, const uint8_t * &char_ptr, size_t & char_size) {

      if (chr >= 'A' && chr <= 'Z')  {
        getCharacterByIndex(chr - 'A', char_ptr, char_size);
      }
      else if (chr >= '0' && chr <= '9')  {
        //getCharacterByIndex(chr - '0' + 'Z' + 1, char_ptr, char_size); // NON ? exemple pour chr = '0' => 123
        getCharacterByIndex(chr - '0' + ('Z' - 'A' + 1), char_ptr, char_size); // les 26 lettres en premier puis les chiffres
      }
      else return false; // char is not supported by this font

      return true;
    }
  };
}
""")

        f.write("\n#endif")
        f.close()