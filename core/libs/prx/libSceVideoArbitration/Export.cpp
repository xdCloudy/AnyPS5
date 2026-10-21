#include <cstddef>
#include <cstdint>
#include "SceTypes.hpp"
#include "prx/libc/include/General.hpp"

extern "C" {

APS5_DUMMY_FUN
int APS5_VABI sceVideoArbitrationAcceptEvent(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceVideoArbitrationEnable(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceVideoArbitrationInitialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

}
