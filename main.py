import plistlib
import zipfile
import os
import argparse
import re


def extract_info_plist(downloadedIPA, appBundleId):
    with zipfile.ZipFile(downloadedIPA, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('Info.plist') and file_name.startswith('Payload/'):
                plist_data = zip_ref.read(file_name)
                os.makedirs(appBundleId, exist_ok=True)
                info_dict = plistlib.loads(plist_data)
                with open(os.path.join(appBundleId, 'Info.plist'), 'wb') as f:
                    plistlib.dump(info_dict, f, fmt=plistlib.FMT_XML)
                break


def extract_entitlements(downloadedIPA, appBundleId):
    with zipfile.ZipFile(downloadedIPA, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if re.match(r'^Payload/[^/]+\.app/([^/.]+)$', file_name):
                print(f"found binary {file_name}")
                binary_data = zip_ref.read(file_name)
                start_idx = binary_data.find(b'<plist version="1.0">\n')
                end_idx = binary_data.find(b"</plist>")
                if start_idx != -1 and end_idx != -1:
                    end_idx += len(b"</plist>")
                    entitlements_data = binary_data[start_idx:end_idx]
                    os.makedirs(appBundleId, exist_ok=True)
                    with open(os.path.join(appBundleId, "entitlements.plist"), "wb") as f:
                        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
                        f.write(
                            b'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
                        f.write(entitlements_data)
                break


def extract_privacy_info(downloadedIPA, appBundleId):
    with zipfile.ZipFile(downloadedIPA, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('PrivacyInfo.xcprivacy') and file_name.startswith('Payload/'):
                os.makedirs(appBundleId, exist_ok=True)
                with open(os.path.join(appBundleId, 'PrivacyInfo.xcprivacy'), 'wb') as f:
                    f.write(zip_ref.read(file_name))
                break


def main():
    parser = argparse.ArgumentParser(
        description="Extract Info.plist and entitlements from an IPA file.")
    parser.add_argument("--downloadedIPA", required=True,
                        help="Path to the IPA file")
    parser.add_argument("--appBundleId", required=True, help="The Bundle ID")
    args = parser.parse_args()
    extract_info_plist(args.downloadedIPA, args.appBundleId)
    extract_entitlements(args.downloadedIPA, args.appBundleId)
    extract_privacy_info(args.downloadedIPA, args.appBundleId)


if __name__ == '__main__':
    main()
