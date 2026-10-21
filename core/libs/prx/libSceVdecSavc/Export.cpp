#include <cstdint>
#include <cstddef>
#include "SceTypes.hpp"
#include "prx/libc/include/General.hpp"

extern "C" {

APS5_DUMMY_FUN
int APS5_VABI sceSdecCreateSw(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSdecDestroySw(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSdecGetVersionSw(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceSdecQueryMemorySw(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

}
