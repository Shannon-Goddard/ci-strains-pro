# Lineage Extraction Patterns by Seed Bank

## Template for Each Seed Bank

---

### Seed Bank Name: [FILL IN]

**Total Strains**: [FILL IN]  
**Missing Lineage**: [FILL IN]  
**Priority**: [High/Medium/Low]

#### Sample Strain for Testing
- **Strain Name**: [FILL IN]
- **Breeder**: [FILL IN]
- **S3 Key**: [FILL IN]

#### HTML Structure Analysis
```
[PASTE RELEVANT HTML SNIPPET SHOWING LINEAGE DATA]
```

#### Extraction Pattern
**Method**: [table / meta / div / span / paragraph]  
**CSS Selector**: [FILL IN]  
**Regex Pattern**: [FILL IN]  
**Parent 1 Location**: [FILL IN]  
**Parent 2 Location**: [FILL IN]

#### Special Cases
- [Any unique formatting, nested crosses, or edge cases]

#### Test Results
- **Tested**: [Yes/No]
- **Success Rate**: [X/Y strains]
- **Notes**: [Any issues or observations]

---

## Extraction Priority by Seed Bank

| Seed Bank | Total Strains | Missing Lineage | Priority | Status |
|-----------|---------------|-----------------|----------|--------|
| Attitude Seed Bank | 7,673 | TBD | High | 📋 Pending |
| Crop King | 3,336 | TBD | High | 📋 Pending |
| North Atlantic | 2,727 | TBD | High | 📋 Pending |
| Gorilla Seed Bank | 2,009 | TBD | Medium | 📋 Pending |
| Neptune | 1,995 | TBD | Medium | 📋 Pending |
| Multiverse Beans | 799 | N/A | NONE | Unchanged |
| Herbies Seeds | 753 | TBD | Medium | 📋 Pending |
| Sensi Seeds | 620 | TBD | Medium | 📋 Pending |
| Seed Supreme | 353 | N/A | NONE | Unchanged |
| Mephisto Genetics | 245 | TBD | Low | 📋 Pending |
| Exotic Genetix | 227 | TBD | Low | 📋 Pending |
| Amsterdam Marijuana | 163 | N/A | NONE | Unchanged |
| Barney's Farm | 88 | TBD | Low | 📋 Pending |
| Royal Queen Seeds | 67 | TBD | Low | 📋 Pending |
| Dutch Passion | 44 | TBD | Low | 📋 Pending |
| Seeds Here Now | 43 | TBD | Low | 📋 Pending |
| ILGM | 133 | TBD | Low | 📋 Pending |
| Great Lakes Genetics | 16 | TBD | Low | 📋 Pending |
| Seedsman | 866 | TBD | Medium | 📋 Pending |

---

## Pattern Examples from Phase 6 (Breeder Extraction)

### Example: Attitude Seed Bank
```python
# Table-based extraction
soup.find('table', class_='product-info')
row = soup.find('td', string=re.compile('Genetics'))
value = row.find_next_sibling('td').get_text()
```

### Example: Crop King
```python
# Div-based extraction
soup.find('div', class_='lineage-info')
parents = div.find_all('span', class_='parent-name')
```

### Example: Meta Tag
```python
# Meta description extraction
meta = soup.find('meta', attrs={'name': 'description'})
content = meta.get('content')
match = re.search(r'cross of ([^x]+) x ([^.]+)', content)
```

---

## Fill Out Instructions

1. **Run analysis script** to get missing lineage counts per seed bank
2. **For each seed bank** (start with High priority):
   - Copy template above
   - Fetch sample HTML from S3
   - Paste relevant HTML snippet
   - Identify extraction pattern
   - Fill in CSS selector and regex
   - Test on 5-10 strains
   - Document success rate

3. **Once patterns documented**, I'll build the extraction script

---

## Notes
- Focus on **parent_1** and **parent_2** extraction first
- Grandparents can be parsed from nested crosses later
- Generation markers (F1/S1/BX1) are bonus if easily available
- Prioritize seed banks with most missing lineage

