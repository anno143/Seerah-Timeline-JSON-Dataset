# Seerah Timeline — JSON Dataset (English, Arabic, Urdu)

A clean, ready-to-use JSON timeline of the life of the **Prophet Muhammad ﷺ (السيرة النبوية)**: 166 dated events from his birth in 571 CE to his death in 632 CE, in **English, Arabic and Urdu**.

Every event has a Gregorian-style date for plotting, a Hijri date for display, a short summary, notes on how certain the date is, and a page reference to *Ar-Raheeq Al-Makhtum (The Sealed Nectar)*.

> "There has certainly been for you in the Messenger of Allah an excellent pattern." — *Surah Al-Ahzab, 33:21*

## Used in the Fajr App

This dataset powers the Seerah timeline in **[Fajr: Prayer Alarm & Adhan](https://play.google.com/store/apps/details?id=com.alifanalytics.fajr_app)**, an Android app by [Alif Analytics](https://play.google.com/store/apps/details?id=com.alifanalytics.fajr_app).

<a href="https://play.google.com/store/apps/details?id=com.alifanalytics.fajr_app">
  <img alt="Get it on Google Play" src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" height="60">
</a>

## Features

- 166 events across three periods: before Prophethood (16), Makkah (39) and Madinah (111)
- **English, Arabic (العربية) and Urdu (اردو)** in separate files with an identical structure
- Stable `id` on every event, so the three languages line up one-to-one
- Hijri date on every event, written out in each language
- Start and end dates for ranges such as sieges, the boycott and the Hajj
- Date precision (`day`, `month`, `year`, `approximate`) so your UI can say "c. 595" instead of a false exact date
- Book section and page number for every event, so each one can be checked
- Plain UTF-8 JSON: Arabic and Urdu are stored as readable characters, not escaped sequences

## Files

```
Seerah_Timeline_en.json   English
Seerah_Timeline_ar.json   Arabic
Seerah_Timeline_ur.json   Urdu
tools/validate.py         Checks that the three files are valid and aligned
```

## Data Structure

Each file is a JSON array of events, sorted by `start`.

```json
{
  "id": "badr",
  "title": "The Battle of Badr",
  "commentary": [
    "Setting out after Abu Sufyan's caravan, 300-317 Muslims with two horses and seventy camels met an army of about 1,000 from Makkah.",
    "The Muslims won decisively: fourteen were martyred, while seventy polytheists, including Abu Jahl, were killed and seventy captured."
  ],
  "notes": "The battle was on Friday 17 Ramadan.",
  "hijri-date": "Friday 17 Ramadan 2 AH",
  "start": "0624-03-16",
  "period": "madinah",
  "date-precision": "day",
  "date-basis": "calculated",
  "source": {
    "book": "Ar-Raheeq Al-Makhtum (The Sealed Nectar), Safiur-Rahman Al-Mubarakpuri, English tr. Issam Diab, Darussalam",
    "section": "Reason of the Battle",
    "page": 136
  }
}
```

The same event in Arabic and Urdu keeps every field except the four text fields, which are translated:

```json
{ "id": "badr", "title": "غزوة بدر", "hijri-date": "الجمعة 17 رمضان 2 هـ", ... }
{ "id": "badr", "title": "غزوہ بدر", "hijri-date": "جمعہ، 17 رمضان 2 ہجری", ... }
```

| Field | Type | Translated | Description |
|---|---|---|---|
| `id` | string | no | Stable key, same in all languages (e.g. `hijrah-departure`) |
| `title` | string | yes | Short event title |
| `commentary` | string[] | yes | One to three sentences summarising the event |
| `notes` | string | yes | Date caveats or alternative reports; may be empty |
| `hijri-date` | string | yes | Hijri date written out (AH / BH, or "Year of the Elephant") |
| `start` | string | no | `YYYY-MM-DD`, Julian calendar (see below) |
| `end` | string | no | Optional; present when the event spans a period |
| `period` | string | no | `pre-prophethood`, `makkah` or `madinah` |
| `date-precision` | string | no | `day`, `month`, `year` or `approximate` |
| `date-basis` | string | no | `book` if the book prints this date, `calculated` if converted from its Hijri date |
| `source.book` | string | no | The edition used |
| `source.section` | string | no | Section heading in the English edition |
| `source.page` | int | no | Page number in the English edition |

### About the dates

- **Calendar.** `start` and `end` use the **Julian calendar**, the standard for dates before 1582 (so the death is 8 June 632, not 11 June). Where the book prints a date in the modern calendar (the week of the Hijrah), it has been converted, and the event's `notes` give the date as the book prints it.
- **Hijri to Julian conversion.** Most events only have a Hijri date in the book. These were converted with the tabular Islamic calendar, so treat day-level dates as accurate to a day or two. Where the book names a weekday (Badr on a Friday, Uhud on a Saturday, the death on a Monday), the date was moved to that weekday.
- **Precision.** Read `date-precision` before showing a date. For `month`, `start` is the first day of that month; for `year`, it is the first day of that year. Show those as "Ramadan 2 AH" or "c. 595 CE" rather than a full date.
- **Before the Hijrah.** The book counts Makkan years as "the Nth year of Prophethood". These appear in `hijri-date` alongside the BH year.

## Usage

**JavaScript**

```js
const lang = "ur"; // "en" | "ar" | "ur"
const res = await fetch(`https://raw.githubusercontent.com/anno143/Seerah-Timeline-JSON-Dataset/main/Seerah_Timeline_${lang}.json`);
const events = await res.json();
console.log(events[0].title, "-", events[0]["hijri-date"]);
```

**Python**

```python
import json

with open("Seerah_Timeline_en.json", encoding="utf-8") as f:
    events = json.load(f)

for e in events:
    if e["period"] == "madinah" and e["date-precision"] == "day":
        print(e["start"], e["hijri-date"], "-", e["title"])
```

**Dart / Flutter**

```dart
final jsonStr = await rootBundle.loadString('assets/Seerah_Timeline_ur.json');
final List events = json.decode(jsonStr);
final madinah = events.where((e) => e['period'] == 'madinah').toList();
print(madinah.first['title']);
```

**Combining languages by `id`**

```js
const [en, ar] = await Promise.all(["en", "ar"].map(l =>
  fetch(`https://raw.githubusercontent.com/anno143/Seerah-Timeline-JSON-Dataset/main/Seerah_Timeline_${l}.json`).then(r => r.json())));
const arById = Object.fromEntries(ar.map(e => [e.id, e]));
en.forEach(e => console.log(e.title, "|", arById[e.id].title));
```

**Plotting on a timeline (vis-timeline)**

The files keep the field names of [OpenIslam/seerah-timeline](https://github.com/OpenIslam/seerah-timeline), so they drop straight into [vis-timeline](https://github.com/visjs/vis-timeline): `id`, `start` and `end` are read directly.

```js
const items = new vis.DataSet(events.map(e => ({ ...e, content: e.title })));
new vis.Timeline(document.getElementById("timeline"), items, { rtl: lang !== "en" });
```

> Tip: Urdu and Arabic are right-to-left. Render them with RTL text direction and a font that supports Arabic script (e.g. Noto Nastaliq Urdu, Noto Naskh Arabic, Amiri). Numbers are stored as Western digits (0-9); convert them to Arabic-Indic digits in your UI if you prefer.

## Validating Changes

```bash
python tools/validate.py
```

The script checks that every file parses, that all three languages have the same events in the same order, that dates and shared fields match, and that no text field is empty.

## Sources and Method

- **Source book:** *Ar-Raheeq Al-Makhtum (The Sealed Nectar)* by Safiur-Rahman Al-Mubarakpuri, English translation by Issam Diab, Darussalam. It was chosen because it is widely available in English, Arabic and Urdu.
- **Summaries:** each `commentary` is a short summary written for this dataset, not a quotation from the book. Use `source.page` to read the full account.
- **Translations:** the Arabic and Urdu text was translated from the English summaries for this dataset. Hijri dates in each language are generated from the same date data, so they always match.
- **Gap in the source text:** the first-revelation section was missing from the text file used, so that event's date comes from the printed edition (see its `notes`).

## A Note on the Content

The Sealed Nectar follows mainstream Sunni historiography. Where scholars differ on a date (the Prophet's birth, Al-Isra' wal-Mi'raj, Dhat Ar-Riqa'), the book's preferred view is used and the alternatives are given in `notes`. This dataset is a learning aid and timeline. It is not a substitute for reading the Seerah in full or for scholarly study.

## Contributing

Corrections are welcome, especially for the Arabic and Urdu translations and for dates. Please open an issue or a pull request with the event `id`, the field, and a source for the correction. Run `python tools/validate.py` before submitting.

## Credits

- Source: *Ar-Raheeq Al-Makhtum (The Sealed Nectar)*, Safiur-Rahman Al-Mubarakpuri (Darussalam)
- Field layout: [OpenIslam/seerah-timeline](https://github.com/OpenIslam/seerah-timeline), used so the data works with its vis.js timeline
- Compilation, summaries and translations: [Alif Analytics](https://play.google.com/store/apps/details?id=com.alifanalytics.fajr_app)

## License

Free to use in personal and commercial projects. Please keep a link back to this repository.
