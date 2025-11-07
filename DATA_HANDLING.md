# Data Handling - Flexible Column Detection

The PSUR Generator now intelligently detects and adapts to different data formats and column naming conventions.

## Your Data Files

### Sales Data: `33_sales.xlsx`
**Detected Columns:**
- `Month` - Month name (January, February, etc.)
- `Calendar year` - Year (2020, 2021, etc.)
- `Quantity` - Units sold
- `Shipping Country` - Country name
- `Region` - Pre-mapped region
- Plus: ItemNumber, ItemDescription, BusinessUnit, Category, etc.

**Format:** 16,358 rows × 15 columns

### Complaints Data: `33_complaints.xlsx`
**Detected Columns:**
- `Date Entered` - Complaint date
- `Complaint Number` - Unique ID
- `Country` - Location
- `Nonconformity` - Issue type
- `Product Number`, `Description`, `Lot Number`
- Investigation and corrective action details
- Plus 30+ additional tracking columns

**Format:** 174 rows × 36 columns

## Intelligent Column Detection

### Section C & G - Sales Processing

The system automatically detects:

**Month Column** - Any column containing "month":
- `Month` ✓
- `Month Name` ✓
- `Sale Month` ✓
- Supports: Full names, abbreviations, or numbers (1-12)

**Year Column** - Any column containing "year":
- `Calendar year` ✓
- `year` ✓
- `Year` ✓
- `Fiscal Year` ✓

**Quantity Column** - Any column with "quantity" or "units":
- `Quantity` ✓
- `Units Sold` ✓
- `Units Distributed` ✓
- `Quantity Shipped` ✓

**Country/Region Column** - Prioritizes specific country columns:
- `Shipping Country` ✓ (primary)
- `Customer Country` ✓
- `Country` ✓
- `Region` ✓ (uses if no country column)

### Section G - Complaints Processing

The system automatically detects:

**Date Column** - Prioritizes date entered:
- `Date Entered` ✓ (primary)
- `CSI Notification Date` ✓
- `Date Closed` ✓
- Any column with "date" (fallback)

**Sheet Detection** - Flexible sheet handling:
- Tries `CSI Complaints` sheet first
- Falls back to first sheet if named sheet doesn't exist

## How It Works

### Example: Section C Processing

```python
# Your data columns:
# ['ItemNumber', 'Month', 'Calendar year', 'Quantity', 'Shipping Country', ...]

# System automatically maps:
Month → 'Month'
Year → 'Calendar year'
Quantity → 'Quantity'
Country → 'Shipping Country'

# Then processes:
1. Maps country to PSUR region (North America, Europe, etc.)
2. Converts month names to dates
3. Aggregates by region and period
4. Generates sales trends
```

### Example: Section G Processing

```python
# Sales data auto-detected
# Complaints data auto-detected with 'Date Entered'

# System processes:
1. Aggregates sales by month
2. Counts complaints by month
3. Calculates complaint rate (complaints/units sold)
4. Identifies UCL breaches
5. Generates trend charts
```

## Supported Data Variations

### Month Formats
```
Full names: January, February, March, ...
Abbreviations: Jan, Feb, Mar, ...
Numbers: 1, 2, 3, ... 12
```

### Year Formats
```
Full year: 2020, 2021, 2022
Any numeric year column
```

### Region Handling
```
If Country column exists:
  → Maps to PSUR regions (North America, Europe, Asia-Pacific, etc.)
  → Unmapped countries → 'Other'

If Region column exists (no country):
  → Uses existing regions

If neither exists:
  → Uses 'Global' aggregate
```

### Date Formats
```
Any Excel date format
Text dates (parsed automatically)
Multiple date columns (prioritizes 'Date Entered')
```

## What Gets Printed

When you run a section generator, you'll see:

```bash
Loading sales data from inputs/33_sales.xlsx...
  Detected columns: ['ItemNumber', 'ItemDescription', 'BusinessUnit', ...]
  Using columns: Month=Month, Year=Calendar year, Quantity=Quantity, Country=Shipping Country
  WARNING: 15 unmapped countries assigned to 'Other'
  Processed 48 periods across 8 regions
  Total units: 250,000
  Regions: ['Asia-Pacific', 'Europe', 'North America', 'Other']
```

```bash
Loading complaints data...
  Complaints columns: ['Complaint Number', 'Date Entered', 'Country', ...]
  Using date column: Date Entered
  Found 174 complaints
```

## Error Handling

### Missing Required Columns

If a required column is missing, you'll see:

```
ERROR: Required columns not found
  Need: Month column, Year column, Quantity/Units column
  Found: ['ItemNumber', 'Description', 'Value', ...]
```

### Solution: Rename Columns
Your Excel file needs at minimum:
- One column with "month" in the name
- One column with "year" in the name  
- One column with "quantity" or "units" in the name

## Country to Region Mapping

Automatically maps 150+ countries to PSUR regions:

**North America**
- United States, Canada, Mexico

**Europe**
- All EU countries, UK, Norway, Switzerland, etc.

**Asia-Pacific**
- China, Japan, South Korea, Australia, India, Singapore, etc.

**Latin America**
- Brazil, Argentina, Chile, Colombia, etc.

**Middle East & Africa**
- UAE, Saudi Arabia, Israel, South Africa, etc.

**Other**
- Any unmapped countries

## Adding Custom Mappings

If you need to add countries to the region map, edit `section_c/c.py`:

```python
COUNTRY_TO_REGION = {
    'Your Country': 'Your Region',
    # ... existing mappings
}
```

## Summary

The system intelligently adapts to your data structure:

✓ Flexible column name detection
✓ Multiple date format support
✓ Automatic country-to-region mapping
✓ Fallback handling for missing data
✓ Clear diagnostic messages
✓ Works with variations in naming conventions

Your data files are fully supported with automatic column detection and mapping.

