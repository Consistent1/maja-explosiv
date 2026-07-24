# Quick Reference: Gallery Images for Migration

**Last Updated:** December 28, 2025  
**Source:** DAM & RG Smooth Gallery investigation  
**Status:** VALIDATED ✅

---

## Critical Information

**USE THIS FILE:** `project_docs/gallery-images-configured.json`

**Total Images to Migrate:** 99 images (not ~1,500 from filesystem)

**DO NOT** import all images from project directories - that includes unused images!

---

## Painting Projects & Images

### 1. Wohlgroth (10 images)
**Page ID:** 919  
**DAM Folder:** 10  
**Path:** `fileadmin/s-maj/images/BilderMaja/1994muralsFassaden/1993Wohlgroth/`

```
Wohl.jpg
wohl1.jpg
wohl2.jpg
wohl3.jpg
wohl4.jpg
wohl5.jpg
wohl6.jpg
WohlgrothOli1.jpg
WohlgrothOli2.jpg
spritzen3.jpg
```

### 2. Felix und Regula (18 images)
**Page ID:** 918  
**DAM Folder:** 18  
**Path:** `fileadmin/s-maj/images/BilderMaja/1994muralsFassaden/1994FelixRegula/`

```
f1.jpg, f11.jpg, f12.jpg, f2.jpg, f3.jpg, f4.jpg, f5.jpg, f6.jpg, f7.jpg, f8.jpg, f9.jpg
fr_detail1.jpg, fr_detail2.jpg, fr_gesamt.jpg, fr_gesamt2.jpg, fr_gesamt3.jpg
fr_klein.jpg, fr_rechts.jpg
```

### 3. Murals Europe (12 images)
**Page ID:** 866  
**DAM Folder:** 12  
**Path:** `fileadmin/s-maj/images/BilderMaja/1994muralsFassaden/199495MuralsTravel/`

```
KavkovaPrag.jpg
KavkovaPrag2.jpg
KleineaHaifischBarBerlin.jpg
KoepiBerlin.jpg
Kvu2.jpg
Mai1995.jpg
Murals1.jpg
Sonja1.jpg
T-Port.jpg
T-Port2.jpg
bauwagen.jpg
bauwagen2.jpg
```

### 4. Akwa (9 images)
**Page ID:** 921  
**DAM Folder:** 7  
**Path:** `fileadmin/s-maj/images/BilderMaja/2005Akwa/`

```
1.page6.jpg
1page.jpg
Akwa1.jpg
Akwa2.jpg
Akwa3.jpg
krebs2_1layer.jpg
krebs31layer.jpg
krebs4.jpg
page2.jpg
```

### 5. Malaga la Vache (17 images)
**Page ID:** 922  
**DAM Folder:** 15  
**Path:** `fileadmin/s-maj/images/BilderMaja/2005Malaga/`

```
Monalisa.jpg
Scetch2.jpg
camping1.jpg
campingcolori.jpg
gDance.jpg
gDance2.jpg
geatDance.jpg
mlv1.jpg
mlv2.jpg
mlvRainbow.jpg
mlvRainbow2.jpg
mlvscetch1.jpg
mlvvache1.jpg
mlvvache2.jpg
sketchColo2.jpg
vache5.jpg
vache6.jpg
```

### 6. Graphical Work (33 images)
**Page ID:** 920  
**DAM Folder:** 18  
**Path:** `fileadmin/s-maj/images/BilderMaja/`

```
Alchemybar2.jpg
Figure1_1.jpg
Figure1_forest.jpg
Figure1_rail.jpg
Figure1_sky.jpg
Figure2.jpg
Figure3.jpg
Figure5.jpg
angel1.jpg
angel2.jpg
blondi.jpg
dorf_4.jpg
euro_1.jpg
euro_2.jpg
figure4.jpg
grafic_frau1.jpg
grafic_frau2.jpg
grafic_frau3.jpg
insel1.jpg
insel3.jpg
insel4.jpg
insel5.jpg
insel_Stu.jpg
mann2.jpg
red_blue.jpg
rot_blau.jpg
schiff1.jpg
schiff_2.jpg
stern1.jpg
turm_2.jpg
ursula1.jpg
ursula2.jpg
waiting1.jpg
```

---

## How to Use This Data

### In Python Scripts:
```python
import json

# Load the definitive image list
with open('project_docs/gallery-images-configured.json', 'r') as f:
    gallery_images = json.load(f)

# Access images for a specific project
wohlgroth_images = gallery_images['Wohlgroth']['images']
print(f"Wohlgroth has {len(wohlgroth_images)} images")

# Copy only configured images
for project_name, project_data in gallery_images.items():
    source_path = project_data['filesystem_path']
    for image in project_data['images']:
        copy_image(source_path + image, destination)
```

### Validation:
```python
# Verify image count
total_images = sum(
    len(project['images']) 
    for project in gallery_images.values()
)
assert total_images == 99, f"Expected 99 images, got {total_images}"
```

---

## Important Notes

⚠️ **DO NOT scan filesystem directories** - they contain extra images not used on the site

✅ **USE the JSON file** - it contains ONLY images displayed in galleries

✅ **Exact count:** 99 images total across 6 projects

✅ **Validated:** Cross-referenced against DAM database, FlexForm configs, and filesystem

---

## For Quick Copy-Paste

**JSON File Location:**
```
project_docs/gallery-images-configured.json
```

**Total Count by Project:**
- Wohlgroth: 10
- Felix und Regula: 18
- Murals Europe: 12
- Akwa: 9
- Malaga la Vache: 17
- Graphical Work: 33
- **TOTAL: 99**

---

**Ready for Migration:** ✅ YES  
**Data Quality:** ✅ VALIDATED  
**Source:** DAM table + FlexForm configuration
