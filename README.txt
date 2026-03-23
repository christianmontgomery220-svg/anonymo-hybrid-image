ANONYMO AI / TCF-TFB
Hybrid Invisible Provenance Package
Version: 1.0
Date: 2026-03-23

PURPOSE
This package serves as a proof-of-existence and verification scaffold for a visual asset
created under a hybrid Human–AI workflow.

AUTHORSHIP
Author: Chris Montgomery
ORCID: 0009-0009-5364-249X
Original Authorship: Human
Creation Type: Human-AI Hybrid
AI Assistance: Yes
Intellectual Framework: TCF/TFB
Project: Anonymo AI
Copyright: © 2025–2026 Chris Montgomery

PACKAGE CONTENTS
- metadata.json ............. descriptive metadata layer
- manifest.json ............. provenance / verification manifest
- checksum.txt .............. SHA-256 placeholders or computed values
- README.txt ............... package explanation
- README.md ................ GitHub-friendly public proof text
- TEMPLATE_XMP.xml ......... embeddable invisible metadata template
- ASSET_FILES_HERE.txt ..... instructions for inserting the final asset

HOW TO USE
1. Put the final image file in this package folder.
2. Rename it consistently, for example:
   - asset_original.png
   - asset_with_metadata.png
3. Generate SHA-256 hashes for the files.
4. Replace the placeholders in:
   - metadata.json
   - manifest.json
   - checksum.txt
   - TEMPLATE_XMP.xml
5. Re-zip the package and publish it as a frozen release, GitHub proof-of-existence package,
   or DOI-attached verification bundle.

VERIFICATION MODEL
This package combines:
- Embedded metadata (XMP/IPTC)
- Human-AI hybrid declaration
- External SHA-256 integrity verification
- Public documentation and proof-of-existence

RECOMMENDED LINKS
Documentation: https://anonymodocs.com/
Theory site: https://tfbtheory.com/

NOTES
This scaffold was generated without the final image binary, so hash fields remain as placeholders
until the asset is inserted and frozen.
