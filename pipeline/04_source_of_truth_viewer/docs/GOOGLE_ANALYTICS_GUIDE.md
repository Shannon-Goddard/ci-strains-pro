# Google Analytics Tracking Guide

**Property**: strains.loyal9.app  
**Measurement ID**: G-YN2FMG2XT8  
**Platform**: GA4 (Google Analytics 4)

---

## Events Being Tracked

### 1. Page Views (Automatic)
**Event**: `page_view`  
**Triggered**: Every page load  
**Parameters**: 
- `page_title`: "CI Strains Pro - Source of Truth Viewer"
- `page_location`: Full URL

**Use Case**: Track total traffic, bounce rate, session duration

---

### 2. Legal Acceptance
**Event**: `legal_acceptance`  
**Triggered**: User clicks "I Understand & Accept" on legal modal  
**Parameters**:
- `action`: "accepted"

**Use Case**: Track how many users accept legal terms (should be 100% of active users)

---

### 3. Seed Bank Filter
**Event**: `seed_bank_filter`  
**Triggered**: User selects a seed bank from dropdown  
**Parameters**:
- `seed_bank`: Name of selected seed bank (e.g., "North Atlantic") or "all"

**Use Case**: 
- Identify most popular seed banks
- Understand user browsing patterns
- Prioritize seed bank data quality

---

### 4. Strain Search
**Event**: `strain_search`  
**Triggered**: User types in strain search box (after 3+ characters)  
**Parameters**:
- `query`: Search term (e.g., "og kush")

**Use Case**:
- Identify most searched strains
- Discover missing strains in inventory
- Improve search functionality

---

### 5. Lookup Success
**Event**: `lookup_success`  
**Triggered**: API returns signed URL successfully  
**Parameters**:
- `seed_bank`: Source seed bank
- `url`: Strain URL (for debugging, may want to hash for privacy)

**Use Case**:
- Track successful lookups per seed bank
- Measure conversion rate (search → view)
- Identify most viewed strains

---

### 6. Lookup Error
**Event**: `lookup_error`  
**Triggered**: API returns error (404, 500, rate limit)  
**Parameters**:
- `error`: Error message
- `url`: Failed URL (for debugging)

**Use Case**:
- Identify broken URLs in inventory
- Track rate limiting issues
- Monitor API health

---

## Viewing Data in GA4

### Real-Time Reports
1. Go to https://analytics.google.com/
2. Select "strains.loyal9.app" property
3. Navigate to "Reports" → "Realtime"
4. See live users, events, and pages

### Custom Reports

#### Most Popular Seed Banks
1. Go to "Explore" → "Free form"
2. Dimensions: `seed_bank` (from `seed_bank_filter` event)
3. Metrics: Event count
4. Sort by count descending

#### Top Searched Strains
1. Go to "Explore" → "Free form"
2. Dimensions: `query` (from `strain_search` event)
3. Metrics: Event count
4. Sort by count descending

#### Lookup Success Rate
1. Go to "Explore" → "Free form"
2. Metrics: 
   - `lookup_success` event count
   - `lookup_error` event count
3. Calculate: Success rate = success / (success + error)

---

## Privacy Considerations

### What We Track
- ✅ Seed bank selections (aggregate data)
- ✅ Search queries (strain names only)
- ✅ Success/error rates (system health)
- ✅ Page views (traffic metrics)

### What We DON'T Track
- ❌ Personal information (names, emails)
- ❌ IP addresses (GA4 anonymizes by default)
- ❌ User accounts (no login system)
- ❌ Sensitive data (medical info, purchases)

### GDPR Compliance
- No cookies required for basic tracking
- No personal data collected
- Users can block GA with browser extensions
- Data retention: 14 months (GA4 default)

---

## Adding Custom Events (Future)

To add new events, use this pattern in `app.js`:

```javascript
function trackEvent(eventName, params = {}) {
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, params);
    }
}

// Example: Track iframe load time
trackEvent('iframe_loaded', {
    load_time_ms: 1234,
    seed_bank: 'North Atlantic'
});
```

---

## Recommended Dashboards

### Dashboard 1: User Engagement
- Total users (last 7 days)
- Page views
- Average session duration
- Bounce rate

### Dashboard 2: Seed Bank Performance
- Lookups by seed bank (bar chart)
- Success rate by seed bank (%)
- Most viewed strains per bank

### Dashboard 3: Search Insights
- Top 20 searched strains
- Search → lookup conversion rate
- Failed searches (no results)

### Dashboard 4: System Health
- API error rate (%)
- Rate limit hits
- Average response time (if tracked)

---

## Alerts to Set Up

### Critical Alerts
1. **Error Rate Spike**: If `lookup_error` > 10% of total lookups
2. **Zero Traffic**: If no page views for 1 hour during business hours
3. **Rate Limiting**: If rate limit errors > 5 per hour

### Warning Alerts
1. **Low Success Rate**: If lookup success < 90%
2. **High Bounce Rate**: If bounce rate > 70%
3. **Slow Load Times**: If page load > 5 seconds (if tracked)

---

## Integration with AWS CloudWatch

For deeper system monitoring, combine GA4 with CloudWatch:

**GA4 tracks**: User behavior, frontend events  
**CloudWatch tracks**: Lambda performance, API Gateway metrics, CloudFront logs

**Example combined insight**:
- GA4: "100 users searched for 'OG Kush'"
- CloudWatch: "50 Lambda cold starts caused 2s delay"
- **Action**: Pre-warm Lambda or optimize cold start

---

## Cost

**Google Analytics 4**: Free (up to 10M events/month)  
**Current usage estimate**: ~1K events/day = 30K/month  
**Headroom**: 333x before hitting limits

---

## Testing GA4 Integration

### 1. Real-Time Test
1. Open https://strains.loyal9.app in browser
2. Open GA4 Real-Time report in another tab
3. Interact with site (search, filter, lookup)
4. Verify events appear in real-time (5-10 second delay)

### 2. Debug Mode (Chrome)
1. Install "Google Analytics Debugger" extension
2. Open browser console
3. Look for `gtag` debug messages
4. Verify event parameters are correct

### 3. Event Validation
```javascript
// In browser console, manually trigger event
gtag('event', 'test_event', { test_param: 'test_value' });

// Check GA4 Real-Time → Events → test_event
```

---

## Next Steps

1. ✅ **GA4 installed** (tracking code in `index.html`)
2. ✅ **Events defined** (6 custom events)
3. ⏳ **Deploy to strains.loyal9.app** (after CloudFront setup)
4. ⏳ **Test real-time tracking** (verify events fire)
5. ⏳ **Create custom dashboards** (seed bank performance, search insights)
6. ⏳ **Set up alerts** (error rate, zero traffic)

---

**Questions?** Check GA4 documentation:
- [GA4 Events Guide](https://support.google.com/analytics/answer/9322688)
- [Custom Event Tracking](https://developers.google.com/analytics/devguides/collection/ga4/events)
- [GA4 Reports](https://support.google.com/analytics/answer/9212670)

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
