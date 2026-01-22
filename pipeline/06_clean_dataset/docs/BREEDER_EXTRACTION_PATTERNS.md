# Breeder Name Extraction Patterns

**Purpose**: Document HTML extraction patterns for breeder names from each seed bank  
**Reviewer**: Shannon Goddard  
**Date**: January 20, 2026

---

## Instructions

For each seed bank:
1. Pick 3-5 sample URLs from the dataset
2. View the HTML source (or use browser inspector)
3. Find where the breeder name appears
4. Document the CSS selector, class name, or text pattern
5. Note any variations or edge cases

---

## Seed Bank Extraction Patterns

### Attitude Seed Bank (7,673 strains)

**Sample URLs**:
```
https://www.cannabis-seeds-bank.co.uk/00-seeds-auto-blueberry/prod_5459
```

**Breeder location in HTML**:
```
<a href="/00-seeds/cat_195">00 Seeds</a>
```

**Example HTML snippet**:
```html
<div class="breadCrumb">
    <a href="/00-seeds/cat_195">00 Seeds</a>
    <span> &gt; </span>
    <h1>00 Seeds AUTO Blueberry</h1>
</div>
```

**Note**:
```
text inside <a href="/00-seeds/cat_195">00 Seeds</a> = "00 Seeds"
```

---

### Crop King (3,336 strains)

**Sample URLs**:
```
https://www.cropkingseeds.com/
```
**Note**:
```
Crop King Seeds is the bank and the breeder
```

---

### North Atlantic (2,727 strains)

**Sample URLs**:
```
https://www.northatlanticseed.com/product/sugar-spice-f/
```

**Breeder location in HTML**:
```
<a href="https://www.northatlanticseed.com/product-category/seeds/twenty20-mendocino/">Twenty20 Mendocino</a>
```
**Example HTML snippet**:
```html
<span class="breeder-link">by <a href="https://www.northatlanticseed.com/product-category/seeds/twenty20-mendocino/">Twenty20 Mendocino</a></span>
```
**Note**:
```
text inside <a href="https://www.northatlanticseed.com/product-category/seeds/twenty20-mendocino/">Twenty20 Mendocino</a> = "Twenty20 Mendocino"
```

---

### Gorilla Seed Bank (2,000 strains)

**Sample URLs**:
```
https://www.gorilla-cannabis-seeds.co.uk/00-seeds/feminized/00-cheese.html
```

**Breeder location in HTML**:
```
<a href="/00-seeds" title="00 Seeds" class="white">00 Seeds</a>
```
**Example HTML snippet**:
```html
<h3 class="product attribute product-manufacturer"><a href="/00-seeds" title="00 Seeds" class="white">00 Seeds</a></h3>
```
**Note**:
```
text inside <a href="/00-seeds" title="00 Seeds" class="white">00 Seeds</a> = "00 Seeds"
```

---

### Neptune (1,995 strains)

**Sample URLs**:
```
https://neptuneseedbank.com/product/h-b-k-genetics-pegasus/
```

**Breeder location in HTML**:
```
<a href="https://neptuneseedbank.com/brand/h-b-k-genetics/" class="breeder-link">H.B.K Genetics</a>
```
**Example HTML snippet**:
```html
<div class="product-breeder">
    <span class="breeder-label">Breeder:</span>
        <a href="https://neptuneseedbank.com/brand/h-b-k-genetics/" class="breeder-link">H.B.K Genetics</a>
</div>
```
**Note**:
```
text inside <a href="https://neptuneseedbank.com/brand/h-b-k-genetics/" class="breeder-link">H.B.K Genetics</a> = "H.B.K Genetics"
```

---

### Seedsman JS (866 strains)

**Sample URLs**:
```
https://www.seedsman.com/us-en/baja-blast-s1-feminised-seeds-mosca-babls1-fem
```

