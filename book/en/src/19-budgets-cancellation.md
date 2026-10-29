# 19. Budgets, deadlines and cancellation

<a id="n050"></a>

**N050.** An enabled implementation MUST enforce and advertise bounds for source/body size, AST nodes/depth, result columns/page bytes, row mutations, execution ownership, concurrency and every physical-work/intermediate resource used by its plans. If a required budget cannot be enforced, the plan MUST be refused.

Initial design ceilings are <=64 KiB request body, <=1,024 AST nodes, depth<=32, <=32 selected columns, <=4 sort keys, page_size default 50/max 100, page bytes<=256 KiB, batch items<=16 and total mutation rows<=16. These are proposed admission bounds, not capacity/SLO measurements. A qualified installation may publish lower bounds; raising a bound requires corresponding qualification.

Scan rows/bytes, input snapshot size, join fanout, aggregate groups, sort memory, result materialization, execution duration and tenant concurrency need explicit effective numeric ceilings and enforcement modes in the manifest. LIMIT 1 does not bound an aggregate/join/sort's work. A time spent waiting for an RPC is not a bound on physical work.

<a id="n051"></a>

**N051.** The service MUST distinguish client wait timeout, execution deadline, cancel intent, confirmed worker completion and confirmed commit outcome. Ownership/permits must remain accounted for until actual completion or established fencing/reconciliation permits release. The service MUST withhold unauthorized or expired late results.

Partial read bytes already published cannot be recalled. Publication fencing must define the point after which withdrawal blocks future bytes; no claim of network-byte retraction is allowed. Streaming and resumability need evidence beyond buffered page tests.
