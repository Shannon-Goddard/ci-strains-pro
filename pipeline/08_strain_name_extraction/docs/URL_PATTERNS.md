# URL Patterns for Strain Name Extraction

**Purpose**: Document URL structure for each seed bank  
**Reviewer**: Shannon Goddard  
**Date**: January 27, 2026

---

## Instructions

For each seed bank:
`pipeline\08_strain_name_extraction\input\09_autoflower_classified.csv`
1. Pick 3-5 sample URLs from the CSV
2. Identify the URL pattern
3. Document what to extract and what to remove
4. Note any edge cases

---

## Attitude Seed Bank (7,673 strains)

**Sample URLs**:
```
https://www.cannabis-seeds-bank.co.uk/auto-seeds-auto-1/prod_1705
https://www.cannabis-seeds-bank.co.uk/00-seeds-00-hashchis-aka-00-cheese/prod_3495
https://www.cannabis-seeds-bank.co.uk/afghan-selection-seeds-chimtal/prod_6210
https://www.cannabis-seeds-bank.co.uk/barneys-farm-seeds-cbd-blue-shark/prod_2866
https://www.cannabis-seeds-bank.co.uk/grounded-genetics-zwisher/prod_9439
```

**URL Pattern**: `{breeder}-{seeds|genetics|seedbank|farm}-{strain-name}/prod_####`

**Extraction Logic**:
1. Get slug: second-to-last path segment
2. Split on: `-seeds-`, `-genetics-`, `-seedbank-`, `-seed-`, `-farm-`
3. Take everything AFTER the separator
4. Convert hyphens to spaces
5. Title case

**Expected Results**:
- `auto-seeds-auto-1` → "Auto 1"
- `00-seeds-00-hashchis-aka-00-cheese` → "00 Hashchis Aka 00 Cheese"
- `afghan-selection-seeds-chimtal` → "Chimtal"
- `barneys-farm-seeds-cbd-blue-shark` → "Cbd Blue Shark"
- `grounded-genetics-zwisher` → "Zwisher"

---

## North Atlantic (2,726 strains)

**Sample URLs**:
```
https://www.northatlanticseed.com/product/auto-1-auto/
https://www.northatlanticseed.com/product/zweet-auto/
https://www.northatlanticseed.com/product/zuzu-fruit/
https://www.northatlanticseed.com/product/the-brunch-s1-f-drop-10-13-12pm-est/
```

**URL Pattern**: `/product/{strain-name}-{auto|fem}/`

**Extraction Logic**:
1. Get slug: second-to-last path segment
2. Remove suffix: `-auto`, `-fem`, `-feminized`, `-f`, `-regular` (ONLY at end)
3. Convert hyphens to spaces
4. Title case
5. Preserve "Auto" at start if followed by other words
6. Reomove all characters after `-drop` example: `-drop-10-13-12pm-est`

**Expected Results**:
- `auto-1-auto` → "Auto 1"
- `zweet-auto` → "Zweet"
- `zuzu-fruit` → "Zuzu Fruit"

---

## Amsterdam (163 strains)

**Sample URLs**:
```
https://amsterdammarijuanaseeds.com/green-crack-autoflower-seeds/
https://amsterdammarijuanaseeds.com/gipsy-king-feminized-seeds/
https://amsterdammarijuanaseeds.com/afghan/
https://amsterdammarijuanaseeds.com/forest-fruits-auto-feminized-marijuana-seeds/
```

**URL Pattern**: `/{strain-name}-{autoflower|feminized}-seeds/` or `/{strain-name}/`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove keywords: `autoflower`, `feminized`, `seeds`, `marijuana`, `seed`
3. Convert hyphens to spaces
4. Title case

**Expected Results**:
- `green-crack-autoflower-seeds` → "Green Crack"
- `gipsy-king-feminized-seeds` → "Gipsy King"
- `afghan` → "Afghan"

---

## Crop King (3,336 strains)