**Breeder location in HTML**:
```
<a href="https://www.seedsman.com/us-en/cannabis-seed-breeders/mosca-seeds" title="Mosca Seeds" target="_self">Mosca Seeds</a>
```
**Example HTML snippet**:
```html
<div class="Brand"><a href="https://www.seedsman.com/us-en/cannabis-seed-breeders/mosca-seeds" title="Mosca Seeds" target="_self">Mosca Seeds</a></div>
```
**Note**:
```
text inside <a href="https://www.seedsman.com/us-en/cannabis-seed-breeders/mosca-seeds" title="Mosca Seeds" target="_self">Mosca Seeds</a> = "Mosca Seeds"

**Source:** JS-rendered HTML from S3 `html_js/` folder

## Current S3 Status
- **HTML Type**: JavaScript shell only
- **Content**: CSS, React components, API endpoints
- **Product Data**: ❌ Not in HTML (loaded via GraphQL/REST API)
```

---

### Herbies (753 strains)

**Sample URLs**:
```
https://herbiesheadshop.com/cannabis-seeds/apple-fritter
```

**Breeder location in HTML**:
```
<a href="https://herbiesheadshop.com/producers/barneys-farm">Barney's Farm</a>
```
**Example HTML snippet**:
```html
<tr class="row item__property properties-list__item" title="Strain brand"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain brand </span> </td> <td class="col-6" style="padding: 0"><a href="https://herbiesheadshop.com/producers/barneys-farm">Barney's Farm</a></td> </tr>
```
**Note**:
```
text inside <a href="https://herbiesheadshop.com/producers/barneys-farm">Barney's Farm</a> = "Barney's Farm"
```

---

### Sensi Seeds (620 strains)

**Sample URLs**:
```
https://sensiseeds.us/autoflowering-seeds/banana-kush-cake/
```

**Note**:
```
Sensi Seeds is both the bank and the breeder

They do list these options: 
Sensi Seeds(31)
Breeding Grounds(26)
White Label(16)
Research(8)
White Label USA(3)

However, on the product page none are specified outside a wordy description, if mentioned at all. 
```

---

### Multiverse Beans (528 strains)

**Sample URLs**:
```
https://multiversebeans.com/product/fast-buds-tropicana-cookies-ff-strain-fem-photo/
```

**Breeder location in HTML**:
```
<a href="https://multiversebeans.com/brand/fast-buds/" rel="tag">Fast buds</a>
```
**Example HTML snippet**:
```html
<div class="product_meta"> <span class="sku_wrapper">SKU: <span class="sku">PARENT-FASTBUDS-040</span></span> <span class="posted_in">Categories: <a href="https://multiversebeans.com/product-category/photoperiod/" rel="tag">Photoperiod</a>, <a href="https://multiversebeans.com/product-category/breeders/fast-buds/" rel="tag">Fast buds</a></span> <span class="posted_in">Brand: <a href="https://multiversebeans.com/brand/fast-buds/" rel="tag">Fast buds</a></span></div>
```
**Note**:
```
text inside <a href="https://multiversebeans.com/brand/fast-buds/" rel="tag">Fast buds</a> = "Fast buds"
```

---

### Seed Supreme (353 strains)

**Sample URLs**:
```
https://seedsupreme.com/fruity-pebbles-feminized.html
```

**Breeder location in HTML**:
```
<td class="col data">Seed Supreme</td>
```
**Example HTML snippet**:
```html
<table class="data table additional-attributes" id="product-attribute-specs-table"><tbody> <tr> <td class="col label">SKU:</td><td class="col data">SSSB-FPF-FX</td> <td class="col label">Seedbank:</td><td class="col data">Seed Supreme</td> </tr> <tr> <td class="col label">Genetics:</td><td class="col data">Green Ribbon x Grandaddy Purps x Tahoe Alien</td> <td class="col label">Variety:</td><td class="col data">Mostly Indica</td> </tr> <tr> <td class="col label">Flowering Type:</td><td class="col data">Photoperiod</td> <td class="col label">THC Content:</td><td class="col data">Very High (over 20%)</td> </tr> <tr> <td class="col label">CBD Content:</td><td class="col data">Low (0-1%)</td> <td class="col label">Yield:</td><td class="col data">Average</td> </tr> <tr> <td class="col label">Effects:</td><td class="col data">Creative, Energetic, Relaxed</td> <td class="col label">Flavors:</td><td class="col data">Fruity, Pine, Sweet, Tropical</td> </tr> <tr> <td class="col label">Terpenes:</td><td class="col data">Limonene, Linalool, Terpineol</td> <td class="col label">Flowering Time:</td><td class="col data"> 8–10 weeks</td> </tr> <tr> <td class="col label">Plant Height:</td><td class="col data">Medium</td>  <td class="col label"></td><td class="col data"></td></tr></tbody></table>
```
**Note**:
```
text inside <td class="col data">Seed Supreme</td> = "Seed Supreme"
```

