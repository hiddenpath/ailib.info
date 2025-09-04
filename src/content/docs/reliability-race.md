---
title: Race / Hedging
group: Reliability
order: 30
status: stable
---

# Race / Hedging (Stable)

Launch multiple contenders simultaneously or with small delays; first successful response wins and cancels the rest.

```rust
// let race = RacePolicy::new()
//   .contender("gpt-4o", Duration::from_millis(0))
//   .contender("claude-3-haiku", Duration::from_millis(120))
//   .cancel_others(true);
```

Use for interactive latency-sensitive flows (chat UI). Cost increases with redundant tokens.
