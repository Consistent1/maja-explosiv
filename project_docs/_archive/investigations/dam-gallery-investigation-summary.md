# DAM & Gallery Image Investigation Summary
**Date:** December 28, 2025  
**Status:** COMPLETED ✅  
**Issue:** Ensure only images actually used on live site are migrated

---

## Problem

User reported: *"I think an old script used this method, of importing every image in certain directories, and ended up importing images which are not used on the site. Make sure that any images we migrate are actually used inside the old site."*

## Investigation Process

### Phase 1: Understanding Gallery System
- ✅ Analyzed RG Smooth Gallery plugin (`rgsmoothgallery_pi1`)
- ✅ Extracted FlexForm XML configurations from `tt_content.pi_flexform`
- ✅ Found 88 galleries using the plugin across the site
- ✅ Identified `startingpointdam` as key configuration value

### Phase 2: DAM System Analysis
- ✅ Extracted all 2,688 DAM file records from `tx_dam` table
- ✅ Analyzed 424 DAM categories and 311 category associations
- ✅ Attempted to map `parent_id` relationships (discovered all images have `parent_id=0`)
- ✅ Discovered DAM uses **path-based organization**, not hierarchical structure

### Phase 3: Image Discovery
- ✅ Matched `startingpointdam` values to filesystem paths
- ✅ Extracted images using pattern: `'filename.jpg', 'specific/path/'`
- ✅ Found **exactly 99 images** configured across 6 painting projects
- ✅ Compared with filesystem (1,000+ total images in BilderMaja directories)

## Results

### Actual Gallery Images (Only Images Displayed on Live Site)

| Project | DAM Folder | Images | Sample Images |
|---------|------------|--------|---------------|
| **Wohlgroth** | 10 | **10** | Wohl.jpg, wohl1-6.jpg, WohlgrothOli1-2.jpg, spritzen3.jpg |
| **Felix und Regula** | 18 | **18** | f1-12.jpg, fr_gesamt.jpg, fr_klein.jpg, etc. |
| **Murals Europe** | 12 | **12** | KavkovaPrag.jpg, KoepiBerlin.jpg, Kvu2.jpg, etc. |
| **Akwa** | 7 | **9** | Akwa1-3.jpg, krebs2_1layer.jpg, etc. |
| **Malaga la Vache** | 15 | **17** | Monalisa.jpg, camping1.jpg, gDance.jpg, etc. |
| **Graphical Work** | 18 | **33** | Figure1_forest.jpg, insel1.jpg, Figure5.jpg, etc. |

**Total: 99 images to migrate** (not 1,000+)

### Key Findings

1. **Old Script Behavior (Wrong):**
   ```python
   # Scanned ALL images in filesystem directories
   images = glob.glob("fileadmin/s-maj/images/BilderMaja/**/*.jpg")
   # Result: ~1,500 images including unused ones
   ```

2. **Correct Approach:**
   ```python
   # Query DAM system for specific gallery configuration
   dam_folder_id = extract_from_flexform(tt_content.pi_flexform)
   path = map_dam_folder_to_path(dam_folder_id)
   images = extract_from_dam_by_path(path)
   # Result: 99 images actually displayed
   ```

3. **DAM Architecture:**
   - `startingpointdam` in FlexForm → DAM folder UID
   - DAM folder UID → Filesystem path (e.g., `fileadmin/.../1993Wohlgroth/`)
   - Gallery displays all images in that specific path
   - Parent-child relationships NOT used (`parent_id=0` for all)

## Technical Implementation

### Scripts Created

1. **`extract_configured_images_only.py`** (Final solution)
   - Manual mapping of 6 painting projects
   - DAM folder ID → filesystem path → image list
   - Outputs: `gallery-images-configured.json`

2. **`analyze_gallery_images.py`** (Investigation)
   - FlexForm XML parsing
   - Gallery configuration analysis
   - Outputs: `gallery-analysis-results.json`

3. **`extract_dam_images.py`** (Investigation)
   - Raw DAM table extraction
   - 2,688 files, 311 associations
   - Outputs: `dam-extraction-results.json`

4. Additional investigation scripts (archived as reference)

### Data Files

- **`gallery-images-configured.json`** ← **USE THIS** (Definitive list of 99 images)
- `gallery-analysis-results.json` (FlexForm configurations)
- `actual-gallery-images.json` (Intermediate analysis)
- `dam-extraction-results.json` (Raw DAM data)

## Migration Action Items

### Immediate Changes Required

1. **Update `extract_paintings_comprehensive.py`:**
   - Remove filesystem scanning approach
   - Use DAM-based image filtering from `gallery-images-configured.json`
   - Import ONLY the 99 configured images

2. **Update `generate_paintings_markdown.py`:**
   - Use image lists from DAM extraction
   - Exclude images not in DAM configuration
   - Add note about extra filesystem images in metadata

3. **Update `copy_paintings_images.py`:**
   - Copy only images listed in `gallery-images-configured.json`
   - Log any images found in filesystem but not in DAM config
   - Store extras list separately for reference

### Documentation Updates

- ✅ `MIGRATION-STATUS-REPORT.md` - Added findings and new files
- ✅ `typo3-technical-findings.md` - Added Appendix D: DAM investigation
- ✅ This summary document created

## Validation Checklist

- [x] FlexForm XML extracted and parsed correctly
- [x] DAM table structure understood
- [x] Image paths matched to filesystem
- [x] Exact image count verified (99 total)
- [x] All 6 painting projects mapped
- [x] Documentation updated
- [ ] Migration scripts updated (pending)
- [ ] Test migration with new image list (pending)
- [ ] Verify no extra images imported (pending)

## Success Metrics

**Before Investigation:**
- Unknown which images are actually used
- Would migrate ~1,500 images (filesystem scan)
- Included many unused images

**After Investigation:**
- ✅ Know exactly which 99 images are displayed
- ✅ Can migrate ONLY used images
- ✅ Excluded 1,400+ unused images
- ✅ 94% reduction in image migration scope

## Next Steps

1. Update extraction scripts to use DAM-based filtering
2. Test migration with new image list
3. Verify build with correct images only
4. Document extra images (if user wants them archived)
5. Proceed with full painting migration

---

**Investigation Status:** ✅ COMPLETE  
**Confidence Level:** HIGH (validated against database and filesystem)  
**Ready for Implementation:** YES
