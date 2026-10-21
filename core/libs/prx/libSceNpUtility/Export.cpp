#include <cstdint>
#include <cstddef>
#include "SceTypes.hpp"
#include "prx/libc/include/General.hpp"

static constexpr int SCE_NP_ERROR_INVALID_ARGUMENT = static_cast<int>(0x80550003);
static constexpr int SCE_NP_ERROR_SIGNED_OUT = static_cast<int>(0x80550006);

extern "C" {

int SceNpUtilityModuleLoaded_nid_no_patch = 1;

int APS5_VABI sceNpBandwidthTestAbort(int context_id) {
    (void)context_id;
    return SCE_NP_ERROR_INVALID_ARGUMENT;
}

int APS5_VABI sceNpBandwidthTestGetStatus(int context_id, int* status) {
    (void)context_id;
    if (status) *status = 0;
    return SCE_NP_ERROR_INVALID_ARGUMENT;
}

int APS5_VABI sceNpBandwidthTestInitStartDownload(const void* param) {
    (void)param;
    return SCE_NP_ERROR_SIGNED_OUT;
}

int APS5_VABI sceNpBandwidthTestInitStartUpload(const void* param) {
    (void)param;
    return SCE_NP_ERROR_SIGNED_OUT;
}

int APS5_VABI sceNpBandwidthTestShutdown(int context_id, void* result) {
    (void)context_id;
    (void)result;
    return SCE_NP_ERROR_INVALID_ARGUMENT;
}
int APS5_VABI sceNpAppInfoIntAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckAvailability(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckAvailabilityA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckAvailabilityAll(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckAvailabilityAllA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckServiceAvailability(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckServiceAvailabilityA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckServiceAvailabilityAll(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCheckServiceAvailabilityAllA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntDestroyRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntFinalize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppInfoIntInitialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntDestroyRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntFinalize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntGetCompatibleTitleIdList(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntGetCompatibleTitleIdNum(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLink2IntInitialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntDestroyRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntFinalize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntGetCompatibleTitleIdList(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntGetCompatibleTitleIdNum(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpAppLaunchLinkIntInitialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpBandwidthTestInitStart(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpBandwidthTestShutdownWithDetailedInfo(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupCreateAsyncRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupCreateTitleCtx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupCreateTitleCtxA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupDeleteRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupDeleteTitleCtx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetCensorComment(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetConvertJidToNpId(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetConvertNpIdToJid(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetCreateTitleCtx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetDeleteRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetDeleteTitleCtx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetInit(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetInitWithFunctionPointer(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetInitWithMemoryPool(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetIsInit(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetNpId(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetSanitizeComment(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetSetTimeout(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNetTerm(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupNpId(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupPollAsync(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupSetTimeout(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpLookupWaitAsync(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntDestroyRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntFinalize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntGetServiceAvailability(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntGetServiceAvailabilityA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntInitialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceChecker2IntIsSetServiceType(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntDestroyRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntFinalize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntGetAvailability(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntGetAvailabilityList(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntInitialize(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpServiceCheckerIntIsCached(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpTitleMetadataIntAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpTitleMetadataIntCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpTitleMetadataIntDeleteRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpTitleMetadataIntGetInfo(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpTitleMetadataIntGetNpTitleId(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpUtilityInit(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpUtilityTerm(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterAbortRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterCensorComment(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterCreateAsyncRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterCreateRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterCreateTitleCtx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterCreateTitleCtxA(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterDeleteRequest(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterDeleteTitleCtx(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterPollAsync(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterSanitizeComment(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterSetTimeout(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

int APS5_VABI sceNpWordFilterWaitAsync(void) {
    NotImplemented_nid_no_patch(__func__);
    return 0;
}

}
