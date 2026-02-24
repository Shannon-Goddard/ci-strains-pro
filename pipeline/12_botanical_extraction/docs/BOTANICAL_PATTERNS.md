# URL Patterns for Strain Name Extraction

**Purpose**: Document HTML structure for each seed bank  
**Reviewer**: Shannon Goddard  
**Date**: February 23, 2026

---

## Instructions

For each seed bank:
`pipeline\12_botanical_extraction\input\pipeline_11_final.csv`
1. Pick samples from the CSV
2. Identify the HTML pattern
3. Document what to extract and what to remove
4. Note any edge cases

---

## Amsterdam

**Sample HTML**:
```htmlhtml
<div class="ams-attr-table"><div class="ams-attr-row"><div class="ams-attr-label">THC</div><div class="ams-attr-value"><b>High THC</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">THC Level</div><div class="ams-attr-value"><b>Up to 21%</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Effects</div><div class="ams-attr-value"><b>Happy, Relaxed</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Flavor</div><div class="ams-attr-value"><b>Earthy, Herbs, Pine, Sweet</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Climate</div><div class="ams-attr-value"><b>Continental, Mediterranean, Temperate, Warm Dry</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Yield</div><div class="ams-attr-value"><b>Average</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Seed Type</div><div class="ams-attr-value"><b>Hybrid</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Indica / Sativa</div><div class="ams-attr-value"><b>60% / 40%</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Plant size</div><div class="ams-attr-value"><b>Compact</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Grow difficulty</div><div class="ams-attr-value"><b>Easy</b></div></div><div class="ams-attr-row"><div class="ams-attr-label">Flowering time</div><div class="ams-attr-value"><b>Fast (6-10 weeks)</b></div></div></div>
```

**URL**: https://amsterdammarijuanaseeds.com/ams-supreme-autoflower/

---

## Barney's Farm

**Sample HTML**:
```htmlhtml
<table cellspacing="0" cellpadding="0" class="strain-info-table active">
<tbody><tr>
<td>
<span><img src="/us/images/product-icons/genetics.svg" alt="Genetics" class="genetics"></span>
				                  Genetics				                </td>
<td>
				                  Blue Sunset Sherbert Strain x Thin Mint Girl Scout Cookies Strain				                </td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/thc.svg" alt="THC Content"></span>
				                  THC %
</td>
<td>28%</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/type.svg" alt="Type"></span>
				                  Type				                </td>
<td>FEMINISED</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/sativa.svg" alt="Sativa"></span>
				                  Sativa %				                </td>
<td>40</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/indica.svg" alt="Indica"></span>
				                  Indica %				                </td>
<td>60</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/taste.svg" alt="Taste"></span>
				                  Taste				                </td>
<td>Sugary, Creamy, Fresh Lavender, Sweet Red Berries</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/effect.svg" alt="Effect"></span>
				                  Effect				                </td>
<td>Relaxed,Happy, Euphoric, Uplifted, Creative</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/aroma.svg" alt="Aroma"></span>
				                  Aroma				                </td>
<td>Creamy Vanilla, Sweet Fruits, Earthy, Strawberry</td>
</tr>
</tbody></table>
```

**URL**: https://www.barneysfarm.com/us/gelato-weed-strain-628

---

## Crop King

**Sample HTML**:
```html
<table class="tablesorter eael-data-table " id="eael-data-table-1294693">
<thead>
<tr class="table-header">
<th class="" id="" colspan="">
<span class="data-table-header-text"></span></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Genetics												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Zkittles x Moonbow #75												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
THC Level												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
20-25%												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
CBD Level												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
low												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Category Type												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Balanced Hybrid												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Growing Level												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Flowering Time												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
8-9 weeks												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Indoor Height												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Medium (5 to 8 FT)												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Outdoor Height												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Medium (5 to 8 FT)												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Harvest Time												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Late September to early October												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Indoor Yields												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
400-500 g/m²												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Outdoor Yields												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
500-600 g/plant												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Taste and Smell												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Terpenes												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
</div></div>
</td>
</tr>
</tbody>
</table>
```

**URL**: https://www.cropkingseeds.com/feminized-seeds/rainbow-belts-2-0-strain-feminized-marijuana-seeds/

---

## Dutch Passion

**Sample HTML**:
```html
<table style="border-collapse: collapse; width: 100%; height: 544.3px;" border="1" cellpadding="3">
<tbody>
<tr style="height: 49.8px; background-color: #f4efe9;">
<th style="height: 49.8px; width: 100%;" colspan="3">
<h3 id="IGD1V8L" style="text-align: center;"></h3>
<h3 id="IGD1V8L" style="text-align: left;"><span style="font-size: 16px;">&nbsp;Passion #1 data sheet<br></span></h3>
</th>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; height: 40px; vertical-align: middle;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/feminised-cannabis-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/feminised-cannabis-seeds.png" alt="Feminized cannabis seeds" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><strong>Strain type:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Feminized / Regular<br></span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/dutch-outdoor-cannabis-strains-collection.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/dutch-outdoor-cannabis-strains-collection.png" alt="Dutch Outdoor cannabis strain" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Family:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Dutch Outdoor<br></span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/cannabis-genetics.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/cannabis-genetics.png" alt="Lineage" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Lineage:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Californian Indica</span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/hybrid-cannabis-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/hybrid-cannabis-seeds.png" alt="Hybrid cannabis seeds" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Genetics:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Hybrid</span></td>
</tr>
<tr style="height: 49.5px;">
<td style="width: 9.96593%; vertical-align: middle; height: 49.5px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/outdoor-cannabis-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/outdoor-cannabis-seeds.png" alt="Outdoor growing" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 49.5px; text-align: left;"><span style="font-size: 14px;"><strong>Environment:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 49.5px;"><span style="font-size: 14px;">Outdoor, greenhouse</span></td>
</tr>
<tr style="height: 42.5px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/plant-height.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/plant-height.png" alt="Plant height" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; text-align: left; height: 42.5px;"><span style="font-size: 14px;"><strong>Plant height:<br></strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;">Tall<br></span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/flowering-time.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/flowering-time.png" alt="Flowering time" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Flowering time:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">7-9 weeks</span></td>
</tr>
<tr style="height: 42.5px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/plant-yield.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/plant-yield.png" alt="Plant yield" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; text-align: left; height: 42.5px;"><span style="font-size: 14px;"><strong>Yield:<br></strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;">XL<br></span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/thc-content.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/thc-content.png" alt="THC content" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>THC level:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Very high (15-20%)</span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/flavor-profile.webp"><img style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/flavor-profile.png" alt="Taste" width="20" height="20" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Taste:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Herbal, piney, fruity</span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/hybrid-effect.webp"><img style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/hybrid-effect.png" alt="Hybrid effects" width="20" height="20" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Effects:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Hybrid high</span></td>
</tr>
</tbody>
</table>
```

**URL**: https://dutch-passion.us/cannabis-seeds/passion-1


---

## Exotic Genetics

**Sample HTML**:
```html
<div class="description woocommerce-product-details__short-description">
	<p><strong>Mother:</strong> Bonkers<br>
<strong>Reversal:</strong> Gary Poppins<br>
<strong>Sex: </strong>Feminized<br>
<strong>Pack Size:</strong> 6-Seeds</p>
<p><a href="https://exoticgenetix.com/coa/GP/sha-boink.pdf" target="_blank" rel="noopener"><img class="alignnone size-medium wp-image-10430" src="https://exoticgenetix.com/wp-content/uploads/2022/11/satisfaction_guarantee3-300x300.png" alt="" width="150" height="150"></a></p>
</div>
```

