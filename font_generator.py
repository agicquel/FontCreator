from netlistParser import *
import pyinstaller_path


class FontGenerator:
    def __init__(self, leds, headerFile, sourceFile):
        self.leds = leds
        self.headerFile = headerFile
        self.sourceFile = sourceFile
        self.nl = NetParse(pyinstaller_path.resource_path("./pcb/pcb.net"))
        self.nl.analyse()
        self.sorted_an_ca = sorted(self.nl.leds, key=lambda d: (d['an'], d['ca']))
        self.sorted_ca_an = sorted(self.nl.leds, key=lambda d: (d['ca'], d['an']))
        self.optimize()

    def generateFontSource(self):
        f = open(self.sourceFile, "w")
        f.write("#include \"" + self.headerFile + "\"\n")
        f.write("""
namespace hpasteur {
""")
        str_size_list = []
        str_font_list = []
        for id_list, leds in self.leds.items():
            f.write("\n\tconst uint8_t PROGMEM Font::font_" + str(leds[0]) + "[" + str(len(leds[1])) + "] = {" + str(
                leds[1])[1:-1] + "};")
            str_size_list.append("Font::size_" + str(leds[0]))
            str_font_list.append("Font::font_" + str(leds[0]))
        f.write("\n\n\tconst uint8_t * const Font::characters[" + str(len(self.leds)) + "] = {" + (
            ', '.join(str_font_list)) + "};")
        f.write("\n\tconst size_t    Font::characters_size[" + str(len(self.leds)) + "] = {" + (
            ', '.join(str_size_list)) + "};")
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

    def _find_an(self, led_id):
        return list(filter(lambda l: l['led'] == led_id, self.nl.leds))[0]['an']

    def _find_ca(self, led_id):
        return list(filter(lambda l: l['led'] == led_id, self.nl.leds))[0]['ca']

    def _count_swap(self, led_list):
        if len(led_list) == 0:
            return 0
        counter = 2
        last_an = self._find_an(led_list[0])
        last_ca = self._find_ca(led_list[0])
        for l in led_list:
            led_an = self._find_an(l + 1)
            led_ca = self._find_an(l + 1)
            if led_an != last_an:
                counter += 1
                last_an = led_an
            if led_ca != last_ca:
                counter += 1
                last_ca = led_ca
        return counter

    def optimize(self):
        # print("before opti")
        # print("\n")
        # for id_list, leds in self.leds.items():
        #     print(str(id_list) + " : " + str(self._count_swap(leds[1])))
        for id_list, leds in self.leds.items():
            new_leds_list_1 = []
            new_leds_list_2 = []
            for l in self.sorted_an_ca:
                if l['led'] in leds[1]:
                    new_leds_list_1.append(l['led'])
            for l in self.sorted_ca_an:
                if l['led'] in leds[1]:
                    new_leds_list_2.append(l['led'])
            if self._count_swap(new_leds_list_1) < self._count_swap(new_leds_list_2):
                self.leds[id_list] = (self.leds[id_list][0], new_leds_list_1)
            else:
                self.leds[id_list] = (self.leds[id_list][0], new_leds_list_2)
        # print("\n")
        # print("after opti")
        # print("\n")
        # for id_list, leds in self.leds.items():
        #     print(str(id_list) + " : " + str(self._count_swap(leds[1])))
