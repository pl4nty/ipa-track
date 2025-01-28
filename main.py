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
                with open(os.path.join(appBundleId, 'Info.xml'), 'wb') as f:
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
                    with open(os.path.join(appBundleId, "entitlements.xml"), "wb") as f:
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


def extract_app_info(app_dir):
    info_plist_path = os.path.join(app_dir, 'Info.xml')
    entitlements_path = os.path.join(app_dir, 'entitlements.xml')

    with open(info_plist_path, 'rb') as f:
        info_plist = plistlib.load(f)

    with open(entitlements_path, 'rb') as f:
        entitlements = plistlib.load(f)

    name = info_plist.get('CFBundleDisplayName', info_plist.get('CFBundleName', 'N/A'))
    bundle_id = info_plist.get('CFBundleIdentifier', 'N/A')
    url_schemes = ';'.join(
        scheme for url_type in info_plist.get('CFBundleURLTypes', [])
        for scheme in url_type.get('CFBundleURLSchemes', [])
    )
    universal_links = ';'.join(
        f"http://{domain[9:]}/*;https://{domain[9:]}/*"
        for domain in entitlements.get('com.apple.developer.associated-domains', [])
        if domain.startswith('applinks:')
    )

    return name, bundle_id, url_schemes, universal_links


def update_readme(readme_path, app_info):
    # Single app info tuple: (name, bundle_id, url_schemes, universal_links)
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.readlines()

    apps_section_index = next(
        (i for i, line in enumerate(readme_content) if line.strip() == '## Apps'), None
    )

    if apps_section_index is None:
        return

    # Parse existing table into a dictionary
    existing_apps = {}
    table_start = apps_section_index + 3  # Skip header and separator
    for line in readme_content[table_start:]:
        if not line.strip().startswith('|'):
            break
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) == 4:
            existing_apps[parts[1].strip('` ')] = parts

    # Update or add the new app info
    name, bundle_id, url_schemes, universal_links = app_info
    existing_apps[bundle_id] = [name, f'`{bundle_id}`', "N/A" if url_schemes == "" else f'`{url_schemes}`', f'`{universal_links}`']

    table_rows = [
        f"| {' | '.join(row)} |\n"
        for row in existing_apps.values()
    ]

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.writelines(readme_content[:apps_section_index + 3])
        f.writelines(table_rows)


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
    update_readme(os.path.join('ipa-track', 'README.md'), extract_app_info(args.appBundleId))


if __name__ == '__main__':
    main()