**Sample URLs**:
```
https://www.cropkingseeds.com/feminized-seeds/cookie-wreck-strain-feminized-marijuana-seeds/  
https://www.cropkingseeds.com/feminized-seeds/purple-punch-feminized-fast-version-marijuana-seeds/  
https://www.cropkingseeds.com/feminized-seeds/ny-diesel-marijuana-seeds-2/  
https://www.cropkingseeds.com/feminized-seeds/suncake-strain/
```

**URL Pattern**: `/{strain-name}-{strain|feminized|marijuana}-seeds/` or `/{strain-name}/`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove keywords: `strain`, `feminized`, `autoflowering`, `marijuana`, `seeds`, `fast-version`
3. Remove trailing numbers (e.g., `-2`)
4. Convert hyphens to spaces
5. Title case
6. Preserve numbers in strain names (e.g., "Project 4516")

**Expected Results**:
- `cookie-wreck-strain-feminized-marijuana-seeds` → "Cookie Wreck"
- `purple-punch-feminized-fast-version-marijuana-seeds` → "Purple Punch"
- `ny-diesel-marijuana-seeds-2` → "Ny Diesel"
- `suncake-strain` → "Suncake"

---

## Gorilla (2,000 strains)

**Sample URLs**:
```
https://www.gorilla-cannabis-seeds.co.uk/growerschoice/feminized/frosty-gelato.html  
https://www.gorilla-cannabis-seeds.co.uk/growerschoice/feminized/chocolate-sherbet.html  
https://www.gorilla-cannabis-seeds.co.uk/fastbuds/feminized/purple-lemonade-ff.html  
https://www.gorilla-cannabis-seeds.co.uk/sweetseeds/f1-fast-version/mental-rainbow-f1-fast-version.html  
https://www.gorilla-cannabis-seeds.co.uk/barneysfarm/autoflowering/wedding-cake-auto.html
```

**URL Pattern**: `/{strain-name}.html`

**Extraction Logic**:
1. Extract from `strain_name_raw` column (not URL)
2. Remove keywords: Feminized, Feminised, Autoflowering, Autoflower, Fast Flowering, Regular, Cannabis Seeds, Early Version, Automatic
3. Remove "Auto" from end UNLESS followed by "CBD" (preserves "Auto CBD")
4. Preserve aka names in format "(aka Name)" or "Aka Name"
5. Convert to title case

**Expected Results**:
- `Big Bud Auto` → "Big Bud"
- `Watermelon Punch Autoflowering` → "Watermelon Punch"
- `Sweet Nurse Auto CBD` → "Sweet Nurse Auto CBD"

---

## Neptune (1,995 strains)

**Sample URLs**:
```
https://neptuneseedbank.com/product/sour-og-mango-strain/  
https://neptuneseedbank.com/product/the-cali-connection-blackwater-f-2/
```

**URL Pattern**: `/{breeder-name}-{strain-name}-{generation}/` or `/{strain-name}-strain/`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove `-strain` suffix
3. Remove generation markers: `-f`, `-f-2`, `-f2`, `-s1`, `-bx1`
4. Remove pack sizes: `-2pack`, `-2-pack`
5. Find 140 common breeder prefixes (appearing 5+ times)
6. Remove breeder prefixes from start of name
7. Remove keywords: Strain Seeds, Seeds, Genetics, Pre Sale, Freebie
8. Remove "Auto" unless at start
9. Convert to title case

**Expected Results**:
- `sour-og-mango-strain` → "Sour Og Mango"
- `the-cali-connection-blackwater-f-2` → "Blackwater"
- `in-house-genetics-zurkle-f-1-2pack` → "Zurkle"

---

## Seedsman JS (866 strains)

**Sample URLs**:
```
https://www.seedsman.com/us-en/sour-banana-sherbet-regular-seeds-12-dna-cff-006  
https://www.seedsman.com/us-en/sour-apple-auto-feminised-seeds-humb-saa-f  
https://www.seedsman.com/us-en/sour-cherry-diesel-feminised-seeds-atl-scd-fem
```

**URL Pattern**: `/{strain-name}-{regular|auto|feminised}-seeds-{codes}`

**Extraction Logic**:
1. Get slug: last path segment
2. Split on keywords: `regular-seeds`, `auto-feminised`, `feminised-seeds`, `autoflowering-seeds`, `regular`, `auto`, `feminised`, `feminized`
3. Take first part before keyword
4. Convert hyphens to spaces
5. Title case