### Attitude Seed Bank
```html
# example from url: https://www.cannabis-seeds-bank.co.uk/archive-seeds-zwoosh/prod_9996
# Genetic information is "Zkittlez x Oishii"

<div id="tabChar" class="prodCharTab infoTab" style="">
   <ul>
      <li>Genetics: <span>Zkittlez x Oishii </span></li>
      <li>Sex: <span>Regular</span></li>
      <li>Flowering: <span>Photoperiod</span></li>
      <li>Type: <span>Indica/Sativa</span></li>
      <li>Flowering Time: <span>50 days</span></li>
      <li>Area: <span>Indoor &amp; Outdoor</span></li>
   </ul>
</div>
```
### Barney's Farm Seed Bank
```html
# example from url: https://www.barneysfarm.com/us/mimosa-evo-weed-strain-510
# Genetic information is "Mimosa Strain x Orange Punch Strain"

<table cellspacing="0" cellpadding="0" class="strain-info-table active">
<tbody><tr>
<td>
<span><img src="/us/images/product-icons/genetics.svg" alt="Genetics" class="genetics"></span>
				                  Genetics				                </td>
<td>
				                  Mimosa Strain x Orange Punch Strain				                </td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/thc.svg" alt="THC Content"></span>
				                  THC %
</td>
<td>30%</td>
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
<td>Tropical Lemon, Orange Citrus with Hints of Berries</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/effect.svg" alt="Effect"></span>
				                  Effect				                </td>
<td>Happy,  Uplifted,</td>
</tr>
<tr>
<td>
<span><img src="/us/images/product-icons/aroma.svg" alt="Aroma"></span>
				                  Aroma				                </td>
<td>Fruit Punch &amp; Citrus Tangerine Aroma</td>
</tr>
</tbody></table>
```
### Crop King Seed Bank
```html
# example from url: https://www.cropkingseeds.com/feminized-seeds/white-wedding-strain-feminized-marijuana-seeds/
# Genetic information is "Wedding Cake and Girl Scout Cookies"

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
Wedding Cake and Girl Scout Cookies												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
THC Level												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
25%												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
CBD Level												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Low												</div></div>
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
8-10 weeks												</div></div>
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
September												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Indoor Yields												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
14 oz/m2												</div></div>
</td>
</tr>
<tr>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
Outdoor Yields												</div></div>
</td>
<td colspan="" rowspan="" class="" id="">
<div class="td-content-wrapper"><div class="td-content">
18 – 21 oz/plant												</div></div>
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
### Dutch Passion
```html
# example from url: https://dutch-passion.us/cannabis-seeds/sugar-bomb-punch
# Genetic information is "THC Bomb X (Critical Orange Punch x Bubba Island Kush)"

