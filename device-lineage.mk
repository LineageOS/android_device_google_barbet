#
# Copyright (C) 2021 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

$(call inherit-product, device/google/redbull/device-lineage.mk)

# CHRE
$(call soong_config_set,chre,chre_daemon_dsp_library,//vendor/google/barbet:libadsprpc)

# HBM
PRODUCT_PACKAGES += \
    HbmSVManagerOverlay
