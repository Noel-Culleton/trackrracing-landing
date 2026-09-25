---
name: bulgariaready
description: Working on BulgariaReady — the live Base44 relocation app at bulgariaready.com and the learn.bulgariaready.com SEO content site. Use whenever asked to add content, pages, guides or features to BulgariaReady, to do SEO or keyword work for it, to change its Base44 schema or data, or to write anything about moving to or buying property in Bulgaria. Covers what already exists (so content is not duplicated), the verified Bulgaria facts, the keyword data, and the Base44 traps specific to this app.
---

# BulgariaReady

Two properties, one brand. Know which you're touching before you start.

| | What it is | Where |
|---|---|---|
| **The app** | Live Base44 relocation planner, ~34 pages, login + paywall | `bulgariaready.com`, also `move-smart-bulgaria.base44.app` |
| **The content site** | Static SEO pages, public, no login | `learn.bulgariaready.com` (repo: `bulgaria-ready/`) |

Base44 app ID: `6a26bb4be9a8686320627b09`

Owner: Noel Culleton. Irish. Audience is UK and Irish movers, heavily 50+.

## Rule zero: read the app before writing content for it

**The app is much more built than its entity schema suggests.** A previous session
nearly loaded a 30-letter alphabet and 60 phrases into it that were already there in
better form. Before proposing any content, `list_directory` on `src/pages` and read the
relevant page.

You cannot browse the live site — the sandbox egress proxy blocks both
`bulgariaready.com` and `*.base44.app`. You *can* read all source and query all data
through the Base44 MCP tools. Inspect, don't guess, and never tell the user you looked
at the live site.

## What the app already has

34 pages in `src/pages/`. The substantial ones:

