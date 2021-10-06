#
# Copyright (C) 2021 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Boot animation
TARGET_SCREEN_HEIGHT := 2340
TARGET_SCREEN_WIDTH := 1080

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit device configuration
$(call inherit-product, device/google/barbet/aosp_barbet.mk)

-include device/google/barbet/device-lineage.mk

## Device identifier. This must come after all inclusions
PRODUCT_NAME := lineage_barbet
PRODUCT_BRAND := google
PRODUCT_MODEL := Pixel 5a
TARGET_MANUFACTURER := Google

PRODUCT_BUILD_PROP_OVERRIDES += \
    PRODUCT_NAME=barbet \
    PRIVATE_BUILD_DESC="barbet-user 11 RD2A.211001.002 7644766 release-keys"

BUILD_FINGERPRINT := google/barbet/barbet:11/RD2A.211001.002/7644766:user/release-keys