**Expected Results**:
- `sour-banana-sherbet-regular-seeds-12-dna-cff-006` → "Sour Banana Sherbet"
- `sour-apple-auto-feminised-seeds-humb-saa-f` → "Sour Apple"
- `sour-cherry-diesel-feminised-seeds-atl-scd-fem` → "Sour Cherry Diesel"

---

## Herbies (753 strains)

**Sample URLs**:
```
https://herbiesheadshop.com/cannabis-seeds/purple-haze-fem-sensi-seeds  
https://herbiesheadshop.com/cannabis-seeds/purple-haze-auto-herbies-seeds-usa
```

**URL Pattern**: `/{strain-name}-{fem|auto}-{breeder-name}`

**Extraction Logic**:
1. Get slug: last path segment
2. Find 28 common breeder suffixes (appearing 5+ times)
3. Remove breeder suffixes from end
4. Remove Auto/Autoflower unless at start
5. Remove Fast Version
6. Remove abbreviations at end: Ghs, Gg, Fastbuds, Gc
7. Convert to title case

**Expected Results**:
- `purple-haze-fem-sensi-seeds` → "Purple Haze"
- `purple-haze-auto-herbies-seeds-usa` → "Purple Haze"
- `northern-lights-autoflower-growers-choice` → "Northern Lights"

---

## Sensi Seeds (115 strains)

**Sample URLs**:
```
https://sensiseeds.us/autoflowering-seeds/pineapple-kush-cake/
https://sensiseeds.us/feminized-seeds/strawberry-kush/
```

**URL Pattern**: `/{category}/{strain-name}/`

**Extraction Logic**:
1. Get slug: last path segment
2. Convert hyphens to spaces
3. Title case

**Expected Results**:
- `pineapple-kush-cake` → "Pineapple Kush Cake"
- `strawberry-kush` → "Strawberry Kush"

---

## Multiverse Beans (518 strains)

**Sample URLs**:
```
https://multiversebeans.com/product/barneys-farm-gelato-strain-fem-photo/  
https://multiversebeans.com/product/barneys-farm-glookies-fem-photo/  
https://multiversebeans.com/product/dimebag-seed-co-xendra-photo-reg-7-pack/  
https://multiversebeans.com/product/dry-erase-marker-atlas-seeds/
```

**URL Pattern**: `/{breeder-name}-{strain-name}-{type}-{pack}/`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove suffixes: `-strain`, `-fem`, `-photo`, `-reg`, `-pack`, `-auto`
3. Remove generation markers: `-r1`, `-r2`, `-r3`, `-s1`
4. Remove `-ff-` (but not ff in names)
5. Remove pack sizes: `-2pack`, `-3-pack`, etc.
6. Find 18 common breeder prefixes (appearing 5+ times)
7. Remove breeder prefixes from start
8. Find 13 common breeder suffixes
9. Remove breeder suffixes from end
10. Remove keywords: Autoflower Cannabis Seeds Female, Photoperiod Cannabis Seeds Female, Female, Seeds
11. Remove Auto unless at start
12. Convert to title case

**Expected Results**:
- `barneys-farm-gelato-strain-fem-photo` → "Gelato"
- `barneys-farm-glookies-fem-photo` → "Glookies"
- `dimebag-seed-co-xendra-photo-reg-7-pack` → "Dimebag Seed Co Xendra"

---

## Seed Supreme (353 strains)

**Sample URLs**:
```
https://seedsupreme.com/skunk-1-feminized.html
https://seedsupreme.com/skunk-autoflower.html
https://seedsupreme.com/sweet-16-feminized-cannabis-seeds.html  
https://seedsupreme.com/gelato-regular.html
```

**URL Pattern**: `/{strain-name}-{feminized|autoflower|regular}.html`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove .html extension
3. Split on keywords: `feminized-cannabis-seeds`, `autoflower-cannabis-seeds`, `regular-cannabis-seeds`, `feminized`, `autoflower`, `regular`
4. Take first part before keyword
5. Convert hyphens to spaces
6. Title case

