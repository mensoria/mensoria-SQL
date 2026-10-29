# 13. Request transactions, idempotency and unknown outcomes

## 13.1 Atomic request contract

A transaction is one submitted array of W1 statements, not an interactive SQL session. Base limits are <=16 items and <=16 total row mutations, same scope/incarnation, one mutation per target logical row. SELECT and DDL items, savepoints, value dependencies between items and cross-request BEGIN/COMMIT are prohibited. RETURNING supplies the write's read result.

<a id="n036"></a>

**N036.** The transaction MUST atomically validate current native actor/session/family, schema/mapping, record guards and admission obligations, then commit business changes, ordered per-item outcomes, the original Operation receipt and Outbox records together. A confirmed precommit failure MUST leave no partial business changes or partial RETURNING publication.

An optional request-level `require_affected_rows: 1` assertion on an UPDATE/DELETE item aborts the entire transaction when it would match zero rows. Ordinary standalone SQL retains zero-match success. Item outcomes follow request order; no intermediate result is published before the batch commit.

No named SQL isolation level is implied by this atomic request guarantee. `SET TRANSACTION`, SERIALIZABLE labels and phantom/write-skew claims require a separate qualified contract; unsupported requests are rejected rather than ignored.

## 13.2 Original-key identity

<a id="n037"></a>

**N037.** Every accepted execution MUST have one original idempotency key bound to its actor, scope/incarnation, language/compiler/profile fingerprint, canonical typed IR, typed values, expected revisions and ordered batch assertions. Same key/different identity MUST conflict; same key/same identity MUST attach to the original operation under current authorization.

The canonical IR must preserve all semantic distinctions, including literal values, decimal scale where meaningful, NULL types, duplicate-sensitive operators and item order. No particular JSON serializer or cryptographic digest is mandated by the language; the implementation contract must pin its canonicalization and keyed-identity protocol.

Repeated reads attach to their original execution; they are not fresh reads. If protected results expire, the original read returns `SQL_RESULT_EXPIRED`; a deliberate new read may use a new key. A lookup MUST NOT create or replay the old operation body.

## 13.3 Outcome and cancellation

<a id="n038"></a>

**N038.** A lost reply, deadline, disconnected client, missing observation or cancel request MUST NOT be interpreted as rollback, failure, physical completion or permission to issue a fresh-key mutation. Reconciliation MUST refer to the original operation/key/incarnation.

The existing operation authority distinguishes accepted/running, confirmed committed, confirmed failed and unknown/reconciliation-required outcomes. SQL must reuse that authority rather than maintain an independently writable commit state. A backend-confirmed conflict may permit bounded full-transaction retry only after the original attempt is proven uncommitted; a generic transport error does not.

Revocation may prevent a user from observing an existing operation. Authorization failure does not change the durable operation's outcome. After recovery, old-incarnation identities and artifacts cannot access a new target merely by reusing the key.
