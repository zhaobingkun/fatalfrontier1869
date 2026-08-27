# Fatal Frontier 1869 Wiki Launch Checklist

## Current status

- Site content and local production files: **ready for deployment after the final automated and browser audit**.
- Candidate production URL: `https://fatalfrontier1869.wiki/`.
- Hosting and DNS: **not configured in this project**. The candidate domain must resolve before the site can be called live.

## Before deployment

- Choose a static host and connect `fatalfrontier1869.wiki`.
- Set the project root as the publish directory; there is no build step.
- Force HTTPS and redirect HTTP to HTTPS.
- Configure `/404.html` as the custom not-found page.
- Confirm the host preserves clean directory routes such as `/guides/` and `/systems/`.
- Update `/privacy.html` with the hosting provider, analytics, advertising, cookies, and contact details actually used at launch.
- If the final domain changes, replace it in canonical tags, Open Graph URLs, structured data, `robots.txt`, and `sitemap.xml` before publishing.

## Deployment verification

- Open the homepage and every Hub page directly on the production domain.
- Confirm one canonical URL per page and no accidental `noindex` outside `/404.html`.
- Confirm `https://fatalfrontier1869.wiki/robots.txt` and `/sitemap.xml` return HTTP 200.
- Confirm images, CSS, JavaScript, internal navigation, browser back/forward, and mobile menu all work over HTTPS.
- Confirm external download buttons lead to `https://www.fatalfrontier.com/lpdownload`.
- Check the production 404 response and page.

## Search launch

- Add the domain property to Google Search Console.
- Submit `https://fatalfrontier1869.wiki/sitemap.xml`.
- Request indexing for the homepage, Guides, Gameplay, Payout Methods, Is It Legit, Claims, Greenbacks, Pioneers, and Weapons.
- Monitor indexing and impressions for 2–4 weeks before making large structural changes.
- Refresh game facts after official patches and display a reviewed date on updated pages.

## Optional after launch

- Add privacy-respecting analytics only after the privacy page is updated.
- Add a correction/contact method.
- Capture real in-game field data for weapons, Claims, Quests, Skill Checks, and item tables; keep unverified values labeled until then.
