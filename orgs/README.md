# Org Avatar Patterns

Design rules for the organization and profile avatars in this folder. Follow them when
adding a new org so the set keeps reading as one family.

## Canvas

| Property    | Value                                                  |
| ----------- | ------------------------------------------------------ |
| Dimensions  | 1254 × 1254 px, square                                  |
| Format      | JPEG, 72 dpi                                            |
| Bleed       | Full bleed — no baked-in border, frame or rounded corner |
| Safe area   | Keep all meaningful content inside the centre 84%       |
| Filename    | The GitHub org or user login, lowercase (`r523.jpg`)    |

GitHub rounds org avatars itself, so a frame drawn into the image double-rounds. The safe
area matters because a user avatar is cropped to a circle — anything in the corners is lost.

## Color tokens

Five values carry the whole set. Nothing else should appear as a large area.

| Token         | Hex       | Use                                                  |
| ------------- | --------- | ---------------------------------------------------- |
| `bg`          | `#A1E477` | Background. Flat fill, no gradient, no vignette.      |
| `fur-dark`    | `#4A4364` | Panda body, ear patches, eye patches. Indigo-charcoal, never pure black. |
| `fur-light`   | `#FEFEFE` | Panda face, chest, muzzle.                            |
| `outline`     | `#201E33` | Every contour. Uniform weight, no tapering.           |
| `accent`      | `#3BA22C` | Prop green — books, mugs, safes, boards.              |

Hardware (laptops, switches, racks) uses neutral greys between `#3F3F4C` and `#8A8A96`.
Institutional colors may override `accent` when the org has its own — `9231058.jpg` uses
AUT/CEIT orange for exactly that reason.

## Mascot

A chibi panda, always. It is the same character across every avatar — treat it as a model
sheet, not a fresh subject each time.

- Head-to-body ratio ~1:1.5. Big head, short limbs, no neck.
- Eye patches are large rounded teardrops tilted outward, with one white specular dot each.
- Muzzle is small and low; open smile with a pink tongue.
- Seated or standing three-quarter view, facing the viewer. Never in profile.
- Flat vector: uniform heavy contour, no gradients, no cast shadows, no texture, no
  rendered lighting.
- Grounded on an implied floor with no horizon line — the subject sits on flat color.

## Composition tiers

Pick a tier by how much the org needs to say, not by how much can fit. Everything here is
consumed at 32–64 px in org lists and comment threads; only the profile page shows it large.

**Tier 1 — portrait.** Panda plus one or two props, filling ~70% of the frame.
Reads perfectly at 40 px. Default to this.
`1995parham-learning.jpg`, `code-chorus-io.jpg`, `parham-alvani.jpg`

**Tier 2 — subject with props.** Panda plus a small cluster of domain objects.
Still legible at 40 px if the props stay chunky.
`citado.jpg`, `1995parham-goodies.jpg`, `9231058.jpg`

**Tier 3 — full scene.** Desk environments with background walls and many small objects.
These collapse to grey mush at 40 px and lose the green field that ties the set together.
Avoid for new orgs.
`reinnet.jpg`, `r523.jpg`, `1995parham-me.jpg`

## Identity by prop

An org is identified by what the panda is holding or working on, never by a wordmark. The
prop should be recognizable in silhouette.

| Org               | Domain              | Props                                    |
| ----------------- | ------------------- | ---------------------------------------- |
| `reinnet`         | Networking          | Switch, router, topology board, Wireshark |
| `r523`            | Embedded / IoT      | Breadboard, dev board, sensors, probe    |
| `citado`          | LoRaWAN             | Gateway, antenna, coverage diagram       |
| `1995parham-me`   | Infrastructure      | Rack, laptop, switch, router             |
| `parham-alvani`   | Secrets / security  | Safe, keys, wallet                       |
| `1995parham-learning` | Study           | Books                                    |
| `1995parham-goodies`  | Collection      | Photo album, camera                      |
| `9231058`         | University          | Cap, diploma, AUT/CEIT banner            |
| `code-chorus-io`  | Anonymity           | Masquerade mask                          |

## Text

Avoid it. Rendered text at 40 px is noise, and generated lettering degrades into
near-words — the current set carries `IPAŘHAM` on a t-shirt in `1995parham-me.jpg` and a
mangled `AUT CEIT 9V` banner in `9231058.jpg`.

If a mark genuinely needs a word, use one short word in a heavy geometric sans, set large
enough to survive a 40 px downscale, and check the render before committing.

## Legacy marks

`i1820.jpg`, `aolab.jpg` and `ceit-ssc.jpg` are pre-existing institutional logos on white.
They are intentionally outside the system — that branding is not ours to restyle. Do not
convert them to the panda pattern, and do not treat their white backgrounds as precedent
for new work.

Note that `ceit-ssc.jpg` is thin black line art on white: it nearly disappears at avatar
size and on GitHub's dark theme. That is a limitation of the source mark, not a bug to fix
here.

## Before committing a new avatar

1. Downscale to 40 px and confirm the subject still reads.
2. Sample the background — it must be `#A1E477`, not a near miss. The existing files were
   normalized to this value; a new avatar that lands a few units off is visible as soon as
   it sits next to them.
3. Check the corners are clean and the content clears a circular crop.
4. Read any text at 100%. If it is not a real word, remove it.

## Generation prompt template

The panda avatars are generated. This prompt reproduces the house style:

> Flat vector cartoon illustration, kawaii chibi panda mascot, large head with rounded
> teardrop eye patches and a white highlight dot in each eye, small muzzle, open smile with
> pink tongue, seated three-quarter view facing the viewer. Uniform heavy dark outline, no
> gradients, no shadows, no texture. Solid flat light-green background `#A1E477`. The panda
> is `<ACTION WITH PROPS>`. Centered composition, square, generous margin, no text.

Replace `<ACTION WITH PROPS>` with the domain objects from the table above. Keep "no text"
in the prompt — it is the single most reliable way to avoid the garbled-lettering problem.
