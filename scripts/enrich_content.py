#!/usr/bin/env python3
"""Add the next source-labeled content layer to the static wiki pages."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-04"


def insert_once(path: Path, marker: str, addition: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if addition.strip() in text:
        return False
    if marker not in text:
        raise SystemExit(f"Insertion marker missing in {path}")
    text = text.replace(marker, addition + marker, 1)
    path.write_text(text, encoding="utf-8")
    return True


def replace_once(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    changed: list[str] = []

    home_addition = """
<section class="section ink-section"><div class="container split"><div class="split-copy"><p class="kicker">Use the field guide well</p><h2>Start with an answer, then verify the details.</h2><p>This Wiki is built for players who want a useful next step without pretending that Early Access data is permanent. The short route is simple: learn the expedition loop, choose a Pioneer for the job, protect the return trip and only then investigate the optional prospecting economy.</p></div><div><h3>What each section is for</h3><p><strong>Guides</strong> explain actions in order, from installing the launcher to surviving a first expedition. <strong>Systems</strong> explain rules such as Claims, Skill Checks, Greenbacks, Traits and extraction. <strong>Pioneers</strong> compare published abilities and practical roles. <strong>Reviews</strong> separate official statements, independent checks and player anecdotes.</p><p>When a number is not published or repeatable, we leave it marked as unknown. That is especially important for weapons, loot values, payout outcomes and any claim about making money. Check the source note on the page, then use the official FAQ or Terms for rules that may affect eligibility.</p><p class="source-note">Editorial check: this section follows the Wiki's source-labeling policy. See <a href="/about.html">How we work</a>, the <a href="/guides/gameplay.html">gameplay guide</a> and the <a href="/reviews/is-fatal-frontier-1869-legit.html">evidence review</a>.</p></div></div></section>
"""
    if insert_once(ROOT / "index.html", "</main>", home_addition):
        changed.append("index.html")

    updates_addition = """
<figure class="roster-illustration"><img src="/assets/update-log.jpg" width="1200" height="800" loading="lazy" decoding="async" alt="Original fan-made illustration of a brass compass and field ledger used to track frontier updates"><figcaption>Unofficial update-log illustration. Dates and claims below link back to the official Community page.</figcaption></figure>
"""
    updates = ROOT / "updates/index.html"
    if insert_once(updates, '<section class="section"><div class="container split">', updates_addition):
        changed.append("updates/index.html")
    update_old = '<div class="log-list"><a class="log-row" href="https://www.fatalfrontier.com/community" rel="nofollow noopener"><span class="log-date">19 Aug 2026</span>'
    update_new = '<div class="log-list"><a class="log-row" href="https://www.fatalfrontier.com/community/pioneers-extracted-more-than-100000-in-august" rel="nofollow noopener"><span class="log-date">01 Sep 2026</span><span class="log-title">Pioneers extracted more than $100,000 in August, according to the developer.</span><span class="log-arrow">↗</span></a><a class="log-row" href="https://www.fatalfrontier.com/community" rel="nofollow noopener"><span class="log-date">19 Aug 2026</span>'
    if replace_once(updates, update_old, update_new):
        changed.append("updates/index.html")
    updates_addition_2 = """
<section class="section"><div class="container"><div class="section-header"><div><p class="kicker">Read the headline carefully</p><h2>What does the August $100,000 post prove?</h2></div><p class="section-intro">It is a current developer-reported milestone, useful for understanding activity around the game but not a player-income average.</p></div><div class="callout"><p>The official Community post dated September 1, 2026 says that Pioneers extracted more than $100,000 in August. The post does not establish how many players contributed, the distribution of results, the cost of Claims or Passes, the share of failed runs, or whether every region can participate. We therefore label it <strong>Developer report</strong> and keep it separate from independent field evidence.</p><p>That distinction matters for returning players: a growing activity headline can justify checking the current build, but it cannot answer “How much will I make?” or “Can I withdraw from my country?” Use the current Terms, Game Lobby and payout guide for those questions.</p><p class="source-note">Source: <a href="https://www.fatalfrontier.com/community/pioneers-extracted-more-than-100000-in-august" rel="nofollow noopener">official August extraction announcement</a>, checked September 4, 2026.</p></div></div></section>
"""
    if insert_once(updates, "</main>", updates_addition_2):
        changed.append("updates/index.html")

    reviews_addition = """
