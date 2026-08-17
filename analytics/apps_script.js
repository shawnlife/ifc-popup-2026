/**
 * IFC Cape Town Pop-Up 2026 — usage tracking backend.
 *
 * This is a REFERENCE COPY. The live version lives in Google Apps Script.
 * See SETUP.md for how to deploy it.
 *
 * What it does:
 *   doPost  — the site sends batches of events; they get appended to the Events sheet
 *   doGet   — ?action=summary returns aggregated counts as JSON for the dashboard
 *
 * What it deliberately does NOT store: no IP addresses, no user agents, no
 * cookies, no names, nothing that identifies a person. Just "someone opened
 * session-3b at this time". The `sid` is a random per-page-load string the site
 * generates in memory so visits can be counted; it is not stored anywhere on the
 * visitor's device and cannot be traced back to anyone.
 */

var SHEET_NAME = 'Events';
var CACHE_KEY = 'summary_v1';
var CACHE_SECONDS = 60;      // dashboard reads are cheap and near-live

// Only these event types are accepted. Anything else is dropped, so a stray
// script posting junk cannot invent new columns of noise.
var ALLOWED = ['visit', 'tab', 'session', 'speaker', 'filter', 'ticket',
               'linkedin', 'outbound'];
var MAX_EVENTS_PER_POST = 60;
var MAX_TARGET_LEN = 80;


function sheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['timestamp', 'session_id', 'type', 'target']);
    sh.setFrozenRows(1);
  }
  return sh;
}


function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) return ok_({ stored: 0 });

    var payload = JSON.parse(e.postData.contents);
    var sid = String(payload.sid || '').slice(0, 16);
    var events = payload.events || [];
    if (!events.length) return ok_({ stored: 0 });
    if (events.length > MAX_EVENTS_PER_POST) events = events.slice(0, MAX_EVENTS_PER_POST);

    var rows = [];
    for (var i = 0; i < events.length; i++) {
      var ev = events[i];
      var type = String(ev.type || '');
      if (ALLOWED.indexOf(type) === -1) continue;          // drop anything unexpected
      var when = Number(ev.t);
      if (!when || when < 1600000000000 || when > Date.now() + 86400000) when = Date.now();
      rows.push([new Date(when), sid, type,
                 String(ev.target || '').slice(0, MAX_TARGET_LEN)]);
    }
    if (!rows.length) return ok_({ stored: 0 });

    // One setValues() call, not one appendRow() per event. Per-row writes are
    // what blew the 6-minute execution cap on the other projects.
    var sh = sheet_();
    sh.getRange(sh.getLastRow() + 1, 1, rows.length, 4).setValues(rows);

    return ok_({ stored: rows.length });
  } catch (err) {
    return ok_({ error: String(err) });
  }
}


function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) || 'summary';
  if (action !== 'summary') return ok_({ error: 'unknown action' });

  var cache = CacheService.getScriptCache();
  if (!(e && e.parameter && e.parameter.fresh)) {
    var hit = cache.get(CACHE_KEY);
    if (hit) return ok_(JSON.parse(hit));
  }

  var summary = buildSummary_();
  try { cache.put(CACHE_KEY, JSON.stringify(summary), CACHE_SECONDS); } catch (err) {}
  return ok_(summary);
}


function buildSummary_() {
  var sh = sheet_();
  var last = sh.getLastRow();
  if (last < 2) {
    return { generated: new Date().toISOString(), total: 0, visits: 0,
             uniqueVisits: 0, sessions: [], speakers: [], tabs: [], filters: [],
             outbound: [], visitsByHour: [],
             clicks: { ticket: 0, linkedin: 0, outbound: 0 } };
  }

  var values = sh.getRange(2, 1, last - 1, 4).getValues();
  var sessions = {}, speakers = {}, tabs = {}, filters = {}, outbound = {};
  var visitsByHour = {}, sids = {};
  var clicks = { ticket: 0, linkedin: 0, outbound: 0 };
  var total = 0, visits = 0;
  var tz = Session.getScriptTimeZone();

  for (var i = 0; i < values.length; i++) {
    var ts = values[i][0], sid = values[i][1], type = values[i][2], target = values[i][3];
    if (!type) continue;
    total++;
    if (sid) sids[sid] = 1;

    // One full hourly series of visits. The dashboard rolls it up to days or
    // zooms into the event day itself, so only one series has to be sent.
    if (ts instanceof Date && type === 'visit') {
      var hour = Utilities.formatDate(ts, tz, 'yyyy-MM-dd HH');
      visitsByHour[hour] = (visitsByHour[hour] || 0) + 1;
    }

    if (type === 'visit') visits++;
    else if (type === 'session') sessions[target] = (sessions[target] || 0) + 1;
    else if (type === 'speaker') speakers[target] = (speakers[target] || 0) + 1;
    else if (type === 'tab') tabs[target] = (tabs[target] || 0) + 1;
    else if (type === 'filter') filters[target] = (filters[target] || 0) + 1;
    else if (type === 'ticket') clicks.ticket++;
    else if (type === 'linkedin') {
      clicks.linkedin++;
      speakers[target] = speakers[target] || 0;   // keep zero-open profiles listed
      outbound['LinkedIn — ' + (target || 'unknown')] =
        (outbound['LinkedIn — ' + (target || 'unknown')] || 0) + 1;
    }
    else if (type === 'outbound') {
      clicks.outbound++;
      outbound[target || '(unknown)'] = (outbound[target || '(unknown)'] || 0) + 1;
    }
  }

  return {
    generated: new Date().toISOString(),
    total: total,
    visits: visits,
    uniqueVisits: Object.keys(sids).length,
    clicks: clicks,
    sessions: rank_(sessions),
    speakers: rank_(speakers),
    tabs: rank_(tabs),
    filters: rank_(filters),
    outbound: rank_(outbound),
    visitsByHour: rank_(visitsByHour, true)
  };
}


/** {key: count} -> [{name, count}], by count desc, or by key asc for time series. */
function rank_(obj, byKey) {
  var out = Object.keys(obj).map(function (k) { return { name: k, count: obj[k] }; });
  out.sort(byKey
    ? function (a, b) { return a.name < b.name ? -1 : 1; }
    : function (a, b) { return b.count - a.count; });
  return out;
}


function ok_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}


/** Run once from the editor to confirm the sheet and aggregation work. */
function selfTest() {
  var sh = sheet_();
  sh.getRange(sh.getLastRow() + 1, 1, 2, 4).setValues([
    [new Date(), 'selftest', 'visit', ''],
    [new Date(), 'selftest', 'session', 'session-1a']
  ]);
  Logger.log(JSON.stringify(buildSummary_(), null, 2));
  Logger.log('Now delete the two "selftest" rows from the Events sheet.');
}