---

### Mephisto Genetics (245 strains)

**Sample URLs**:
```
https://mephistogenetics.com/
```

**Note:**:
```
Mephisto Genetics is both the bank and the breeder
```

---

### Exotic Genetix (227 strains)

**Sample URLs**:
```
https://exoticgenetix.com/
```

**Note:**:
```
Exotic Genetix is both the bank and the breeder
```

---

### ILGM JS (169 strains)

**Sample URLs**:
```
https://ilgm.com/products/pineapple-diesel-autoflower-seeds?variant=UHJvZHVjdFZhcmlhbnQ6MTM2OQ==
```

**Breeder location in HTML**:
```
<span class="group font-display text-display-xs font-black"><!--[-->Happy Valley Genetics<!--]--></span>
```
**Example HTML snippet**:
```html
<div class="mb-1 space-y-1"><span class="group font-display text-display-xs font-black"><!--[-->Happy Valley Genetics<!--]--></span><h1 class="group font-display text-display-lg font-black"><!--[-->Pineapple Diesel Autoflower Seeds<!--]--></h1><div id="yotpo-widget-instance-1176798-UHJvZHVjdDozMDQ=" class="yotpo-widget-instance min-h-[33px] pt-1" data-yotpo-instance-id="1176798" data-yotpo-product-id="304" data-yotpo-element-loaded="true" data-yotpo-widget-uuid="3b785fad-e0ad-48ee-80c0-37e6c6d0bb78">
<div class="yotpo-reviews-star-ratings-widget yotpo-star-ratings-widget-override-css yotpo-device-laptop yotpo-display-m" id="yotpo-reviews-star-ratings-widget" style="display: flex; justify-content: left; flex-direction: row; margin-bottom: 5px;">
		<div class="yotpo-widget-clear yotpo-bottom-line-scroll-panel" style="display: flex; align-items: flex-start; flex-flow: column wrap;">
        <div style="display: none;"></div>

        <button class="yotpo-sr-bottom-line-summary yotpo-sr-bottom-line-button" type="button" aria-label="4.8 out 5 stars rating in total 12 reviews. Jump to reviews." style="display: flex; flex-direction: row; align-items: flex-start; direction: ltr; cursor: pointer;" fdprocessedid="7kuhey">
    <span style="display: flex; cursor: pointer;">
        <span aria-hidden="true" style="display: flex; flex-direction: row; align-items: center; height: 28px; cursor: pointer;">
    <svg aria-hidden="true" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" class="star-container yotpo-sr-star-full" width="15" height="15" style="display: flex; flex-direction: row; margin-inline-end: 3.5px;">
	    <defs>
		    <linearGradient id="yotpo_stars_gradient_0.3881005196172358">
		        <stop offset="100%" stop-color="rgba(255,136,17,1)"></stop>
		        <stop stop-opacity="1" offset="100%" stop-color="#FFFFFF"></stop>
			</linearGradient>
		</defs>
		<path style="pointer-events: none;" d="M9 14.118L14.562 17.475L13.086 11.148L18 6.891L11.529 6.342L9 0.375L6.471 6.342L0 6.891L4.914 11.148L3.438 17.475L9 14.118Z" stroke="rgba(255,136,17,1)" fill="url('#yotpo_stars_gradient_0.3881005196172358')"></path>
	</svg><svg aria-hidden="true" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" class="star-container yotpo-sr-star-full" width="15" height="15" style="display: flex; flex-direction: row; margin-inline-end: 3.5px;">
	    <defs>
		    <linearGradient id="yotpo_stars_gradient_0.9428814097658837">
		        <stop offset="100%" stop-color="rgba(255,136,17,1)"></stop>
		        <stop stop-opacity="1" offset="100%" stop-color="#FFFFFF"></stop>
			</linearGradient>
		</defs>
		<path style="pointer-events: none;" d="M9 14.118L14.562 17.475L13.086 11.148L18 6.891L11.529 6.342L9 0.375L6.471 6.342L0 6.891L4.914 11.148L3.438 17.475L9 14.118Z" stroke="rgba(255,136,17,1)" fill="url('#yotpo_stars_gradient_0.9428814097658837')"></path>
	</svg><svg aria-hidden="true" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" class="star-container yotpo-sr-star-full" width="15" height="15" style="display: flex; flex-direction: row; margin-inline-end: 3.5px;">
	    <defs>
		    <linearGradient id="yotpo_stars_gradient_0.9609790481690816">
		        <stop offset="100%" stop-color="rgba(255,136,17,1)"></stop>
		        <stop stop-opacity="1" offset="100%" stop-color="#FFFFFF"></stop>
			</linearGradient>
		</defs>
		<path style="pointer-events: none;" d="M9 14.118L14.562 17.475L13.086 11.148L18 6.891L11.529 6.342L9 0.375L6.471 6.342L0 6.891L4.914 11.148L3.438 17.475L9 14.118Z" stroke="rgba(255,136,17,1)" fill="url('#yotpo_stars_gradient_0.9609790481690816')"></path>
	</svg><svg aria-hidden="true" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" class="star-container yotpo-sr-star-full" width="15" height="15" style="display: flex; flex-direction: row; margin-inline-end: 3.5px;">
	    <defs>
		    <linearGradient id="yotpo_stars_gradient_0.8854347607306429">
		        <stop offset="100%" stop-color="rgba(255,136,17,1)"></stop>
		        <stop stop-opacity="1" offset="100%" stop-color="#FFFFFF"></stop>
			</linearGradient>
		</defs>
		<path style="pointer-events: none;" d="M9 14.118L14.562 17.475L13.086 11.148L18 6.891L11.529 6.342L9 0.375L6.471 6.342L0 6.891L4.914 11.148L3.438 17.475L9 14.118Z" stroke="rgba(255,136,17,1)" fill="url('#yotpo_stars_gradient_0.8854347607306429')"></path>
	</svg><svg aria-hidden="true" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" class="star-container yotpo-sr-star-full" width="15" height="15" style="display: flex; flex-direction: row; margin-inline-end: 8px;">
	    <defs>
		    <linearGradient id="yotpo_stars_gradient_0.5730556054278372">
		        <stop offset="100%" stop-color="rgba(255,136,17,1)"></stop>
		        <stop stop-opacity="1" offset="100%" stop-color="#FFFFFF"></stop>
			</linearGradient>
		</defs>
		<path style="pointer-events: none;" d="M9 14.118L14.562 17.475L13.086 11.148L18 6.891L11.529 6.342L9 0.375L6.471 6.342L0 6.891L4.914 11.148L3.438 17.475L9 14.118Z" stroke="rgba(255,136,17,1)" fill="url('#yotpo_stars_gradient_0.5730556054278372')"></path>
	</svg>
</span>
        
            <span class="yotpo-sr-bottom-line-left-panel yotpo-sr-bottom-line-score" style="display: flex; align-self: center; color: rgb(255, 136, 17); font-family: Aleo; font-style: normal; font-weight: 400; font-size: 16px; margin-inline: 0px 10px; margin-bottom: 1px; padding-top: 3px;">
            4.8
            </span>
        
    </span>
    
        <span class="yotpo-sr-vertical-border" style="display: flex; place-self: center; height: 11px; border-right: 1px solid black; margin-right: 12px; margin-left: 0px;">
    </span>
    
        <span class="yotpo-sr-bottom-line-right-panel" style="display: flex;">
        <span class="yotpo-sr-bottom-line-text yotpo-sr-bottom-line-text--right-panel" style="white-space: nowrap; font-size: 16px; text-align: start; font-family: Aleo; font-style: normal; font-weight: 400; color: rgb(57, 24, 28); padding-top: 2px; line-height: 28px;">
        (12)
        </span>
        </span>
    
    <!--v-if-->
</button>

        <!--v-if-->
        
        <!--v-if-->
        <!--v-if-->
        <!--v-if-->
        <!--v-if-->
        
        <!--v-if-->
    </div>
</div>
</div></div>
```
**Note**:
```
**Source:** JS-rendered HTML from S3 `html_js/` folder

text inside <span class="group font-display text-display-xs font-black"><!--[-->Happy Valley Genetics<!--]--></span> = "Happy Valley Genetics"
```

