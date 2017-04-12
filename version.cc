#include "G4Version.hh"
extern "C" {
  int getG4VersionNumber() {
    return G4VERSION_NUMBER;
  }
}