**URL**: https://exoticgenetix.com/product/sha-boink/

---

## Gorilla

**Sample HTML**:
```html
<div class="g-product-features">
      <ul>
<li> 22% THC</li>
<li>Yield  350 - 450 gr/m2</li>
<li>FLowering 45 - 50 days.</li>
<li>Height  85 - 95 cm.</li>
</ul>
    </div>
```

**URL**: https://www.gorilla-cannabis-seeds.co.uk/00-seeds/feminized/00-kush-fast.html

---

## Great Lakes

**Sample HTML**:
```html
<div class="et_pb_module et_pb_wc_description et_pb_wc_description_0_tb_body et_pb_bg_layout_light  et_pb_text_align_left"><div class="et_pb_module_inner"><h3>Backyard Boogie - Lavender Boogie</h3><p><strong>Genetics</strong>: <span data-olk-copy-source="MessageBody">Line worked Lemon Wookie V1 from Bodhi</span><br> <strong>Sex:</strong> Regular<br> <strong>Type</strong>: Hybrid<br> <strong>Flowering Time:&nbsp;</strong>65-72 days<br> <strong>Yield:&nbsp;</strong>High<br> <strong>Area (Indoor, Outdoor, Both):&nbsp;</strong>Both</p><p><strong>Notes:&nbsp;</strong>You many not want to grow anything else after trying this. Very grower friendly, big yields, and some of the most wonderful smells/effects I've ever experienced in cannabis. Expect extremely floral/lavender old lady perfume mixed with gas. With some added tennis ball rubber flavor when smoked. Feels like a warm hug that will put a smile on your face. Loved by rookie and veteran smokers alike, and is a perfect all day smoke.</p></div></div>
```

**URL**: https://www.greatlakesgenetics.com/product/backyard-boogie-lavender-boogie-11-reg-seeds/

---

## Herbies

**Sample HTML**:
```html
<table class="properties-list clamp-table-content"> <tbody><tr class="row item__property properties-list__item" title="Strain brand"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain brand </span> </td> <td class="col-6" style="padding: 0"><a href="https://herbiesheadshop.com/producers/alphafem-seeds">AlphaFem Seeds</a></td> </tr> <tr class="row item__property properties-list__item" title="Strain Gender"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain Gender </span> </td> <td class="col-6" style="padding: 0">Feminized</td> </tr> <tr class="row item__property properties-list__item" title="Strain light cycle"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain light cycle </span> </td> <td class="col-6" style="padding: 0">Photoperiod</td> </tr> <tr class="row item__property properties-list__item" title="Suitable for growing"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Suitable for growing </span> </td> <td class="col-6" style="padding: 0">Outdoor, Indoor</td> </tr> <tr class="row item__property properties-list__item" title="thc_range"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain THC level </span> </td> <td class="col-6 value" style="padding: 0; border: none;">30%</td> </tr> <tr class="row item__property properties-list__item" title="cbd"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain CBD level </span> </td> <td class="col-6 value" style="padding: 0; border: none;">2%</td> </tr> <tr class="row item__property properties-list__item" title="sainru"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> % Sativa/ Indica/ Ruderalis </span> </td> <td class="col-6 value" style="padding: 0; border: none;">Indica dominant</td> </tr> <tr class="row item__property properties-list__item" title="harvest"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain harvest </span> </td> <td class="col-6 value" style="padding: 0; border: none;">2 oz/ft² indoors<br>35.3 oz/plant outdoors</td> </tr> <tr class="row item__property properties-list__item" title="flow_time"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Indoor flowering time </span> </td> <td class="col-6 value" style="padding: 0; border: none;">65 - 75 days </td> </tr> <tr class="row item__property properties-list__item" title="height"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain height </span> </td> <td class="col-6 value" style="padding: 0; border: none;">47.2 - 78.7 inches indoors<br>47.2 - 78.7 inches outdoors</td> </tr> <tr class="row item__property properties-list__item" title="effect"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain effect </span> </td> <td class="col-6 value" style="padding: 0; border: none;">Blissful numbness</td> </tr> <tr class="row item__property properties-list__item" title="genetic"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Genetics </span> </td> <td class="col-6 value" style="padding: 0; border: none;">Different GG#4 x Sunset Sherbert</td> </tr> </tbody></table>
```

**URL**: https://herbiesheadshop.com/cannabis-seeds/glue-sherbert

---

## ILGM

**Sample HTML**:
```html
<table><tbody><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Plant Type</td><td class="p-0 text-right text-sm">Autoflower, Sativa</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Genotype</td><td class="p-0 text-right text-sm">Sativa Dominant</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Lineage</td><td class="p-0 text-right text-sm">Mimosa x ruderalis</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Effects</td><td class="p-0 text-right text-sm">Energetic, Focused, Uplifted</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Yield Potential</td><td class="p-0 text-right text-sm">400 gr/m²</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Taste and Aroma</td><td class="p-0 text-right text-sm">Citrus, Grapefruit, Orange, Pine</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">THC Level</td><td class="p-0 text-right text-sm">Medium</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">THC Percentage</td><td class="p-0 text-right text-sm">20</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBD Level</td><td class="p-0 text-right text-sm">Low</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBD Percentage</td><td class="p-0 text-right text-sm">0</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBG Level</td><td class="p-0 text-right text-sm">Low</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBG Percentage</td><td class="p-0 text-right text-sm">0</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Difficulty</td><td class="p-0 text-right text-sm">Beginner</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Climate</td><td class="p-0 text-right text-sm">Outdoor, Indoor, Sunny, Continental, Mediterranean</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Terpenes</td><td class="p-0 text-right text-sm">Caryophyllene, Myrcene, Pinene</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Bud Structure</td><td class="p-0 text-right text-sm">Medium Density, Medium Size</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Optimal Growing Temperature</td><td class="p-0 text-right text-sm">72-80°F</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Optimal Humidity Level</td><td class="p-0 text-right text-sm">40-60%</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Autoflower Total Growth Cycle</td><td class="p-0 text-right text-sm">70 days</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Harvest Height</td><td class="p-0 text-right text-sm">Medium</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Resilience</td><td class="p-0 text-right text-sm">Diseases</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Original Genetics Developed By</td><td class="p-0 text-right text-sm">Symbiotic Genetics</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Brand</td><td class="p-0 text-right text-sm">ILGM</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">SKU</td><td class="p-0 text-right text-sm">ILG-MIM-FAP</td></tr></tbody></table>
```

**URL**: https://ilgm.com/products/mimosa-autoflower-seeds

---

## Mephisto

**Sample HTML**:
```html
<div data-w-tab="In The Weeds" class="product-header6_tab-details w-tab-pane w--tab-active">
                    <div class="margin-top margin-small">
                      <div class="w-layout-grid grid">
                        
                          <div id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f7-d7b2c481" class="text-weight-bold">Indica/Sativa</div>
                          <div id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f9-d7b2c481">50/50</div>
```

**URL**: https://mephistogenetics.com/products/double-delirium