**Expected Results**:
- `skunk-1-feminized` → "Skunk 1"
- `skunk-autoflower` → "Skunk"
- `sweet-16-feminized-cannabis-seeds` → "Sweet 16"
- `gelato-regular` → "Gelato"

---

## Mephisto Genetics (245 strains)

**Sample URLs**:
```
https://mephistogenetics.com/products/sundae-scout
https://mephistogenetics.com/products/illuminauto-61-white-creme
```

**URL Pattern**: `/products/{strain-name}`

**Extraction Logic**:
1. Get slug: last path segment
2. Convert hyphens to spaces
3. Title case

**Expected Results**:
- `sundae-scout` → "Sundae Scout"
- `illuminauto-61-white-creme` → "Illuminauto 61 White Creme"

---

## Exotic Genetix (216 strains, 11 filtered)

**Sample URLs**:
```
https://exoticgenetix.com/product-category/seeds/box-sets/falcon-9-boxes/  
https://exoticgenetix.com/product-category/seeds/grape-jubilee/
https://exoticgenetix.com/product/big-league-sherb-regs/
```

**URL Pattern**: `/{strain-name}/` (filter out `/box-sets/`)

**Extraction Logic**:
1. Filter out URLs containing `/box-sets/` (mixed strains)
2. Get slug: last path segment
3. Remove suffixes: Regs, Player Packs, Ltd Edition, Gen
4. Remove trailing numbers
5. Convert hyphens to spaces
6. Title case

**Expected Results**:
- `grape-jubilee` → "Grape Jubilee"
- `big-league-sherb-regs` → "Big League Sherb"
- `alpha-one-3231313` → "Alpha One"

---

## ILGM JS (133 strains)

**Sample URLs**:
```
https://ilgm.com/products/jack-herer-feminized-seeds  
https://ilgm.com/products/jack-herer-autoflower-seeds  
https://ilgm.com/products/andes-mintz-seeds
https://ilgm.com/products/granite-haze-f5-autoflower-seeds
```

**URL Pattern**: `/products/{strain-name}-{feminized|autoflower}-seeds`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove suffixes: `-feminized-seeds`, `-autoflower-seeds`, `-seeds`
3. Remove generation markers: `-f5`, `-f2`, etc.
4. Convert hyphens to spaces
5. Title case

**Expected Results**:
- `jack-herer-feminized-seeds` → "Jack Herer"
- `jack-herer-autoflower-seeds` → "Jack Herer"
- `andes-mintz-seeds` → "Andes Mintz"
- `granite-haze-f5-autoflower-seeds` → "Granite Haze"

---

## Dutch Passion (54 strains)

**Sample URLs**:
```
https://dutch-passion.us/cannabis-seeds/kerosene-krash  
https://dutch-passion.us/cannabis-seeds/auto-CBG-force
https://dutch-passion.us/cannabis-seeds/auto-ultimate
```

**URL Pattern**: `/cannabis-seeds/{strain-name}`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove `auto-` prefix
3. Convert hyphens to spaces
4. Title case

**Expected Results**:
- `kerosene-krash` → "Kerosene Krash"
- `auto-CBG-force` → "CBG Force"
- `auto-ultimate` → "Ultimate"

---

## Barney's Farm (88 strains)

**Sample URLs**:
```
https://www.barneysfarm.com/us/cherry-poppers-weed-strain-712  
https://www.barneysfarm.com/us/dos-si-dos-auto-autoflower-strain-513
https://www.barneysfarm.com/us/critical-kush-weed-strain-23
```

**URL Pattern**: `/{strain-name}-{weed-strain|auto-autoflower|autoflower-strain}-{number}`

**Extraction Logic**:
1. Get slug: last path segment
2. Split on keywords: `weed-strain`, `auto-autoflower`, `autoflower-strain`, `strain`
3. Take first part before keyword
4. Remove trailing numbers
5. Convert hyphens to spaces
6. Title case

**Expected Results**:
- `cherry-poppers-weed-strain-712` → "Cherry Poppers"
- `dos-si-dos-auto-autoflower-strain-513` → "Dos Si Dos"
- `critical-kush-weed-strain-23` → "Critical Kush"

