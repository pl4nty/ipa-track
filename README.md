# IPA Track

Track changes to iOS app metadata from source archives (`.ipa`). [Click here](https://github.com/pl4nty/ipa-track/commits/main.atom) to subscribe with RSS.

This tool can also find [URL schemes](https://github.com/search?q=repo%3Apl4nty%2Fipa-track%20%22CFBundleURLSchemes%22&type=code) and [Universal Links](https://github.com/search?q=repo%3Apl4nty%2Fipa-track+%22associated-domains%22&type=code) for [Intune app protection policies](https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy-settings-ios). Looking for [Intune app config policies](https://learn.microsoft.com/en-us/mem/intune/apps/app-configuration-policies-use-ios)? Check out Jamf's [config generator](https://beta.appconfig.jamfresearch.com/generator).

Want to track a new app? Just add a bundle ID folder under `data` with an empty `Info.plist` file, and send a pull request.

## Apps

| Name       | Bundle ID                     | URL Schemes         | Universal Links                                                                 |
|------------|-------------------------------|---------------------|--------------------------------------------------------------------------------|
| Proton Mail | ch.protonmail.protonmail      | protonmail;mailto   | http://proton.me/*, https://proton.me/*, http://account.protonmail.com/*, https://account.protonmail.com/*, http://account.proton.me/*, https://account.proton.me/* |
| 1Password  | com.1password.1password        | onepassword;onepassword8;otpauth;otpauth-apple | http://1password.com/*, https://1password.com/*, http://*.1password.com/*, https://*.1password.com/*, http://b5dev.com/*, https://b5dev.com/*, http://b5test.com/*, https://b5test.com/*, http://b5dev.ca/*, https://b5dev.ca/*, http://*.b5dev.com/*, https://*.b5dev.com/*, http://*.b5test.com/*, https://*.b5test.com/*, http://*.b5dev.ca/*, https://*.b5dev.ca/*, http://*.b5rev.ca/*, https://*.b5rev.ca/* |
| Bitwarden  | com.8bit.bitwarden             | bitwarden;org-appextension-feature-password-management;otpauth | http://*.bitwarden.com/*, https://*.bitwarden.com/*, http://*.bitwarden.eu/*, https://*.bitwarden.eu/*, http://*.bitwarden.pw/*, https://*.bitwarden.pw/* |
| Authy      | com.authy                      | authy;fb478660785554616;otpauth |                                                                                 |
| Bitwarden Authenticator | com.bitwarden.authenticator | bitwarden |                                                                                 |
| Bloomberg  | com.bloomberg.mobile.anywhere  | bbg;bbgvappstore    | http://blinks.bloomberg.com/*, https://blinks.bloomberg.com/*                   |
| Brave      | com.brave.ios.browser          | http;https;brave    | http://vpn.brave.com/*, https://vpn.brave.com/*                                 |
| Calendly   | com.calendly.Calendly          | com.calendly.app    |                                                                                 |
| DocuSign Intune | com.docusign.DocuSignIt.MDMIntune | docusignit;docusignit-intunemam;docusign-v1;docusign-v1-intunemam;db-jtg8lnr1d6xz9ri;db-jtg8lnr1d6xz9ri-intunemam;appx;appx-intunemam;signwithdocusign-extension;signwithdocusign-extension-intunemam;com.googleusercontent.apps.529120587856-giapq9bl6qtn2ec5l8up6vtbdou6sp8a;com.googleusercontent.apps.529120587856-giapq9bl6qtn2ec5l8up6vtbdou6sp8a-intunemam;boxsdk-jjbs68dp748qf20xk2xpxg8thhfhod2p;boxsdk-jjbs68dp748qf20xk2xpxg8thhfhod2p-intunemam;msauth.com.docusign.DocuSignIt.MDMIntune;msauth.com.docusign.DocuSignIt.MDMIntune-intunemam;msauth.com.microsoft.intunemam;msauth.com.microsoft.intunemam-intunemam | http://*.docusign.net/*, https://*.docusign.net/*, http://*.docusign.com/*, https://*.docusign.com/*, http://account-s.docusign.com/*, https://account-s.docusign.com/*, http://account-d.docusign.com/*, https://account-d.docusign.com/*, http://*.account.docusign.com/*, https://*.account.docusign.com/* |
| DocuSign   | com.docusign.DocuSignIt        | docusignit;docusign-v1;db-jtg8lnr1d6xz9ri;appx;signwithdocusign-extension;com.googleusercontent.apps.529120587856-giapq9bl6qtn2ec5l8up6vtbdou6sp8a;boxsdk-jjbs68dp748qf20xk2xpxg8thhfhod2p;msauth.com.docusign.DocuSignIt |                                                                                 |