<table style="border-collapse: collapse; width: 100%; height: 622.3px;" border="1" cellpadding="3">
<tbody>
<tr style="height: 49.8px; background-color: #f4efe9;">
<th style="height: 49.8px; width: 100%;" colspan="3">
<h3 id="IGD1V8L" style="text-align: center;"></h3>
<h3 id="IGD1V8L" style="text-align: left;"><span style="font-size: 16px;">&nbsp;Sugar Bomb Punch data sheet<br></span></h3>
</th>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; height: 40px; vertical-align: middle;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/feminised-cannabis-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/feminised-cannabis-seeds.png" alt="Feminized cannabis seeds" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><strong>Strain type:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Feminized</span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/usa-special-cannabis-strains-collection.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/usa-special-cannabis-strains-collection.png" alt="USA Special cannabis strain" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Family:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">USA Special<br></span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/cannabis-genetics.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/cannabis-genetics.png" alt="Lineage" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Lineage:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">THC Bomb X (Critical Orange Punch x Bubba Island Kush)</span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/indica-cannabis-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/indica-cannabis-seeds.png" alt="Indica cannabis seeds" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Genetics:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Indica</span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/cannabis-cup-winning-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/cannabis-cup-winning-seeds.png" alt="Cannabis cup winner" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Cannabis cups:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">2x (2020, 2021)<br></span></td>
</tr>
<tr style="height: 49.5px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 49.5px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/indoor-cannabis-seeds.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/indoor-cannabis-seeds.png" alt="Grow environment" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 49.5px; text-align: left;"><span style="font-size: 14px;"><strong>Environment:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 49.5px;"><span style="font-size: 14px;">Indoor, outdoor, greenhouse</span></td>
</tr>
<tr style="height: 42.5px;">
<td style="width: 9.96593%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/plant-height.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/plant-height.png" alt="Plant height" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; text-align: left; height: 42.5px;"><span style="font-size: 14px;"><strong>Plant height:<br></strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;">Very tall<br></span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/flowering-time.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/flowering-time.png" alt="Flowering time" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Flowering time:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">9 weeks</span></td>
</tr>
<tr style="height: 42.5px;">
<td style="width: 9.96593%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/plant-yield.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/plant-yield.png" alt="Plant yield" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; text-align: left; height: 42.5px;"><span style="font-size: 14px;"><strong>Yield:<br></strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 42.5px;"><span style="font-size: 14px;">XL<br></span></td>
</tr>
<tr style="height: 38px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 38px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/thc-content.webp"><img id="CTAGNLB" style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/thc-content.png" alt="THC content" width="100%" height="100%" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; text-align: left; height: 38px;"><span style="font-size: 14px;"><strong>THC level:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 38px;"><span style="font-size: 14px;">Extremely high (&gt;20%) <br></span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/terpenes.webp"><img style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/terpenes.png" alt="Terpenes" width="20" height="20" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Terpenes:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Limonene, B-Caryophyllene, B-Myrcene, Humulene, B-Pinene<br></span></td>
</tr>
<tr style="height: 40px; background-color: #f4efe9;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/flavor-profile.webp"><img style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/flavor-profile.png" alt="Taste" width="20" height="20" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Taste:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Piney, fuel, sweet, earthy, creamy</span></td>
</tr>
<tr style="height: 40px;">
<td style="width: 9.96593%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;"><picture><source type="image/webp" srcset="https://dutch-passion.us/media/wysiwyg/data/hybrid-effect.webp"><img style="display: block; margin-left: auto; margin-right: auto; width: 20px; height: 20px;" src="/media/wysiwyg/data/hybrid-effect.png" alt="Hybrid effects" width="20" height="20" loading="lazy"></picture></span></td>
<td style="width: 39.9489%; vertical-align: middle; height: 40px; text-align: left;"><span style="font-size: 14px;"><strong>Effects:</strong></span></td>
<td style="width: 50.0852%; vertical-align: middle; height: 40px;"><span style="font-size: 14px;">Hybrid high</span></td>
</tr>
</tbody>
</table>
```
### Exotic Genetics Seed Bank
```html
# example from url: https://exoticgenetix.com/product/alpha-one-3231313/
# Genetic information is "Mother: The One", "Reversal: Grape Jubilee"
# note: Make sure that we do NOT get any of the text after <br> in <p>Reversal: Grape Jubilee<br>6 Feminized Seeds</p>

<div class="tab-content resp-tab-content resp-tab-content-active" id="tab-description" aria-labelledby="tab_item-0" style="display:block">
<h2>Description</h2>
<p>Mother: The One</p>
<p>Reversal: Grape Jubilee<br>6 Feminized Seeds</p>
</div>
```
### Gorilla Seed Bank
```html
# example from url: https://www.gorilla-cannabis-seeds.co.uk/dinafem/autoflowering/haze-automatic.html
# Genetic information is "Roadrunner (Lowryder #1 X DinaFem #1) X JYD Haze"

