# Working With AI — syndicate brief

Single-file interactive brief for 57 CSC Syn 1 on how to actually use AI tools.
Open `index.html` in any browser, or serve the folder.

**Unclassified.** Built on a personal account, on personal time. Contains no official material.

## Running it

Just open `index.html` — everything is relative and works from the file system
except the videos, which need a server:

```
python3 -m http.server 8793
```

## Presenting

- **Notes button** (or press `N`) reveals the speaking notes — the "SAY THIS" boxes.
  Leave them off when you share the link.
- **Light button** switches themes. Dark for the room, light for phones in daylight.
- Both settings persist in the browser.

## Structure

| § | Section | Interactive |
|---|---------|-------------|
| 01 | The edge was free and on YouTube | Filterable list, 16 videos + 4 channels |
| 02 | From answering to doing | Timeline; 4-rung autonomy ladder |
| 03 | What it costs, and what Perplexity is | Price table; "what should I pay" picker |
| 04 | The plumbing nobody explains | MCP before/after diagram; local-vs-cloud picker |
| 05 | Now you build one | Prompt builder with 5 worked examples |

## Assets

`assets/video/` — four clips generated with Higgsfield (Google Veo 3.1 Lite), ~30 credits total.
`assets/img/` — poster frames pulled from the videos with ffmpeg.

The intro clip has audio; the three stingers are silent and loop on scroll.

## Maintenance

Everything factual is date-stamped **7 Oct 2026** and will rot fast:

- Prices moved four times in the quarter before this was written.
- Video links were verified via the YouTube oEmbed API on 7 Oct 2026.
- The Perplexity student discount was confirmed against Perplexity's own help centre.

Re-check section 03 before presenting this more than a few weeks out.