---

## Multiverse

**Sample HTML**:
```html
<div class="woocommerce-product-details__short-description"><div class="classic-editor page-width"><ul><li data-start="601" data-end="636"><strong data-start="603" data-end="612">Type:</strong> Autoflower, Feminized</li><li data-start="637" data-end="678"><strong data-start="639" data-end="652">Genetics:</strong> Nova OG x Pure Michigan</li><li data-start="679" data-end="725"><strong data-start="681" data-end="699">Indica/Sativa:</strong> 80% Indica / 20% Sativa</li><li data-start="763" data-end="796"><strong data-start="765" data-end="785">Seed to Harvest:</strong> ~85 Days</li><li data-start="797" data-end="878"><strong data-start="799" data-end="824">Flowering Initiation:</strong> Around Days 18-28 (influenced by pot size &amp; stress)</li><li data-start="879" data-end="920"><strong data-start="881" data-end="906">Recommended Pot Size:</strong> 3-5 gallons</li><li data-start="921" data-end="986"><strong data-start="923" data-end="940">Growth Style:</strong> Best results with <strong data-start="959" data-end="984">LST or natural growth</strong></li></ul><p>&nbsp;</p><p><strong data-start="64" data-end="86">Son of a Mich Auto</strong> is a <strong data-start="92" data-end="150">high-yielding, terpene-rich Indica-dominant autoflower</strong> bred from <strong data-start="161" data-end="188">Nova OG x Pure Michigan</strong>.</p><p>This strain delivers <strong data-start="252" data-end="279">dense, resinous flowers</strong> bursting with <strong data-start="294" data-end="331">candy, bubblegum, and kush aromas</strong>.</p><p>Expect a <strong data-start="342" data-end="362">robust main cola</strong> with <strong data-start="368" data-end="403">large, well-formed side flowers</strong>, making it a <strong data-start="417" data-end="472">top-tier choice for both indoor and outdoor growers</strong>.</p><p><strong data-start="474" data-end="490">Best results</strong> come from <strong data-start="501" data-end="526">LST or natural growth</strong>, as topping tends to produce smaller plants.</p></div></div>
```

**URL**: https://multiversebeans.com/product/son-of-a-mich-aeque-genetics-autoflower-cannabis-seeds-female/

---

## Neptune

**Sample HTML**:
```html
<div class="tab-content-container">
            <div id="description" class="tab-content active" tabindex="-1">
                <h2>Product description</h2>
                <h2 class="" data-start="174" data-end="224"><strong data-start="177" data-end="224">Green Crack BX Strain Seeds – “42” (Regular Seeds)</strong></h2>
<hr class="" data-start="474" data-end="477">
<h3 class="" data-start="479" data-end="513">What Are Green Crack BX Seeds?</h3>
<p class="" data-start="515" data-end="950"><strong data-start="515" data-end="539">Green Crack BX strain seeds</strong> by <strong data-start="543" data-end="551">“42”</strong> offer a reimagined version of the legendary sativa-dominant strain <strong data-start="619" data-end="634">Green Crack</strong>, now backcrossed with the gas-heavy <strong data-start="671" data-end="686">Animal Face</strong> for extra resin, potency, and depth. This <strong data-start="729" data-end="757">12-pack of regular seeds</strong> delivers uplifting, energetic effects with a flavor profile that balances <strong data-start="832" data-end="864">sweet citrus and earthy funk</strong>. If you’re after <strong data-start="882" data-end="919">vigor, flavor, and frosty results</strong>, Green Crack BX is a top pick.</p>
<hr class="" data-start="952" data-end="955">
<h3 class="" data-start="957" data-end="985">Structure and Appearance</h3>
<p class="" data-start="987" data-end="1323">Green Crack BX grows with classic sativa traits—<strong data-start="1035" data-end="1102">tall structure, strong branching, and explosive vertical growth</strong> during flower. However, thanks to Animal Face, it also develops <strong data-start="1167" data-end="1189">tight, chunky buds</strong> coated in thick trichomes. Expect lime green flowers, fiery orange hairs, and dense coverage perfect for both flower and extract use.</p>
<hr class="" data-start="1325" data-end="1328">
<h3 class="" data-start="1330" data-end="1358">Flavor and Aroma Profile</h3>
<p class="" data-start="1360" data-end="1647">This cross blends the <strong data-start="1382" data-end="1405">sweet, zesty citrus</strong> of Green Crack with the <strong data-start="1430" data-end="1451">fuel-forward funk</strong> of Animal Face. The result is an uplifting terpene mix of lemon-lime, sour pine, and earthy gas with a slightly creamy backend. The flavor is bright and lingers long on the palate and in the jar.</p>
<hr class="" data-start="1649" data-end="1652">
<h3 class="" data-start="1654" data-end="1683">Effects and Medicinal Use</h3>
<p class="" data-start="1685" data-end="2000"><strong data-start="1685" data-end="1709">Green Crack BX seeds</strong> produce flower with <strong data-start="1730" data-end="1765">energetic, mood-lifting effects</strong> perfect for daytime use. Users report increased focus, motivation, and creativity—ideal for busy schedules or social sessions. Medicinally, it may help with <strong data-start="1923" data-end="1958">fatigue, depression, and stress</strong> while keeping your mind clear and active.</p>
<hr class="" data-start="2002" data-end="2005">
<h3 class="" data-start="2007" data-end="2039">Growing Green Crack BX Seeds</h3>
<p class="" data-start="2041" data-end="2336">These <strong data-start="2047" data-end="2064">regular seeds</strong> flower in about <strong data-start="2081" data-end="2094">8–9 weeks</strong> and thrive in indoor and outdoor setups. Green Crack BX is <strong data-start="2154" data-end="2171">easy to train</strong> and stretches during flower, so plan for some extra height. Its <strong data-start="2236" data-end="2277">resin-rich buds and terp-heavy output</strong> make it ideal for both flower markets and extract artists.</p>
<hr class="" data-start="2338" data-end="2341">
<h3 class="" data-start="2343" data-end="2379">Why Choose Green Crack BX Seeds?</h3>
<p class="" data-start="2381" data-end="2732"><strong data-start="2381" data-end="2405">Green Crack BX strain seeds</strong> offer an energized, citrus-forward hybrid with boosted resin production and modern gas terps. Bred by “42”, this cross brings new life to a classic sativa-dominant strain. Grab your 12-pack now from <a target="_new" rel="noopener" data-start="2605" data-end="2683">Neptune Seed Bank</a> and enjoy <strong data-start="2694" data-end="2731">vintage vigor with modern potency</strong>.</p>
<hr class="" data-start="2734" data-end="2737">
<h3 class="" data-start="2739" data-end="2767">About the Breeder – “42”</h3>
<p class="" data-start="2769" data-end="3168"><strong data-start="2769" data-end="2777">“42”</strong> is a rising name in the cannabis breeding world, known for releasing <strong data-start="2847" data-end="2877">elite, hash-ready genetics</strong> like <a target="_new" rel="noopener" data-start="2883" data-end="2938">Zesty Drip</a>, <a target="_new" rel="noopener" data-start="2940" data-end="2999">Sour Sage OG</a>, and <a target="_new" rel="noopener" data-start="3005" data-end="3058">Dole Whip</a>. With an eye for flavor and a focus on quality, “42” continues to drop heat for connoisseurs and cultivators.</p>
<hr class="" data-start="3170" data-end="3173">
<h3 class="" data-start="3175" data-end="3205">Similar Strains to Explore</h3>
<ul data-start="3207" data-end="3404">
<li class="" data-start="3207" data-end="3276">
<p class="" data-start="3209" data-end="3276"><a target="_new" rel="noopener" data-start="3209" data-end="3274">Green Crack crosses</a></p>
</li>
<li class="" data-start="3277" data-end="3346">
<p class="" data-start="3279" data-end="3346"><a target="_new" rel="noopener" data-start="3279" data-end="3344">Animal Face hybrids</a></p>
</li>
<li class="" data-start="3347" data-end="3404">
<p class="" data-start="3349" data-end="3404"><a target="_new" rel="noopener" data-start="3349" data-end="3404">Zesty Drip</a></p>
</li>
</ul>
<hr class="" data-start="3406" data-end="3409">
<h3 class="" data-start="3411" data-end="3452">Stay Connected with Neptune Seed Bank</h3>
<p class="" data-start="3454" data-end="3589">Thanks for checking out <strong data-start="3478" data-end="3502">Green Crack BX seeds</strong> by “42”! Follow us for early access to drops, giveaways, and limited-edition releases:</p>
<ul data-start="3591" data-end="3902">
<li class="" data-start="3591" data-end="3656">
<p class="" data-start="3593" data-end="3656"><a class="" href="https://www.instagram.com/neptunesseedsofficial/" target="_new" rel="noopener" data-start="3593" data-end="3654">Instagram</a></p>
</li>
<li class="" data-start="3657" data-end="3705">
<p class="" data-start="3659" data-end="3705"><a class="" href="https://x.com/NeptuneSeedBank" target="_new" rel="noopener" data-start="3659" data-end="3703">X (Twitter)</a></p>
</li>
<li class="" data-start="3706" data-end="3759">
<p class="" data-start="3708" data-end="3759"><a class="" href="https://www.tiktok.com/@neptuneseedbank" target="_new" rel="noopener" data-start="3708" data-end="3757">TikTok</a></p>
</li>
<li class="" data-start="3760" data-end="3819">
<p class="" data-start="3762" data-end="3819"><a class="" href="https://www.youtube.com/@neptuneseedbank4168" target="_new" rel="noopener" data-start="3762" data-end="3817">YouTube</a></p>
</li>
<li class="" data-start="3820" data-end="3902">
<p class="" data-start="3822" data-end="3902"><a class="" href="https://discord.gg/A3YmdxP43M" target="_new" rel="noopener" data-start="3822" data-end="3871">Join our Discord</a> or sign up for the newsletter!</p>
</li>
</ul>
<hr class="" data-start="4320" data-end="4323">
<p class="" data-start="4325" data-end="4496"><strong data-start="4325" data-end="4345"><img draggable="false" role="img" class="emoji" alt="⚠️" src="https://s.w.org/images/core/emoji/17.0.2/svg/26a0.svg"> Legal Notice:</strong><br data-start="4345" data-end="4348">Seeds are sold as adult novelty items. Buyers are responsible for following local laws. Neptune Seed Bank assumes no liability. All sales are final.</p>
            </div>
            
            <div id="technical-info" class="tab-content" tabindex="-1">
                <h2>Technical information</h2>
                            </div>
            
            <div id="reviews" class="tab-content">
                <div id="reviews" class="woocommerce-Reviews">
	<div id="comments">
		<h2 class="woocommerce-Reviews-title">
			Reviews		</h2>

					<p class="woocommerce-noreviews">There are no reviews yet.</p>
			</div>

			<p class="woocommerce-verification-required">Only logged in customers who have purchased this product may leave a review.</p>
	
	<div class="clear"></div>
</div>
            </div>
        </div>
```

