#include <stdlib.h>
#include <avr/pgmspace.h>
typedef unsigned char uint8_t;

namespace hpasteur {
  class Font
  {
  public:

        static const size_t size_A = 3;
static const size_t size_B = 4;
static const size_t size_C = 0;
static const size_t size_D = 0;
static const size_t size_E = 0;
static const size_t size_F = 0;
static const size_t size_G = 0;
static const size_t size_H = 0;
static const size_t size_I = 4;
static const size_t size_J = 0;
static const size_t size_K = 0;
static const size_t size_L = 0;
static const size_t size_M = 0;
static const size_t size_N = 2;
static const size_t size_O = 0;
static const size_t size_P = 0;
static const size_t size_Q = 0;
static const size_t size_R = 0;
static const size_t size_S = 0;
static const size_t size_T = 0;
static const size_t size_U = 0;
static const size_t size_V = 0;
static const size_t size_W = 0;
static const size_t size_X = 0;
static const size_t size_Y = 0;
static const size_t size_Z = 0;

static const uint8_t font_A[3];
static const uint8_t font_B[4];
static const uint8_t font_C[0];
static const uint8_t font_D[0];
static const uint8_t font_E[0];
static const uint8_t font_F[0];
static const uint8_t font_G[0];
static const uint8_t font_H[0];
static const uint8_t font_I[4];
static const uint8_t font_J[0];
static const uint8_t font_K[0];
static const uint8_t font_L[0];
static const uint8_t font_M[0];
static const uint8_t font_N[2];
static const uint8_t font_O[0];
static const uint8_t font_P[0];
static const uint8_t font_Q[0];
static const uint8_t font_R[0];
static const uint8_t font_S[0];
static const uint8_t font_T[0];
static const uint8_t font_U[0];
static const uint8_t font_V[0];
static const uint8_t font_W[0];
static const uint8_t font_X[0];
static const uint8_t font_Y[0];
static const uint8_t font_Z[0];

static const uint8_t * const characters[26];
static const size_t    characters_size[26];

        uint8_t maxIndex = 0;
    
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
        #endif