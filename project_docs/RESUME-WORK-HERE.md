# 🚀 RESUME WORK HERE

**Last Session:** October 29, 2025  
**Status:** PAUSED - Investigation Required

---

## ⚡ Quick Start (30 seconds)

```bash
cd /home/miichael/Code/maja-explosiv
npm run build  # Verify everything still works
```

**Expected:** ✅ Success, 55 files generated

---

## 🎯 What You Need to Do Next

### PRIORITY: Investigate Missing Project "Breath under Water" (UID 982)

**The Problem:**
- You said there should be 8 paintings projects (3 murals + 5 paper work)
- We only found 7 projects
- Missing: "Breath under Water" - page exists but has no content in database

**Your Task:**
Investigate where the content is by combining:
- **Option A:** Check other database tables
- **Option D:** Check website files in `old/` directory

### Quick Investigation Commands

```bash
# Search website files for "breath" or "whale"
find old/ -type f -name "*breath*" -o -name "*whale*" 2>/dev/null

# Search file contents
grep -r "Breath under Water" old/ 2>/dev/null | head -20

# Check database for UID 982 in other tables
grep -a "982" old/usr_p51487_2.sql | grep -v "INSERT INTO \`pages\`" | head -20
```

---

## 📚 Full Documentation

Read in this order:

1. **`SESSION-2025-10-29-SUMMARY.md`** - What was done, what's next (5 min read)
2. **`typo3-technical-findings.md`** - Complete technical details (15 min read)
3. **`encoding-fix-summary.md`** - Encoding fix details (3 min read)

---

## ✅ What Was Completed

- ✅ Character encoding issue RESOLVED
- ✅ 70 projects extracted (7 paintings, 28 sculptures, 26 installations, 9 performance)
- ✅ German characters display correctly (Käthe, Zürich, etc.)
- ✅ Test migration of 20 projects
- ✅ Build succeeds without errors

---

## ⏳ What's Pending

- 🔍 Investigate missing "Breath under Water" project
- ⏳ Image extraction
- ⏳ Full migration (remaining 50 projects)

---

## 🤔 Questions to Answer

1. Where is the content for "Breath under Water"?
2. Is it actually a painting/paper work project? (mentions "whale sculpture")
3. Should it be included in the migration?

---

## 📞 Need Help?

All details are in:
- `project_docs/SESSION-2025-10-29-SUMMARY.md`
- `project_docs/typo3-technical-findings.md` (see "How to Resume This Work" section)

---

**Ready to continue?** Start with the investigation commands above! 🚀