**URL**: https://neptuneseedbank.com/product/green-crack-BX-strain-seeds/

---

## North Atlantic

**Sample HTML**:
```html
<div class="product-specifications">
        <h2 class="section-heading">Specifications</h2>
        <div class="specs-grid">
            <div class="spec-item"><i class="fas fa-cubes"></i><dl><dt class="spec-label">Pack Size</dt><dd class="spec-value">1 pack, 3 pack, 5 pack, 10 pack</dd></dl></div><div class="spec-item"><i class="fas fa-dna"></i><dl><dt class="spec-label">Genetics</dt><dd class="spec-value">Chemdawg x Lemon Thai x Hindu Kush</dd></dl></div><div class="spec-item"><i class="fas fa-venus"></i><dl><dt class="spec-label">Seed Type</dt><dd class="spec-value">Feminized</dd></dl></div><div class="spec-item"><i class="fas fa-sun"></i><dl><dt class="spec-label">Growth Type</dt><dd class="spec-value">Photoperiod</dd></dl></div><div class="spec-item"><i class="fas fa-cannabis"></i><dl><dt class="spec-label">Strain Type</dt><dd class="spec-value">Hybrid, Indica Dominant (60%+)</dd></dl></div><div class="spec-item"><i class="fas fa-clock"></i><dl><dt class="spec-label">Flowering Time</dt><dd class="spec-value">55 - 65 days, Outdoor: Mid to Late September</dd></dl></div><div class="spec-item"><i class="fas fa-ruler-vertical"></i><dl><dt class="spec-label">Height</dt><dd class="spec-value">Indoors: 100-120cm; Outdoors: up to 150–200cm</dd></dl></div><div class="spec-item"><i class="fas fa-wheat-awn"></i><dl><dt class="spec-label">Yield</dt><dd class="spec-value">Indoors: 600-700 gr/m²; Outdoors: up to 1500-2000 gr/plant</dd></dl></div><div class="spec-item"><i class="fas fa-flask"></i><dl><dt class="spec-label">Terpene Profile</dt><dd class="spec-value">Citrus, Sour, Pungent, Skunky, Dank, Earthy</dd></dl></div><div class="spec-item"><i class="fas fa-lemon"></i><dl><dt class="spec-label">Flavor Profile</dt><dd class="spec-value">Sour, Citrus, Herbal, Skunky, Woody Pine</dd></dl></div>        </div>
    </div>
```

**URL**: https://www.northatlanticseed.com/product/cheese-auto/

---

## Royal Queen

