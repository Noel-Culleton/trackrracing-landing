# learn.bulgariaready.com — SEO content site

Static pages designed to rank, pull in search traffic, and hand it to the live
BulgariaReady app. **The app itself is untouched by anything in this folder.**

| File | Serves as | Targets |
|---|---|---|
| `index.html` | `/` | "moving to bulgaria from uk", "living in bulgaria", "cost of living in bulgaria" |
| `bulgarian-alphabet.html` | `/bulgarian-alphabet` | "bulgarian alphabet" + its long tail |
| `styles.css` | shared stylesheet | — |
| `robots.txt`, `sitemap.xml` | crawl directives | — |

Every page links out to `https://bulgariaready.com` (the app). No page writes to it.

---

## 1. Why the alphabet, and not "learn Bulgarian free"

Your instinct — free Bulgarian for people moving over — was right. The specific
phrasing was not, and the gap is large. UK search volumes and difficulty
(DataForSEO, September 2026):

| Keyword | Volume/mo | Difficulty | Verdict |
|---|---:|---:|---|
| **bulgarian alphabet** | **2,400** | **0** | The prize |
| learn bulgarian | 320 | 5 | Decent secondary |
| basic bulgarian phrases | 140 | 0 | Worth a page later |
| bulgarian alphabet in english | 140 | low | Covered by the same page |
| learn bulgarian free | **70** | — | Your original phrasing — too thin |
| bulgarian cyrillic alphabet | 70 | 4 | Covered |
| bulgarian language course | 20 | high | Ignore |
| bulgarian for beginners | 10 | high | Ignore |

"Learn bulgarian free" gets 70 searches a month. "Bulgarian alphabet" gets 2,400 at
**difficulty 0** — meaning a new page with decent content can realistically rank. The
whole alphabet cluster is worth roughly 2,900/mo and nearly all of it is difficulty
0–5.

### Relocation keywords, for the hub page

| Keyword | Volume/mo | Difficulty | Notes |
|---|---:|---:|---|
| property for sale in bulgaria | 3,600 | 9 | **Don't chase** — see below |
| cost of living in bulgaria | 260 | 0 | Easy win, write this next |
| living in bulgaria | 210 | 0 | Easy win |
| buying property in bulgaria | 170 | 23 | Hardest of the set |
| moving to bulgaria from uk | 170 | 0 | **Best intent** — CPC £2.12 |
| moving to bulgaria | 90 | low | — |
| retiring to bulgaria | 40 | 2 | Small but perfectly matched |

**Why not "property for sale in bulgaria"** despite 3,600/mo and difficulty 9: the
intent is transactional. Those people want listings. You have no listings, so they
bounce, and bouncing traffic teaches Google the page is a poor result. Chasing it
would cost you ranking on the terms you *can* satisfy.

**"moving to bulgaria from uk" has a £2.12 CPC** — advertisers pay real money for that
click, which tells you it converts. At difficulty 0 it's the single best target on the
list, which is why it's the `<h1>` on the hub page.

### Honest caveats

- **Volumes are declining.** The alphabet term is down ~21% year on year, and the
  relocation cluster is down similarly. Still worth having; don't model growth on it.
- **Alphabet traffic is mostly not movers.** Search intent is informational —
  students, hobbyists, people curious about Cyrillic. Conversion to a relocation app
  will be a low single-digit percentage. That is still infinitely more than the app
  gets today, and the page costs nothing to keep.
- **These are UK figures.** Ireland is a fraction of the volume; the numbers are
  dominated by UK search.

---

## 2. Pages built, and what's left

Built and cross-linked (the internal linking is what makes a cluster rank rather than a
set of orphan pages):

1. **Hub** `/` — "moving to bulgaria from uk" (170/mo, KD 0, £2.12 CPC)
2. **Bulgarian alphabet** (2,400/mo, KD 0) — the traffic magnet
3. **Cost of living in Bulgaria** (260/mo, KD 0)
4. **Living in Bulgaria** (210/mo, KD 0)
5. **Basic Bulgarian phrases** (140/mo, KD 0)

Still unwritten: **Retiring to Bulgaria** (40/mo, KD 2) — small volume, but precisely
the buyer.

---

## 2a. IMPORTANT: don't duplicate the app

The Base44 app is **far more built than its entity schema suggests** — 34 pages. Before
writing any new content, read the app first:

```
list_directory(appId, path="src/pages")
read_file(appId, paths=["src/pages/<Page>.jsx"])
```

`src/pages/Language.jsx` (22KB) already contains the full alphabet with phonetics,
numbers, and a large categorised phrase bank — including property-viewing questions
("Is the land included?", "Is the road passable in winter?") — plus a `SpeakButton` for
spoken pronunciation and `FREE_LIMIT = 12` gating the rest behind premium.
`Privacy.jsx`, `Terms.jsx`, `Refunds.jsx` and `Upgrade.jsx` exist too.