<section class="section ink-section"><div class="container"><div class="section-header"><div><p class="kicker">Evidence snapshot</p><h2>Four kinds of information belong on four different shelves.</h2></div><p class="section-intro">A good review tells you what is known, who said it and what the evidence cannot prove.</p></div><table class="guide-table"><thead><tr><th>Evidence layer</th><th>What it can answer</th><th>What it cannot answer</th></tr></thead><tbody><tr><td>Official FAQ and Terms</td><td>Published rules, modes, eligibility, currencies and payout conditions.</td><td>Whether every player will get the same result.</td></tr><tr><td>Developer announcements</td><td>What the studio says changed, launched or happened in a period.</td><td>An audited average, profit rate or independent user count.</td></tr><tr><td>Independent checks</td><td>Observed launcher, gameplay and usability issues outside marketing copy.</td><td>Permanent conclusions about a fast-changing Early Access build.</td></tr><tr><td>Community anecdotes</td><td>Possible failure modes and questions worth investigating.</td><td>A representative success rate or universal verdict.</td></tr></tbody></table><div class="callout"><h3>Current reading</h3><p>Fatal Frontier 1869 has a real playable survival loop and an official real-value Gold pathway. The September 1 developer report of more than $100,000 extracted in August is relevant context, but it remains a developer-reported aggregate. The responsible conclusion is still: investigate the current rules and risks before spending or expecting income.</p><p class="source-note">Continue to <a href="/reviews/is-fatal-frontier-1869-legit.html">Is Fatal Frontier 1869 Legit?</a>, <a href="/reviews/money-stories.html">Money Stories</a> and the <a href="/updates/">update watch</a>.</p></div></div></section>
"""
    reviews = ROOT / "reviews/index.html"
    if insert_once(reviews, "</main>", reviews_addition):
        changed.append("reviews/index.html")

    pioneers_addition = """
<section class="section ink-section"><div class="container"><div class="section-header"><div><p class="kicker">Choosing a Pioneer</p><h2>Pick for the route you can actually finish.</h2></div><p class="section-intro">Published bonuses are a starting point. A practical choice also depends on weight, energy, enemies and the return route.</p></div><table class="guide-table"><thead><tr><th>Route need</th><th>Published direction</th><th>Good first question</th></tr></thead><tbody><tr><td>Mining and carrying</td><td>Russell, Wade, Boomstick Bob and Nellie publish mining, carry or resource-related strengths.</td><td>Can this Pioneer bring the pickaxe, supplies and recovery tools home?</td></tr><tr><td>Ranged pressure</td><td>Wyatt, Clara, Jane and Nellie publish ranged-damage bonuses.</td><td>Will distance reduce risk enough to protect the extraction plan?</td></tr><tr><td>Melee and defense</td><td>Wade and Skookum Joe publish melee or defensive directions.</td><td>Do you have enough energy and a clear escape route if a fight starts?</td></tr><tr><td>Stealth and movement</td><td>Clara, Skookum Joe, Jane and Russell publish movement, dodge or stealth-related bonuses.</td><td>Can you avoid unnecessary fights rather than treating speed as permission to rush?</td></tr></tbody></table><div class="callout"><p><strong>How to read this table:</strong> these are use-case inferences from official profile bonuses, not a developer tier list. The Wiki does not convert Mining Speed into a guaranteed Gold amount, or a combat bonus into a universal best build. Open a character page for the exact published attributes, then compare the route with <a href="/systems/traits-and-loadouts.html">Traits &amp; Loadouts</a> and <a href="/guides/how-to-extract.html">Extraction</a>.</p></div></div></section>
"""
    pioneers = ROOT / "pioneers/index.html"
    if insert_once(pioneers, "</main>", pioneers_addition):
        changed.append("pioneers/index.html")

    weapons_addition = """