---

### Amsterdam (163 strains)

**Sample URLs**:
```
https://amsterdammarijuanaseeds.com/
```
**Note**:
```
Amsterdam Marijuana Seeds is both the bank and the breeder
```

---

### Dutch Passion (119 strains)

**Sample URLs**:
```
https://dutch-passion.us/
```

**Note**:
```
Dutch Passion is both the bank and the breeder
```

---

### Barney's Farm (88 strains)

**Sample URLs**:
```
https://www.barneysfarm.com/us/
```
**Note**:
```
Barney's Farm is both the bank and the breeder
```

---

### Royal Queen Seeds (67 strains)

**Sample URLs**:
```
https://www.royalqueenseeds.com/us/
```

**Breeder location in HTML**:
```
Royal Queen Seeds is both the bank and the breeder
```

---

### Seeds Here Now (43 strains)

**Sample URLs**:
```
https://seedsherenow.com/shop/skywalker-og-autoflower-barneys-farm/
```

**Breeder location in HTML**:
```
<span class="last">Skywalker OG (Autoflower) – Barney’s Farm</span>
```
**Example HTML snippet**:
```html
<nav aria-label="breadcrumbs" class="rank-math-breadcrumb"><p><a href="https://seedsherenow.com" title="Home">Home</a><span class="separator"> | </span><a href="https://seedsherenow.com/shop/" title="Crypto Folks Get 15% Off Instantly — Pay Smart, Grow...">Shop</a><span class="separator"> | </span><span class="last">Skywalker OG (Autoflower) – Barney’s Farm</span></p></nav>
```
**Note**:
```
text inside and on right of "– " <span class="last">Skywalker OG (Autoflower) – Barney’s Farm</span> = "Barney’s Farm"
```