**The overlap is deliberate and correct.** The app's content sits behind login and a
paywall, so Google cannot index it. These public pages are the top-of-funnel the app
can never be. They should *tease* the app's extras — audio, property phrases — not try
to replace them, which is exactly what the `FREE_LIMIT = 12` model already implies. Both
language pages now close with that pitch.

What this means in practice: **write public pages that rank, and push depth into the
app.** Never port app content out to the site, or site content into the app, without
reading both first.

---

## 3. Deploying to the subdomain

Target: **`learn.bulgariaready.com`**, leaving the app on the root domain.

1. Host the folder on Netlify, Vercel or Cloudflare Pages (drag-and-drop works).
2. Add `learn.bulgariaready.com` as a custom domain there.
3. At your DNS provider, add a `CNAME` for `learn` pointing at the host.
4. **Don't touch the MX records** — that's your Zoho mailbox.
5. Submit `https://learn.bulgariaready.com/sitemap.xml` in Google Search Console.

Pretty URLs: the alphabet page should serve at `/bulgarian-alphabet`, not
`/bulgarian-alphabet.html`. Netlify and Cloudflare Pages do this automatically. On
Vercel set `"cleanUrls": true` in `vercel.json`. The canonical tags already assume the
clean URL.

### One SEO tradeoff worth knowing

Google treats a subdomain as a largely separate site, so `learn.bulgariaready.com`
won't inherit much authority from the root domain. A subfolder —
`bulgariaready.com/learn/` — is meaningfully better for SEO. The subdomain is the
right call *only* because you want the app untouched, and it is a genuine cost. If you
later get comfortable putting a reverse proxy or rewrite in front of the app, moving
this to a subfolder is the single biggest ranking upgrade available.

---

## 4. Email capture

**Zoho Mail on its own will not work.** It's a mailbox — it receives messages, it
doesn't collect or segment a list. You need **Zoho Campaigns** (free tier is plenty),
with Zoho Mail as the address people see and reply to.

1. Zoho Campaigns → **Contacts → Manage Lists → Create List**.
2. Add three custom fields: `Passport` → `CONTACT_CF1`, `Reason` → `CONTACT_CF2`,
   `Budget` → `CONTACT_CF3`.
3. **Signup Forms → Embed Form**, then copy the generated form's `action` URL and every
   `<input type="hidden">` into the `ZOHO` object at the bottom of `index.html`:

```js
var ZOHO = {
  ACTION: 'https://xxxxx.maillist-manage.eu/weboptin.zc',
  HIDDEN: { 'zc_trackCode': '...', 'lD': '...', 'zx': '...' }
};
```

4. Turn on double opt-in and send confirmations from your Zoho address.

**Preview mode:** while `ACTION` is empty the form validates and confirms but posts
nothing. Safe to deploy before Zoho is connected — it just won't capture anything.

Dropdown values (`retiring`, `uk`, `under_30k`…) deliberately match the `UserProfile`
enums in the Base44 app, so a Zoho export maps onto app profiles without re-keying.

---

## 5. Placeholders to fill

Search `TODO`. Also:

- `hello@bulgariaready.com` — replace with your real Zoho address (3 places)
- `/privacy.html` — **write this.** You're collecting email addresses from UK and EU
  residents, so GDPR applies. The form already has explicit unticked consent, which is
  the part most sites get wrong, but you still need the policy page.

---

## 6. Facts on these pages

Verified September 2026 — re-check each January:

- Bulgaria adopted the euro **1 January 2026** at 1.95583 BGN; the lev ceased to be
  legal tender **1 February 2026**.
- Full **Schengen member since 1 January 2025**.
- **Non-EU nationals (including UK citizens) cannot own land** in their own name. They
  can own apartments and buildings. Land needs a Bulgarian entity, typically an EOOD.
  Agricultural and forest land is restricted regardless of nationality.
- UK citizens need a **Type D long-stay visa** before travelling, then an annually
  renewed residence permit; permanent residence after five years.

Both pages carry a "correct as of September 2026" line and a not-legal-advice
disclaimer. Keep both.

---

## 7. Built-in behaviour

- **Honeypot** `website_url` field — bots fill it, submissions are silently dropped
- **Returning visitors** see the confirmed state (`localStorage`, try/catch wrapped)
- **Accessibility** — real labels, visible focus rings, `aria-pressed` on the letter
  grid, reduced-motion respected, 17px base type
- **No tracking** — no analytics or pixels, so no cookie banner needed. Adding
  analytics changes that.
- The alphabet table is **static HTML**, not JS-rendered, so Google indexes all 30 rows
