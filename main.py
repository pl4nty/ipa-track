import plistlib
import zipfile
import os
import argparse
import re
import json


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

    name = info_plist.get('CFBundleName', 'N/A')
    bundle_id = info_plist.get('CFBundleIdentifier', 'N/A')
    url_schemes = ';'.join(
        scheme for url_type in info_plist.get('CFBundleURLTypes', [])
        for scheme in url_type.get('CFBundleURLSchemes', [])
    )
    universal_links = ', '.join(
        f"http://{domain[9:]}/\\*, https://{domain[9:]}/\\*"
        for domain in entitlements.get('com.apple.developer.associated-domains', [])
        if domain.startswith('applinks:')
    )

    return name, bundle_id, url_schemes, universal_links


def update_readme(apps_info):
    readme_path = 'README.md'
    with open(readme_path, 'r') as f:
        readme_content = f.readlines()

    apps_section_index = next(
        (i for i, line in enumerate(readme_content) if line.strip() == '## Apps'), None
    )

    if apps_section_index is not None:
        readme_content = readme_content[:apps_section_index + 1]

    table_header = (
        "| Name       | Bundle ID                     | URL Schemes         | Universal Links                                                                 |\n"
        "|------------|-------------------------------|---------------------|--------------------------------------------------------------------------------|\n"
    )

    table_rows = [
        f"| {name} | `{bundle_id}` | `{url_schemes}` | {universal_links} |\n"
        for name, bundle_id, url_schemes, universal_links in apps_info
    ]

    with open(readme_path, 'w') as f:
        f.writelines(readme_content)
        f.write(table_header)
        f.writelines(table_rows)


def main():
    parser = argparse.ArgumentParser(
        description="Extract Info.plist and entitlements from an IPA file.")
    parser.add_argument("--apps", required=True,
                        help="JSON string containing list of apps with appBundleId and downloadedIPA")
    args = parser.parse_args()
    apps = json.loads(args.apps)

    for app in apps:
        appBundleId = f"ipa-track/data/{app['appBundleId']}"
        extract_info_plist(app['downloadedIPA'], appBundleId)
        extract_entitlements(app['downloadedIPA'], appBundleId)
        extract_privacy_info(app['downloadedIPA'], appBundleId)

    apps_info = [
        extract_app_info(os.path.join(app_dir))
        for app_dir in os.listdir('ipa-track/data')
    ]

    update_readme(apps_info)


if __name__ == '__main__':
    main()