- `Language.jsx` (22KB) — full 30-letter alphabet with phonetics, numbers, a large
  phrase bank categorised Greetings / Property / Area, a `SpeakButton` for
  text-to-speech, and `FREE_LIMIT = 12` gating the rest behind premium. The property
  phrases are genuinely good ("Is the land included?", "Is the road passable in
  winter?"). **Do not rebuild this.**
- `Practice.jsx` (17KB), `CanIMove.jsx` (15KB), `Places.jsx` (14KB), `Home.jsx` (13KB)
- `Costs.jsx`, `Healthcare.jsx`, `TaxFinance.jsx`, `BuyingProcess.jsx`, `SettlingIn.jsx`,
  `Pets.jsx`, `ViewingTrip.jsx`, `CommunityCheck.jsx`, `Renovation.jsx`,
  `MoneyBanking.jsx`, `AvoidScams.jsx`, `SafeQuestions.jsx`, `Partners.jsx`
- `Privacy.jsx`, `Terms.jsx`, `Refunds.jsx` — legal pages exist
- `Upgrade.jsx` — the pricing/upgrade page exists

Entities (`base44/entities/*.jsonc`): `UserProfile`, `ChecklistItem`, `WaitlistSignup`,
`ViewingNote`, `PetProfile`, `CommunityCheck`, `AppSettings`, `Article`, `Enquiry`,
`PartnerListing`, `User`.

### How the Bulgarian audio works

`src/lib/speech.js` resolves playback in three steps:

1. **Recorded MP3** from `src/lib/audioManifest.js` (Azure neural voice
   `bg-BG-KalinaNeural`, served from `/audio/bg/*.mp3`) — device-independent, works on
   any phone.
2. **Device Bulgarian voice** via `speechSynthesis` with `lang: 'bg-BG'`.
3. Neither available → `canSpeak()` returns false and `SpeakButton` **renders nothing**.
   The button disappears rather than failing silently, which is good design but means
   "no button" and "broken" look identical to a user.

The manifest holds ~88 entries: the phrase bank, the alphabet **example words**
(Аптека, Къща, Нотариус…) and the numbers.

**Known gap: the 30 individual letters have no recordings.** `speech.js` exports
`letterOnly()` to say just "Б" from a "Б б" card, but `audioManifest["Б"]` doesn't
exist, so it falls through to the device voice. Bulgarian TTS voices are not installed
by default on iOS or most Android devices, so on a typical phone the speaker button on
each *letter* is invisible while the example word beside it plays fine. Fix is to
generate 30 more clips with the same voice and add them to the manifest.

### The state that actually matters

As of September 2026:

- **`ChecklistItem` is empty.** Zero records. The nine-category checklist is a core
  feature with no content in it.
- **`WaitlistSignup` is empty.** Zero records.
- **2 users total** — Noel (admin) and one other person.
- **`AppSettings.payments_enabled = "false"`**, described as "show the waitlist email
  capture form instead" on the Upgrade page.

The app is not broken. It is **built, empty in places, and unvisited**. Traffic is the
bottleneck, not features. Weight recommendations accordingly — another feature is
almost never the answer.

## Base44 traps for this app

Load the `base44-build-protocol` skill for the full list. The two that will actually
bite here:

1. **`update_entity_schema` is not durable.** It returns success, `list_entity_schemas`
   confirms it, and then the sandbox re-syncs from `base44/entities/<Name>.jsonc` and
   your fields vanish. To change an existing entity: `read_file` the `.jsonc`, merge,
   `write_file` with overwrite, then verify. `create_entity_schema` (new entities) and
   `create_entities` (records) *are* safe and additive.
2. **Checkpoint before and after any batch.** `create_checkpoint` is the only undo.

Also: `list_entity_schemas` intermittently returns "Unable to access this app" while
`query_entities` and `read_file` work fine on the same app. It's a tool quirk. Fall back
to reading `base44/entities/*.jsonc` directly, which is the source of truth anyway.

## Verified Bulgaria facts

Checked September 2026. Re-verify each January — and never write Bulgarian legal,
residency or tax claims from memory.

- **Euro since 1 January 2026** at a fixed 1.95583 BGN. The lev ceased to be legal
  tender **1 February 2026**. Everything is priced in euro now.
- **Full Schengen member since 1 January 2025** — no land, air or sea border checks.
- **Non-EU nationals, including UK citizens, cannot own land** in their own name. They
  *can* own apartments and buildings. Land requires a Bulgarian legal entity, typically
  an EOOD (~€1 share capital, a few working days). Agricultural and forest land is
  restricted regardless of nationality.
- **Irish/EU citizens can own land** in their own name. This Irish-vs-British split is
  the most valuable and most under-served angle the brand has.
- **UK citizens need a Type D long-stay visa** applied for before travelling, then a
  residence permit renewed annually. Permanent residence after 5 years continuous legal
  residence.
- Minimum wage €620/mo (Jan 2026). Median gross salary ~€945. Average gross ~€1,475 —
  badly skewed by Sofia tech. **Quote the median**, not the average.
- Flat 10% personal income tax.

Every page making these claims carries a "correct as of" date and a not-legal-advice
disclaimer. Keep both.

## SEO: what the data says

UK volumes and difficulty, DataForSEO, September 2026. Volumes are declining ~21% YoY
across the board — don't model growth.

**Win these (difficulty 0–5):**

| Keyword | Vol/mo | KD | Status |
|---|---:|---:|---|
| bulgarian alphabet | 2,400 | 0 | Page live |
| learn bulgarian | 320 | 5 | Secondary |
| cost of living in bulgaria | 260 | 0 | Page live |
| living in bulgaria | 210 | 0 | Page live |
| moving to bulgaria from uk | 170 | 0 | Hub h1 — **£2.12 CPC, best intent** |
| basic bulgarian phrases | 140 | 0 | Page live |
| retiring to bulgaria | 40 | 2 | Not written |

**Don't chase `property for sale in bulgaria`** (3,600/mo, KD 9). The intent is
transactional — those people want listings, there are none, they bounce, and that
teaches Google the page is a poor result for terms the site *can* satisfy.

**Don't target `learn bulgarian free`** (70/mo). It was the owner's instinct but the
volume isn't there; `bulgarian alphabet` is 34× bigger at difficulty 0.

### Why duplicate-looking content is correct here

The app's language content is behind login and a paywall, so Google cannot index it. The
public alphabet and phrases pages are the top-of-funnel that the app can never be. They
should *tease* the app's extras — audio pronunciation, property-viewing phrases — rather
than try to replace them. That mirrors the `FREE_LIMIT = 12` model already in the app.

### Subdomain cost

`learn.bulgariaready.com` is a subdomain, so Google treats it as largely a separate site
and it inherits little authority from the root domain. A subfolder
(`bulgariaready.com/learn/`) would rank meaningfully better. The subdomain exists only
because the owner wanted the app untouched. Flag this as the biggest available ranking
upgrade whenever SEO comes up.

## The content site

Repo folder `bulgaria-ready/`. Plain static HTML, shared `styles.css`, no build step.

Design: warm sand `#F7F4ED`, deep green `#1B5E43`, terracotta `#C0562E`, Fraunces
headings, Inter body, **17px base type** — deliberately large for a 50+ audience. Keep
it.

Email capture posts to **Zoho Campaigns**, configured via a single `ZOHO` object at the
bottom of `index.html`. **Zoho Mail alone cannot collect a list** — it's a mailbox.
While `ZOHO.ACTION` is empty the form runs in preview mode: validates, confirms, sends
nothing. Form dropdown values deliberately match the app's `UserProfile` enums
(`retiring`, `uk`, `under_30k`…) so a Zoho export maps onto app profiles without
re-keying.

Every page: honeypot field, explicit unticked GDPR consent, no analytics or cookies (so
no cookie banner — adding analytics changes that).

## Working with Noel

- He communicates in short bursts, often voice-to-text, sometimes garbled. Read for
  intent and act; don't demand clarification for something you can reasonably infer.
- He dismisses multiple-choice question prompts. Prefer stating a recommendation and
  proceeding over `AskUserQuestion`.
- He moves fast and changes direction mid-task. Re-read the brief before assuming an
  earlier instruction still stands — "the app stays unchanged" became "go into base44
  and update" within one session.
- Tell him plainly when a finding kills an earlier plan. He'd rather hear it than have
  work quietly wasted.
