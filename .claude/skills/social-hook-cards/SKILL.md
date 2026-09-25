---
name: social-hook-cards
description: Create text-on-image hook cards for social posts — Facebook and LinkedIn group posts, Instagram, X, blog headers, link previews. Use whenever asked for post images, hook images, quote cards, carousel slides, thumbnails, OG images, or "a picture with the text in it" to go with written posts. Renders real typography via headless Chromium from a JSON spec, so a set of cards stays on-brand and can be regenerated after an edit.
---

# Social hook cards

Text-on-image cards that stop a scroll. Rendered as HTML through headless Chromium, so
you get real webfonts, flexbox and CSS rather than fighting an image library.

`make_cards.py` in this folder does the rendering. You write the JSON spec.

```bash
python3 .claude/skills/social-hook-cards/make_cards.py cards.json ./out
```

## The five rules that matter

**1. One idea per card.** A card competing with a caption loses. The image carries a
single hook; the post carries the detail. If the headline needs a comma and a clause,
it is two cards.

**2. Headline under about eight words.** These are read at thumbnail size while
someone's thumb is moving. "A nod means no" works. "Understanding Bulgarian non-verbal
communication" does not.

**3. Nothing below 30px on a 1080 canvas.** A phone renders a 1080-wide image at
roughly 400px, so 24px type becomes ~9px — invisible. This is the single most common
mistake; the script's brand mark defaults to 32px for exactly this reason. Check every
element against that floor, not just the headline.

**4. Vary the design across a set.** Eight identical-looking cards read as a template in
a feed, and platforms flag near-duplicate images posted in sequence as spam. Rotate
background colour, layout and emphasis while keeping one palette and one type pairing.
Cards from the same brand should look related, not cloned.

**5. Look at the output.** Read the PNG back before delivering. A DOM probe telling you
an element exists is not the same as it being legible — an element can be present,
correctly positioned and still far too small to read. Both checks are useful; neither
replaces the other.

## The viewport trap

The screenshot is always exactly as tall as `--window-size`. But headless Chromium's
**layout viewport is about 87px shorter than the window it is given** — ask for
1080×1080 and elements lay out in 1080×993.

So `position:absolute; bottom:58px` on a 1080px-tall body puts the element at y≈1022,
outside the painted area, and it silently clips. Compensating by enlarging the window
does not help: the PNG then comes out 1080×1167, which is the wrong asset.

**The fix is layout, not arithmetic.** The template sets `height:100vh` and uses a flex
column — a `.stage` that grows and centres the content, then the brand as the last
child. Everything stays inside the painted area at any window size, and the unused strip
at the foot simply carries the background colour, which reads as deliberate whitespace.

Never anchor to the viewport bottom in a card. Let flow layout place things.

## Fonts

Chromium's own fetch of `fonts.googleapis.com` frequently fails behind an agent proxy
even when `curl` and `urllib` succeed on the same URL. So do **not** link a stylesheet
and hope. The script downloads the TTFs and installs them into `~/.fonts`, then runs
`fc-cache`, which works offline and bakes the real typeface into the PNG.

List families in the spec:

```json
"google_fonts": ["Fraunces:wght@700", "Inter:wght@400;600;700"]
```

If the download fails the script says so and falls back to system fonts. Check the
output — a card that silently rendered in DejaVu Serif is a card you have to redo.

Baseline system fonts, when there is no network: DejaVu Sans/Serif, Liberation
Sans/Serif/Mono, FreeSans/Serif, Bitstream Charter.

## Sizes

| Key | Pixels | Use |
|---|---|---|
| `square` | 1080×1080 | **Default.** Safe in every feed, never awkwardly cropped |
| `portrait` | 1080×1350 | Most mobile feed real estate; best for Instagram and FB |
| `landscape` | 1200×630 | Link previews, OG images, blog headers |
| `story` | 1080×1920 | Stories and Reels covers |

Type scales automatically off canvas height, so one spec renders at any size.

## Spec format

```json
{
  "size": "square",
  "brand": "BulgariaReady",
  "google_fonts": ["Fraunces:wght@700", "Inter:wght@400;600;700"],
  "theme": {
    "bg": "#F7F4ED", "fg": "#1A2420",
    "accent": "#1B5E43", "muted": "#5E6B63",
    "display_font": "'Fraunces',Georgia,serif",
    "body_font": "'Inter',sans-serif"
  },
  "cards": [
    {
      "name": "01-the-nod",
      "bg": "#C0562E", "fg": "#FFFFFF",
      "accent": "rgba(255,255,255,.72)", "muted": "rgba(255,255,255,.88)",
      "h1": 150,
      "extra_css": ".sub{max-width:820px}",
      "content": "<div class=\"kicker\">Before you arrive</div><h1>A nod<br>means<br>no.</h1><p class=\"sub\">Yes and no are the wrong way round.</p>"
    }
  ]
}
```

Per-card keys override `theme`. Available classes: `.kicker`, `h1`, `.sub`, `.brand`
(auto-added). Add anything else through `extra_css` and write the markup in `content`.

Sizes in the spec are given **as if on a 1080-tall canvas** and scaled from there.

## Writing the hooks

Pull hooks from the specific, surprising or contrarian bits of the underlying content,
not from its summary:

- **A reversal** — "A nod means no"
- **A concrete number** — "€1,732 in Sofia. €1,475 nationally."
- **A trap** — "You can buy the house. Not the land."
- **A correction** — "Everyone views in August. Go back in February."
- **A short list rendered as the image** — six letters, four signs. The data *is* the
  design.

Avoid: brand names in the headline, exclamation marks, stock-photo captions, and
anything that reads as an ad rather than a fact.

**Never put a claim on a card you have not verified.** An image gets screenshotted and
shared with no context and no way to add a correction. Numbers especially: source them
first, and if a figure cannot be confirmed, build the card around one that can.

## Layout patterns that work

- **Statement** — kicker, huge headline, one supporting line. The default.
- **Data pair** — two or three big numbers in tinted panels. Good for comparisons.
- **List-as-design** — 4–6 items in a grid or rows; content and layout are the same
  thing.
- **Two-tone contrast** — first clause dimmed, second in accent colour. Good for
  before/after and corrections.
- **Oversized glyph** — a giant quote mark or character as texture behind the headline.

Keep 70–80px of padding on a 1080 canvas. Crowded cards look amateur and get cropped.

## Delivering

Send the PNGs with `SendUserFile`. Name them in posting order (`01-`, `02-`) so they
pair with the written posts. Say which card belongs to which post — the mapping is not
obvious from filenames alone once there are eight.

Keep the JSON spec in the repo. Copy changes constantly, and regenerating from a spec
beats rebuilding a card by hand.
