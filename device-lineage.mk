#
# Copyright (C) 2021 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

$(call inherit-product, device/google/redbull/device-lineage.mk)

# Camera
PRODUCT_PACKAGES += \
    android.hardware.camera.provider@2.7-service-google

# HBM
PRODUCT_PACKAGES += \
    HbmSVManagerOverlay