**Sample HTML**:
```html
<table id="idTab2" class="bullet product-features-list">
								<caption><h5>Cherry Pie Auto data sheet</h5></caption>
																											<tbody><tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/1773_val_family-auto_1.svg">
																							</td>
											<th class="feature-name">Variety:</th>
											<td class="feture-value">Autoflowering</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/23_genetic background_1.svg">
																							</td>
											<th class="feature-name">Genetic Background:</th>
											<td class="feture-value">Cherry Pie x Granddaddy Purple Auto</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/29_THC_1.svg">
																							</td>
											<th class="feature-name">THC:</th>
											<td class="feture-value">Up to 19%</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/30_CBD_1.svg">
																							</td>
											<th class="feature-name">CBD:</th>
											<td class="feture-value">Low</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/28_Type-Blend_1.svg">
																							</td>
											<th class="feature-name">Type:</th>
											<td class="feture-value">Sativa 30%, Indica 65%, Ruderalis 5%</td>
										</tr>
																																																																						<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/31_plant height outdoor_1.svg">
																							</td>
											<th class="feature-name">Height Indoor:</th>
											<td class="feture-value">2 to 3 feet</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/32_plant height outdoors_1.svg">
																							</td>
											<th class="feature-name">Height Outdoor:</th>
											<td class="feture-value">4 to 5 feet</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/33_Yield indoors_1.svg">
																							</td>
											<th class="feature-name">Yield Indoor :</th>
											<td class="feture-value">14 to 16 oz/m²</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/34_yield outdoor_1.svg">
																							</td>
											<th class="feature-name">Yield Outdoor:</th>
											<td class="feture-value">3 to 6 oz/plant</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/25_flowering time_1.svg">
																							</td>
											<th class="feature-name">Flowering time:</th>
											<td class="feture-value">50 - 60 days</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/110_harvest.svg">
																							</td>
											<th class="feature-name">Harvest:</th>
											<td class="feture-value">65 - 70 days after germination</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/35_Climate_1.svg">
																							</td>
											<th class="feature-name">Climate:</th>
											<td class="feture-value">Long Summers</td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/22_Effect_1.svg">
																							</td>
											<th class="feature-name">Effect:</th>
											<td class="feture-value">Balanced, Physically Relaxing, Uplifting </td>
										</tr>
																																				<tr>
											<td class="feature-icon">
																									<img width="30" src="/modules/featureicons/icons/46_Flavour.svg">
																							</td>
											<th class="feature-name">Flavor:</th>
											<td class="feture-value">Blueberry, Candy, Fruity</td>
										</tr>
																								</tbody></table>
```

**URL**: https://www.royalqueenseeds.com/us/autoflowering-cannabis-seeds/654-cherry-pie-automatic.html

---

## Seed Supreme

**Sample HTML**:
```html
<table class="data table additional-attributes" id="product-attribute-specs-table"><tbody> <tr> <td class="col label">SKU:</td><td class="col data">SSSB-HV-PND-FAX</td> <td class="col label">Seedbank:</td><td class="col data">Happy Valley Genetics (Powered by ETHOS)</td> </tr> <tr> <td class="col label">Genetics:</td><td class="col data">Banana Daddy × Pineapple Runtz</td> <td class="col label">Variety:</td><td class="col data">Hybrid</td> </tr> <tr> <td class="col label">Flowering Type:</td><td class="col data">Autoflowering</td> <td class="col label">THC Content:</td><td class="col data">Very High (over 20%)</td> </tr> <tr> <td class="col label">CBD Content:</td><td class="col data">Low (0-1%)</td> <td class="col label">Yield:</td><td class="col data">Average</td> </tr> <tr> <td class="col label">Effects:</td><td class="col data">Hungry, Relaxed</td> <td class="col label">Flavors:</td><td class="col data">Fruity, Grape, Pineapple, Woody</td> </tr> <tr> <td class="col label">Terpenes:</td><td class="col data">Caryophyllene, Humulene, Myrcene</td> <td class="col label">Flowering Time:</td><td class="col data">8-10 Weeks from Seed</td> </tr> <tr> <td class="col label">Plant Height:</td><td class="col data">Medium</td>  <td class="col label"></td><td class="col data"></td></tr></tbody></table>
```

**URL**: https://seedsupreme.com/pineapple-daddy-autoflower-cannabis-seeds.html

---

## Seeds Here Now

**Sample HTML**:
```html
<div class="product-add-info">
        <div class="add-info-content">
            <h2 style="display: none;">STRAIN INFORMATION</h2>
            <div class="add-info-grid">
                 <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">

                    </div>
                    <h3 class="add-info-title">Seed Type</h3>
                    <p class="add-info-description">Feminized                    </p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <h3 class="add-info-title">Strain Type</h3>
                    <p class="add-info-description">Hybrid                    </p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[3][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">

                    </div>
                    <h3 class="add-info-title">Lineage</h3>
                    <p class="add-info-description">Gorilla Glue x Thin Mint Girl Scout Coolies                    </p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[4][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">

                    </div>
                    <h3 class="add-info-title">Pack Size</h3>
                    <p class="add-info-description">3 Seeds, 5 Seeds                    </p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[5][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <h3 class="add-info-title">Indica / Sativa</h3>
                    <p class="add-info-description">/                    </p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[6][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/thc.svg" alt="Yield" class="add-info-icon" loading="lazy" title="Yield">
                    </div>
                    <h3 class="add-info-title">THC %</h3>
                    <p class="add-info-description">21% to 26% %</p>
                </div>

                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[7][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/aroma.svg" alt="Aroma" class="add-info-icon" loading="lazy" title="Aroma">

                    </div>
                    <h3 class="add-info-title">Aroma</h3>
                    <p class="add-info-description">earthy,&nbsp;sweet,&nbsp;citrus,&nbsp;fuel</p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[8][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <h3 class="add-info-title">Flower Time</h3>
                    <p class="add-info-description">8 to 10 weeks</p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[9][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/thc.svg" alt="Yield" class="add-info-icon" loading="lazy" title="Yield">
                    </div>
                    <h3 class="add-info-title">Yield</h3>
                    <p class="add-info-description">High</p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[10][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <h3 class="add-info-title">Terpenes</h3>
                    <p class="add-info-description">caryophyllene,&nbsp;limonene,&nbsp;myrcene</p>
                </div>


                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[11][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <h3 class="add-info-title">Effects</h3>
                    <p class="add-info-description">euphoric,&nbsp;relaxing,&nbsp;happy,&nbsp;stress relief</p>
                </div>

                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[2][self::DIV]/*[12][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <h3 class="add-info-title">Best Use</h3>
                    <p class="add-info-description">Evening</p>
                </div>
            </div>

            <div class="grow-tips-info">
                <div class="add-info-card">
                    <div class="icon-container">
                        <img data-od-xpath="/HTML/BODY/DIV[@id='page']/*[6][self::SECTION]/*[1][self::DIV]/*[2][self::DIV]/*[1][self::DIV]/*[3][self::DIV]/*[1][self::DIV]/*[1][self::DIV]/*[1][self::IMG]" src="https://seedsherenow.com/wp-content/themes/seeds-here-now-2025/images/cannabis.svg" alt="Grow Tips" class="add-info-icon" loading="lazy" title="Grow Tips">
                    </div>
                    <div class="des-container">
                        <h3 class="add-info-title">Grow Tips</h3>
                        <p class="add-info-description">Thrives in controlled environments, requires regular pruning.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
```

**URL**: https://seedsherenow.com/shop/glookies-feminized-barneys-farm/

---

## Seedsman

