# Real-client screenshot runbook

Last reviewed: 2026-09-17.

Only evidence recorded from the current Windows client belongs here. Generated illustrations, marketing images, video frames and recreated interfaces must never be labelled as a playtest.

## Before recording

1. Put untouched files in `field-captures/raw/`; Git ignores this directory.
2. Record date, time zone and displayed client/launcher version. Write `not shown` instead of guessing.
3. Hide email, legal name, account ID, authentication data, payment identifiers, KYC documents and balances.
4. Do not break the launcher intentionally, buy Claims, mask location or start a withdrawal only to create content.
5. Record errors only when they occur naturally.

## Capture list

| ID | Destination | Evidence |
| --- | --- | --- |
| L-01 | Launcher | Home/update screen and displayed version |
| L-02 | Launcher | Natural install, login, update or service error with full message and stage |
| B-01 | Getting Started | Lobby before the first expedition; mode and Pioneer visible |
| B-02 | Getting Started | Tutorial prompt and resulting action |
| B-03 | Getting Started | Found weapon equipped in inventory and character state |
| B-04 | Getting Started | Camp recovery with before/after Health or Energy |
| B-05 | Getting Started | Camp trade screen with balances hidden |
| B-06 | Getting Started | Completed first exit or returned Lobby state |
| E-01 | Extraction | Southern dock and Steamer/ticket requirement |
| E-02 | Extraction | Western Signal Fire interaction prompt |
| E-03 | Extraction | Post-fire threat, only if observed naturally |
| E-04 | Extraction | Lobby after extraction; account and balance hidden |
| G-01 | Equipment | Weapon tooltip with every displayed field |
| G-02 | Equipment | Tool/pickaxe durability in the same build |
| G-03 | Equipment | Inventory/Loadout slots and equipped items |
| G-04 | Traits | Trait names, effects and unlock requirements if shown |
| Q-01 | Quests | Quest Panel and objective states |
| Q-02 | Quests | Completion state and exact displayed reward |
| P-01 | Payout | Dashboard before submission; private data and balance hidden |
| P-02 | Payout | Request confirmation, not a completed-payment claim |
| P-03 | Payout | Processor status with identifiers hidden |
| P-04 | Payout | Optional receipt volunteered by an eligible player with publication consent |

First batch: L-01, B-01–B-06, E-01, E-02, G-01, G-03, G-04 and Q-01. Error and payout images are conditional and must not be manufactured.

## Files and publication gate

- Raw: `<ID>_<YYYY-MM-DD>_<description>.png`.
- Published: `ff1869-<topic>-<description>-<YYYY-MM-DD>.webp`.
- Keep relevant UI context and complete `docs/field-capture-manifest.csv`.
- Captions state Windows client, date and displayed version or `version not shown`.
- Alt text describes only visible evidence.

Use opaque rectangles, not reversible blur, over secrets. Inspect the export at 100% and remove EXIF/location metadata. A file enters `assets/field/` only after its manifest row has date, source, privacy review, consent status where applicable and page destination. Do not compare different builds as a controlled test. Measurements require repeated observations and stay separate from tooltip facts.
