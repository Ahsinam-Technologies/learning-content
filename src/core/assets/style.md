The implemented BayesStack UI is primarily a teal-and-mint system with dark green-black text, white surfaces, and very light green backgrounds. The strongest reference is [packages/ui/src/styles.css](/home/sagar/Desktop/bayesstack/bayesstack/packages/ui/src/styles.css) plus the implemented auth app.

## Core color palette

| Use | Hex |
|---|---|
| Primary interactive teal | `#0B6763` |
| Primary brand teal | `#056766` |
| Deep teal / hover | `#084C49` |
| Dark background | `#091A18` |
| Soft teal background | `#E4F2EF` |
| Very light canvas background | `#F1F8F6` |
| White surface | `#FFFFFF` |
| Primary text | `#123333` |
| Secondary text | `#4A6360` |
| Muted text | `#59716E` |
| Light text / disabled text | `#94A3B8` |
| Borders and dividers | `#D7E8E4` |
| Neutral light background | `#F0F4F4` / `#F0F7F6` |
| Standard dark UI text | `#0F172A` |
| Slate secondary text | `#64748B` |
| Focus/error-border neutral | `#E2E8F0` |

For most PDFs, slides, and website material, use:

- Primary teal: `#0B6763`
- Deep teal: `#084C49`
- Pale teal: `#E4F2EF`
- Canvas: `#F1F8F6`
- Text: `#123333`
- Secondary text: `#4A6360`
- Border: `#D7E8E4`
- White: `#FFFFFF`

There are two official-looking teal values in the repository. The brand token file defines `#056766` as the primary brand color, but the actual shared UI components, auth app, admin app, landing page, and coding studio use `#0B6763` most often. Therefore, use `#0B6763` as the default working teal, and reserve `#056766` for formal brand or print contexts if needed. See [colors.ts](/home/sagar/Desktop/bayesstack/bayesstack/packages/assets/src/tokens/colors.ts) and [brand-palette.json](/home/sagar/Desktop/bayesstack/bayesstack/packages/assets/brand-palette.json).

## Typography

The visual system uses:

- Display/headings: `Outfit`
- Body/UI text: `Inter`
- Code and technical content: `JetBrains Mono`

Recommended weights:

- Outfit 800: major titles and hero headings
- Outfit 700: section headings, labels, brand name
- Outfit 600: subheadings and emphasis
- Inter 400: paragraphs and descriptions
- Inter 500–600: buttons, navigation, metadata
- Inter 700: strong emphasis
- JetBrains Mono 400–500: code, commands, technical identifiers

The apps load these fonts from Google Fonts and define them in [auth/globals.css](/home/sagar/Desktop/bayesstack/bayesstack/apps/auth/app/globals.css) and [admin/globals.css](/home/sagar/Desktop/bayesstack/bayesstack/apps/admin/app/globals.css).

## Recommended PDF/slide hierarchy

- Cover title: Outfit ExtraBold, `#123333`
- Cover accent or rule: `#0B6763`
- Section titles: Outfit Bold, `#123333`
- Body copy: Inter Regular, `#4A6360`
- Key numbers or callouts: Outfit Bold, `#0B6763`
- Captions: Inter Regular, `#59716E`
- Dark panels: background `#091A18`, text `#FFFFFF`, muted text `#94A3B8`
- Cards: `#FFFFFF` with `1px #D7E8E4` border
- Highlight boxes: `#E4F2EF` background with `#0B6763` text

## Visual style

Use a clean, modern, enterprise-education aesthetic:

- White cards on pale mint canvases
- Teal for actions, links, icons, rules, and important metrics
- Dark green-black for high-contrast panels
- Fine pale-teal borders
- Rounded corners, generally 6–12px
- Light, restrained shadows
- Generous spacing and strong typographic hierarchy
- Avoid excessive gradients, saturated colors, or decorative illustrations

For print, the official primary teal token is approximately:

- RGB: `5, 103, 102`
- CMYK: `95, 0, 1, 60`

Use white space heavily, with teal appearing as a deliberate accent rather than covering every surface.