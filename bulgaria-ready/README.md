# BulgariaReady — registration landing page

A single, self-contained `index.html`. No build step, no dependencies, no framework.
Open it in a browser and it works.

Launch target for the app itself: **January 2027**.

---

## 1. Fill in the placeholders

Search `index.html` for `TODO` — there are three spots:

| What | Where | Currently |
|---|---|---|
| Live domain (OG tags + JSON-LD) | `<head>` | `https://bulgariaready.com/` |
| Contact email | footer | `hello@bulgariaready.com` |
| Privacy / Terms links | footer | `/privacy.html`, `/terms.html` |

The privacy page is **not optional** — you're collecting email addresses from EU and UK
residents, so GDPR applies. The form already has an explicit, unticked consent box and
tells people what they're signing up for, which is the part most sites get wrong.

---

## 2. Wire up the email capture

**Zoho Mail on its own will not work here.** Zoho Mail is a mailbox — it receives
messages, it doesn't collect, store or segment a signup list. You need **Zoho
Campaigns** (free tier is plenty for a pre-launch list) sitting behind the form, with
Zoho Mail as the address people see and reply to.

### Steps

1. Zoho Campaigns → **Contacts → Manage Lists → Create List**. Call it something like
   `BulgariaReady Waitlist`.
2. Add three custom fields to that list, so the dropdowns on the page have somewhere to
   land:
   - `Passport` (single line) → receives `CONTACT_CF1`
   - `Reason` (single line) → receives `CONTACT_CF2`
   - `Budget` (single line) → receives `CONTACT_CF3`
3. **Signup Forms → Embed Form.** Build a form with Email, First Name and those three
   custom fields.
4. Zoho gives you generated HTML. From it, copy:
   - the `<form>` tag's `action` URL
   - every `<input type="hidden">` as a name/value pair
5. Paste them into the `ZOHO` object near the bottom of `index.html`:

```js
var ZOHO = {
  ACTION: 'https://xxxxx.maillist-manage.eu/weboptin.zc',
  HIDDEN: {
    'zc_trackCode':  '...',
    'lD':            '...',
    'emailReportId': '...',
    'zx':            '...',
    'submitType':    'optinCustomView',
    'mode':          'OptinCreateView'
  }
};
```

6. Turn on **double opt-in** in the list settings, and set the confirmation and welcome
   emails to send from your Zoho Mail address on your own domain.

### Preview mode

While `ACTION` is empty the form runs in preview mode: it validates properly and shows
the success state, but posts nothing anywhere. The page is safe to put live before Zoho
is connected — it just won't capture anything, so don't drive traffic at it yet.

### Why the field names look like that

`CONTACT_EMAIL`, `FIRSTNAME` and `CONTACT_CF1..3` are Zoho Campaigns' own naming. The
dropdown *values* (`retiring`, `holiday_home`, `under_30k`, `uk`, `eu`…) deliberately
match the `UserProfile` enums in the Base44 app, so in January you can map a Zoho export
straight onto app profiles without re-keying anything.

---

## 3. Deploying

The page is static — anything that serves HTML will do.

**It cannot be served from this repo's GitHub Pages site.** `trackrracing-landing` has a
`CNAME` pointing at `join.trackrracing.com`, and GitHub Pages allows one custom domain
per repository. The files live here for now; they need their own home.

Pick one:

- **New GitHub repo + Pages** — recommended. Copy `index.html` to the root of a fresh
  repo, add a `CNAME` containing your Bulgaria domain, enable Pages. Clean separation,
  free, and TrackrRacing stays untouched.
- **Vercel / Netlify** — drag-and-drop or point at the repo, then attach the domain.
- **Cloudflare Pages** — if you want the domain's DNS there too. Watch the MX records
  when transferring, or you'll knock out the Zoho mailbox.

---

## 4. Built-in behaviour worth knowing

- **Honeypot** — a hidden `website_url` field. Bots fill it, people don't; submissions
  that contain it are silently discarded.
- **Returning visitors** — anyone who has already registered on that device sees the
  confirmed state instead of the form. Stored in `localStorage`, wrapped in try/catch so
  private browsing doesn't break the page.
- **Accessibility** — real labels on every field, visible focus rings, `prefers-reduced-motion`
  respected, 17px base body size (deliberately large: a lot of this audience is 50+).
- **No tracking** — no analytics, no pixels, no third-party scripts. Add them if you
  want, but that then needs a cookie banner.

---

## 5. Facts on the page, and when to re-check them

The page makes specific factual claims. They were verified in September 2026:

- Bulgaria adopted the euro on **1 January 2026** at 1.95583 BGN; the lev ceased to be
  legal tender on **1 February 2026**.
- Bulgaria has been a **full Schengen member since 1 January 2025** — no land, air or
  sea border checks.
- **Non-EU nationals (including UK citizens) cannot own land** in Bulgaria in their own
  name. They can own apartments and buildings. Land requires a Bulgarian legal entity,
  typically an EOOD. Agricultural and forest land is restricted regardless of
  nationality.
- UK citizens need a **Type D long-stay visa**, applied for before travelling, then a
  residence permit renewed annually; permanent residence after five years of continuous
  legal residence.

Re-check before any significant traffic push, and again each January. The page carries a
"correct as of September 2026" line and a prominent not-legal-advice disclaimer — keep
both.

---

## 6. Suggested next step

The strongest single upgrade is a **lead magnet**: a "Bulgaria Move Starter Checklist"
PDF delivered instantly by the Zoho autoresponder. It reliably lifts signup rates versus
"we'll email you eventually", and it gives your January launch email a warm list that
already knows who you are.