**Sample HTML**:
```html
<table id="product-attribute-specs-table" class="data table additional-attributes"><tbody><tr><th scope="row" class="col label"><h4>SKU</h4></th><td data-th="SKU" class="col data"><h3>ACE-THXPAN-REG</h3></td></tr><tr><th scope="row" class="col label"><h4>Brand/breeder</h4></th><td data-th="Brand/breeder" class="col data"><h3><span><a href="https://www.seedsman.com/us-en/cannabis-seed-breeders/ace-seeds" title="Ace Seeds" target="_self">Ace Seeds</a></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Parental lines</h4></th><td data-th="Parental lines" class="col data"><h3>Thai Chiang Mai x Panama (latest generation parents)</h3></td></tr><tr><th scope="row" class="col label"><h4>Variety</h4></th><td data-th="Variety" class="col data"><h3><span>Sativa dominant</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Flowering type</h4></th><td data-th="Flowering type" class="col data"><h3><span>Photoperiod</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Sex</h4></th><td data-th="Sex" class="col data"><h3><span>Regular</span></h3></td></tr><tr><th scope="row" class="col label"><h4>THC content</h4></th><td data-th="THC content" class="col data"><h3><span>High THC (16-24%)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>CBD content</h4></th><td data-th="CBD content" class="col data"><h3><span>Low CBD (0-1%)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Yield outdoor</h4></th><td data-th="Yield outdoor" class="col data"><h3><span>High Yield (450-750gr/plant)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Yield indoor</h4></th><td data-th="Yield indoor" class="col data"><h3><span>High Yield (450-600gr/m2)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Plant size</h4></th><td data-th="Plant size" class="col data"><h3><span>Large</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Photoperiod flowering time</h4></th><td data-th="Photoperiod flowering time" class="col data"><h3><span>12 to 14 weeks</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Northern hemisphere harvest</h4></th><td data-th="Northern hemisphere harvest" class="col data"><h3><span><span>October</span></span><span><span> | November</span></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Suitable climates</h4></th><td data-th="Suitable climates" class="col data"><h3><span><span>Dry</span></span><span><span> | Hot</span></span><span><span> | Warm</span></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Generational type</h4></th><td data-th="Generational type" class="col data"><h3><span><span>F1</span></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Odor</h4></th><td data-th="Odor" class="col data"><h3><span>Medium</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Aroma</h4></th><td data-th="Aroma" class="col data"><h3><span><span>Fruity</span></span><span><span> | Spicy</span></span><span><span> | Woody</span></span></h3></td></tr></tbody></table>
```

**URL**: https://www.seedsman.com/us-en/thai-x-panama-regular-seeds-ace-thxpan-reg

---

## Sensi

