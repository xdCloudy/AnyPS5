#include <cstddef>
#include <cstdint>
#include "SceTypes.hpp"
#include "prx/libc/include/General.hpp"

extern "C" {

APS5_DUMMY_FUN
int APS5_VABI sceSystemLogger2GetTimestamp(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSystemLogger2Initialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSystemLogger2SetEventAsync(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSystemLogger2SetEventAsyncEx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSystemLogger2Terminate(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

}