---

## Royal Queen Seeds (67 strains)

**Sample URLs**:
```
https://www.royalqueenseeds.com/us/autoflowering-cannabis-seeds/145-royal-creamatic.html  
https://www.royalqueenseeds.com/us/autoflowering-cannabis-seeds/178-white-widow-automatic.html
https://www.royalqueenseeds.com/us/feminized-cannabis-seeds/122-white-widow.html
```

**URL Pattern**: `/{category}/{###-strain-name}.html`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove .html extension
3. Remove 3-digit number prefix (e.g., `145-`)
4. Remove `-automatic` suffix
5. Convert hyphens to spaces
6. Title case

**Expected Results**:
- `145-royal-creamatic` → "Royal Creamatic"
- `178-white-widow-automatic` → "White Widow"
- `122-white-widow` → "White Widow"

---

## Seeds Here Now (43 strains)

**Sample URLs**:
```
https://seedsherenow.com/shop/dos-si-dos-33-feminized-barneys-farm/  
https://seedsherenow.com/shop/elev8-seeds-apple-fritter-fem-6pk/
https://seedsherenow.com/shop/purple-punch-autoflower-barneys-farm/
```

**URL Pattern**: `/{breeder-name}-{strain-name}-{type}-{breeder-name}/`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove breeder suffixes: barneys-farm, exotic-genetix, omuerta-genetix, fast-buds, cali-connection, cali-kush-farms, swamp-boys-seeds, top-dawg-seeds, skunk-house-genetics, strait-a-genetics
3. Remove breeder prefixes: dominion-seed-company-, elite-clone-seed-company-, thug-pug-genetics-, humboldt-seed-company-, fast-buds-, elev8-seeds-, aficionado-seeds-
4. Remove pack sizes: `-10pk`, `-6pk`, `-reg-10pk`, `-fem-6pk`
5. Remove keywords: `-feminized`, `-autoflower`, `-autofem`, `-regular`, `-fem`, `-reg`, `-auto`
6. Remove generation markers: `-f2`, `-f1`
7. Convert to title case

**Expected Results**:
- `dos-si-dos-33-feminized-barneys-farm` → "Dos Si Dos 33"
- `elev8-seeds-apple-fritter-fem-6pk` → "Apple Fritter"
- `purple-punch-autoflower-barneys-farm` → "Purple Punch"

---

## Great Lakes (16 strains)

**Sample URLs**:
```
https://www.greatlakesgenetics.com/product/northern-leaf-seeds-hoochie-seeds-f1-12-reg-seeds/
https://www.greatlakesgenetics.com/product/night-owl-seeds-space-station-gold-3-auto-fem-seeds/
https://www.greatlakesgenetics.com/product/bodhi-seeds-eureka-lemon-g-x-lavender-lemonaid-11-reg-seeds/
```

**URL Pattern**: `/{breeder-name}-{strain-name}-{count}-{type}-seeds/`

**Extraction Logic**:
1. Get slug: last path segment
2. Remove seed count and type at end: `-12-reg-seeds`, `-3-auto-fem-seeds`
3. Remove breeder prefixes: green-wolfe-seed-co-, night-owl-seeds-, satori-seeds-, off-grid-seeds-, northern-leaf-seeds-, matchmaker-genetics-, sunny-valley-seed-co-, subcool-seeds-, forests-fires-, jaws-genetics-, strayfox-gardenz-, tonygreens-tortured-beans-, bodhi-seeds-, backyard-boogie-, anthos-seeds-, twenty20-
4. Remove generation markers: `-f1`, `-f2`, `-bc1-f2`, `-bc1`
5. Remove `-seeds` suffix
6. Remove `-fast-auto`
7. Convert to title case

**Expected Results**:
- `northern-leaf-seeds-hoochie-seeds-f1-12-reg-seeds` → "Hoochie"
- `night-owl-seeds-space-station-gold-3-auto-fem-seeds` → "Space Station Gold"
- `bodhi-seeds-eureka-lemon-g-x-lavender-lemonaid-11-reg-seeds` → "Eureka Lemon G X Lavender Lemonaid"

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