<section class="section ink-section"><div class="container"><div class="section-header"><div><p class="kicker">Armory workbench</p><h2>What can this Wiki safely tell you today?</h2></div><p class="section-intro">Use confirmed role information to plan a run while the item-level catalog is still being tested.</p></div><table class="guide-table"><thead><tr><th>Field</th><th>Status</th><th>How to use it</th></tr></thead><tbody><tr><td>Named item</td><td>Justice is confirmed in the official Wyatt Earp profile.</td><td>Use the <a href="/weapons/justice-double-barreled-shotgun.html">Justice record</a> as the current reference point.</td></tr><tr><td>Weapon role</td><td>Ranged, melee and demolition directions are visible in Pioneer profiles.</td><td>Match the route and Pioneer, not an invented tier list.</td></tr><tr><td>Damage, range and reload</td><td>Not published in a complete official catalog.</td><td>Wait for repeatable in-game captures before comparing numbers.</td></tr><tr><td>Acquisition and durability</td><td>Field data still incomplete and version-sensitive.</td><td>Record where the item was found and which build was tested.</td></tr></tbody></table><div class="callout"><h3>Why the unknowns stay visible</h3><p>A useful armory is not a list of guesses. When a player asks for the best shotgun, the honest answer depends on the current build, ammunition, carry pressure, Pioneer bonuses and the route home. We will add records when a name, source and repeatable detail are available; until then, the blank field is part of the guide.</p><p class="source-note">See <a href="/systems/tools-and-equipment.html">Tools &amp; Equipment</a>, <a href="/systems/traits-and-loadouts.html">Traits &amp; Loadouts</a> and the official <a href="https://www.fatalfrontier.com/faqs" rel="nofollow noopener">FAQ</a>.</p></div></div></section>
"""
    weapons = ROOT / "weapons/index.html"
    if insert_once(weapons, "<p class=\"source-note\">", weapons_addition):
        changed.append("weapons/index.html")

    pioneer_guidance = {
        "wade-tornstrom.html": "Use Wade when the route asks for a steady generalist who can carry a sensible load and survive contact. His published defensive and melee direction is useful for a beginner learning when to disengage, but the lower Energy value means a heavy pack and long sprint chain can still create a bad return. Test a small loadout first and treat his free availability as a reason to learn the loop, not proof that he is best at every job.",
        "wyatt-earp.html": "Use Wyatt when a close-range answer and a clear sightline matter more than quiet resource farming. Justice is the named double-barreled shotgun in the official profile, while his ranged, defense and view bonuses suggest a deliberate combat role. The profile does not publish damage, ammo or reload data, so plan around positioning and extraction rather than assuming the signature weapon solves every encounter.",
        "clara-mckinley.html": "Use Clara for a distance-first route where movement, ranged pressure and stealth can reduce unnecessary contact. Her published bonuses point toward a fast sharpshooter, but the lower Health, Energy and Encumbrance values make preparation important. Keep the expedition short until you know how much ammunition, food and recovery capacity your current build consumes.",
        "russell-greeneberry.html": "Use Russell for a resource-focused route when carrying capacity and mining speed are more valuable than a forgiving mistake budget. His published bonuses strongly suggest a haul-building role, but the page does not turn Mining Speed into a guaranteed Gold result. Set a carrying limit before leaving camp so the advantage does not become an excuse to stay out past a safe extraction window.",
        "boomstick-bob.html": "Use Boomstick Bob when a route benefits from resource clearing and you understand the cost of noisy or dangerous encounters. His official profile describes a demolitionist direction with mining, chopping and ranged bonuses. Exact explosive items and damage remain unverified, so treat Bob as a role hypothesis and test one objective at a time rather than planning around imagined blast values.",
        "skookum-joe-mason.html": "Use Skookum Joe for a stealth-and-melee route that values approach, movement and choosing the fight. His published bonuses support a quiet scout interpretation, but stealth break conditions and enemy awareness are still field questions. Carry an exit plan: a stealth bonus helps you avoid risk, it does not make a loud recovery or signal-fire sequence safe by itself.",
        "jane-splinter-holloway.html": "Use Jane when chopping, movement and a durable field rhythm are central to the route. Her published profile combines woodsman and combat directions, which makes her a natural candidate for clearing paths and collecting timber. The best loadout still depends on current stamina, tools and enemy pressure; do not infer unique weapon damage from the character story.",
        "nellie-cashman.html": "Use Nellie as a flexible support-leaning Pioneer when you want resource and ranged options with a large Energy pool. Her official profile also names Finnegan as an animal companion, but the Wiki does not invent companion damage or healing numbers. Protect the return route and confirm which companion behavior is present in the current build before treating her as a dedicated healer.",
    }
    for filename, copy in pioneer_guidance.items():
        path = ROOT / "pioneers" / filename
        addition = f'''<div class="callout pioneer-usage"><h3>Practical expedition use</h3><p>{copy}</p><p><strong>Build rule:</strong> match the published role to the route, then test the smallest loadout that can survive and extract. Unknown damage, drop rates, durability and payout effects stay unconfirmed.</p></div>\n'''
        if insert_once(path, '<p class="source-note">', addition):
            changed.append(f"pioneers/{filename}")

    touched = {
        "index.html",
        "updates/index.html",
        "reviews/index.html",
        "pioneers/index.html",
        "weapons/index.html",
        *[f"pioneers/{filename}" for filename in pioneer_guidance],
    }
    for rel in touched:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        updated = text.replace("Last checked Aug 2026", "Last checked Sep 2026")
        updated = updated.replace("Checked Aug 2026", "Checked Sep 2026")
        updated = updated.replace("Updated Aug 2026", "Updated Sep 2026")
        updated = updated.replace('dateModified":"2026-08-26"', f'dateModified":"{TODAY}"')
        updated = updated.replace('dateModified":"2026-08-27"', f'dateModified":"{TODAY}"')
        updated = updated.replace('dateModified":"2026-08-28"', f'dateModified":"{TODAY}"')
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            if rel not in changed:
                changed.append(rel)

    sitemap = ROOT / "sitemap.xml"
    sitemap_text = sitemap.read_text(encoding="utf-8")
    for rel in touched:
        if rel == "index.html":
            route = "/"
        elif rel.endswith("/index.html"):
            route = "/" + rel.removesuffix("index.html")
        else:
            route = "/" + rel
        sitemap_text = sitemap_text.replace(
            f"<loc>https://fatalfrontier1869.wiki{route}</loc><lastmod>2026-08-27</lastmod>",
            f"<loc>https://fatalfrontier1869.wiki{route}</loc><lastmod>{TODAY}</lastmod>",
        )
        sitemap_text = sitemap_text.replace(
            f"<loc>https://fatalfrontier1869.wiki{route}</loc><lastmod>2026-08-26</lastmod>",
            f"<loc>https://fatalfrontier1869.wiki{route}</loc><lastmod>{TODAY}</lastmod>",
        )
    sitemap.write_text(sitemap_text, encoding="utf-8")
    changed.append("sitemap.xml")

    print(f"Enriched {len(set(changed))} files")
    for item in sorted(set(changed)):
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
