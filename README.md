# Fatal Frontier 1869 Wiki

An unofficial, independent English-language Wiki and field guide for **Fatal Frontier 1869**. The site covers getting started, gameplay, Pioneers, weapons, equipment, quests, Claims, Greenbacks, extraction, payout rules and Early Access updates.

## Project status

- Static, crawlable HTML site
- 34 indexable pages plus a custom 404 page
- Responsive Wiki layout with a fixed desktop sidebar and mobile menu
- Unique title, description and canonical metadata per indexable page
- Open Graph, Twitter metadata, JSON-LD, `robots.txt` and `sitemap.xml`
- Source labels and risk disclosures for money-related content

## Local preview

From the project directory, run any static file server. For example:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173/`.

## Quality checks

After changing `styles.css`, synchronize the homepage inline copy first:

```bash
python3 scripts/inline_home_css.py
```

Then run the launch checks:

```bash
python3 scripts/audit_site.py
node --check script.js
xmllint --noout sitemap.xml
```

When the local server is running on port 4173:

```bash
python3 scripts/audit_local_http.py
```

## Deployment

This is a no-build static site. Publish the repository root, configure `404.html` as the custom not-found page, force HTTPS and connect `fatalfrontier1869.wiki`.

See [LAUNCH-CHECKLIST.md](LAUNCH-CHECKLIST.md) for the complete pre-launch and post-launch checklist.

## Editorial note

This project is not affiliated with Paydirt Games. Official claims, independent reviews, community reports and unverified field data are labeled separately. Nothing on the site promises earnings or financial returns.

## Real-client evidence

Follow [`docs/field-capture-runbook.md`](docs/field-capture-runbook.md) before collecting screenshots. Keep originals only under ignored `field-captures/raw/` and complete [`docs/field-capture-manifest.csv`](docs/field-capture-manifest.csv) before publishing a redacted image. Generated illustrations are never labelled as playtest evidence.
