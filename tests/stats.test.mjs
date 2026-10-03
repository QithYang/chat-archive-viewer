// Tests for the stats computation in index.html.
// Run: node --test tests/
// The block between the <stats-core> markers is extracted and evaluated
// on its own, so these tests need no browser. Local time is pinned to UTC+8.
process.env.TZ = 'Asia/Shanghai';

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const core = html.slice(html.indexOf('// <stats-core>'), html.indexOf('// </stats-core>'));
const computeStats = new Function(core + '\nreturn computeStats;')();

// Minimal stand-ins for the normalizer: a message is visible when it has text.
const norm = {
  getMsgData: m => ({ text: (m.content || []).filter(c => c.type === 'text').map(c => c.text).join('\n\n') }),
  isMsgVisible: m => (m.content || []).some(c => c.type === 'text' && c.text),
};
const msg = (sender, localTime, text) => ({
  sender,
  created_at: new Date(localTime + '+08:00').toISOString(),
  content: text == null ? [] : [{ type: 'text', text }],
});
const conv = (uuid, title, msgs) => ({ uuid, title, chat_messages: msgs });

test('empty input', () => {
  assert.deepEqual(computeStats([], norm), { empty: true });
});

test('counts, span, active days and a streak across a month boundary', () => {
  const s = computeStats([
    conv('a', 'A', [
      msg('human', '2026-01-30T10:00:00', 'hi'),
      msg('assistant', '2026-01-31T10:00:00', 'hello'),
      msg('human', '2026-02-01T10:00:00', 'x'),
    ]),
    conv('b', 'B', [msg('human', '2026-02-05T10:00:00', 'y')]),
  ], norm);
  assert.equal(s.convCount, 2);
  assert.equal(s.msgCount, 4);
  assert.equal(s.activeDays, 4);
  assert.equal(s.longestStreak, 3);
  assert.equal(s.spanDays, 7);
  assert.equal(s.firstConv.uuid, 'a');
  assert.equal(s.lastConv.uuid, 'b');
  assert.deepEqual(s.monthSeries, [{ key: '2026-01', human: 2, assistant: 5 }, { key: '2026-02', human: 2, assistant: 0 }]);
});

test('deep night is 02:00-04:59 local time', () => {
  const s = computeStats([
    conv('early', 'E', [msg('human', '2026-03-01T01:59:00', 'a')]),
    conv('deep', 'D', [msg('human', '2026-03-01T02:00:00', 'a'), msg('assistant', '2026-03-01T04:59:00', 'b')]),
    conv('late', 'L', [msg('human', '2026-03-01T05:00:00', 'a')]),
  ], norm);
  assert.equal(s.deepConvCount, 1);
  assert.deepEqual(s.topDeep.map(c => [c.uuid, c.deep]), [['deep', 2]]);
  assert.equal(s.hours[2], 1);
  assert.equal(s.hours[4], 1);
});

test('character count skips whitespace, counts code points, splits by sender', () => {
  const s = computeStats([conv('a', 'A', [
    msg('human', '2026-03-01T10:00:00', '你好 world\n'),
    msg('assistant', '2026-03-01T10:01:00', '😊 ok'),
  ])], norm);
  assert.equal(s.chars.human, 7);
  assert.equal(s.chars.assistant, 3);
});

test('emoji: ZWJ sequence counts once, text-style symbols are ignored', () => {
  const s = computeStats([conv('a', 'A', [
    msg('human', '2026-03-01T10:00:00', '👨‍💻👨‍💻 © ® ™ ❤️ ❤ 😊'),
  ])], norm);
  const got = Object.fromEntries(s.emoji.map(x => [x.e, x.n]));
  assert.deepEqual(got, { '👨‍💻': 2, '❤️': 1, '😊': 1 });
});

test('invisible messages and conversations without visible messages are skipped', () => {
  const s = computeStats([
    conv('a', 'A', [msg('human', '2026-03-01T10:00:00', 'x'), msg('assistant', '2026-03-09T10:00:00', null)]),
    conv('ghost', 'G', [msg('human', '2026-03-02T10:00:00', null)]),
  ], norm);
  assert.equal(s.convCount, 1);
  assert.equal(s.msgCount, 1);
  assert.equal(s.spanDays, 1);
});

test('weekday is Monday-first; longest list breaks ties by characters', () => {
  const s = computeStats([
    conv('short', 'S', [msg('human', '2026-03-02T10:00:00', 'a'), msg('assistant', '2026-03-02T10:01:00', 'b')]),
    conv('wordy', 'W', [msg('human', '2026-03-08T10:00:00', 'aaaa'), msg('assistant', '2026-03-08T10:01:00', 'bbbb')]),
  ], norm);
  // 2026-03-02 is a Monday, 2026-03-08 a Sunday
  assert.equal(s.weekday[0], 2);
  assert.equal(s.weekday[6], 2);
  assert.deepEqual(s.topLongest.map(c => c.uuid), ['wordy', 'short']);
});
