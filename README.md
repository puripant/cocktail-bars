# Cocktail Bars

Each cocktail recipe is drawn as one horizontal stacked bar chart, where segment width is the ingredient's share of the drink. Color encodes eight ingredient types (spirit, liqueur/amaro, soda/mixer, lemon & lime, syrup, juice, cream/egg/coffee, wine/vermouth). Dashes, garnishes, and muddled solids have no volume, so they are listed after the bar chart.

There are two cocktail lists from IBA website (102 cocktails) and Information Is Beautiful (IIB) data (77 cocktails). 63 cocktails are in both lists, which can be shown side by side.

The cocktails can be sorted by their names, volumes, share of ingredient type, or (in comparison view) how much the two recipes differ.

The bars can be adjusted to scale to 100% or show the real volume. Click an ingredient type to keep only the cocktails that contain it. Or search to match names and ingredients.

It is a single self-contained file. The only external request is for the Barlow typeface from Google Fonts.

## Data Sources & Processing

| File | What it is |
|---|---|
| `data/iba-site.json` | Recipes scraped from [iba-world.com](https://iba-world.com/cocktails/all-cocktails/) in October 2026 |
| `data/iba-to-js.py` | Converts that JSON into the `IBA` array in `index.html` (ml to cl, ingredient types, estimates) |
| `data/iib-sheet.csv` | Export of the [IBA cocktail sheet](https://docs.google.com/spreadsheets/d/1TIYjGZBCVy8qC0SSa4wv3ztgRc-MDUANuLegEBBuK0U/edit?gid=0) by Information is Beautiful |

The `IIB` array in `index.html` was transcribed from the sheet by hand and has no generator. `iba-to-js.py` still expects its input as `iba.json` and writes `iba.js` in the current directory.

Conventions:
- All quantities are in centilitres. Unitless numbers in the sheet are read as cl.
- Amounts given as "top with", "splash", spoons or eggs are estimates (a splash is 3 cl, an egg white 3 cl, a bar spoon 0.5 cl). These segments are hatched and marked with `~`.
- The sheet is transcribed as listed, including its gaps (for example, Grasshopper has no cream there).
- In compare view, the difference between two recipes is the share of the drink that moves between ingredient types.

## Prompts

Built with Claude Code (Opus 5.5 at medium effort). These are the prompts:

> I want to create a cocktail recipe visualization. Each cocktail recipe should be compact; possibly just one horizontal stacked bar chart to show the proportion of ingredients. Data can be scraped from https://iba-world.com/cocktails/all-cocktails/ or this Google Sheets by IIB https://docs.google.com/spreadsheets/d/1TIYjGZBCVy8qC0SSa4wv3ztgRc-MDUANuLegEBBuK0U/edit?gid=0#gid=0

> Name this as Cocktail Bars instead, playing on the word "bar"

> Add the rest of the cocktails from the IBA site

> I think the lists should be separate. There may be a dropdown on top to choose either IBA or IIB list. You can analyze and tell me if the recipe of the same cocktail is the same or similar or not.

> Create a compare mode to show the same cocktails side by side.