**Sample HTML**:
```html
<div class="surver-product-bottom">
		<div class="surver-product-bottom-left">
			<div class="surver-product-description">
			<h3>
				Description			</h3>
			<p>Sweet &amp; Sour Cream Automatic seeds result from crossbreeding Sour Florida OG and Gelato #420 strains, with a 65% indica and 35% sativa ratio. It develops into a low-profile plant, excellent for tents or discreet outdoor gardens. Sweet &amp; Sour Cream Automatic offers a combination of characteristics from both ends of the spectrum. Growers will enjoy shades of green and purple as this fast-flowering plant finishes its growth cycle. Dried flowers are incredibly sticky and have an exotic terpene profile.</p>
<h2>Growth pattern of Sweet &amp; Sour Cream Automatic</h2>
<p>The indica dominance in Sweet &amp; Sour Cream Automatic is evident in its compact structure, tight nodal spacing with strong branches, and prominent central cola. Sweet &amp; Sour Cream Automatic has a flowering of between 55 and 65 days. Indoors, this plant typically reaches a height of 39 inches, while outdoors, it can grow even taller in open soil. It has a compact structure.</p>
<p>Indoor cultivators of Sweet &amp; Sour Cream Automatic can expect a bountiful harvest, with an average yield of around 250 to 300 grams per meter. Meanwhile, outdoor growers can enjoy a yield of 200 grams per plant. Sweet &amp; Sour Cream Automatic flowers are known to form into medium to large-sized golf ball-like buds that are dense and chunky due to the tightly packed, swollen bracts. Growers can expect to see vibrant hues and dense resin-coated flowers.</p>
<p>While Sweet &amp; Sour Cream Auto performs exceptionally well in controlled indoor environments, it thrives in temperate/continental regions when grown outdoors. Sweet &amp; Sour Cream Automatic can be topped to produce larger colas. However, traditional plant training methods like SOG, SCROG, or supercropping are unnecessary.</p>
<h2><strong>&nbsp;</strong>Taste and smell of Sweet &amp; Sour Cream Automatic</h2>
<p>Sweet &amp; Sour Cream Auto boasts a robust floral fragrance that intensifies during the final stages of growth. However, its true aroma shines once the flowers are dried and cured. Dried flowers have an unmistakable vanilla fragrance that lingers on the nose, similar to the creaminess of Gelato #420. Accompanying that aroma are undertones of exotic sandalwood, nuts, and a hint of cookie dough. The overall terpene profile is smooth and inviting to the nose.</p>
<p>Sweet &amp; Sour Cream Automatic has exquisite flavors that build on the aroma profile, and the distinctive vanilla flavor coats the taste buds with this pleasingly smooth taste. While consuming Sweet &amp; Sour Cream Auto, a hint of sweet honey can be detected at the back of the palate. Subtle notes of sour lemon and diesel fuel from the Sour Florida OG come with the exhale.</p>
<h2>Did you know?</h2>
<ul>
<li>Sour Florida OG, one parent strain, hails from Florida.</li>
<li>The other parent, Gelato #420, was created by White Label Seeds by crossing Gelato 33, Durban, and Hindu Kush.</li>
</ul>
			</div>
			<div class="surver-product-reviews">
			<h3>
				Reviews			</h3>

			<div class="yotpo yotpo-main-widget yotpo-small" data-product-id="P1530047" data-price="32.00" data-currency="USD" data-name="Sweet &amp; Sour Cream Automatic Seeds" data-url="https://sensiseeds.us/autoflowering-seeds/sweet-sour-cream/" data-yotpo-element-id="1"> <div class="main-widget yotpo-display-wrapper yotpo-no-reviews" style="visibility: hidden;" data-source="default">      <div class="yotpo-label-container ">      <a href="https://www.yotpo.com/?utm_campaign=branding_link_reviews_widget_v2&amp;utm_medium=widget&amp;utm_source=sensiseeds.us" class="yotpo-logo-link-new" aria-label="Powered by Yotpo link to their homepage" tabindex="0" target="_blank"> <span class="yotpo-logo-title  yotpo-powered "> Powered by </span> <div class="yotpo-icon-btn-big transparent-color-btn yotpo-logo-btn yotpo-icon yotpo-icon-yotpo-logo yotpo-logo-icon-new yotpo-icon yotpo-icon-yotpo-logo ">  </div> </a>    <div class="yotpo-logo-line"> </div> </div>    <span class="yotpo-display-wrapper" style="visibility: hidden;">  <div class="yotpo-regular-box yotpo-bottomline bottom-line-items-container"> <div class="bottom-line-items">   <span class="yotpo-filter-stars rating-stars-container mL0"> <span class="yotpo-icon yotpo-icon-empty-star rating-star pull-left"></span><span class="yotpo-icon yotpo-icon-empty-star rating-star pull-left"></span><span class="yotpo-icon yotpo-icon-empty-star rating-star pull-left"></span><span class="yotpo-icon yotpo-icon-empty-star rating-star pull-left"></span><span class="yotpo-icon yotpo-icon-empty-star rating-star pull-left"></span><span class="sr-only">0.0 star rating</span> </span> <span class="reviews-qa-labels-container mL0"> <span class="reviews-qa-label font-color-gray">0 Reviews</span>  </span>  </div> <div class="yotpo-clr"></div>  </div>  <div class="yotpo-clr"></div> </span>   <div class="write-question-review-buttons-container">  <button type="button" class="yotpo-default-button yotpo-icon-btn write-question-review-button write-button write-review-button" role="tab" aria-label="Click the button to write a review" aria-controls="write-review-tabpanel-main-widget" aria-expanded="false" fdprocessedid="vlrq2"> <span class="yotpo-icon yotpo-icon-write-no-frame write-question-review-button-icon yotpo-hidden-mobile"></span> <span class="write-question-review-button-text font-color-gray-darker">Write A Review</span> </button>   </div>    <form aria-label="Write A Review Form"> <div class="write-review-wrapper write-form"> <div class="write-review yotpo-regular-box" id="write-review-tabpanel-main-widget" role="tabpanel">  <div class="yotpo-header"> <div> <h2 class="y-label yotpo-header-title">WRITE A REVIEW</h2> </div> <div class="yotpo-mandatory-explain"> <span class="yotpo-mandatory-mark">*</span> Indicates a required field </div> <br> <span class="yotpo-mandatory-mark">* </span> <span class="y-label" id="write-review-score-1ff941b8-0126-44e3-9e7e-2071074e5392">Score: <span class="form-input-error yotpo-hidden" id="yotpo_score_message_1ff941b8-0126-44e3-9e7e-2071074e5392"></span></span> <div aria-describedby="yotpo_score_message_1ff941b8-0126-44e3-9e7e-2071074e5392" aria-labelledby="write-review-score-1ff941b8-0126-44e3-9e7e-2071074e5392" role="radiogroup" tabindex="-1"> <span class="stars-wrapper">  <span class="yotpo-icon yotpo-icon-empty-star pull-left review-star" data-score="1" aria-label="score 1" role="radio" tabindex="0" aria-checked="false" aria-required="true"></span>  <span class="yotpo-icon yotpo-icon-empty-star pull-left review-star" data-score="2" aria-label="score 2" role="radio" tabindex="-1" aria-checked="false" aria-required="true"></span>  <span class="yotpo-icon yotpo-icon-empty-star pull-left review-star" data-score="3" aria-label="score 3" role="radio" tabindex="-1" aria-checked="false" aria-required="true"></span>  <span class="yotpo-icon yotpo-icon-empty-star pull-left review-star" data-score="4" aria-label="score 4" role="radio" tabindex="-1" aria-checked="false" aria-required="true"></span>  <span class="yotpo-icon yotpo-icon-empty-star pull-left review-star" data-score="5" aria-label="score 5" role="radio" tabindex="-1" aria-checked="false" aria-required="true"></span>  </span> </div> </div> <div class="write-review-content"> <div class="form-group"> <div class="form-element"> <span class="yotpo-mandatory-mark">* </span> <label class="y-label" for="yotpo_input_review_title_1ff941b8-0126-44e3-9e7e-2071074e5392"> Title: <span class="form-input-error yotpo-hidden" id="yotpo_input_review_title_error_1ff941b8-0126-44e3-9e7e-2071074e5392"></span> </label> <input id="yotpo_input_review_title_1ff941b8-0126-44e3-9e7e-2071074e5392" class="y-input" name="review_title" maxlength="150" aria-required="true" placeholder="" aria-describedby="yotpo_input_review_title_error_1ff941b8-0126-44e3-9e7e-2071074e5392"> </div> <div class="form-element"> <span class="yotpo-mandatory-mark">* </span> <label class="y-label" for="yotpo_input_review_content_1ff941b8-0126-44e3-9e7e-2071074e5392"> Review: <span class="form-input-error yotpo-hidden" id="yotpo_input_review_content_error_1ff941b8-0126-44e3-9e7e-2071074e5392"></span> </label> <textarea id="yotpo_input_review_content_1ff941b8-0126-44e3-9e7e-2071074e5392" class="y-input yotpo-text-box" name="review_content" aria-required="true" placeholder="" aria-describedby="yotpo_input_review_content_error_1ff941b8-0126-44e3-9e7e-2071074e5392"></textarea> </div>   </div> </div> <div class="yotpo-footer yotpo-animation-opacity visible" style="display: inherit;">  <div class="socialize-wrapper"> <div class="connected">You are connected as <span class="username"></span></div> <div class="socialize"> <span class="y-label">Connect with:</span> <div> <div class="yotpo-default-button yotpo-icon-btn" data-network="twitter" aria-label="connect with twitter" role="link" tabindex="0"><span class="yotpo-icon yotpo-icon-twitter pull-left"></span></div> <div class="yotpo-default-button yotpo-icon-btn" data-network="facebook" aria-label="connect with facebook" role="link" tabindex="0"><span class="yotpo-icon yotpo-icon-facebook pull-left"></span></div> </div> </div> <div class="yotpo-or"> -OR- </div> </div>  <div class="connect-wrapper visible " style="display: inherit;">  <div class="form-element name-input visible" style="display: inherit;"> <span class="yotpo-mandatory-mark">* </span> <label class="y-label" for="yotpo_input_review_username_1ff941b8-0126-44e3-9e7e-2071074e5392">Use your name: <span class="form-input-error yotpo-hidden" id="yotpo_input_review_username_error_1ff941b8-0126-44e3-9e7e-2071074e5392"></span></label> <input id="yotpo_input_review_username_1ff941b8-0126-44e3-9e7e-2071074e5392" class="y-input" autocomplete="nickname" name="display_name" maxlength="40" aria-required="true" placeholder="" aria-describedby="yotpo_input_review_username_error_1ff941b8-0126-44e3-9e7e-2071074e5392"> </div> <div class="form-element email-input visible" style="display: inherit;"> <span class="yotpo-mandatory-mark">* </span> <label class="y-label" for="yotpo_input_review_email_1ff941b8-0126-44e3-9e7e-2071074e5392">Email: <span class="form-input-error yotpo-hidden" id="yotpo_input_review_email_error_1ff941b8-0126-44e3-9e7e-2071074e5392"></span></label> <input id="yotpo_input_review_email_1ff941b8-0126-44e3-9e7e-2071074e5392" class="y-input" autocomplete="email" name="email" aria-required="true" placeholder="" aria-describedby="yotpo_input_review_email_error_1ff941b8-0126-44e3-9e7e-2071074e5392"> </div> <div class="yotpo-clr"></div> </div> </div>   <div class="error-box yotpo-hidden"> <div class="text-wrapper"> <span class="error-text empty yotpo-hidden">Review's title &amp; body can't be empty</span>
<span class="error-text empty_question yotpo-hidden">Question's body can't be empty</span>
<span class="error-text score yotpo-hidden">Please enter a star rating for this review</span>
<span class="error-text display_name_empty yotpo-hidden">Name field cannot be empty</span>
<span class="error-text email yotpo-hidden">Invalid email</span>
<span class="error-text user-already-reviewed yotpo-hidden">Your review has already been submitted.</span>
<span class="error-text max_length yotpo-hidden">Max length was exceeded</span>
<span class="error-text mandatory_field yotpo-hidden">Please fill out all of the mandatory (*) fields</span>
<span class="error-text open_question_answer_length yotpo-hidden">One or more of your answers does not meet the required criteria</span>

 </div> <div class="yotpo-icon-btn-small transparent-color-btn"><span class="yotpo-icon yotpo-icon-cross" role="button" tabindex="0" aria-label="close error message"></span></div> </div>  <div class="form-element submit-button"> <span class="form-input-error yotpo-hidden"></span> <input type="button" class="yotpo-default-button primary-color-btn yotpo-submit" aria-disabled="true" data-button-type="submit" value="Post"> </div>  <div class="yotpo-preloader-wrapper">
    <div class="yotpo yotpo-pre-loader">
		<span class="yotpo-empty-stars">
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
		</span>

		<span class="yotpo-full-stars">
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
		</span>
    </div>
</div> <div class="yotpo-clr"></div> </div> </div> </form> <div class="yotpo-messages"> <div class="yotpo-thank-you yotpo-hidden" data-type="share" aria-label="Thank you for posting a review" tabindex="-1"> <div class="yotpo-icon-btn transparent-color-btn"><span class="yotpo-icon yotpo-icon-cross" role="button" tabindex="0"></span></div> <div class="yotpo-thankyou-header text-3xl"> <span class="yotpo-icon yotpo-icon-heart"></span> <span>Thank you for posting a review!</span> </div>  <div class="yotpo-thankyou-content"> <span>We value your input. Share your review so everyone else can enjoy it too.</span> </div> <div class="yotpo-thankyou-footer" role="list">  <div class="yotpo-default-button yotpo-icon-btn" role="list-item"> <a class="social-link popup-link" href="#" target="_blank" data-network="facebook"> <span class="yotpo-icon yotpo-icon-facebook"></span> <span class="yotpo-icon-button-text" aria-label="share the review on facebook">share</span> </a> </div>  <div class="yotpo-default-button yotpo-icon-btn" role="list-item"> <a class="social-link popup-link" href="#" target="_blank" data-network="twitter"> <span class="yotpo-icon yotpo-icon-twitter"></span> <span class="yotpo-icon-button-text" aria-label="share the review on twitter">share</span> </a> </div>  <div class="yotpo-default-button yotpo-icon-btn" role="list-item"> <a class="social-link popup-link" href="#" target="_blank" data-network="linkedin"> <span class="yotpo-icon yotpo-icon-linkedin"></span> <span class="yotpo-icon-button-text" aria-label="share the review on linkedin">share</span> </a> </div>  </div>  </div> <div class="yotpo-thank-you yotpo-hidden" data-type="pending-for-review-approval"> <div class="yotpo-icon-btn transparent-color-btn"><span class="yotpo-icon yotpo-icon-cross" role="button" tabindex="0"></span></div> <div class="yotpo-thankyou-header text-3xl"> <span class="yotpo-icon yotpo-icon-heart"></span> <span>Thank you for posting a review!</span> </div> <div class="yotpo-thankyou-content"> <span>Your review was sent successfully and is now waiting for our staff to publish it.</span> </div> </div> </div>   <div class="new-yotpo-small-box reviews yotpo-hidden"> <div class="yotpo-nav yotpo-nav-primary"> <ul role="tablist">      <li class="yotpo-nav-tab yotpo-active" data-type="reviews" data-content="yotpo-reviews-4a1d7f37-6095-46ff-92f8-51d7e298e9a7 yotpo-reviews-header-4a1d7f37-6095-46ff-92f8-51d7e298e9a7" aria-controls="yotpo-reviews-4a1d7f37-6095-46ff-92f8-51d7e298e9a7 yotpo-reviews-header-4a1d7f37-6095-46ff-92f8-51d7e298e9a7" role="tab" tabindex="0" aria-selected="true"> <div class="yotpo-nav-wrapper"> <span>REVIEWS</span>  </div> </li>   </ul>     <span class="mobile-clear-filters-btn yotpo-hidden">Clear All</span>  <div class="yotpo-clr"></div> </div> </div> <div class="yotpo-nav-content">     <div class="search-in-progress"> <div class="search-in-progress-text font-color-gray" role="status" aria-live="polite"> Updating Results </div> <div class="yotpo-spinner">
    <div class="sk-spinner sk-spinner-three-bounce">
        <div class="sk-bounce1"></div>
        <div class="sk-bounce2"></div>
        <div class="sk-bounce3"></div>
    </div>
</div>
 </div> <div class="yotpo-reviews yotpo-active" id="yotpo-reviews-4a1d7f37-6095-46ff-92f8-51d7e298e9a7" data-host-widget="main_widget" role="tabpanel">  <div class="yotpo-preloader-wrapper">
    <div class="yotpo yotpo-pre-loader">
		<span class="yotpo-empty-stars">
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
			<span class="yotpo-icon yotpo-icon-empty-star"></span>
		</span>

		<span class="yotpo-full-stars">
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
			<span class="yotpo-icon yotpo-icon-star"></span>
		</span>
    </div>
</div>   <div class="total-reviews-search" total-reviews-search="0"></div>          <div class="yotpo-first-review"> <div class="yotpo-first-review-stars"> <span class="stars-wrapper"> <span class="yotpo-icon yotpo-icon-star"></span> <span class="yotpo-icon yotpo-icon-star"></span> <span class="yotpo-icon yotpo-icon-star"></span> <span class="yotpo-icon yotpo-icon-star"></span> <span class="yotpo-icon yotpo-icon-star"></span> </span> </div> <div class="yotpo-first-review-content">  <button type="button" class="yotpo-default-button write-review-button write-first-review-button" tabindex="0" fdprocessedid="rmp96c">be the first to write a review</button>  </div> </div>    </div>   </div>  </div></div>
			</div>
		</div>
		
		<div class="surver-product-bottom-right">
			<div class="attributes">
		</div>
		</div>
	</div>
```