<table class="g-spec-table" style="width:100%; border-collapse:collapse;">
        <tbody>
                                                <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  INDOOR                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Yes                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  OUTDOOR                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Yes                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  CANNABIS GENETICS                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Roadrunner (Lowryder #1 X DinaFem #1) X JYD Haze                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  FLOWERING TIME                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Autoflowering                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  THC                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Average                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  THC NOTES                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  6 to 12%                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  HEIGHT NOTES                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  100 cm max                </td>
              </tr>
                                                            <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  FLAVOUR                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Strong                </td>
              </tr>
                                                                                                                                <tr>
                <th style="text-align:left; font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:rgba(255,255,255,.7); padding:6px 10px 6px 0; vertical-align:top;">
                  GREENHOUSE                </th>
                <td style="text-align:right; color:rgba(255,255,255,.92); padding:6px 0; vertical-align:top;">
                  Yes                </td>
              </tr>
                              </tbody>
      </table>
```
### Herbies Seed Bank
```html
# example from url: https://herbiesheadshop.com/cannabis-seeds/dozy-whale
# Genetic information is "Dozy Doz x (White Widow IBL x Haze IBL)"

<table class="properties-list clamp-table-content"> <tbody><tr class="row item__property properties-list__item" title="Strain brand"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain brand </span> </td> <td class="col-6" style="padding: 0"><a href="https://herbiesheadshop.com/producers/alphafem-seeds">AlphaFem Seeds</a></td> </tr> <tr class="row item__property properties-list__item" title="Strain Gender"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain Gender </span> </td> <td class="col-6" style="padding: 0">Feminized</td> </tr> <tr class="row item__property properties-list__item" title="Strain light cycle"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Strain light cycle </span> </td> <td class="col-6" style="padding: 0">Photoperiod</td> </tr> <tr class="row item__property properties-list__item" title="Suitable for growing"> <td class="col-6 properties-list__name"> <span class="properties-list__name-text"> Suitable for growing </span> </td> <td class="col-6" style="padding: 0">Outdoor, Indoor</td> </tr> <tr class="row item__property properties-list__item" title="thc_range"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain THC level </span> </td> <td class="col-6 value" style="padding: 0; border: none;">26%</td> </tr> <tr class="row item__property properties-list__item" title="cbd"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain CBD level </span> </td> <td class="col-6 value" style="padding: 0; border: none;">2%</td> </tr> <tr class="row item__property properties-list__item" title="sainru"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> % Sativa/ Indica/ Ruderalis </span> </td> <td class="col-6 value" style="padding: 0; border: none;">Sativa dominant</td> </tr> <tr class="row item__property properties-list__item" title="harvest"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain harvest </span> </td> <td class="col-6 value" style="padding: 0; border: none;">1.6 oz/ft² indoors<br>19.4 - 21.2 oz/plant outdoors</td> </tr> <tr class="row item__property properties-list__item" title="flow_time"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Indoor flowering time </span> </td> <td class="col-6 value" style="padding: 0; border: none;">65 - 70 days </td> </tr> <tr class="row item__property properties-list__item" title="height"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain height </span> </td> <td class="col-6 value" style="padding: 0; border: none;">59.1 - 78.7 inches indoors<br>59.1 - 78.7 inches outdoors</td> </tr> <tr class="row item__property properties-list__item" title="effect"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Strain effect </span> </td> <td class="col-6 value" style="padding: 0; border: none;">Mind-warping energy</td> </tr> <tr class="row item__property properties-list__item" title="genetic"> <td class="col-6 properties-list__name" style="border: none;"> <span class="properties-list__name-text"> Genetics </span> </td> <td class="col-6 value" style="padding: 0; border: none;">Dozy Doz x (White Widow IBL x Haze IBL)</td> </tr> </tbody></table>
```
### Mephisto Genetics Seed Bank
```html
# example from url: https://mephistogenetics.com/products/zo-raven
# Genetic information is "Do-si-delirium x Ravenberry", "F1"

<div class="w-layout-grid grid">
                  
                  <div id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430ef-d7b2c481" class="text-weight-bold">Genetic Heritage</div>
                  <div id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f1-d7b2c481">Do-si-delirium x Ravenberry</div>
                  
                  
                    <div id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f3-d7b2c481" class="text-weight-bold">Seed Type</div>
                    <div id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f5-d7b2c481">F1 Feminised Automatic</div>
                  
                </div>
```
### Neptune Seed Bank
```html
# example from url: https://neptuneseedbank.com/product/nasha-genetics-zz-bang
# Genetic information is "Jokerz #31 x Zoap"

<div class="woocommerce-product-details__short-description">
                            <h3>Nasha Genetics – ZZ Bang</h3>
<p><strong></strong><br>
<strong>Lineage:</strong> Jokerz #31 x Zoap<br>
<strong>Seeds Per Pack:</strong> 10<br>
<strong>Sex:</strong> (F)</p>
                        </div>
```
### North Atlantic
```html
# example from url: https://www.northatlanticseed.com/product/zweet-inzanity-rBX-f/
# Genetic information is "Zweet Inzanity #22 x Durban Poison"

<div class="product-specifications">
        <h2 class="section-heading">Specifications</h2>
        <div class="specs-grid">
            <div class="spec-item"><i class="fas fa-cubes"></i><dl><dt class="spec-label">Pack Size</dt><dd class="spec-value">5 pack, 10 pack</dd></dl></div><div class="spec-item"><i class="fas fa-dna"></i><dl><dt class="spec-label">Genetics</dt><dd class="spec-value">Zweet Inzanity #22 x Durban Poison</dd></dl></div><div class="spec-item"><i class="fas fa-venus"></i><dl><dt class="spec-label">Seed Type</dt><dd class="spec-value">Feminized</dd></dl></div><div class="spec-item"><i class="fas fa-sun"></i><dl><dt class="spec-label">Growth Type</dt><dd class="spec-value">Photoperiod</dd></dl></div><div class="spec-item"><i class="fas fa-clock"></i><dl><dt class="spec-label">Flowering Time</dt><dd class="spec-value">60 - 70 days</dd></dl></div><div class="spec-item"><i class="fas fa-wheat-awn"></i><dl><dt class="spec-label">Yield</dt><dd class="spec-value">Very High</dd></dl></div><div class="spec-item"><i class="fas fa-flask"></i><dl><dt class="spec-label">Terpene Profile</dt><dd class="spec-value">Powdered Sugar, Sweet Citrus, Sour Gasoline</dd></dl></div>        </div>
    </div>
```
### Royal Queen Seed Bank
```html
# example from url: https://www.royalqueenseeds.com/us/autoflowering-cannabis-seeds/657-trainwreck-automatic.html
# Genetic information is "Trainwreck x Big Skunk Auto"

<h2 class="h5 product-keywords">Trainwreck x Big Skunk Auto</h2>
```
### Seeds Here Now Seed Bank
```html
# example from url: https://seedsherenow.com/shop/island-punch-autoflower-cali-connection/
# Genetic information is "Reversed"

<table>
<tbody><tr>
<th>Breeder</th>
<td><a href="https://seedsherenow.com/product-category/cannabis-seed-breeders/cali-connection/" target="_blank" rel="noopener" title="Cali Connection">Cali Connection</a></td>
</tr>
<tr>
<th>Island Punch Auto</th>
<td>Island Punch Auto</td>
</tr>
<tr>
<th>Genetics</th>
<td>Reversed</td>
</tr>
<tr>
<th>Seed Type</th>
<td><a href="https://seedsherenow.com/product-category/autoflower-cannabis-seeds/" target="_blank" rel="noopener" title="Autoflower Seeds">Autoflower</a></td>
</tr>
<tr>
<th>Island Punch Auto Type</th>
<td><a href="https://seedsherenow.com/product-category/sativa-dominant/" target="_blank" rel="noopener" title="Sativa-dominant hybrid">Sativa-dominant hybrid</a></td>
</tr>
<tr>
<th>THC</th>
<td><a href="https://www.whtcla.com/blog/what-is-thc-lets-talk-tetrahydrocannabinol/" target="_blank" rel="noopener" title="22% to 26%">18% to 22%</a></td>
</tr>
<tr>
<th>CBD</th>
<td><a href="https://seedsherenow.com/product-category/high-cbd/" target="_blank" rel="noopener">1%</a></td>
</tr>
<tr>
<th>Flowering Time</th>
<td>7 to 9 weeks</td>
</tr>
<tr>
<th>Yield</th>
<td>Average</td>
</tr>
<tr>
<th>Difficulty</th>
<td><a href="https://seedsherenow.com/how-to-grow-cannabis-a-complete-guide/" target="_blank" rel="noopener" title="Intermediate">Intermediate</a></td>
</tr>
<tr>
<th>Aroma / Flavor</th>
<td>Tropical, citrus, fruity, sweet, pine</td>
</tr>
<tr>
<th>Effects</th>
<td>Tropical, euphoric, uplifting, relaxing, happy, creative</td>
</tr>
<tr>
<th>Pack Size</th>
<td>[6pk]</td>
</tr>
</tbody></table>
```
### Attitude Seed Bank
```html
# example from url: https://www.cannabis-seeds-bank.co.uk/archive-seeds-zwoosh/prod_9996
# Genetic information is "Zkittlez x Oishii"

<div id="tabChar" class="prodCharTab infoTab" style="">
   <ul>
      <li>Genetics: <span>Zkittlez x Oishii </span></li>
      <li>Sex: <span>Regular</span></li>
      <li>Flowering: <span>Photoperiod</span></li>
      <li>Type: <span>Indica/Sativa</span></li>
      <li>Flowering Time: <span>50 days</span></li>
      <li>Area: <span>Indoor &amp; Outdoor</span></li>
   </ul>
</div>
```
### Attitude Seed Bank
```html
# example from url: https://www.cannabis-seeds-bank.co.uk/archive-seeds-zwoosh/prod_9996
# Genetic information is "Zkittlez x Oishii"

<div id="tabChar" class="prodCharTab infoTab" style="">
   <ul>
      <li>Genetics: <span>Zkittlez x Oishii </span></li>
      <li>Sex: <span>Regular</span></li>
      <li>Flowering: <span>Photoperiod</span></li>
      <li>Type: <span>Indica/Sativa</span></li>
      <li>Flowering Time: <span>50 days</span></li>
      <li>Area: <span>Indoor &amp; Outdoor</span></li>
   </ul>
</div>
```
### Seedsman Seed Bank
```html
# example from url: https://www.seedsman.com/us-en/shiskaberry-feminised-seeds-bfsshkb-fem
# Genetic information is "Blueberry x Afghan"

<table id="product-attribute-specs-table" class="data table additional-attributes"><tbody><tr><th scope="row" class="col label"><h4>SKU</h4></th><td data-th="SKU" class="col data"><h3>BFSSHKB-Fem</h3></td></tr><tr><th scope="row" class="col label"><h4>Brand/breeder</h4></th><td data-th="Brand/breeder" class="col data"><h3><span><a href="https://www.seedsman.com/us-en/cannabis-seed-breeders/barney-s-farm" title="Barney's Farm" target="_self">Barney's Farm</a></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Parental lines</h4></th><td data-th="Parental lines" class="col data"><h3>Blueberry x Afghan</h3></td></tr><tr><th scope="row" class="col label"><h4>Variety</h4></th><td data-th="Variety" class="col data"><h3><span>Indica dominant</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Flowering type</h4></th><td data-th="Flowering type" class="col data"><h3><span>Photoperiod</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Sex</h4></th><td data-th="Sex" class="col data"><h3><span>Feminised</span></h3></td></tr><tr><th scope="row" class="col label"><h4>THC content</h4></th><td data-th="THC content" class="col data"><h3><span>Very High THC (25%+)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>CBD content</h4></th><td data-th="CBD content" class="col data"><h3><span>Low CBD (0-1%)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Yield outdoor</h4></th><td data-th="Yield outdoor" class="col data"><h3><span>Very High Yield (above 750gr/plant)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Yield indoor</h4></th><td data-th="Yield indoor" class="col data"><h3><span>High Yield (450-600gr/m2)</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Plant size</h4></th><td data-th="Plant size" class="col data"><h3><span>Medium</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Photoperiod flowering time</h4></th><td data-th="Photoperiod flowering time" class="col data"><h3><span>7 to 9 weeks</span></h3></td></tr><tr><th scope="row" class="col label"><h4>Northern hemisphere harvest</h4></th><td data-th="Northern hemisphere harvest" class="col data"><h3><span><span>September</span></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Suitable climates</h4></th><td data-th="Suitable climates" class="col data"><h3><span><span>Cool</span></span><span><span> | Dry</span></span><span><span> | High altitude</span></span><span><span> | Hot</span></span><span><span> | Temperate</span></span><span><span> | Warm</span></span></h3></td></tr><tr><th scope="row" class="col label"><h4>Aroma</h4></th><td data-th="Aroma" class="col data"><h3><span><span>Earthy</span></span><span><span> | Spicy</span></span></h3></td></tr></tbody></table>
```
### ILGM Seed Bank
```html
# example from url: https://ilgm.com/products/jack-herer-feminized-seeds
# Genetic information is "Haze, Northern Lights #5, and Shiva Skunk"

<table><tbody><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Plant Type</td><td class="p-0 text-right text-sm">Photoperiod, Sativa, Feminized</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Genotype</td><td class="p-0 text-right text-sm">Sativa Dominant</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Lineage</td><td class="p-0 text-right text-sm">Haze, Northern Lights #5, and Shiva Skunk</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Effects</td><td class="p-0 text-right text-sm">Creative, Energetic, Uplifted</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Yield Potential</td><td class="p-0 text-right text-sm">510 gr/m²</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Taste and Aroma</td><td class="p-0 text-right text-sm">Citrus, Earthy, Herbal, Pine, Spicy, Woody</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">THC Level</td><td class="p-0 text-right text-sm">High</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">THC Percentage</td><td class="p-0 text-right text-sm">23</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBD Level</td><td class="p-0 text-right text-sm">Low</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBD Percentage</td><td class="p-0 text-right text-sm">0</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBG Level</td><td class="p-0 text-right text-sm">Low</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">CBG Percentage</td><td class="p-0 text-right text-sm">0</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Difficulty</td><td class="p-0 text-right text-sm">Beginner</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Climate</td><td class="p-0 text-right text-sm">Outdoor, Indoor, Sunny, Continental, Mediterranean</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Terpenes</td><td class="p-0 text-right text-sm">Caryophyllene, Pinene, Terpinolene</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Bud Structure</td><td class="p-0 text-right text-sm">Medium Density, Medium Size, Large Size, Elongated</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Optimal Growing Temperature</td><td class="p-0 text-right text-sm">65-80°F</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Optimal Humidity Level</td><td class="p-0 text-right text-sm">55-65%</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Flowering Time Indoor</td><td class="p-0 text-right text-sm">63 days</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Flowering Time Outdoor</td><td class="p-0 text-right text-sm">Mid to late October</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Vegetative Stage</td><td class="p-0 text-right text-sm">56 days</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Harvest Height</td><td class="p-0 text-right text-sm">Tall</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Resilience</td><td class="p-0 text-right text-sm">Diseases</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Original Genetics Developed By</td><td class="p-0 text-right text-sm">Sensi Seeds</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">Brand</td><td class="p-0 text-right text-sm">ILGM</td></tr><tr class="flex justify-between gap-10 p-4 even:bg-gray-100"><td class="p-0 text-sm font-bold">SKU</td><td class="p-0 text-right text-sm">ILG-JCK-FP</td></tr></tbody></table>
```