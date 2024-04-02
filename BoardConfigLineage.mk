#
# Copyright (C) 2021 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Add before redbull BoardConfigLineage.mk
BOOT_KERNEL_MODULES += ftm5.ko

include device/google/redbull/BoardConfigLineage.mk

BOOT_SECURITY_PATCH := 2024-04-05
VENDOR_SECURITY_PATCH := 2024-04-05

include vendor/google/barbet/BoardConfigVendor.mk
