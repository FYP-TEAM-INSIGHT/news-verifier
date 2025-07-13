# News Verifier - Test Cases & Documentation

## Overview
This document contains all the test cases and expected responses for the News Verifier application.

## Test Cases

### ✅ Successful Verifications

#### 1. Celebrity Death Hoax (LIKELY FAKE)
**Keywords:** celebrity, died, death, passed away
**Example Input:** "Breaking: Famous celebrity died in hotel room last night"
**Expected Result:** 
- Score: 23%
- Status: LIKELY FAKE ❌
- Low entity similarity and source credibility

#### 2. Vaccine Conspiracy (FAKE NEWS)
**Keywords:** vaccine, microchip, 5g, conspiracy
**Example Input:** "New study proves vaccines contain microchips for 5G tracking"
**Expected Result:**
- Score: 18%
- Status: FAKE NEWS ❌
- Very low semantic similarity and source credibility

#### 3. Election Fraud Claims (LIKELY FAKE)
**Keywords:** election, fraud, stolen, rigged
**Example Input:** "Election was completely rigged and stolen from the people"
**Expected Result:**
- Score: 31%
- Status: LIKELY FAKE ❌
- Low credibility across all metrics

#### 4. Climate Change Denial (FAKE NEWS)
**Keywords:** climate, hoax, not real, fake science
**Example Input:** "Climate change is a hoax created by fake science"
**Expected Result:**
- Score: 22%
- Status: FAKE NEWS ❌
- Low source credibility and semantic similarity

#### 5. Legitimate Breaking News (NOT FAKE)
**Keywords:** breaking, confirmed, official, reuters, ap news
**Example Input:** "Reuters confirms official government announcement on new policy"
**Expected Result:**
- Score: 87%
- Status: NOT FAKE ✅
- High scores across all metrics

#### 6. Academic Research (NOT FAKE)
**Keywords:** study, research, university, published, journal
**Example Input:** "University study published in peer-reviewed journal shows promising results"
**Expected Result:**
- Score: 79%
- Status: NOT FAKE ✅
- Good credibility scores

#### 7. Default Case (NEEDS VERIFICATION)
**Any other news content not matching specific keywords**
**Expected Result:**
- Score: 65%
- Status: NEEDS VERIFICATION ⚠️
- Moderate scores across metrics

### ❌ Error Cases (400 Bad Request)

#### 1. Greeting Messages
**Keywords:** hello, hi, how are you, good morning, good evening
**Example Input:** "Hello, how are you doing today?"
**Error:** "This appears to be a greeting, not news content"

#### 2. Recipe Content
**Keywords:** recipe, cooking, ingredients, bake, cook
**Example Input:** "Here's a recipe for chocolate cake with ingredients"
**Error:** "This appears to be a recipe, not news content"

#### 3. Shopping Content
**Keywords:** shopping, buy, sale, discount, price
**Example Input:** "Great sale on electronics, buy now with 50% discount"
**Error:** "This appears to be shopping content, not news"

#### 4. Personal/Relationship Content
**Keywords:** love, relationship, dating, romance
**Example Input:** "I love spending time with my partner on romantic dates"
**Error:** "This appears to be personal content, not news"

#### 5. Test Content
**Keywords:** test, testing, sample, example
**Example Input:** "This is just a test message for testing purposes"
**Error:** "No matched news found in verified database"

#### 6. Too Short Content
**Any text with less than 10 characters**
**Error:** "Text is too short to analyze. Please provide more content."

#### 7. Invalid Format
**Text with no alphabetic characters (only numbers/symbols)**
**Example Input:** "123456 !@#$%^"
**Error:** "Invalid content format. Please provide readable news text."

## Color Coding System

### Score Ranges
- **🔴 Red (0-50%):** Low credibility, likely fake news
- **🟡 Yellow (51-70%):** Medium credibility, needs verification
- **🟢 Green (71-100%):** High credibility, likely authentic

### Configurable Thresholds
\`\`\`javascript
const COLOR_THRESHOLDS = {
  red: { min: 0, max: 50 },
  yellow: { min: 51, max: 70 },
  green: { min: 71, max: 100 }
}
\`\`\`

## API Response Format

### Successful Response
\`\`\`json
{
  "final_score": 0.81,
  "result": "NOT FAKE ✅",
  "relevant_news": [
    {
      "score": 0.91,
      "link": "https://example.com/related-article"
    }
  ],
  "breakdown": {
    "entity_similarity": 0.95,
    "semantic_similarity": 0.73,
    "source_credibility": 1.0,
    "per_entity": {
      "persons": 1.0,
      "locations": 0.92,
      "events": 0.97,
      "organizations": 0.89
    }
  }
}
\`\`\`

### Error Response
\`\`\`json
{
  "status": 400,
  "message": "This appears to be a greeting, not news content"
}
\`\`\`

## Usage Tips

1. **For Testing Fake News:** Use keywords like "celebrity died", "vaccine microchip", "election fraud"
2. **For Testing Real News:** Use keywords like "Reuters confirms", "university study", "official announcement"
3. **For Testing Errors:** Try greetings, recipes, or very short text
4. **For Default Response:** Use general news content without specific keywords

## Development Notes

- Mock API simulates 2-3 second response time
- Error handling includes both API errors and validation errors
- UI shows different error states with appropriate messaging
- All test cases are deterministic based on keyword matching