**URL**: https://sensiseeds.us/autoflowering-seeds/sweet-sour-cream/

---

## Attitude

**Sample HTML**:
```html
<div id="tabDesc" class="infoTab" style="">
                            <p><u><strong>Hashchis Berry AKA Cheese Berry&nbsp;</strong></u><u><strong>Feminized Marujuana Seeds from 00 Seedbank</strong></u><br>
<br>
00 Seed Bank Hashchis Berry AKA Cheese Berry are Feminized cannabis seeds, which were crossed with British home Cheese genetic and a selection of the Blueberry strain. The taste and flavour is exquisite. This strain also provides you with big yields. (formerly Cheese Berry) <br>
<br>
Indoor:<br>
Yield: 450 - 550 gr/m2<br>
Flowering period: 55 - 60 days<br>
Height: 80 - 100 cm<br>
<br>
Outdoor:<br>
Flowering period: End of October<br>
Height: 200 - 300 cm<br>
THC: 19%<br>
</p>
<p><br>
</p>
                                <p class="prodDisc">
                                    Please Note: This content is for informational and educational use only. The Attitude Seed bank sells all seeds strictly for souvenir purposes or for
                                    storage and preservation of genetics in case the laws may change. We do not condone or encourage the germination of cannabis seeds and we will refuse
                                    a sale to anyone who leads us to believe they intend to use our products in an unlawful way.
                                    <br>
                                    WARNING: IT IS A CRIMINAL OFFENCE TO GERMINATE CANNABIS SEEDS IN THE UK AND MANY OTHER COUNTRIES.
                                </p>
                        </div>
```

**URL**: https://www.cannabis-seeds-bank.co.uk/00-seeds-hashchis-berry-aka-cheese-berry/prod_3429

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
