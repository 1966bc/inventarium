# Submitting Inventarium to Debian

This document describes the process for submitting Inventarium to the official Debian repositories.

## Prerequisites

1. Read the [Debian New Maintainers' Guide](https://www.debian.org/doc/manuals/maint-guide/)
2. Read the [Debian Policy Manual](https://www.debian.org/doc/debian-policy/)
3. Have a GPG key for signing packages

## Step 1: File an ITP (Intent To Package)

Send this email to `submit@bugs.debian.org`:

```
To: submit@bugs.debian.org
Subject: ITP: inventarium -- Laboratory inventory management system

Package: wnpp
Severity: wishlist
Owner: Giuseppe Costanzi <giuseppecostanzi@gmail.com>
X-Debbugs-Cc: debian-devel@lists.debian.org

* Package name    : inventarium
  Version         : 0.1.0
  Upstream Author : Giuseppe Costanzi <giuseppecostanzi@gmail.com>
* URL             : https://github.com/1966bc/inventarium
* License         : GPL-3+
  Programming Lang: Python
  Description     : Laboratory inventory management system

Inventarium is a lightweight inventory management system designed for small
laboratory teams who need a simple, fast, and reliable way to track
consumables, reagents, and supplies.

It uses SQLite for storage and Tkinter for the GUI, with no external
server dependencies.

Key features:
- Product hierarchy: Products → Packages → Batches → Labels
- Barcode generation and scanning (Code128)
- Expiration tracking with FEFO (First Expired, First Out) management
- Purchase request workflow and delivery tracking
- Multi-language UI (English, Italian, Spanish, German, French)
- Statistics dashboard with consumption analysis and ABC classification

The package is already functional and tested on Debian 12 (Bookworm).
It is currently used in production at the Mass Spectrometry Laboratory,
Sant'Andrea University Hospital, Rome.

I intend to maintain this package myself.
```

You will receive a bug number (e.g., #1234567) - save it for reference.

## Step 2: Subscribe to debian-mentors

1. Go to https://lists.debian.org/debian-mentors/
2. Subscribe to the mailing list
3. This is where you'll ask for package review and find a sponsor

## Step 3: Prepare Source Package

The binary package (.deb) is not enough for Debian. You need a source package:

```bash
# Clean build artifacts
debian/rules clean

# Build source package
dpkg-buildpackage -S -us -uc

# This creates in parent directory:
# - inventarium_0.1.0-1.dsc
# - inventarium_0.1.0-1.tar.xz
# - inventarium_0.1.0-1_source.changes
```

## Step 4: Check Package Quality

```bash
# Install lintian (Debian package checker)
sudo apt install lintian

# Check the package
lintian -i ../inventarium_0.1.0-1_all.deb
lintian -i ../inventarium_0.1.0-1.dsc

# Fix any errors (E:) and warnings (W:) reported
```

## Step 5: Create Account on mentors.debian.net

1. Go to https://mentors.debian.net/
2. Create an account
3. Upload your GPG public key

## Step 6: Upload to mentors.debian.net

Create `~/.dput.cf`:

```ini
[mentors]
fqdn = mentors.debian.net
incoming = /upload
method = https
allow_unsigned_uploads = 0
progress_indicator = 2
# Allow uploads for UNRELEASED packages
allowed_distributions = .*
```

Then upload:

```bash
# Sign the changes file
debsign ../inventarium_0.1.0-1_source.changes

# Upload
dput mentors ../inventarium_0.1.0-1_source.changes
```

## Step 7: Request Sponsorship

Send an email to debian-mentors@lists.debian.org:

```
To: debian-mentors@lists.debian.org
Subject: RFS: inventarium/0.1.0-1 [ITP] -- Laboratory inventory management system

Dear mentors,

I am looking for a sponsor for my package "inventarium":

* Package name    : inventarium
  Version         : 0.1.0-1
  Upstream Author : Giuseppe Costanzi <giuseppecostanzi@gmail.com>
* URL             : https://github.com/1966bc/inventarium
* License         : GPL-3+
* Section         : science

It builds this binary package:
  inventarium - Laboratory inventory management system

To access further information about this package, please visit:
https://mentors.debian.net/package/inventarium/

Alternatively, download with dget:
  dget -x https://mentors.debian.net/debian/pool/main/i/inventarium/inventarium_0.1.0-1.dsc

Changes since last upload:
  * Initial release (Closes: #XXXXXXX)

(Replace #XXXXXXX with your ITP bug number)

Regards,
Giuseppe Costanzi
```

## Step 8: Address Feedback

- Sponsors will review your package and provide feedback
- Fix any issues they report
- Upload new versions as needed
- Be patient - this process can take weeks or months

## Useful Resources

- [Debian Mentors FAQ](https://mentors.debian.net/intro-maintainers/)
- [Debian New Maintainers' Guide](https://www.debian.org/doc/manuals/maint-guide/)
- [Debian Policy Manual](https://www.debian.org/doc/debian-policy/)
- [Debian Python Policy](https://www.debian.org/doc/packaging-manuals/python-policy/)
- [Lintian Tags](https://lintian.debian.org/tags)

## Timeline Expectations

- ITP filing: immediate
- Package preparation: 1-2 weeks
- Finding a sponsor: weeks to months
- First upload to Debian unstable: depends on sponsor availability
- Migration to testing: ~10 days after unstable (if no RC bugs)
- Included in next stable release: next Debian release cycle

## Alternative: Personal Repository

If the official process takes too long, consider:

1. **GitHub Releases** (already done): Users download .deb directly
2. **Launchpad PPA**: For Ubuntu users
3. **Own APT repository**: Host on your server

The package is already available at:
https://github.com/1966bc/inventarium/releases
