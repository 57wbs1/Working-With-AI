# Working With AI

A thirteen-lesson, self-paced course on using AI tools properly, from The Disruptive Company.

**Live:** https://57wbs1.github.io/Working-With-AI/

**Unclassified.** Written on a personal account in personal time, using no official material.

## Files

- `index.html`: sales landing page with the three-day outline, the $50 PayNow QR and the access-code entry
- `course.html`: the course itself, one page per section (29 pages)
- `assets/audio/`: the narration for chapters 2 to 8, one mp3 each
- `assets/video/`: abstract stingers and hero loops; `face/` holds the lip-synced presenter tracks; `explainer/` holds the edited chapter videos with WebVTT captions
- `assets/img/academy/`: course and lesson photography (generated)
- `academy.html`: course catalogue for The Disruptive Company
- `assets/img/`: poster frames and the PayNow QR
- `scripts/`: narration scripts, on-screen captions, the embed script and the PayNow QR builder

## Running locally

Audio and video need a server, because relative paths do not load from `file://`:

```bash
python3 -m http.server 8793
```

## Using it

- **Light** button: light theme for phones in daylight.
- `←` `→` move between pages, `Alt`+`C` opens contents, `Esc` closes overlays.
- Each lesson has its own accent colour, so the dots and contents list show progress at a glance.
- Progress and theme persist per browser.

## Structure

Three days, 30 sections: 13 lessons, 15 labs, a troubleshooting playbook and a capstone.
Roughly 20 hours, ending with a deployed URL.

| Day | Covers | Labs |
|---|---|---|
| 1: Foundations | Agentic AI, the toolkit, costs | Delegate by intent · Choose your stack · Sanitisation drill |
| 2: Working | Skills, MCP, research, decks, files | Build a skill · Connectors · First agentic task · Citation audit · Research end-to-end · Your format · Point it at a folder |
| 3: Building | Failure modes, vibe coding, design thinking | Circling drill · Spec · Build v1 · Break and harden · Ship it · **Capstone** |

Every lesson carries a four-question MCQ (48 total, options shuffled, skippable).
Every lab carries a persistent checklist (112 checks) feeding a per-day progress bar.
Ticks and quiz scores save to the browser only and are never transmitted.

## Narration

Chapters 2 to 8 each open with a narrated briefing of about two minutes, voiced by an AI voice at 172 words per minute.

- `scripts/vo/ch0*_*.txt`: the narration script, one paragraph per line. The same lines are the on-page transcript.
- `scripts/scenes.py`: the on-screen captions, each timed as a fraction of the audio length.
- `scripts/embed_vox.py`: copies both into the `VOXSCENES` and `VOXLINES` lines of `course.html`. Run `python3 scripts/embed_vox.py` after editing either source, and leave those two lines alone by hand.
- `assets/audio/`: the rendered mp3 for each chapter.

Changing a narration line means re-rendering that chapter's mp3 and then re-timing its scenes against the new audio. Whisper word timestamps give the start of each passage.

## Access gate

The gate works on the honour system and gives no real protection. This is a static site in a public repo, so:

- `course.html` sends visitors back to `index.html` unless the `wwai-access` flag is set in the browser. It lets everyone in when storage is blocked, and anyone can set the flag by hand.
- The whole course is readable in this repo without paying.
- Access codes are stored as SHA-256 hashes, which hides them from casual readers of the source only.

If the paywall needs to hold, the repo has to go private and the site needs a host with real
server-side auth. As it stands the gate stops casual forwarding and little else.

Codes live as hashes in `index.html`. To change them, replace the hashes; the hashing recipe is in that page's script.

## PayNow QR

`assets/img/paynow-50.png` encodes an EMVCo/SGQR payload: SGD 50.00 to +6591817066, reference `AIBRIEF`,
fixed amount. The CRC is self-checked at build time.

**Test it with a real scan before sharing.** The payload is constructed to spec and the checksum
validates, but it has not been put through an actual bank app.

To regenerate, see `scripts/paynow.py`.

## Maintenance

Everything factual carries a date stamp on the page and dates fast:

- Prices and plans change every few weeks; re-check Lesson 04 before each cohort.
- Video links were verified via the YouTube oEmbed API.
- The Perplexity student discount was confirmed against Perplexity's own help centre.
- Model tiers in Lesson 11 will age fastest of all.

Re-check Lessons 04 and 11 before presenting this more than a few weeks out.
