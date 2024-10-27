#!/usr/bin/env -S PYTHONPATH=../../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.extract import extract_fns_user_type
from extract_utils.extract_pixel import (
    extract_pixel_factory_image,
    extract_pixel_firmware,
    pixel_factory_image_regex,
    pixel_firmware_regex,
)
from extract_utils.file import FileArgs, FileList
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/google/interfaces',
    'hardware/google/pixel',
    'hardware/qcom/sm7250/display',
    'hardware/qcom/sm7250/gps',
    'hardware/qcom/wlan/legacy',
    'vendor/qcom/opensource/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.hardware.tui_comm@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
    'libwpa_client': lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'product/etc/felica/common.cfg': blob_fixup()
        .patch_file('osaifu-keitai.patch'),
    'product/etc/sysconfig/nexus.xml': blob_fixup()
        .regex_replace('qulacomm', 'qualcomm'),
    'system_ext/priv-app/HbmSVManager/HbmSVManager.apk': blob_fixup()
        .apktool_patch('HbmSVManager.patch', '-r'),
    (
        'vendor/bin/hw/android.hardware.rebootescrow-service.citadel',
        'vendor/lib64/android.hardware.keymaster@4.1-impl.nos.so',
    ): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/lib64/libgooglecamerahal.so': blob_fixup()
        .add_needed('libmeminfo_shim.so'),
}  # fmt: skip

extract_fns: extract_fns_user_type = {
    pixel_factory_image_regex: extract_pixel_factory_image,
    pixel_firmware_regex: extract_pixel_firmware,
}

module = ExtractUtilsModule(
    'barbet',
    'google',
    device_rel_path='device/google/barbet/barbet',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_generated_carriersettings_file=True,
    add_firmware_proprietary_file=True,
    extract_fns=extract_fns,
)


def fix_vendor_file_list(file_list: FileList):
    file_list.get_file(
        'vendor/app/adreno_graphics_driver/adreno_graphics_driver.apk'
    ).set_arg(FileArgs.PRESIGNED, True)

    file_list.get_file('vendor/app/CneApp/CneApp.apk').set_arg(
        FileArgs.REQUIRED, 'CneApp.libvndfwk_detect_jni.qti_symlink'
    )

    file_list.get_file('vendor/lib/egl/libEGL_adreno.so').set_arg(
        FileArgs.SYMLINK, 'vendor/lib/libEGL_adreno.so'
    )
    file_list.get_file('vendor/lib/egl/libGLESv2_adreno.so').set_arg(
        FileArgs.SYMLINK, 'vendor/lib/libGLESv2_adreno.so'
    )
    file_list.get_file('vendor/lib/egl/libq3dtools_adreno.so').set_arg(
        FileArgs.SYMLINK, 'vendor/lib/libq3dtools_adreno.so'
    )
    file_list.get_file('vendor/lib64/egl/libEGL_adreno.so').set_arg(
        FileArgs.SYMLINK, 'vendor/lib64/libEGL_adreno.so'
    )
    file_list.get_file('vendor/lib64/egl/libGLESv2_adreno.so').set_arg(
        FileArgs.SYMLINK, 'vendor/lib64/libGLESv2_adreno.so'
    )
    file_list.get_file('vendor/lib64/egl/libq3dtools_adreno.so').set_arg(
        FileArgs.SYMLINK, 'vendor/lib64/libq3dtools_adreno.so'
    )

    # 32bit libmmcamera_faceproc is unable to resolved the following symbols:
    # __aeabi_memcpy@LIBC_PRIVATE, __aeabi_memset@LIBC_PRIVATE, __gnu_Unwind_Find_exidx@LIBC_PRIVATE
    # lowi-server, libcne, libwqe depend on libwpa_client, which is a gnu makefile target
    disable_checkelf_file_paths = [
        'vendor/bin/lowi-server',
        'vendor/lib/libcne.so',
        'vendor/lib/libmmcamera_faceproc.so',
        'vendor/lib/libwqe.so',
        'vendor/lib64/libcne.so',
        'vendor/lib64/libmmcamera_faceproc.so',
        'vendor/lib64/libwqe.so',
    ]
    for file_path in disable_checkelf_file_paths:
        file_list.get_file(file_path).set_arg(FileArgs.DISABLE_CHECKELF, True)

    module_suffix_file_paths = [
        'vendor/lib/vendor.qti.hardware.tui_comm@1.0.so',
        'vendor/lib/vendor.qti.imsrtpservice@3.0.so',
        'vendor/lib64/vendor.qti.hardware.tui_comm@1.0.so',
        'vendor/lib64/vendor.qti.imsrtpservice@3.0.so',
    ]

    for file_path in module_suffix_file_paths:
        file_list.get_file(file_path).set_arg(FileArgs.MODULE_SUFFIX, '_vendor')


module.add_generated_proprietary_file(
    'proprietary-files-vendor.txt',
    partition='vendor',
    skip_file_list_name='skip-files-vendor.txt',
    fix_file_list=fix_vendor_file_list,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