---

### Great Lakes Genetics (16 strains)

**Sample URLs**:
```
https://www.greatlakesgenetics.com/product/3rd-coast-family-farms-chemical-pie-10-seeds/
```

**Breeder location in HTML**:
```
<h3>3rd Coast Family Farms - Chemical Pie</h3>
```
**Example HTML snippet**:
```html
<div class="et_pb_module_inner"><h3>3rd Coast Family Farms - Chemical Pie</h3><p><strong>Genetics:</strong> Chemical Candy x Sweet as Pie<br> <strong>Seeds per pack:</strong> 10<br> <strong>Sex:</strong> Regular<br> <strong>Type:</strong> Hybrid<br> <strong>Flowering:</strong> 8-10 weeks<br> <strong>Yield: </strong>Medium to Heavy<br> <strong>Area: </strong>Indoor and Outdoor</p><p><strong>Notes: </strong>Chemical Pie has the nose of piney, earthy with a tad of lemon combining the smell of diesel and citrus with a bit of armpit. Rock hard frosty buds that will please any connoisseur.</p></div>
```
**Note**:
```
text inside and on left of " –" <h3>3rd Coast Family Farms - Chemical Pie</h3> = "3rd Coast Family Farms"
```

---

### Compound Genetics (1 strain)

**Sample URLs**:
```
https://seeds.compound-genetics.com/products/compound-genetics-x-method-seven
```

**Note:**:
```
The one url from Compound Genetics is for Sun Glasses. Row needs to be removed. Non-cannabis strain data. Also, need to remove it from our list of seed banks on Readme.md 
```

---

## Summary
**Notes:**:
```
Found a source_url_raw with no data, but other columns filled. Need to inspect if there are other source_url_raw missing, then if urls are recoverable. If not recoverable, then delete rows.
```

---
**Total seed banks**: 20  
**Patterns documented**: 19 (15 extractable + 4 self-branded)
**Ready for extraction**: Yes

---

**Next Steps**:
1. Shannon completes pattern documentation
2. Amazon Q builds seed-bank-specific extraction scripts
3. Re-extract breeder names from S3 HTML files
4. Merge with existing dataset
5. Verify 100% coverage

---

**Documented by**: Shannon Goddard  
**Scripts by**: Amazon Q
